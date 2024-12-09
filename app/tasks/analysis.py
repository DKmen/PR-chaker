from celery import Celery
from app.core.github import Github
from app.core.llm import LLM_Analysis
from app.models.result import Result
from app.models.task import Task, TaskStatus
from sqlmodel import Session
from app.db.session import engine
from app.core.config import settings
from app.core.logger import logger
import json

app = Celery("tasks", broker=settings.broker_url)


@app.task
def analyze_pull_request(task_id):
    # Create a new session
    session = Session(engine)

    # Fetch Task
    task = session.get(Task, task_id)
    logger.debug({"task_id": task_id, "task": task})

    # Initialize the GitHub class
    github = Github(token=task.github_token)

    # fetch the PR files
    pr_files = github.get_files(
        owner=task.owner, repo=task.repo, pr_id=task.pull_request_id
    )
    logger.debug({"pr_files": pr_files, "task": task})

    # Analyze the files in the pull request using the LLM model
    llm = LLM_Analysis("llama3:latest")

    analysis_result = []
    for file in pr_files:
        # Get the file content
        file_content = github.get_file_content(
            owner=task.owner,
            repo=task.repo,
            file_path=file["filename"],
            branch=task.refrance_branch,
        )

        # Get the file changes
        file_changes = file.get("patch")

        # Analyze the file
        analysis = llm.analyze(file_content=file_content, file_changes=file_changes)

        # Parse analysis JSON string
        analysis = json.loads(analysis)
        logger.debug({"analysis": analysis})

        # Check analysis is list or not if not then key is list or not
        if not isinstance(analysis, list):
            if analysis.get("analyses") != None:
                analysis = analysis["analyses"]
            elif analysis.get("issues") != None:
                analysis = analysis["issues"]
            else:
                analysis = [analysis]

        # Parse analysis JSON string
        analysis_result.append(
            Result(
                task_id=task.id,
                result=analysis,
                status="SUCCESS",
                file_name=file["filename"],
            )
        )

    try:
        # Add each Result object individually
        for result in analysis_result:
            session.add(result)

        # Check if all result generate successfully then make task to complete
        task.status = TaskStatus.SUCCESS
        task.total_files = len(pr_files)

        # Update Task
        session.add(task)

        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()

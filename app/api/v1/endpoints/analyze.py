from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.models.task import Task
from app.core.github import Github
from app.tasks.analysis import analyze_pull_request
from app.db.session import SessionDep
from app.core.logger import logger


class Repo(BaseModel):
    repo_url: str = Field(None, example="https://github.com/user/repo")
    pr_id: int = Field(None, example=1)
    github_token: str = Field(None, example="ghp_1234567890")


router = APIRouter()


@router.post("/")
async def inilize_pr_analyze(repo: Repo, session: SessionDep):
    # Extract the owner and repo name from the repo_url
    owner, repo_name = repo.repo_url.split("/")[-2:]
    logger.debug({"owner": owner, "repo_name": repo_name, "repo": repo})

    # Extract the pull request id
    pr_id = repo.pr_id

    # Extract the github token
    github_token = repo.github_token

    # Initialize the GitHub class
    github = Github(token=github_token)

    # Get the branch name
    branch_name = github.get_branch_name(owner=owner, repo=repo_name, pr_id=pr_id)
    branch_title = github.get_pr_title(owner=owner, repo=repo_name, pr_id=pr_id)
    pr_files = github.get_files(owner=owner, repo=repo_name, pr_id=pr_id)

    # store the data in the database
    task = Task(
        owner=owner,
        repo=repo_name,
        pull_request_id=pr_id,
        github_token=github_token,
        title=branch_title,
        refrance_branch=branch_name,
        total_files=len(pr_files),
    )

    try:
        # Add the Task object to the database
        session.add(task)
        session.commit()

        # Refresh the instance to get the updated data from the database
        session.refresh(task)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

    # Call analyze_pull_request job
    analyze_pull_request.delay(task_id=task.id)
    logger.debug(
        {"message": "Task created successfully and send for analyze", "task": task}
    )

    # Return the saved data
    return task

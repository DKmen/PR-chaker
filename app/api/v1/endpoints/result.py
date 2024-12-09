from fastapi import APIRouter, Path, HTTPException
from typing import Annotated
from app.db.session import SessionDep
from app.models.task import Task, TaskStatus
from app.models.result import Result
from app.core.logger import logger

router = APIRouter()


@router.get("/{task_id}")
async def inilize_pr_analyze(
    task_id: Annotated[int, Path(title="The ID of task ID")], session: SessionDep
):
    # fetch the task
    task = session.get(Task, task_id)
    logger.debug({"task_id": task_id, "task": task})

    # throw error if task is not define
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status == TaskStatus.PENDING:
        return {"status": "PENDING"}

    if task.status == TaskStatus.FAILURE:
        return {"message": "Task failed", "status": "FAILURE"}

    # fetch the results
    results =  (
        session.query(
            Result.file_name.label("name"),
            Result.result.label("issues")
        )
        .filter(Result.task_id == task_id)
        .all()
    )
    
    # Calculate critical issues (if type is bug and error then it is critical)
    total_critical = 0
    total_issue = 0
    results_list = []
    for result in results:
        for issue in result.issues:
            if issue["type"] in ["bug", "error"]:
                total_critical += 1
            total_issue += 1
        results_list.append({"name": result.name, "issues": result.issues})
    
    # log the results
    logger.debug({"results_list": results_list})
    logger.debug({"total_critical": total_critical, "total_issue": total_issue})
    
    return {
        "task_id": task.id,
        "status": task.status,
        "results": {
            "summary": {
                "total_files": len(results_list),
                "total_issues": total_issue,
                "total_critical": total_critical
            },
            "files": results_list
        },
    }

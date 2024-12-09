from fastapi import APIRouter, Path, HTTPException
from typing import Annotated
from app.db.session import SessionDep
from app.models.task import Task
from app.core.logger import logger

router = APIRouter()


@router.get("/{task_id}")
async def inilize_pr_analyze(
    task_id: Annotated[int, Path(title="The ID of task ID")], session: SessionDep
):
    task = session.get(Task, task_id)
    logger.debug({"task_id": task_id, "task": task})

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

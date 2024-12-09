from typing import Union, Optional
from sqlmodel import Field, SQLModel
from enum import Enum


class TaskStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    refrance_branch: Optional[str] = Field(nullable=True)
    title: Optional[str] = Field(nullable=True)
    repo: Optional[str] = Field(nullable=True)
    owner: Optional[str] = Field(nullable=True)
    pull_request_id: Optional[str] = Field(nullable=True)
    total_files: Union[int, None] = Field(nullable=True)
    github_token: Optional[str] = Field(nullable=True)
    status: Optional[TaskStatus] = Field(nullable=True, default=TaskStatus.PENDING)

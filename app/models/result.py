from typing import Optional
from sqlmodel import Field, SQLModel, Column, JSON
from enum import Enum


class ResultStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class Result(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    task_id: int = Field(foreign_key="task.id")
    file_name: Optional[str] = Field(nullable=True)
    status: Optional[ResultStatus] = Field(nullable=True, default=ResultStatus.PENDING)
    result: Optional[dict] = Field(default={}, sa_column=Column(JSON))

    class Config:
        arbitrary_types_allowed = True

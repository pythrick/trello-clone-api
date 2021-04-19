from typing import Optional

from pydantic import BaseModel

from trello_clone_api.enums import TaskStatus


class ProjectInSchema(BaseModel):
    name: str
    description: str


class ProjectSchema(BaseModel):
    id: int
    name: str
    description: str
    progress: float = 0.0

    class Config:
        orm_mode = True


class TaskInSchema(BaseModel):
    name: str
    description: str
    status: TaskStatus
    project_id: int


class TaskUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskSchema(BaseModel):
    id: int
    name: str
    description: str
    status: TaskStatus
    project_id: int

    class Config:
        orm_mode = True

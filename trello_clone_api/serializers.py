from pydantic import BaseModel
from typing import Optional


class BoardIn(BaseModel):
    name: str
    description: str


class Board(BaseModel):
    id: int
    name: str
    description: str
    progress: Optional[float]

    class Config:
        orm_mode = True

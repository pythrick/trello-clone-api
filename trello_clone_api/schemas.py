from typing import Optional

from pydantic import BaseModel

from trello_clone_api.enums import CardStatus


class BoardInSchema(BaseModel):
    name: str
    description: str


class BoardSchema(BaseModel):
    id: int
    name: str
    description: str
    progress: Optional[float]

    class Config:
        orm_mode = True


class CardInSchema(BaseModel):
    name: str
    description: str
    status: CardStatus
    board_id: int


class CardUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[CardStatus] = None


class CardSchema(BaseModel):
    id: int
    name: str
    description: str
    status: CardStatus
    board_id: int

    class Config:
        orm_mode = True

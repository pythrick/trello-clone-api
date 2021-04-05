from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Board(BaseModel):
    id: int
    name: str
    description: str
    progress: float


@app.get("/boards/", response_model=List[Board])
def list_boards() -> List[Board]:
    return [
        Board(**{
            "id": 1,
            "name": "Trello Clone",
            "description": "Mais um clone do trello, só que muito melhor.",
            "progress": 13
        })
    ]




@app.post("/boards/", response_model=Board)
def create_board(board: Board) -> Board:
    return Board(**{
        "id": 1,
        "name": "Trello Clone",
        "description": "Mais um clone do trello, só que muito melhor.",
        "progress": 13
    })

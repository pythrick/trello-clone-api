from fastapi import Depends, FastAPI
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from trello_clone_api.db.base import init_models, get_session
from trello_clone_api.serializers import Board, BoardIn
from trello_clone_api.services import create_board
import uvicorn
import asyncio

app = FastAPI()


@app.post("/boards/", response_model=Board)
async def add_board(board: BoardIn, session: AsyncSession = Depends(get_session)) -> Board:
    new_board = await create_board(session, board)
    await session.commit()
    return Board.from_orm(new_board)


@app.get("/boards/", response_model=List[Board])
def list_boards() -> List[Board]:
    return [
        Board(**item) 
        for item in 
        [{
            "id": 1,
            "name": "Trello Clone",
            "description": "Um clone do Trello, só que muito melhor.",
            "progress": 23.5,
        },
        {
            "id": 2,
            "name": "Lorem ipsum dolor sit amet,",
            "description":
            "uspendisse at nisi at diam viverra maximus quis in est. Sed at vulputate mauris.",
            "progress": 15,
        },
        {
            "id": 3,
            "name": " bibendum consectetur arcu",
            "description":
            "Nulla facilisi. Curabitur pellentesque eu sapien sit amet dictum.",
            "progress": 55,
        },
        {
            "id": 4,
            "name": "Suspendisse at nisi at diam",
            "description": "Nunc accumsan neque tincidunt rutrum consectetur.",
            "progress": 0,
        },
        {
            "id": 5,
            "name": "Suspendisse facilisis mauris metus",
            "description": " Quisque finibus sit amet lorem a gravida",
            "progress": 73,
        },
        {
            "id": 6,
            "name": "Curabitur rhoncus id",
            "description": "Sed vitae nisl placerat, varius sapien ut, sagittis erat",
            "progress": 28,
        },
        {
            "id": 7,
            "name": "Ut vestibulum velit nec",
            "description":
            "Duis pellentesque quam lacus, a viverra magna ornare sit amet.",
            "progress": 48,
        },
        {
            "id": 8,
            "name": "Aenean nec lacus",
            "description": "In quis eros malesuada, rutrum magna id, feugiat nisl",
            "progress": 36,
        },
        ]
    ]


if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

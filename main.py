import asyncio
from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from trello_clone_api import schemas
from trello_clone_api.db.base import get_session, init_models
from trello_clone_api.services import board as board_services
from trello_clone_api.services import card as card_services

app = FastAPI()


@app.post("/boards/", status_code=201, response_model=schemas.BoardSchema)
async def add_board(
    board: schemas.BoardInSchema, session: AsyncSession = Depends(get_session)
) -> schemas.BoardSchema:
    new_board = await board_services.create_board(session, board)
    try:
        await session.commit()
    except IntegrityError as e:
        raise HTTPException(status_code=422, detail="Board already created.") from e
    return schemas.BoardSchema.from_orm(new_board)


@app.get("/boards/", response_model=List[schemas.BoardSchema])
async def list_boards(
    session: AsyncSession = Depends(get_session),
) -> List[schemas.BoardSchema]:
    return [
        schemas.BoardSchema.from_orm(board)
        for board in await board_services.list_boards(session)
    ]


@app.post("/cards/", status_code=201, response_model=schemas.CardSchema)
async def add_card(
    card: schemas.CardInSchema, session: AsyncSession = Depends(get_session)
) -> schemas.CardSchema:
    new_card = await card_services.create_card(session, card)
    await session.commit()
    return schemas.CardSchema.from_orm(new_card)


@app.patch("/cards/:id", status_code=200, response_model=schemas.CardSchema)
async def edit_card(
    id: int,
    card: schemas.CardUpdateSchema,
    session: AsyncSession = Depends(get_session),
) -> schemas.CardSchema:
    try:
        card_db = await card_services.get_card(session, id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Card not found.") from e
    updated_card = await card_services.update_card(session, card_db.id, card)
    await session.commit()
    return schemas.CardSchema.from_orm(updated_card)


@app.get("/cards/", response_model=List[schemas.CardSchema])
async def list_cards(
    board_id: int,
    session: AsyncSession = Depends(get_session),
) -> List[schemas.CardSchema]:
    return [
        schemas.CardSchema.from_orm(card)
        for card in await card_services.list_cards(session, board_id)
    ]


if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from trello_clone_api import schemas
from trello_clone_api.db.base import get_session
from trello_clone_api.services import board as board_services

router = APIRouter(prefix="/boards", tags=["boards"])


@router.post("/", status_code=201, response_model=schemas.BoardSchema)
async def add_board(
    board: schemas.BoardInSchema, session: AsyncSession = Depends(get_session)
) -> schemas.BoardSchema:
    new_board = await board_services.create_board(session, board)
    try:
        await session.commit()
    except IntegrityError as e:
        raise HTTPException(status_code=422, detail="Board already created.") from e
    return schemas.BoardSchema.from_orm(new_board)


@router.get("/", response_model=List[schemas.BoardSchema])
async def list_boards(
    session: AsyncSession = Depends(get_session),
) -> List[schemas.BoardSchema]:
    return [
        schemas.BoardSchema.from_orm(board)
        for board in await board_services.list_boards(session)
    ]


@router.patch(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.BoardSchema
)
async def edit_board(
    id: int,
    board: schemas.BoardInSchema,
    session: AsyncSession = Depends(get_session),
) -> schemas.BoardSchema:
    try:
        board_db = await board_services.get_board(session, id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Board not found.") from e
    updated_board = await board_services.update_board(session, board_db.id, board)
    await session.commit()
    return schemas.BoardSchema.from_orm(updated_board)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_board(
    id: int,
    session: AsyncSession = Depends(get_session),
):
    try:
        board_db = await board_services.get_board(session, id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Card not found."
        ) from e
    await board_services.delete_board(session, board_db.id)
    await session.commit()

from typing import List

from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from trello_clone_api import schemas
from trello_clone_api.db.base import get_session


from trello_clone_api.services import board as board_services

from fastapi import APIRouter

router = APIRouter(prefix="/boards", tags=["boards"])

# TODO: Criar rota para excluir Board
# TODO: Criar rota para edição de Board
# TODO: Implementar `progress` na consulta de Board


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

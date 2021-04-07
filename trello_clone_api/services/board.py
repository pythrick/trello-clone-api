from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from trello_clone_api.models import Board
from trello_clone_api.schemas import BoardInSchema


async def create_board(session: AsyncSession, board: BoardInSchema) -> Board:
    board = Board(name=board.name, description=board.description)
    session.add(board)
    return board


async def list_boards(session: AsyncSession) -> list[Board]:
    stmt = select(Board)
    result = await session.execute(stmt)
    return result.scalars().all()

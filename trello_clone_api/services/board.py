from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from trello_clone_api.models import Board
from trello_clone_api.schemas import BoardInSchema


async def get_board(session: AsyncSession, id: int) -> Board:
    result = await session.execute(select(Board).where(Board.id == id))
    return result.first()[0]


async def create_board(session: AsyncSession, board: BoardInSchema) -> Board:
    board = Board(name=board.name, description=board.description)
    session.add(board)
    return board


async def update_board(
    session: AsyncSession, id: int, board_schema: BoardInSchema
) -> Board:
    data = board_schema.dict(exclude_none=True)
    await session.execute(update(Board).values(**data).where(Board.id == id))
    return await get_board(session, id)


async def delete_board(session: AsyncSession, id: int) -> None:
    await session.execute(delete(Board).where(Board.id == id))


async def list_boards(session: AsyncSession) -> list[Board]:
    stmt = select(Board)
    result = await session.execute(stmt)
    return result.scalars().all()

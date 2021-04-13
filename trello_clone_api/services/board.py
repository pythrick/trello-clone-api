from sqlalchemy import and_, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import delete, func, select, update
from trello_clone_api.enums import CardStatus
from trello_clone_api.models import Board, Card
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
    done_query = (
        select(Board.id, func.count(Card.id).label("cards_count"))
        .outerjoin(
            Card, and_(Card.board_id == Board.id, Card.status == CardStatus.DONE)
        )
        .group_by(Board.id)
    ).subquery()
    cards_count = func.count(Card.id).label("cards_count")
    done_count = done_query.c.cards_count
    # TODO: Refactor this, include progress calc on query
    stmt = (
        select(
            Board,
            done_count,
            cards_count,
        )
        .select_from(Board)
        .outerjoin(Card)
        .group_by(Board.id, "cards_count")
        .where(
            Board.id == done_query.c.id,
        )
        .order_by(Board.id)
    )
    result = await session.execute(stmt)
    result = result.all()
    boards_list = []
    for board, done_count, total_count in result:
        if done_count:
            board.progress = round(done_count / total_count, 2)
        boards_list.append(board)
    return boards_list

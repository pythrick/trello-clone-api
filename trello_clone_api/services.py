from sqlalchemy.ext.asyncio import AsyncSession
from trello_clone_api.models import Board
from trello_clone_api.serializers import BoardIn


async def create_board(session: AsyncSession, board: BoardIn) -> Board:
    board = Board(name=board.name, description=board.description)
    session.add(board)
    return board
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from trello_clone_api.db.base import Base
from trello_clone_api.enums import CardStatus


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    cards = relationship("Card", back_populates="board")
    progress = 0
    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    status = Column(Enum(CardStatus))
    board_id = Column(Integer, ForeignKey("boards.id"))
    board = relationship("Board", back_populates="cards")

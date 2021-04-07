from trello_clone_api.db.base import Base
from sqlalchemy import Column, Float, String, Integer


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)

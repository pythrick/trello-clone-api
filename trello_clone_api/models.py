from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from trello_clone_api.db.base import Base
from trello_clone_api.enums import TaskStatus


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    tasks = relationship("Task", back_populates="project")
    progress = 0
    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    status = Column(Enum(TaskStatus))
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="tasks")

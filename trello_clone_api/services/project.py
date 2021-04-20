from sqlalchemy import and_, case, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import delete, func, select, update
from trello_clone_api.enums import TaskStatus
from trello_clone_api.models import Project, Task
from trello_clone_api.schemas import ProjectInSchema


async def get_project(session: AsyncSession, id: int) -> Project:
    result = await session.execute(select(Project).where(Project.id == id))
    return result.first()[0]


async def create_project(session: AsyncSession, project: ProjectInSchema) -> Project:
    project = Project(name=project.name, description=project.description)
    session.add(project)
    return project


async def update_project(
    session: AsyncSession, id: int, project_schema: ProjectInSchema
) -> Project:
    data = project_schema.dict(exclude_none=True)
    await session.execute(update(Project).values(**data).where(Project.id == id))
    return await get_project(session, id)


async def delete_project(session: AsyncSession, id: int) -> None:
    await session.execute(delete(Project).where(Project.id == id))


async def list_projects(session: AsyncSession) -> list[Project]:
    done_query = (
        select(Project.id, func.count(Task.id).label("tasks_count"))
        .outerjoin(
            Task, and_(Task.project_id == Project.id, Task.status == TaskStatus.DONE)
        )
        .group_by(Project.id)
    ).subquery()
    tasks_count = func.count(Task.id).label("tasks_count")
    done_count = done_query.c.tasks_count
    # TODO: Refactor this, include progress calc on query
    stmt = (
        select(
            Project,
            done_count,
            tasks_count,
        )
        .select_from(Project)
        .outerjoin(Task)
        .group_by(Project.id, "tasks_count")
        .where(
            Project.id == done_query.c.id,
        )
        .order_by(desc(Project.id))
    )
    result = await session.execute(stmt)
    result = result.all()
    projects_list = []
    for project, done_count, total_count in result:
        if done_count:
            project.progress = round(done_count / total_count, 2)
        projects_list.append(project)
    return projects_list

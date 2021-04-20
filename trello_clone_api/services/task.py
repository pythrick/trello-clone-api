from sqlalchemy import delete, desc, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from trello_clone_api.models import Task
from trello_clone_api.schemas import TaskInSchema, TaskUpdateSchema


async def create_task(session: AsyncSession, task: TaskInSchema) -> Task:
    new_task = Task(
        name=task.name,
        description=task.description,
        status=task.status,
        project_id=task.project_id,
    )
    session.add(new_task)
    return new_task


async def list_tasks(session: AsyncSession, project_id) -> list[Task]:
    result = await session.execute(
        select(Task).where(Task.project_id == project_id).order_by(desc(Task.id))
    )
    return result.scalars().all()


async def get_task(session: AsyncSession, id: int) -> Task:
    result = await session.execute(select(Task).where(Task.id == id))
    return result.first()[0]


async def update_task(
    session: AsyncSession, id: int, task_schema: TaskUpdateSchema
) -> Task:
    data = task_schema.dict(exclude_none=True)
    await session.execute(update(Task).values(**data).where(Task.id == id))
    return await get_task(session, id)


async def delete_task(session: AsyncSession, id: int) -> None:
    await session.execute(delete(Task).where(Task.id == id))

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from trello_clone_api import schemas
from trello_clone_api.db.base import get_session
from trello_clone_api.services import task as task_services

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[schemas.TaskSchema])
async def list_tasks(
    project_id: int,
    session: AsyncSession = Depends(get_session),
) -> List[schemas.TaskSchema]:
    return [
        schemas.TaskSchema.from_orm(task)
        for task in await task_services.list_tasks(session, project_id)
    ]


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.TaskSchema
)
async def add_task(
    task: schemas.TaskInSchema, session: AsyncSession = Depends(get_session)
) -> schemas.TaskSchema:
    new_task = await task_services.create_task(session, task)
    await session.commit()
    return schemas.TaskSchema.from_orm(new_task)


@router.patch(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.TaskSchema
)
async def edit_task(
    id: int,
    task: schemas.TaskUpdateSchema,
    session: AsyncSession = Depends(get_session),
) -> schemas.TaskSchema:
    try:
        task_db = await task_services.get_task(session, id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Task not found.") from e
    updated_task = await task_services.update_task(session, task_db.id, task)
    await session.commit()
    return schemas.TaskSchema.from_orm(updated_task)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_task(
    id: int,
    session: AsyncSession = Depends(get_session),
):
    try:
        task_db = await task_services.get_task(session, id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found."
        ) from e
    await task_services.delete_task(session, task_db.id)
    await session.commit()

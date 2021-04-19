from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from trello_clone_api import schemas
from trello_clone_api.db.base import get_session
from trello_clone_api.services import project as project_services

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", status_code=201, response_model=schemas.ProjectSchema)
async def add_project(
    project: schemas.ProjectInSchema, session: AsyncSession = Depends(get_session)
) -> schemas.ProjectSchema:
    new_project = await project_services.create_project(session, project)
    try:
        await session.commit()
    except IntegrityError as e:
        raise HTTPException(status_code=422, detail="Project already created.") from e
    return schemas.ProjectSchema.from_orm(new_project)


@router.get("/", response_model=List[schemas.ProjectSchema])
async def list_projects(
    session: AsyncSession = Depends(get_session),
) -> List[schemas.ProjectSchema]:
    return [
        schemas.ProjectSchema.from_orm(project)
        for project in await project_services.list_projects(session)
    ]


@router.patch(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ProjectSchema
)
async def edit_project(
    id: int,
    project: schemas.ProjectInSchema,
    session: AsyncSession = Depends(get_session),
) -> schemas.ProjectSchema:
    try:
        project_db = await project_services.get_project(session, id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Project not found.") from e
    updated_project = await project_services.update_project(
        session, project_db.id, project
    )
    await session.commit()
    return schemas.ProjectSchema.from_orm(updated_project)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_project(
    id: int,
    session: AsyncSession = Depends(get_session),
):
    try:
        project_db = await project_services.get_project(session, id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found."
        ) from e
    await project_services.delete_project(session, project_db.id)
    await session.commit()

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from trello_clone_api import schemas
from trello_clone_api.db.base import get_session
from trello_clone_api.services import card as card_services

router = APIRouter(prefix="/cards", tags=["cards"])


@router.get("/", response_model=List[schemas.CardSchema])
async def list_cards(
    board_id: int,
    session: AsyncSession = Depends(get_session),
) -> List[schemas.CardSchema]:
    return [
        schemas.CardSchema.from_orm(card)
        for card in await card_services.list_cards(session, board_id)
    ]


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.CardSchema
)
async def add_card(
    card: schemas.CardInSchema, session: AsyncSession = Depends(get_session)
) -> schemas.CardSchema:
    new_card = await card_services.create_card(session, card)
    await session.commit()
    return schemas.CardSchema.from_orm(new_card)


@router.patch("/:id", status_code=status.HTTP_200_OK, response_model=schemas.CardSchema)
async def edit_card(
    id: int,
    card: schemas.CardUpdateSchema,
    session: AsyncSession = Depends(get_session),
) -> schemas.CardSchema:
    try:
        card_db = await card_services.get_card(session, id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Card not found.") from e
    updated_card = await card_services.update_card(session, card_db.id, card)
    await session.commit()
    return schemas.CardSchema.from_orm(updated_card)


@router.delete("/:id", status_code=status.HTTP_204_NO_CONTENT)
async def remove_card(
    id: int,
    session: AsyncSession = Depends(get_session),
):
    try:
        card_db = await card_services.get_card(session, id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Card not found."
        ) from e
    await card_services.delete_card(session, card_db.id)
    await session.commit()

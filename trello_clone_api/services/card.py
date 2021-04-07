from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from trello_clone_api.models import Card
from trello_clone_api.schemas import CardInSchema, CardUpdateSchema


async def create_card(session: AsyncSession, card: CardInSchema) -> Card:
    new_card = Card(
        name=card.name,
        description=card.description,
        status=card.status,
        board_id=card.board_id,
    )
    session.add(new_card)
    return new_card


async def list_cards(session: AsyncSession, board_id) -> list[Card]:
    result = await session.execute(select(Card).where(Card.board_id == board_id))
    return result.scalars().all()


async def get_card(session: AsyncSession, id: int) -> Card:
    result = await session.execute(select(Card).where(Card.id == id))
    return result.first()[0]


async def update_card(
    session: AsyncSession, id: int, card_schema: CardUpdateSchema
) -> Card:
    data = card_schema.dict(exclude_none=True)
    await session.execute(update(Card).values(**data).where(Card.id == id))
    return await get_card(session, id)

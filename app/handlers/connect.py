from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.repositories import PlayerRepository, UserRepository
from app.handlers.common import get_container
from app.services.clash_api import ClashAPIError
from app.services.sync import sync_player_state

router = Router(name="connect")


def normalize_tag(raw: str) -> str:
    cleaned = raw.strip().upper()
    if not cleaned.startswith("#"):
        cleaned = f"#{cleaned}"
    return cleaned


@router.message(Command("connect"))
async def connect_command(message: Message) -> None:
    args = (message.text or "").split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Usage: /connect #PLAYER_TAG")
        return

    tag = normalize_tag(args[1])
    container = get_container(message.bot)

    async for session in container.db.session():
        user_repo = UserRepository(session)
        user = await user_repo.get_or_create(message.from_user.id)

        try:
            payload = await container.clash_api.get_player(tag)
        except ClashAPIError as exc:
            await message.answer(f"Could not connect account: {exc}")
            await session.rollback()
            return

        player = await PlayerRepository(session).upsert_player(
            user_id=user.id,
            tag=tag,
            name=payload.get("name", "Unknown"),
            town_hall=payload.get("townHallLevel"),
            builder_hall=payload.get("builderHallLevel"),
            raw=payload,
        )
        await sync_player_state(session, container, user_id=user.id, player=player)
        await session.commit()

    await message.answer(f"Connected {payload.get('name', 'Unknown')} ({tag}) and completed initial sync.")

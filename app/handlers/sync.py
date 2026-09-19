from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.database.repositories import PlayerRepository, UserRepository
from app.handlers.common import get_container
from app.services.sync import sync_player_state

router = Router(name="sync")


@router.message(Command("sync"))
async def sync_command(message: Message) -> None:
    container = get_container(message.bot)

    async for session in container.db.session():
        user = await UserRepository(session).get_or_create(message.from_user.id)
        players = await PlayerRepository(session).list_by_user(user.id)
        if not players:
            await message.answer("No connected player found. Use /connect first.")
            await session.commit()
            return

        results = []
        for player in players:
            result = await sync_player_state(session, container, user_id=user.id, player=player)
            results.append(f"{player.tag}: events={result['events']}, recommendations={result['recommendations']}")
        await session.commit()

    await message.answer("Sync complete.\n" + "\n".join(results))


@router.callback_query(F.data == "action:sync")
async def sync_callback(callback: CallbackQuery) -> None:
    if callback.from_user is None:
        await callback.answer()
        return
    container = get_container(callback.bot)
    async for session in container.db.session():
        user = await UserRepository(session).get_or_create(callback.from_user.id)
        players = await PlayerRepository(session).list_by_user(user.id)
        if not players:
            await callback.answer("Connect account first", show_alert=True)
            await session.commit()
            return
        for player in players:
            await sync_player_state(session, container, user_id=user.id, player=player)
        await session.commit()
    await callback.answer("Sync complete")

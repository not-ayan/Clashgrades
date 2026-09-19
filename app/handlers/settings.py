from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.repositories import ModeRepository, PlayerRepository, UserRepository
from app.handlers.common import get_container

router = Router(name="settings")


@router.message(Command("mode"))
async def mode_command(message: Message) -> None:
    args = (message.text or "").split()
    if len(args) < 2:
        await message.answer("Usage: /mode <max|offense|heroes|target_th> [target_town_hall]")
        return

    requested_mode = args[1].lower()
    if requested_mode not in {"max", "offense", "heroes", "target_th"}:
        await message.answer("Unsupported mode. Allowed: max, offense, heroes, target_th")
        return

    container = get_container(message.bot)
    async for session in container.db.session():
        user = await UserRepository(session).get_or_create(message.from_user.id)
        players = await PlayerRepository(session).list_by_user(user.id)
        if not players:
            await message.answer("No account connected. Use /connect first.")
            await session.commit()
            return

        config = {"mode": requested_mode}
        if requested_mode == "target_th" and len(args) >= 3:
            config["target_town_hall"] = int(args[2])
            config["target"] = f"max_available_at_th{args[2]}"

        await ModeRepository(session).set(players[0].id, config)
        await session.commit()

    await message.answer(f"Mode updated to {requested_mode}.")

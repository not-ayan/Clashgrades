from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.database.repositories import PlayerRepository, UserRepository
from app.handlers.common import get_container
from app.keyboards.main import main_menu_keyboard

router = Router(name="start")


@router.message(Command("start"))
async def start_command(message: Message) -> None:
    container = get_container(message.bot)
    async for session in container.db.session():
        user_repo = UserRepository(session)
        user = await user_repo.get_or_create(message.from_user.id)
        players = await PlayerRepository(session).list_by_user(user.id)
        await session.commit()

    summary = f"Connected accounts: {len(players)}"
    await message.answer(
        "Welcome to Clash Command Center.\n"
        "Use /connect #TAG to connect a Clash account.\n"
        f"{summary}",
        reply_markup=main_menu_keyboard(),
    )


@router.callback_query(F.data.startswith("nav:"))
async def nav_callback(callback: CallbackQuery) -> None:
    mapping = {
        "dashboard": "Use /dashboard to view your latest status.",
        "builders": "Builder view is integrated into dashboard in this build.",
        "upgrades": "Upgrade recommendations are shown in /dashboard and /ask.",
        "plan": "Use /mode and /dashboard to manage your deterministic plan.",
        "progress": "Progress appears in /dashboard based on verified snapshots.",
        "ask": "Ask with /ask <question>.",
        "settings": "Use /mode max|offense|heroes|target_th to update planning mode.",
        "audit": "Use /audit to inspect freshness and source confidence.",
    }
    screen = callback.data.split(":", 1)[1]
    await callback.answer()
    await callback.message.edit_text(mapping.get(screen, "Not implemented yet."), reply_markup=main_menu_keyboard())

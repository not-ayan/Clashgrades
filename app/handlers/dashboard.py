from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.repositories import ModeRepository, PlayerRepository, RecommendationRepository, UserRepository
from app.handlers.common import get_container
from app.renderers.dashboard import render_dashboard
from app.services.schemas import PlannerRecommendation

router = Router(name="dashboard")


@router.message(Command("dashboard"))
async def dashboard_command(message: Message) -> None:
    container = get_container(message.bot)

    async for session in container.db.session():
        user = await UserRepository(session).get_or_create(message.from_user.id)
        players = await PlayerRepository(session).list_by_user(user.id)
        if not players:
            await message.answer("No account connected. Use /connect #TAG first.")
            await session.commit()
            return

        player = players[0]
        mode = await ModeRepository(session).get(player.id)
        rec_row = await RecommendationRepository(session).latest(player.id)
        recs = []
        if rec_row:
            recs = [PlannerRecommendation.model_validate(item) for item in rec_row.data.get("recommendations", [])]
        text = render_dashboard(player.name, player.tag, player.town_hall, mode.get("mode", "max"), recs)
        await session.commit()

    await message.answer(text)

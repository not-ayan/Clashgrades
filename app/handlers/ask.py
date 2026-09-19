from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.repositories import PlayerRepository, RecommendationRepository, UserRepository
from app.handlers.common import get_container
from app.services.schemas import PlannerRecommendation

router = Router(name="ask")


@router.message(Command("ask"))
async def ask_command(message: Message) -> None:
    question = (message.text or "").replace("/ask", "", 1).strip()
    if not question:
        await message.answer("Usage: /ask <question>")
        return

    container = get_container(message.bot)
    async for session in container.db.session():
        user = await UserRepository(session).get_or_create(message.from_user.id)
        players = await PlayerRepository(session).list_by_user(user.id)
        if not players:
            await message.answer("No account connected. Use /connect first.")
            await session.commit()
            return
        rec_row = await RecommendationRepository(session).latest(players[0].id)
        recs = []
        if rec_row:
            recs = [PlannerRecommendation.model_validate(item) for item in rec_row.data.get("recommendations", [])]
        answer = await container.gemini.answer_question(question, recs)
        await session.commit()

    await message.answer(answer)

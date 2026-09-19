from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.repositories import PlayerRepository, SnapshotRepository, UserRepository
from app.handlers.common import get_container
from app.services.audit import build_audit_report

router = Router(name="audit")


@router.message(Command("audit"))
async def audit_command(message: Message) -> None:
    container = get_container(message.bot)

    async for session in container.db.session():
        user = await UserRepository(session).get_or_create(message.from_user.id)
        players = await PlayerRepository(session).list_by_user(user.id)
        if not players:
            await message.answer("No account connected. Use /connect first.")
            await session.commit()
            return

        player = players[0]
        latest = await SnapshotRepository(session).latest(player.id)
        report = build_audit_report(
            player_tag=player.tag,
            latest_snapshot_at=latest.observed_at if latest else None,
            game_data_version=(latest.game_data_version if latest else None),
            unresolved_items=0,
        )
        await session.commit()

    freshness = f"{report.snapshot_age_minutes:.1f}m" if report.snapshot_age_minutes is not None else "unknown"
    await message.answer(
        "🧪 Audit\n"
        f"Player: {report.player_tag}\n"
        f"Freshness: {freshness}\n"
        f"Game data: {report.game_data_version or 'unknown'}\n"
        f"Planner: {report.planner_version}\n"
        f"Confidence: {report.source_confidence}"
    )

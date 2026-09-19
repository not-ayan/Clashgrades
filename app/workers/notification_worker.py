from __future__ import annotations

from datetime import datetime, timezone

from aiogram import Bot

from app.database.models import User
from app.database.repositories import NotificationRepository


async def run_notification_cycle(container, bot: Bot) -> int:
    sent = 0
    async for session in container.db.session():
        repo = NotificationRepository(session)
        for notification in await repo.queued():
            user = await session.get(User, notification.user_id)
            if user is None:
                continue
            await bot.send_message(user.telegram_id, f"{notification.kind}: {notification.payload}")
            await repo.mark_sent(notification.id)
            sent += 1
        await session.commit()
    return sent


async def run_maintenance_cycle(container) -> dict:
    return {"timestamp": datetime.now(timezone.utc).isoformat(), "status": "ok"}

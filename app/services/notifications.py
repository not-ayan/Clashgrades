from __future__ import annotations

from aiogram import Bot

from app.database.repositories import NotificationRepository


class NotificationService:
    def __init__(self, bot: Bot | None = None) -> None:
        self.bot = bot

    async def dispatch_queued(self, repository: NotificationRepository) -> int:
        queued = await repository.queued()
        sent = 0
        for item in queued:
            if self.bot:
                await self.bot.send_message(
                    item.user.telegram_id if hasattr(item, "user") and item.user else item.user_id,
                    f"{item.kind}: {item.payload}",
                )
            await repository.mark_sent(item.id)
            sent += 1
        return sent

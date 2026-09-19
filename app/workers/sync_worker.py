from __future__ import annotations

from app.database.repositories import PlayerRepository
from app.services.sync import sync_player_state


async def run_sync_cycle(container) -> int:
    synced = 0
    async for session in container.db.session():
        player_repo = PlayerRepository(session)
        for player in await player_repo.list_all():
            await sync_player_state(session, container, user_id=player.user_id, player=player)
            synced += 1
        await session.commit()
    return synced

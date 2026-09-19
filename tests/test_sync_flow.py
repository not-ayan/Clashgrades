import pytest

from app.container import AppContainer
from app.database.repositories import EventRepository, PlayerRepository, SnapshotRepository, UserRepository
from app.database.session import Database
from app.services.assets import AssetService
from app.services.game_data import GameDataService
from app.services.gemini import GeminiService
from app.services.planner import PlannerService
from app.services.sync import sync_player_state


class FakeClashAPI:
    def __init__(self) -> None:
        self.calls = 0

    async def get_player(self, tag: str) -> dict:
        self.calls += 1
        level = 80 if self.calls == 1 else 81
        return {
            "tag": tag,
            "name": "Tester",
            "townHallLevel": 14,
            "troops": [],
            "heroes": [{"name": "Archer Queen", "level": level}],
            "spells": [],
            "heroEquipment": [],
        }


@pytest.mark.asyncio
async def test_sync_flow_creates_single_upgrade_event() -> None:
    db = Database("sqlite+aiosqlite:///:memory:")
    await db.create_schema()

    container = AppContainer(
        db=db,
        clash_api=FakeClashAPI(),
        planner=PlannerService(),
        gemini=GeminiService(None),
        game_data=GameDataService(version="test", source="test"),
        assets=AssetService(),
    )

    async for session in db.session():
        user = await UserRepository(session).get_or_create(telegram_id=1)
        player = await PlayerRepository(session).upsert_player(
            user_id=user.id,
            tag="#TAG",
            name="Tester",
            town_hall=14,
            builder_hall=None,
            raw={},
        )

        await sync_player_state(session, container, user_id=user.id, player=player)
        await sync_player_state(session, container, user_id=user.id, player=player)
        await sync_player_state(session, container, user_id=user.id, player=player)

        latest = await SnapshotRepository(session).latest(player.id)
        events = await EventRepository(session).exists_by_key("#TAG:UPGRADE_COMPLETED:hero:archer_queen:80:81")
        await session.commit()

    assert latest is not None
    assert events is True

    await db.dispose()

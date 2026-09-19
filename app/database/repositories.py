from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Select, desc, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import DomainEvent, ModeConfig, Notification, Player, Recommendation, Snapshot, SyncRun, User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_or_create(self, telegram_id: int) -> User:
        result = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if user:
            return user
        user = User(telegram_id=telegram_id)
        self.session.add(user)
        await self.session.flush()
        return user


class PlayerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def upsert_player(self, user_id: int, tag: str, name: str, town_hall: int | None, builder_hall: int | None, raw: dict) -> Player:
        result = await self.session.execute(select(Player).where(Player.user_id == user_id, Player.tag == tag))
        player = result.scalar_one_or_none()
        if player is None:
            player = Player(user_id=user_id, tag=tag, name=name, town_hall=town_hall, builder_hall=builder_hall, raw=raw)
            self.session.add(player)
        else:
            player.name = name
            player.town_hall = town_hall
            player.builder_hall = builder_hall
            player.raw = raw
            player.updated_at = datetime.now(timezone.utc)
        await self.session.flush()
        return player

    async def get_by_user_and_tag(self, user_id: int, tag: str) -> Player | None:
        result = await self.session.execute(select(Player).where(Player.user_id == user_id, Player.tag == tag))
        return result.scalar_one_or_none()

    async def list_by_user(self, user_id: int) -> list[Player]:
        result = await self.session.execute(select(Player).where(Player.user_id == user_id).order_by(Player.updated_at.desc()))
        return list(result.scalars().all())

    async def list_all(self) -> list[Player]:
        result = await self.session.execute(select(Player))
        return list(result.scalars().all())


class SnapshotRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_snapshot(self, player_id: int, data: dict, sync_run_id: str, source: str = "clash_api", game_data_version: str = "unknown") -> Snapshot:
        snap = Snapshot(player_id=player_id, source=source, data=data, sync_run_id=sync_run_id, game_data_version=game_data_version)
        self.session.add(snap)
        await self.session.flush()
        return snap

    async def latest(self, player_id: int) -> Snapshot | None:
        result = await self.session.execute(
            select(Snapshot).where(Snapshot.player_id == player_id).order_by(desc(Snapshot.observed_at), desc(Snapshot.id)).limit(1)
        )
        return result.scalar_one_or_none()

    async def previous_to(self, player_id: int, snapshot_id: int) -> Snapshot | None:
        result = await self.session.execute(
            select(Snapshot)
            .where(Snapshot.player_id == player_id, Snapshot.id < snapshot_id)
            .order_by(desc(Snapshot.observed_at), desc(Snapshot.id))
            .limit(1)
        )
        return result.scalar_one_or_none()


class EventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def exists_by_key(self, event_key: str) -> bool:
        result = await self.session.execute(select(DomainEvent.id).where(DomainEvent.event_key == event_key))
        return result.scalar_one_or_none() is not None

    async def create(self, player_id: int, kind: str, event_key: str, payload: dict) -> DomainEvent:
        event = DomainEvent(player_id=player_id, kind=kind, event_key=event_key, payload=payload)
        self.session.add(event)
        await self.session.flush()
        return event


class ModeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, player_id: int) -> dict:
        result = await self.session.execute(select(ModeConfig).where(ModeConfig.player_id == player_id))
        mode = result.scalar_one_or_none()
        return mode.config if mode else {"mode": "max"}

    async def set(self, player_id: int, config: dict) -> ModeConfig:
        result = await self.session.execute(select(ModeConfig).where(ModeConfig.player_id == player_id))
        mode = result.scalar_one_or_none()
        if mode is None:
            mode = ModeConfig(player_id=player_id, config=config, enabled=True)
            self.session.add(mode)
        else:
            mode.config = config
        await self.session.flush()
        return mode


class RecommendationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def store(self, player_id: int, data: dict) -> Recommendation:
        rec = Recommendation(player_id=player_id, data=data)
        self.session.add(rec)
        await self.session.flush()
        return rec

    async def latest(self, player_id: int) -> Recommendation | None:
        result = await self.session.execute(
            select(Recommendation).where(Recommendation.player_id == player_id).order_by(desc(Recommendation.generated_at), desc(Recommendation.id)).limit(1)
        )
        return result.scalar_one_or_none()


class NotificationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def queue(self, user_id: int, player_id: int, kind: str, dedupe_key: str, payload: dict) -> Notification | None:
        existing = await self.session.execute(select(Notification).where(Notification.dedupe_key == dedupe_key))
        if existing.scalar_one_or_none() is not None:
            return None
        notification = Notification(user_id=user_id, player_id=player_id, kind=kind, dedupe_key=dedupe_key, payload=payload)
        self.session.add(notification)
        await self.session.flush()
        return notification

    async def queued(self) -> list[Notification]:
        result = await self.session.execute(select(Notification).where(Notification.status == "queued").order_by(Notification.created_at))
        return list(result.scalars().all())

    async def mark_sent(self, notification_id: int) -> None:
        await self.session.execute(
            update(Notification)
            .where(Notification.id == notification_id)
            .values(status="sent", sent_at=datetime.now(timezone.utc))
        )


class SyncRunRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def start(self, run_id: str, player_id: int | None = None, source: str = "clash_api") -> SyncRun:
        run = SyncRun(run_id=run_id, player_id=player_id, source=source)
        self.session.add(run)
        await self.session.flush()
        return run

    async def finish(self, run_id: str, status: str, error: str | None = None) -> None:
        await self.session.execute(
            update(SyncRun)
            .where(SyncRun.run_id == run_id)
            .values(finished_at=datetime.now(timezone.utc), status=status, error=error)
        )

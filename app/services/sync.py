from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories import (
    EventRepository,
    ModeRepository,
    NotificationRepository,
    RecommendationRepository,
    SnapshotRepository,
    SyncRunRepository,
)
from app.services.normalizer import normalize_api_player
from app.services.planner import PlannerConfig
from app.services.reconciliation import reconcile_snapshots
from app.services.schemas import NormalizedState


async def sync_player_state(
    session: AsyncSession,
    container,
    *,
    user_id: int,
    player,
) -> dict:
    run_id = uuid4().hex
    sync_repo = SyncRunRepository(session)
    await sync_repo.start(run_id=run_id, player_id=player.id)

    try:
        payload = await container.clash_api.get_player(player.tag)
        normalized = normalize_api_player(payload)

        snapshots = SnapshotRepository(session)
        latest_before = await snapshots.latest(player.id)
        snap = await snapshots.create_snapshot(
            player_id=player.id,
            data=normalized.model_dump(mode="json"),
            sync_run_id=run_id,
            source="clash_api",
            game_data_version=container.game_data.meta.version,
        )

        previous_state = None
        if latest_before:
            previous_state = NormalizedState.model_validate(latest_before.data)
        events = reconcile_snapshots(player.tag, previous_state, normalized)

        event_repo = EventRepository(session)
        notification_repo = NotificationRepository(session)
        new_events = 0
        for event in events:
            if await event_repo.exists_by_key(event.event_key):
                continue
            await event_repo.create(player.id, event.kind, event.event_key, event.payload)
            dedupe_key = f"notif:{event.event_key}"
            await notification_repo.queue(user_id=user_id, player_id=player.id, kind=event.kind, dedupe_key=dedupe_key, payload=event.payload)
            new_events += 1

        mode_repo = ModeRepository(session)
        mode_config = await mode_repo.get(player.id)
        planner_config = PlannerConfig(
            mode=mode_config.get("mode", "max"),
            target_town_hall=mode_config.get("target_town_hall"),
            priorities=mode_config.get("priorities"),
            ignore=set(mode_config.get("ignore", [])),
        )
        recommendations = container.planner.get_recommendations(normalized, planner_config)
        rec_repo = RecommendationRepository(session)
        rec_payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "mode": planner_config.mode,
            "recommendations": [r.model_dump(mode="json") for r in recommendations],
        }
        await rec_repo.store(player.id, rec_payload)

        await sync_repo.finish(run_id=run_id, status="success")
        return {
            "snapshot_id": snap.id,
            "events": new_events,
            "recommendations": len(recommendations),
        }
    except Exception as exc:
        await sync_repo.finish(run_id=run_id, status="failed", error=str(exc))
        raise

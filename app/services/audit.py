from __future__ import annotations

from datetime import datetime, timezone

from app.services.schemas import AuditReport, SourceConfidence


def build_audit_report(player_tag: str, latest_snapshot_at: datetime | None, game_data_version: str | None, unresolved_items: int) -> AuditReport:
    age_minutes: float | None = None
    confidence = SourceConfidence.UNKNOWN
    if latest_snapshot_at:
        age_minutes = (datetime.now(timezone.utc) - latest_snapshot_at).total_seconds() / 60
        confidence = SourceConfidence.VERIFIED
    return AuditReport(
        player_tag=player_tag,
        snapshot_age_minutes=age_minutes,
        latest_sync_at=latest_snapshot_at,
        game_data_version=game_data_version,
        unresolved_items=unresolved_items,
        planner_version="v1",
        source_confidence=confidence,
    )

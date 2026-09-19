from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class SourceConfidence(StrEnum):
    VERIFIED = "VERIFIED"
    DERIVED = "DERIVED"
    HISTORICAL = "HISTORICAL"
    UNKNOWN = "UNKNOWN"


class NormalizedEntity(BaseModel):
    key: str
    name: str
    category: str
    level: int
    source_id: int | None = None
    source: str = "account_snapshot"


class NormalizedState(BaseModel):
    tag: str
    name: str
    town_hall: int | None = None
    builder_hall: int | None = None
    entities: list[NormalizedEntity] = Field(default_factory=list)
    active_upgrades: list[dict] = Field(default_factory=list)


class DomainEventModel(BaseModel):
    kind: str
    event_key: str
    payload: dict


class PlannerRecommendation(BaseModel):
    item: str
    current_level: int
    next_level: int
    cost: int | None = None
    duration_seconds: int | None = None
    priority: int
    reasons: list[str]
    source: str = "derived"


class AuditReport(BaseModel):
    player_tag: str
    snapshot_age_minutes: float | None
    latest_sync_at: datetime | None
    game_data_version: str | None
    unresolved_items: int
    planner_version: str
    source_confidence: SourceConfidence

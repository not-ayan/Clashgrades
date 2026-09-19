from __future__ import annotations

from dataclasses import dataclass

from app.services.schemas import NormalizedState, PlannerRecommendation


@dataclass(slots=True)
class PlannerConfig:
    mode: str = "max"
    target_town_hall: int | None = None
    priorities: dict[str, int] | None = None
    ignore: set[str] | None = None


DEFAULT_PRIORITY = {
    "hero": 10,
    "troop": 20,
    "spell": 25,
    "equipment": 30,
    "building": 40,
    "trap": 50,
}


class PlannerService:
    version = "v1"

    def get_recommendations(self, state: NormalizedState, config: PlannerConfig, limit: int = 5) -> list[PlannerRecommendation]:
        priorities = {**DEFAULT_PRIORITY, **(config.priorities or {})}
        ignore = config.ignore or set()

        ranked = []
        for entity in state.entities:
            if entity.key in ignore:
                continue
            priority = priorities.get(entity.category, 60)
            reasons = ["builder available", "sequential level", f"mode={config.mode}"]
            if config.mode == "heroes" and entity.category == "hero":
                priority = min(priority, 5)
                reasons.append("hero priority mode")
            if config.mode == "offense" and entity.category in {"troop", "spell", "hero", "equipment"}:
                priority = min(priority, 10)
                reasons.append("offense mode")
            ranked.append(
                PlannerRecommendation(
                    item=entity.key,
                    current_level=entity.level,
                    next_level=entity.level + 1,
                    priority=priority,
                    reasons=reasons,
                )
            )

        ranked.sort(key=lambda r: (r.priority, r.item))
        return ranked[:limit]

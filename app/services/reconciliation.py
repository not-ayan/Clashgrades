from __future__ import annotations

from app.services.schemas import DomainEventModel, NormalizedState


def reconcile_snapshots(player_tag: str, previous: NormalizedState | None, current: NormalizedState) -> list[DomainEventModel]:
    events: list[DomainEventModel] = []
    if previous is None:
        return events

    prev_index = {(e.category, e.key): e for e in previous.entities}

    for entity in current.entities:
        prev = prev_index.get((entity.category, entity.key))
        if prev is None:
            key = f"{player_tag}:ITEM_UNLOCKED:{entity.category}:{entity.key}:{entity.level}"
            events.append(
                DomainEventModel(
                    kind="ITEM_UNLOCKED",
                    event_key=key,
                    payload={"entity": entity.key, "category": entity.category, "current_level": entity.level},
                )
            )
            continue

        if entity.level > prev.level:
            key = f"{player_tag}:UPGRADE_COMPLETED:{entity.category}:{entity.key}:{prev.level}:{entity.level}"
            events.append(
                DomainEventModel(
                    kind="UPGRADE_COMPLETED",
                    event_key=key,
                    payload={
                        "entity": entity.key,
                        "category": entity.category,
                        "previous_level": prev.level,
                        "current_level": entity.level,
                        "source": entity.source,
                    },
                )
            )

    if previous.town_hall and current.town_hall and current.town_hall > previous.town_hall:
        key = f"{player_tag}:TOWN_HALL_CHANGED:{previous.town_hall}:{current.town_hall}"
        events.append(
            DomainEventModel(
                kind="TOWN_HALL_CHANGED",
                event_key=key,
                payload={"previous_level": previous.town_hall, "current_level": current.town_hall},
            )
        )

    return events

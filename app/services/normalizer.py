from __future__ import annotations

from app.services.schemas import NormalizedEntity, NormalizedState


CATEGORY_MAPPING = {
    "troops": "troop",
    "heroes": "hero",
    "spells": "spell",
    "heroEquipment": "equipment",
}


def normalize_api_player(payload: dict) -> NormalizedState:
    entities: list[NormalizedEntity] = []

    for source_key, category in CATEGORY_MAPPING.items():
        for item in payload.get(source_key, []) or []:
            if not isinstance(item, dict):
                continue
            level = item.get("level")
            name = item.get("name")
            if not isinstance(level, int) or not isinstance(name, str):
                continue
            entities.append(
                NormalizedEntity(
                    key=name.lower().replace(" ", "_"),
                    name=name,
                    category=category,
                    level=level,
                    source="account_snapshot",
                )
            )

    return NormalizedState(
        tag=str(payload.get("tag", "")),
        name=str(payload.get("name", "Unknown")),
        town_hall=payload.get("townHallLevel"),
        builder_hall=payload.get("builderHallLevel"),
        entities=entities,
        active_upgrades=[],
    )


def normalize_export_state(payload: dict, id_mapping: dict[int, str]) -> NormalizedState:
    entities: list[NormalizedEntity] = []
    for source_key, category in (("buildings", "building"), ("traps", "trap"), ("heroes", "hero"), ("units", "troop"), ("spells", "spell"), ("equipment", "equipment")):
        for item in payload.get(source_key, []) or []:
            if not isinstance(item, dict):
                continue
            source_id = item.get("data")
            level = item.get("lvl") or item.get("level")
            if not isinstance(source_id, int) or not isinstance(level, int):
                continue
            name = id_mapping.get(source_id, f"unknown_{source_id}")
            entities.append(
                NormalizedEntity(
                    key=name.lower().replace(" ", "_"),
                    name=name,
                    category=category,
                    level=level,
                    source_id=source_id,
                    source="game_export",
                )
            )

    return NormalizedState(
        tag=str(payload.get("tag", "")),
        name=str(payload.get("name", "Unknown")),
        town_hall=payload.get("townHallLevel") or payload.get("th"),
        builder_hall=payload.get("builderHallLevel") or payload.get("bh"),
        entities=entities,
        active_upgrades=[],
    )

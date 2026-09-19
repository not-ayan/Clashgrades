from app.services.normalizer import normalize_api_player, normalize_export_state


def test_normalize_api_player_basic() -> None:
    payload = {
        "tag": "#ABC",
        "name": "Ayan",
        "townHallLevel": 14,
        "troops": [{"name": "Barbarian", "level": 10}],
        "heroes": [{"name": "Archer Queen", "level": 70}],
    }
    state = normalize_api_player(payload)

    assert state.tag == "#ABC"
    assert state.town_hall == 14
    assert len(state.entities) == 2
    assert {e.category for e in state.entities} == {"troop", "hero"}


def test_normalize_export_with_mapping() -> None:
    export = {
        "tag": "#AAA",
        "buildings": [{"data": 1000008, "lvl": 18}],
        "heroes": [{"data": 2000001, "lvl": 80}],
    }
    mapping = {1000008: "Cannon", 2000001: "Barbarian King"}
    state = normalize_export_state(export, mapping)

    keys = {e.key for e in state.entities}
    assert "cannon" in keys
    assert "barbarian_king" in keys

from app.services.reconciliation import reconcile_snapshots
from app.services.schemas import NormalizedEntity, NormalizedState


def build_state(level: int) -> NormalizedState:
    return NormalizedState(
        tag="#TAG",
        name="Player",
        town_hall=12,
        entities=[
            NormalizedEntity(
                key="cannon",
                name="Cannon",
                category="building",
                level=level,
                source="account_snapshot",
            )
        ],
    )


def test_reconciliation_upgrade_event_once_for_transition() -> None:
    events = reconcile_snapshots("#TAG", build_state(18), build_state(19))
    assert len(events) == 1
    assert events[0].kind == "UPGRADE_COMPLETED"
    assert events[0].payload["previous_level"] == 18
    assert events[0].payload["current_level"] == 19


def test_reconciliation_no_event_for_same_snapshot() -> None:
    events = reconcile_snapshots("#TAG", build_state(19), build_state(19))
    assert events == []

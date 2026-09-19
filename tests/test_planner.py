from app.services.planner import PlannerConfig, PlannerService
from app.services.schemas import NormalizedEntity, NormalizedState


def sample_state() -> NormalizedState:
    return NormalizedState(
        tag="#ABC",
        name="Player",
        town_hall=15,
        entities=[
            NormalizedEntity(key="archer_queen", name="Archer Queen", category="hero", level=80),
            NormalizedEntity(key="cannon", name="Cannon", category="building", level=18),
            NormalizedEntity(key="freeze_spell", name="Freeze", category="spell", level=7),
        ],
    )


def test_heroes_mode_prioritizes_heroes() -> None:
    recs = PlannerService().get_recommendations(sample_state(), PlannerConfig(mode="heroes"), limit=3)
    assert recs[0].item == "archer_queen"


def test_offense_mode_prioritizes_offense_categories() -> None:
    recs = PlannerService().get_recommendations(sample_state(), PlannerConfig(mode="offense"), limit=3)
    assert recs[0].item in {"archer_queen", "freeze_spell"}

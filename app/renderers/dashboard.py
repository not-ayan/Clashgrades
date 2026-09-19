from __future__ import annotations

from app.services.schemas import PlannerRecommendation


def render_dashboard(player_name: str, player_tag: str, town_hall: int | None, mode: str, recommendations: list[PlannerRecommendation]) -> str:
    rec_line = "No recommendation yet"
    if recommendations:
        first = recommendations[0]
        rec_line = f"{first.item} {first.current_level}→{first.next_level}"

    th_display = f"TH{town_hall}" if town_hall else "TH?"
    return (
        "🏰 CLASH COMMAND CENTER\n\n"
        f"{th_display}\n"
        f"👤 {player_name} ({player_tag})\n"
        f"🎯 Mode: {mode}\n"
        f"✅ Next: {rec_line}\n"
    )

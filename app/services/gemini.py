from __future__ import annotations

from app.services.schemas import PlannerRecommendation


class GeminiService:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key

    async def explain_recommendation(self, recommendation: PlannerRecommendation) -> str:
        reasons = ", ".join(recommendation.reasons)
        return (
            f"Recommended upgrade: {recommendation.item} {recommendation.current_level}→{recommendation.next_level}. "
            f"Reasoning: {reasons}."
        )

    async def answer_question(self, question: str, recommendations: list[PlannerRecommendation]) -> str:
        if not recommendations:
            return "I need a synced account snapshot before I can answer that factually."
        top = recommendations[0]
        return (
            f"Based on the latest verified snapshot, start with {top.item} {top.current_level}→{top.next_level}. "
            f"Question received: {question}"
        )

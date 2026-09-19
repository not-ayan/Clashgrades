from __future__ import annotations

from dataclasses import dataclass

from app.database.session import Database
from app.services.assets import AssetService
from app.services.clash_api import ClashAPIClient
from app.services.game_data import GameDataService
from app.services.gemini import GeminiService
from app.services.planner import PlannerService


@dataclass(slots=True)
class AppContainer:
    db: Database
    clash_api: ClashAPIClient
    planner: PlannerService
    gemini: GeminiService
    game_data: GameDataService
    assets: AssetService

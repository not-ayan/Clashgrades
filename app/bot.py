from __future__ import annotations

import asyncio

from aiogram import Bot, Dispatcher

from app.config import Settings
from app.container import AppContainer
from app.database.session import Database
from app.handlers import setup_router
from app.services.assets import AssetService
from app.services.clash_api import ClashAPIClient
from app.services.game_data import GameDataService
from app.services.gemini import GeminiService
from app.services.planner import PlannerService
from app.workers.sync_worker import run_sync_cycle


async def build_container(settings: Settings) -> AppContainer:
    db = Database(settings.database_url)
    await db.create_schema()
    clash_api = ClashAPIClient(settings.coc_api_base_url, settings.coc_api_token)
    await clash_api.start()
    return AppContainer(
        db=db,
        clash_api=clash_api,
        planner=PlannerService(),
        gemini=GeminiService(settings.gemini_api_key),
        game_data=GameDataService(version="bootstrap", source="local"),
        assets=AssetService(),
    )


async def run_bot(settings: Settings) -> None:
    container = await build_container(settings)

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.include_router(setup_router())
    bot["container"] = container

    stop_event = asyncio.Event()

    async def sync_loop() -> None:
        while not stop_event.is_set():
            await run_sync_cycle(container)
            await asyncio.sleep(settings.sync_interval_minutes * 60)

    worker = asyncio.create_task(sync_loop())
    try:
        await dp.start_polling(bot)
    finally:
        stop_event.set()
        worker.cancel()
        await container.clash_api.close()
        await container.db.dispose()

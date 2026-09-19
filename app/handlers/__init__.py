from aiogram import Router

from app.handlers import ask, audit, connect, dashboard, settings, start, sync


def setup_router() -> Router:
    router = Router()
    router.include_router(start.router)
    router.include_router(connect.router)
    router.include_router(sync.router)
    router.include_router(dashboard.router)
    router.include_router(ask.router)
    router.include_router(settings.router)
    router.include_router(audit.router)
    return router

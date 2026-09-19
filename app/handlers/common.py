from __future__ import annotations

from aiogram import Bot

from app.container import AppContainer


def get_container(bot: Bot) -> AppContainer:
    return bot["container"]

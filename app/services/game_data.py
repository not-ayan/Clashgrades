from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class GameDataMeta:
    version: str
    source: str


class GameDataService:
    def __init__(self, version: str = "unknown", source: str = "unconfigured") -> None:
        self._meta = GameDataMeta(version=version, source=source)

    @property
    def meta(self) -> GameDataMeta:
        return self._meta

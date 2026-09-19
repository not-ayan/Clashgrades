from __future__ import annotations

from pathlib import Path


class AssetService:
    def __init__(self, root: str = "assets") -> None:
        self.root = Path(root)

    def get(self, category: str, key: str, level: int | None = None) -> dict:
        level_suffix = f"_{level}" if level is not None else ""
        local = self.root / category / f"{key}{level_suffix}.png"
        if local.exists():
            return {"status": "VERIFIED", "path": str(local), "source": "local_cache"}
        return {"status": "UNKNOWN", "path": None, "source": "unknown"}

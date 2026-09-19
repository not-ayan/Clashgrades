from __future__ import annotations

import asyncio
from urllib.parse import quote

import httpx


class ClashAPIError(Exception):
    pass


class ClashAPIClient:
    def __init__(self, base_url: str, token: str | None, timeout_seconds: float = 10.0, retries: int = 3) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout_seconds = timeout_seconds
        self.retries = retries
        self._client: httpx.AsyncClient | None = None

    async def start(self) -> None:
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = "Bearer " + self.token
        self._client = httpx.AsyncClient(base_url=self.base_url, headers=headers, timeout=self.timeout_seconds)

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    async def get_player(self, tag: str) -> dict:
        if self._client is None:
            await self.start()
        assert self._client is not None

        encoded_tag = quote(tag.replace("#", "%23"), safe="%")
        last_error: Exception | None = None
        for attempt in range(self.retries):
            try:
                resp = await self._client.get(f"/players/{encoded_tag}")
                if resp.status_code == 429:
                    await asyncio.sleep(min(2**attempt, 8))
                    continue
                if resp.status_code in (401, 403):
                    raise ClashAPIError("Invalid API credentials")
                if resp.status_code == 404:
                    raise ClashAPIError("Player not found")
                resp.raise_for_status()
                payload = resp.json()
                if not isinstance(payload, dict):
                    raise ClashAPIError("Malformed player response")
                return payload
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                last_error = exc
                await asyncio.sleep(min(2**attempt, 8))
            except httpx.HTTPStatusError as exc:
                raise ClashAPIError(f"API error {exc.response.status_code}") from exc

        raise ClashAPIError(f"Could not fetch player after retries: {last_error}")

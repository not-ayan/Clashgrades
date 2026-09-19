import asyncio

from app.bot import run_bot
from app.config import Settings


if __name__ == "__main__":
    asyncio.run(run_bot(Settings()))

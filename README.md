# Clash Command Center

Production-oriented Telegram companion bot for Clash of Clans.

## Features in this build

- Telegram commands: `/start`, `/connect`, `/sync`, `/dashboard`, `/mode`, `/ask`, `/audit`
- Account connection with Clash API fetch
- Snapshot persistence (append-only)
- Deterministic reconciliation for upgrade events
- Event deduplication
- Deterministic planner recommendations with modes (`max`, `offense`, `heroes`, `target_th`)
- Notification queue storage
- Background sync worker
- Audit freshness reporting

## Quick start

1. Create environment variables:

```bash
export BOT_TOKEN="..."
export COC_API_TOKEN="..."
export DATABASE_URL="sqlite+aiosqlite:///./clashgrades.db"
```

2. Install dependencies:

```bash
python -m pip install -e .[dev]
```

3. Run bot:

```bash
python main.py
```

## Test

```bash
pytest
```

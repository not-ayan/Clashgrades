# 3. System Architecture

## Recommended stack

- Python 3.12+
- aiogram 3
- SQLAlchemy 2
- PostgreSQL
- httpx
- APScheduler or equivalent background scheduler
- Pydantic / pydantic-settings
- Gemini API through the official Google GenAI SDK
- Pillow for local asset/image processing where required
- Docker

SQLite may be supported for local development, but PostgreSQL is preferred for production.

## High-level architecture

```text
                         ┌──────────────────┐
                         │ Telegram User    │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │ aiogram 3        │
                         │ handlers/router   │
                         └────────┬─────────┘
                                  ↓
                       ┌──────────────────────┐
                       │ Application Service  │
                       │ / Agent Controller   │
                       └───────┬───────┬──────┘
                               │       │
                       ┌───────┘       └────────┐
                       ↓                        ↓
                ┌─────────────┐          ┌─────────────┐
                │ Gemini      │          │ Deterministic│
                │ language    │          │ engines      │
                └─────────────┘          └──────┬──────┘
                                                │
                   ┌────────────────────────────┼────────────────────┐
                   ↓                            ↓                    ↓
             ┌────────────┐              ┌────────────┐       ┌────────────┐
             │ Clash API  │              │ Game data  │       │ PostgreSQL │
             └────────────┘              └────────────┘       └────────────┘
                   ↑
             In-game export
             where available
```

## Services

### `ClashAPI`

Responsible only for HTTP/API interaction.

### `GameData`

Responsible for static Clash facts.

### `Normalizer`

Converts source-specific data into a stable internal schema.

### `SnapshotService`

Stores immutable observations.

### `ReconciliationEngine`

Compares snapshots.

### `EventEngine`

Turns changes into domain events.

### `Planner`

Determines candidates and schedules.

### `ResourceEngine`

Calculates resource requirements and reservations only from verified data.

### `AssetService`

Resolves Clash item assets.

### `NotificationService`

Sends event-driven Telegram notifications.

### `GeminiService`

Converts natural language into structured intent/tool calls and explains verified results.

### `Renderer`

Builds Telegram messages/cards/timeline images.

## Recommended directory structure

```text
app/
  bot.py
  config.py

  handlers/
    start.py
    dashboard.py
    builders.py
    upgrades.py
    planner.py
    modes.py
    resources.py
    progress.py
    ask.py
    settings.py
    audit.py
    history.py

  keyboards/
    main.py
    builders.py
    upgrades.py
    planner.py
    modes.py
    common.py

  services/
    clash_api.py
    normalizer.py
    snapshots.py
    reconciliation.py
    events.py
    game_data.py
    assets.py
    planner.py
    scheduler.py
    resources.py
    notifications.py
    gemini.py

  database/
    models.py
    repositories.py
    migrations/

  workers/
    sync.py
    notifications.py
    maintenance.py

  renderers/
    dashboard.py
    cards.py
    timeline.py
    progress.py

tests/
```

## Architecture rule

Keep Telegram handlers thin.

Handlers should call services rather than contain Clash logic.

# 19. Codex Instructions

## Mission

Implement the Clash Command Center described by this documentation.

Do not build a superficial chatbot.

Build a maintainable production application.

## First steps

Before writing major code:

1. inspect the existing repository
2. inspect all existing files
3. identify current implementation status
4. preserve working code
5. create a task list from these documents
6. implement incrementally
7. run tests after each major subsystem

## Coding rules

### Separation of concerns

Do not put:

- Clash API logic in Telegram handlers
- planner logic in Gemini handlers
- SQL queries throughout UI code
- game-data constants throughout Python files
- image URLs throughout handlers

Use services/repositories.

### Type safety

Use:

- Pydantic models
- dataclasses where appropriate
- typed callback data
- explicit return types

### Async

Use async I/O consistently for:

- aiogram
- HTTP
- database
- Gemini

Do not block the event loop.

### Error handling

Every external dependency must have:

- timeout
- error handling
- structured logging
- retry where appropriate

### Logging

Never log secrets.

Log:

- sync run ID
- player tag in privacy-safe context
- event kind
- duration
- result
- errors

## Game data

Do not invent missing data.

If a repository/API changes schema:

1. inspect it
2. write adapter
3. validate
4. test
5. activate

## Assets

Use actual Clash assets from a verified source.

Do not make up asset URLs.

If an asset cannot be resolved:

```text
asset_status = UNKNOWN
```

and use a clean fallback UI.

## API

Do not assume unsupported fields exist.

Check official API responses and adapt.

## Planner

The planner must be deterministic.

Given the same:

```text
state
game-data version
mode
configuration
```

it should produce the same result.

## Gemini

Gemini must call backend tools for factual answers.

Use structured tool schemas.

Never pass unbounded raw database state unnecessarily.

Give Gemini only the context needed for the request.

## UI

Primary interface:

- buttons
- edited messages
- visual cards

Commands:

- `/start`
- `/connect`
- `/ask`
- `/sync`
- `/audit`
- optional power-user commands

## No fake capabilities

Do not claim the bot can:

- launch Clash upgrades
- read current loot when no source exists
- know a timer that no source exposes
- know the user's exact in-game action without observing a state change

## Required final quality bar

The project is not considered complete until:

- tests pass
- migrations work
- API sync works
- player connection works
- snapshots persist
- upgrade reconciliation works
- planner works with verified game data
- assets resolve
- notifications work
- Gemini tool calls work
- button navigation works
- errors are handled
- secrets are protected
- Docker deployment works
- `/audit` reports data coverage

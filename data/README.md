# Clash Command Center — Codex Project Documentation

This directory contains the complete project context for building a production-grade Clash of Clans Telegram companion bot with aiogram 3.

## Read order

1. `01-PROJECT-VISION.md`
2. `02-REQUIREMENTS.md`
3. `03-ARCHITECTURE.md`
4. `04-DATA-SOURCES.md`
5. `05-CLASH-API.md`
6. `06-EXPORT-JSON.md`
7. `07-GAME-DATA-AND-ASSETS.md`
8. `08-RECONCILIATION.md`
9. `09-PLANNER.md`
10. `10-GEMINI-AGENT.md`
11. `11-TELEGRAM-UX.md`
12. `12-NOTIFICATIONS.md`
13. `13-DATABASE.md`
14. `14-SYNC-AND-BACKGROUND-WORKERS.md`
15. `15-SECURITY-AND-TRUTHFULNESS.md`
16. `16-IMPLEMENTATION-PLAN.md`
17. `17-TESTING.md`
18. `18-RESEARCH-NOTES.md`
19. `19-CODEX-INSTRUCTIONS.md`

## Core principle

The bot must be a live village-management system, not a chatbot that guesses Clash facts.

```text
Account sources
    ↓
Normalized state
    ↓
Historical snapshots
    ↓
Deterministic reconciliation
    ↓
Events
    ↓
Planner / scheduler
    ↓
Telegram UI + notifications
    ↓
Gemini explanation layer
```

Gemini is an interface and reasoning/orchestration layer. It is never the source of truth for Clash statistics.

## Current implementation status

The repository created during the design process is a foundation/prototype. These documents describe the intended complete production implementation, including pieces that still need to be implemented or replaced with verified game data.

Do not claim the system is complete until all requirements and acceptance tests in these documents pass.

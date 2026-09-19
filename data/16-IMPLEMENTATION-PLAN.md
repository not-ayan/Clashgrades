# 16. Implementation Plan

## Phase 1 — Foundation

- aiogram 3
- configuration
- logging
- DB
- routers
- callback navigation
- start/settings

## Phase 2 — Account connection

- `/connect`
- validate tag
- fetch player
- persist player
- show account dashboard

## Phase 3 — API synchronization

- API client
- rate limits
- retries
- snapshots
- sync runs

## Phase 4 — Export normalization

- ID mapping
- normalized entities
- Builder Base support
- special fields

## Phase 5 — Game data

Integrate:

- structured game data
- max levels
- costs
- durations
- prerequisites
- equipment ore requirements
- Town Hall requirements

## Phase 6 — Assets

- asset provider adapter
- local cache
- building images
- hero images
- troop images
- equipment images
- resource images

## Phase 7 — Reconciliation

- snapshot diff
- idempotent events
- automatic upgrade completion
- history
- state transitions

## Phase 8 — Planner

- candidate generation
- dependency graph
- builder scheduling
- priority rules
- target modes
- custom modes
- resource reservations
- long-term plans
- what-if

## Phase 9 — Telegram presentation

- cards
- image cards
- dashboards
- timelines
- progress visuals
- navigation

## Phase 10 — Notifications

- event queue
- completion
- builder free
- finishing soon
- daily summary

## Phase 11 — Gemini

- tool schemas
- intent parser
- mode parser
- `/ask`
- explanation layer
- strict source policy

## Phase 12 — Audit and observability

- `/audit`
- health
- source freshness
- sync errors
- data coverage

## Phase 13 — Production

- Docker
- PostgreSQL
- migrations
- backup
- monitoring
- deployment
- rate-limit protection

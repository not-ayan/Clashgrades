# 5. Clash API

## Official API role

The official API is the primary account-state source for fields it exposes.

Typical information includes:

- player tag
- player name
- Town Hall
- Builder Hall
- trophies
- clan information
- troops
- heroes
- spells
- equipment
- progression-related account data

## Important limitations

Do not assume the official API provides:

- current Gold balance
- current Elixir balance
- current Dark Elixir balance
- every builder timer
- every upgrade completion timestamp
- all detailed construction state
- every piece of live village UI state

These limitations are central to the architecture.

## Consequence

Use:

```text
Official API
→ account progression/state

In-game JSON export
→ detailed village/export state

Game data
→ costs/durations/requirements/assets

Snapshots
→ change detection

Screenshots/manual input
→ live resources or visual-only state when required
```

## API security

Never hard-code API tokens.

Use:

```env
COC_API_TOKEN=
```

Never commit `.env`.

If a token is exposed publicly, rotate it.

## Rate limiting

Do not poll aggressively.

Default proposal:

- approximately every 10–15 minutes
- configurable
- manual sync available
- event-triggered reconciliation after a successful fetch

Do not call the API every few seconds.

## API client requirements

Implement:

- timeout
- retry for transient errors
- rate-limit handling
- structured errors
- logging without credentials
- response validation
- request correlation ID
- graceful shutdown

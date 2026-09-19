# 4. Data Sources

## Source hierarchy

Use the strongest source for each type of information.

### Account state

1. Official Clash API
2. In-game exported JSON
3. historical snapshots derived from either

### Static game facts

1. versioned structured Clash game-data repository
2. validated secondary source
3. never Gemini

### Visual assets

1. verified Clash asset repository/CDN
2. local cached copies
3. never generated replacement art unless explicitly needed for non-game UI

### Language

Gemini

## Provenance

Every important value should carry provenance.

Recommended values:

- `account_snapshot`
- `game_database`
- `derived`
- `historical`
- `manual`
- `unknown`

Example:

```json
{
  "value": 3500000,
  "source": "game_database",
  "game_data_version": "2026-09-xx"
}
```

## Confidence model

Use internal statuses:

- VERIFIED — direct source
- DERIVED — deterministic calculation
- HISTORICAL — observed previous snapshot
- UNKNOWN — insufficient information

Do not turn UNKNOWN into a guess.

## Source versioning

Store:

- source name
- source version / commit if available
- fetched timestamp
- schema version
- planner version

This allows regression testing when game data changes.

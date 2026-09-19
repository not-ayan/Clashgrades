# 17. Testing

## Unit tests

Test:

- API normalization
- export normalization
- ID mapping
- snapshot diff
- event generation
- idempotency
- max-level lookup
- dependency graph
- planner candidate selection
- scheduler
- resource reservation
- mode parsing
- Gemini tool validation
- asset resolution

## Regression fixture

Use the supplied Clash export format as a regression fixture.

Important categories:

```text
buildings
traps
units
heroes
spells
pets
equipment
buildings2
traps2
units2
heroes2
```

## Reconciliation tests

```text
18 → 19
```

must generate one completion event.

Repeated same snapshot:

```text
18 → 19
18 → 19
18 → 19
```

must generate no additional completion event.

## Planner tests

Test:

- target TH17 interpretation
- max mode
- ignore walls
- hero priority
- dependency blocking
- builder count
- parallel tasks
- sequential levels
- resource reservation
- unavailable resource data

## Truthfulness tests

The system should fail tests if it produces a numeric resource shortfall without a resource source.

The system should fail tests if Gemini output introduces unsupported numerical facts.

## Game-data update tests

When a new dataset is installed:

- all expected categories exist
- known IDs map
- upgrade chains are valid
- costs are non-negative
- durations are non-negative
- maximum levels are consistent
- assets referenced by critical entities exist

## Integration tests

Mock:

- Clash API
- database
- Gemini
- asset provider

Verify:

```text
API state change
→ snapshot
→ event
→ planner
→ notification
```

## Acceptance test

Scenario:

1. connect player
2. fetch initial snapshot
3. store snapshot
4. fetch modified snapshot
5. Cannon changes 18 → 19
6. reconciliation detects completion
7. history is written
8. planner recalculates
9. Telegram notification is queued
10. repeated sync does not duplicate notification

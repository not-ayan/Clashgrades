# 6. In-Game JSON Export

## Observed structure

The supplied export contained categories including:

```text
tag
timestamp
helpers
guardians
buildings
traps
decos
obstacles
units
siege_machines
heroes
spells
pets
equipment
house_parts
skins
sceneries
buildings2
traps2
decos2
obstacles2
units2
heroes2
skins2
sceneries2
```

It can also contain fields related to:

- timers
- gear-up
- supercharge
- modules
- counts
- special state

## Why it matters

The export can contain more detailed village information than the official API, particularly around detailed object state.

Therefore it should be normalized into the same internal account-state schema.

## ID mapping

The Clash export uses internal numeric `data` IDs.

A useful mapping source was discovered:

`pghant/0717bb1e0e4e0d1373e90bdb3057d9dd`

It resembles a `cocMapping.json` mapping from internal data IDs to human-readable names.

Examples discovered during research included mappings for:

- Army Camp
- Town Hall
- Cannon
- Mortar
- Barbarian King
- Archer Queen
- Grand Warden
- Royal Champion
- Minion Prince
- troops
- spells
- other game entities

## Important

The mapping file is NOT the upgrade database.

It maps identifiers to objects.

Costs, durations, requirements, and level data must come from a separate game-data source.

## Normalization

Never let the rest of the application depend on raw export field names.

Convert:

```text
raw export
→ ID resolver
→ normalized entity
```

Example:

```json
{
  "source_id": 1000008,
  "key": "cannon",
  "name": "Cannon",
  "category": "building",
  "level": 18,
  "source": "game_export"
}
```

## Regression data

Keep anonymized/sanitized fixtures based on the real export format.

Tests should verify that changes in the mapping/data source do not break normalization.

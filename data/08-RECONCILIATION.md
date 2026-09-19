# 8. Reconciliation and Automatic Upgrade Detection

## Central principle

Account state is observed repeatedly.

The system compares the latest state with the previous state.

```text
previous snapshot
       +
current snapshot
       ↓
reconciliation
       ↓
domain events
```

## Events

At minimum:

```text
UPGRADE_STARTED
UPGRADE_COMPLETED
BUILDER_AVAILABLE
BUILDER_ASSIGNED
HERO_LEVEL_CHANGED
EQUIPMENT_LEVEL_CHANGED
TOWN_HALL_CHANGED
BUILDER_HALL_CHANGED
ITEM_UNLOCKED
ITEM_CONSTRUCTED
STATE_CHANGED
```

## Example

Previous:

```json
{
  "buildings": [
    {"data": 1000008, "level": 18}
  ]
}
```

Current:

```json
{
  "buildings": [
    {"data": 1000008, "level": 19}
  ]
}
```

Mapping:

```text
1000008 → Cannon
```

Event:

```json
{
  "kind": "UPGRADE_COMPLETED",
  "entity": "cannon",
  "previous_level": 18,
  "current_level": 19,
  "detected_at": "...",
  "source": "clash_api"
}
```

## Idempotency

Repeated polling must not generate duplicate completion events.

Use a deterministic event key such as:

```text
player + entity + previous_level + current_level
```

or a stronger snapshot/event identity.

## Snapshot policy

Never overwrite snapshots.

Store:

- observed time
- source
- raw/normalized state
- data version
- sync run ID

## Reconciliation after API downtime

If multiple levels appear to have changed between snapshots, record the observed transition but do not invent intermediate timestamps.

Example:

```text
18 → 20
```

means:

> observed at 20 after previously observing 18.

It does not prove when level 19 completed.

## Builder inference

Builder state should only be inferred when the available data supports it.

If a builder timer is not available, report unknown rather than pretending to know.

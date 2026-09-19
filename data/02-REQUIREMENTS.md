# 2. Functional Requirements

## Account

The bot must support:

- Telegram user identity
- one or more Clash player tags
- player connection
- player validation
- last successful sync
- data freshness status
- manual refresh
- automatic refresh
- account removal
- account selection if multiple accounts are later supported

## Dashboard

The home screen should show:

- player name
- player tag
- Town Hall
- current planning mode
- active upgrades
- builder status
- next important completion
- next recommended upgrade
- progress summary
- last synchronization time

## Builder system

The bot should show:

- builder count where known
- busy/free state where reliably derivable
- current assignment
- completion time where available
- remaining duration where derivable
- next recommended task
- builder idle risk

## Upgrade system

Each upgrade record should support:

- item
- category
- previous level
- current level
- next level
- cost
- resource type
- duration
- prerequisites
- Town Hall requirement
- planner priority
- status
- start time if known
- completion time if known
- source

## Automatic reconciliation

The system must detect:

- level changes
- completed upgrades
- newly constructed objects
- newly unlocked objects
- Town Hall changes
- Builder Hall changes
- equipment changes
- hero changes
- troop changes
- spell changes
- relevant state changes

## Planning modes

At minimum:

- `max`
- `target_th`
- `catch_up`
- `offense`
- `heroes`
- `custom`
- temporary mode

Example:

```json
{
  "mode": "target_th",
  "target_town_hall": 17,
  "scope": ["buildings", "defenses", "traps"],
  "target": "max_available_at_th17"
}
```

Example custom mode:

```json
{
  "mode": "catch_up",
  "targets": {
    "defenses": {"minimum": 15},
    "traps": {"minimum": 8},
    "heroes": {"minimum": 80},
    "pets": {"minimum": 5}
  },
  "ignore": ["walls"],
  "priorities": {
    "heroes": 10,
    "offense": 20,
    "defenses": 30,
    "traps": 40
  }
}
```

## AI

`/ask` must support natural-language questions such as:

- What should I upgrade today?
- What am I currently upgrading?
- When will my builders be free?
- What will I need tomorrow?
- Why did you choose this?
- How long until my target is complete?
- What should I farm right now?
- Compare max mode with TH17 mode.
- What if I prioritize heroes?

## Progress

Show factual progress, such as:

- completed applicable upgrade levels
- remaining upgrade tasks
- percentage toward a defined target

Do not turn progress into an unsupported "village score".

## Audit

Provide a data-quality screen:

- account snapshot age
- latest successful API sync
- game-data version
- mapping coverage
- unresolved items
- missing resource snapshot
- planner version
- asset availability
- unknown fields

## What-if

Support simulation without changing the actual mode.

Examples:

- What if heroes are priority?
- What if I ignore walls?
- What if I target TH17?
- What if I only upgrade offense?

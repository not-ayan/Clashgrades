# 9. Deterministic Planner

## Planner responsibility

The planner decides what can be upgraded and what should be scheduled according to explicit rules.

Gemini must not replace the planner.

## Inputs

- normalized village state
- Town Hall
- Builder Hall
- active upgrades
- builder availability
- game-data maximums
- costs
- durations
- dependencies
- user mode
- priorities
- exclusions
- resource snapshot
- reservations
- manual overrides

## Planner outputs

Each recommendation should contain:

```json
{
  "item": "cannon",
  "current_level": 18,
  "next_level": 19,
  "cost": 3500000,
  "duration_seconds": 187200,
  "priority": 30,
  "reasons": [
    "matches target",
    "builder available",
    "no dependency blocker"
  ],
  "source": "derived"
}
```

## Modes

### max

Target the maximum available level according to current game-data rules.

### target_th

Example:

```json
{
  "mode": "target_th",
  "target_town_hall": 17,
  "target": "max_available_at_th17"
}
```

Interpretation:

"Max everything applicable to the highest level available at TH17."

Do not interpret this as "make every item's numeric level 17."

### offense

Prioritize:

- army capacity
- offensive buildings
- troops
- spells
- heroes
- equipment
- relevant support infrastructure

Exact priority order should be configurable.

### heroes

Prioritize hero-related progress.

### catch_up

Use minimum target thresholds.

### custom

User-defined target and priority configuration.

## Dependency graph

Represent:

```text
Task A
  ↓
Task B
  ↓
Task C
```

and enforce:

- sequential levels
- Town Hall requirements
- Hero Hall requirements where applicable
- building prerequisites
- unlock prerequisites

## Multiple builders

Treat builders as workers.

Schedule tasks across workers.

Existing researched architecture:

- SPT = shortest processing time
- LPT = longest processing time
- priority first
- duration as secondary ordering
- sequential chain continuity when useful

This is a heuristic scheduler, not a mathematically guaranteed global optimum.

## Resource constraints

A future/full implementation should be resource-aware.

Do not schedule two upgrades that require the same reserved resources unless the model explicitly accounts for the reservation.

## Builder idle risk

Detect:

```text
builder will become free at T
next eligible task begins at T + delay
```

and report avoidable idle time.

## Long-term planning

Generate:

- now
- today
- 3 days
- 7 days
- 30 days
- goal completion estimate

Goal estimates must be based on deterministic schedule assumptions.

## What-if simulation

Never mutate the actual saved mode.

Clone state:

```text
current mode
    ↓
simulation copy
    ↓
apply hypothetical rule
    ↓
run planner
    ↓
return comparison
```

## Recommendation explanation

The planner should return machine-readable reasons.

Gemini may translate those reasons into natural language but must not invent additional factual reasons.

# 10. Gemini Agent Layer

## Role

Gemini is the natural-language interface and tool orchestrator.

It is not the Clash database.

## Core rule

Gemini can only state numerical Clash facts present in verified tool results.

If a value is absent:

```text
UNKNOWN
```

must remain unknown.

## Tools

Recommended backend tools:

```text
get_account()
get_latest_snapshot()
get_snapshot_age()
get_active_upgrades()
get_builders()
get_resources()
get_current_mode()
get_upgrade_candidates()
get_upgrade_cost()
get_upgrade_time()
get_upgrade_requirements()
calculate_upgrade_plan()
calculate_long_term_plan()
simulate_plan()
compare_modes()
set_mode()
get_progress()
get_upgrade_history()
get_audit()
```

## Example

User:

> What should I upgrade today?

Gemini calls:

```text
get_account
get_active_upgrades
get_builders
get_current_mode
get_upgrade_candidates
calculate_upgrade_plan
```

Backend returns verified data.

Gemini explains it.

## Mode parsing

User:

> Change mode to all buildings to townhall 17 level.

Gemini should interpret:

```json
{
  "mode": "target_th",
  "target_town_hall": 17,
  "scope": ["buildings"],
  "target": "max_available_at_th17"
}
```

not:

```json
{
  "level": 17
}
```

## Validation

Gemini's proposed structured configuration must pass Pydantic/backend validation before persistence.

## Anti-hallucination system rules

The agent should be instructed:

- Never invent game values.
- Never infer current resources without a source.
- Never claim an upgrade has started unless the source proves it.
- Never claim an upgrade completed unless reconciliation detected it.
- Never invent a timer.
- Never invent a cost.
- Never invent a requirement.
- Never invent an asset.
- If source data is stale, state the age.
- If two sources disagree, surface the disagreement.
- Prefer unknown over guessing.

## Explanation example

Bad:

> Your Cannon should cost around 3.5M.

Good:

> The current game-data version lists 3.5M Gold for Cannon 18 → 19.

## Natural-language flexibility

Gemini should handle:

- casual phrasing
- typos
- short questions
- comparative questions
- multi-step requests
- mode changes

but always resolve them into deterministic backend actions.

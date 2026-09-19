# 1. Project Vision

## Name

Clash Command Center

## Goal

Build a professional, visual, live Clash of Clans companion inside Telegram.

The user should be able to connect a Clash account and have the bot continuously understand:

- Town Hall / Builder Hall progression
- buildings
- defenses
- traps
- heroes
- pets
- troops
- spells
- hero equipment
- current upgrades where the source exposes enough information
- upgrade history
- available/planned builders
- upgrade costs
- upgrade durations
- target progression
- planning modes
- long-term roadmap
- resource requirements when resource data is available
- progress toward user-defined goals

The bot should continuously synchronize the account and automatically detect changes.

### Critical UX rule

Never ask:

> "Did you upgrade this?"

when a reliable account source can determine that the item changed.

Example:

```text
Snapshot A:
Cannon level 18

Snapshot B:
Cannon level 19

→ UPGRADE_COMPLETED
```

The bot records this automatically, updates history, reconciles builders, recalculates the plan, and optionally sends a notification.

## Product philosophy

The experience should feel closer to a small Clash management application embedded inside Telegram than a conventional command bot.

Primary interaction:

- inline buttons
- edited messages
- visual cards
- Clash item imagery
- concise dashboards

Secondary interaction:

- natural language via `/ask`
- natural-language mode configuration
- commands for power users

## Three system layers

### Monitor

Continuously understand the village.

### Think

Use deterministic rules and Gemini to interpret goals and explain results.

### Plan

Calculate what should happen next based on goals, dependencies, builders, time, and verified resources.

## Non-goals

Do not:

- invent Clash values
- claim API data that is unavailable
- pretend to start upgrades inside the game
- fabricate current loot
- fabricate builder timers
- make unsupported farming-yield predictions
- let Gemini silently create numerical game facts

## Long-term product

Potential future features:

- multiple accounts
- multiple villages
- clan/war awareness if reliable data is available
- richer farming planner
- historical efficiency statistics
- goal completion tracking
- what-if simulations
- comparison between planning modes
- mobile/web companion UI

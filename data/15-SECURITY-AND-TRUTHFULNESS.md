# 15. Security and Truthfulness

## Secrets

Never commit:

- Telegram bot token
- Clash API token
- Gemini API key
- database password

Use environment variables or a secret manager.

## User privacy

Do not expose one user's player information to another user.

Every player lookup must be authorized against the Telegram account that owns it.

## Credential handling

Never log authorization headers.

Never include tokens in exceptions.

## Truthfulness

This project explicitly prioritizes factual integrity.

Every numerical answer should be traceable to:

```text
account snapshot
game database
derived calculation
historical observation
```

or be marked unknown.

## Conflicting sources

Example:

```text
API says level 19
old export says level 18
```

Use source priority and timestamp.

Do not silently merge contradictory values.

## Stale data

Display freshness.

Example:

```text
Last verified sync: 14 minutes ago
```

## Unknown resources

Never estimate current loot without verified observations.

## Farming forecasts

Only calculate observed farming rates if enough historical resource snapshots exist.

Do not invent:

- average loot per attack
- attacks per hour
- win rate
- farming efficiency

unless these are based on actual collected data.

## API actions

The bot is an assistant.

Do not imply it can control the Clash game client.

A button such as "Select upgrade" means selecting a recommendation, not executing the upgrade inside Clash.

## Audit

Users should be able to inspect:

- source
- freshness
- game-data version
- unresolved data
- planner version

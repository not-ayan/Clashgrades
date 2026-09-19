# 12. Notifications

## Event-driven model

Notifications should be driven by domain events, not blind repeated messages.

## Important notifications

### Upgrade completed

```text
UPGRADE_COMPLETED
```

### Builder available

```text
BUILDER_AVAILABLE
```

### Upgrade finishing soon

Use verified completion timestamps only.

Suggested thresholds:

- 6 hours
- 1 hour
- 15 minutes

Make configurable.

### Daily summary

Configurable daily report.

### Resource target

Only if:

- required cost is verified
- current resource balance is verified
- shortfall can be calculated

## Resource limitation

The official API does not provide current loot balances.

Therefore:

```text
Known upgrade cost + unknown current Gold
```

must not become:

```text
You need 1.7M more Gold
```

It should say:

> The upgrade requires 3.5M Gold. Your current Gold balance is not available from a verified source.

## Notification deduplication

Store notification identity.

Do not send the same event repeatedly after each polling cycle.

## User settings

Allow:

- enable/disable notifications
- completion alerts
- builder alerts
- finishing-soon alerts
- daily report
- notification time
- minimum significance

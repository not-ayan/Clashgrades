# 14. Sync and Background Workers

## Sync loop

Suggested default:

```text
every 15 minutes
```

Configurable via environment.

## Workflow

```text
fetch API
  ↓
validate response
  ↓
normalize
  ↓
store snapshot
  ↓
load previous snapshot
  ↓
diff
  ↓
emit events
  ↓
update current state
  ↓
recalculate relevant plan
  ↓
queue notifications
```

## Do not fail the entire worker

If one player fails:

- log error
- retain previous state
- continue with other players

## API errors

Handle:

- timeout
- HTTP 429
- 401/403
- 404
- 5xx
- malformed JSON

## Retry

Use bounded exponential backoff for transient errors.

Do not retry invalid credentials endlessly.

## Notification worker

Can run every minute or use scheduled jobs.

It should process:

- queued event notifications
- completion thresholds
- daily reports

## Maintenance worker

Daily tasks:

- clean expired temporary state
- prune old debug logs
- verify asset cache
- verify game-data version
- database maintenance

Do not automatically delete snapshots required for history unless retention policy explicitly allows it.

## Graceful shutdown

Close:

- Telegram session
- HTTP clients
- DB connections
- background tasks

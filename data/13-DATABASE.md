# 13. Database

## Core tables

### users

```text
id
telegram_id
created_at
```

### players

```text
id
user_id
tag
name
town_hall
builder_hall
raw
updated_at
```

### snapshots

```text
id
player_id
observed_at
source
data
game_data_version
schema_version
sync_run_id
```

### normalized_entities

Optional normalized current state.

```text
id
player_id
category
key
source_id
name
level
max_level
updated_at
```

### upgrades

Current/inferred upgrade records.

```text
id
player_id
entity_id
from_level
to_level
started_at
completed_at
status
source
```

### upgrade_history

Immutable historical upgrade events.

### events

Domain events:

```text
kind
payload
created_at
```

### modes

```text
player_id
config
enabled
created_at
updated_at
```

### goals

Long-term goals.

### recommendations

Planner output snapshots.

### resource_snapshots

Only verified/manual/screenshot-derived resources.

### notifications

Sent/pending notification records.

### sync_runs

```text
started_at
finished_at
status
error
source
```

## Immutability

Snapshots and historical events should be append-only.

Do not rewrite history when a newer snapshot arrives.

## Indexes

Index:

- player tag
- player ID
- snapshot player + observed_at
- event player + created_at
- upgrade player + status
- notification user + sent_at

# 11. Telegram UX

## Design direction

Professional, visual, compact.

The bot should feel like a Clash management app inside Telegram.

Primary navigation is buttons.

Commands remain available for power users.

## Main menu

Concept:

```text
🏰 CLASH COMMAND CENTER

TH18

🔨 Builders       4/6
⚔️ Active         6
🎯 Mode           TH17 MAX

Next completion
👑 Queen 110 → 111
5h 12m

[ 📊 Dashboard ]
[ 🔨 Builders ]
[ ⚔️ Upgrades ]

[ 🎯 Plan ]
[ 💰 Resources ]

[ 📈 Progress ]
[ 🧠 Ask AI ]

[ ⚙️ Settings ]
[ 🔄 Refresh ]
```

## Message editing

Prefer editing the current Telegram message when navigating.

Avoid flooding the chat with new messages.

## Buttons

Use structured aiogram callback data.

Do not encode complex state into fragile strings.

## Dashboard

Should show:

- TH
- mode
- builder state
- active upgrades
- next completion
- recommendation
- progress
- freshness

## Upgrade card

Use actual Clash image:

```text
[CANNON IMAGE]

CANNON

18 → 19

💰 3,500,000 Gold
⏱ 2d 4h

🎯 TH17 MAX
```

Buttons:

```text
[ Details ]
[ Why? ]
[ Timeline ]
[ Back ]
```

## Builder card

```text
[QUEEN IMAGE]

Builder #2
Archer Queen
110 → 111

⏱ 5h 12m
```

## Automatic completion notification

When reconciliation detects a level change:

```text
[CANNON IMAGE]

✅ UPGRADE COMPLETE

Cannon
18 → 19

Builder state:
🟢 Available

Recommended:
[X-BOW IMAGE]
X-Bow 10 → 11
```

Do not ask for confirmation.

## Main screens

Required:

- Dashboard
- Builders
- Upgrades
- Plan
- Resources
- Progress
- AI
- Settings
- Audit
- History

## Imagery

Use real Clash imagery for:

- buildings
- heroes
- troops
- spells
- pets
- equipment
- resources
- Town Hall

Do not replace these with generic emoji.

Emoji can remain as secondary labels.

## Timeline image

Telegram has limited native chart UI.

Generate a compact timeline image where useful:

```text
TODAY             TOMORROW

Builder 1
[CANNON]████████████

Builder 2
[QUEEN]████████

Builder 3
[X-BOW]████████████████
```

Use Pillow or another deterministic renderer.

## Daily report

A visual summary can show:

- active builders
- completions today
- resource targets
- next upgrade
- progress

## Visual performance

Do not send an image for every trivial interaction.

Use imagery strategically to keep Telegram responsive.

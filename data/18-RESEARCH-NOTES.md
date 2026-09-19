# 18. Research Notes

## Clashify

Clashify Village Tracker was examined as a reference product.

Relevant observed behavior:

- accepts Clash in-game JSON
- parses internal IDs
- combines account data with game data
- calculates remaining upgrades
- calculates resource/time requirements
- presents visual tracker information

The exact proprietary implementation is unknown.

Use it as a UX/behavior reference, not as proof of its internal code.

## cocMapping JSON

Research identified:

`https://gist.github.com/pghant/0717bb1e0e4e0d1373e90bdb3057d9dd`

Useful for mapping export `data` IDs to names.

It does not provide the full upgrade database.

## SamBro2901/coc-upgrade-optimizer

Repository:

`https://github.com/SamBro2901/coc-upgrade-optimizer`

Important architectural discoveries:

- React client-side upgrade scheduler
- local game-data JSON
- parses Clash export
- maps IDs
- detects TH/BH
- detects builders
- handles active timers
- creates upgrade tasks
- dependency graph
- multiple-worker scheduling
- SPT/LPT heuristics
- current tasks are treated as in-progress
- priority + duration based scheduling

This is a useful reference architecture.

Important limitation:

It is a heuristic scheduler, not a mathematically proven global optimizer.

## chiefpansancolt/clash-of-clans-data

Repository:

`https://github.com/chiefpansancolt/clash-of-clans-data`

Useful structured source for game data and assets.

Contains broad Clash categories and per-level upgrade data.

## Statscell/clash-of-clans-data

Repository:

`https://github.com/Statscell/clash-of-clans-data`

Useful for raw/normalized data research and possible future update pipeline.

## ClashKing assets

Repository:

`https://github.com/ClashKingInc/ClashKingAssets`

Useful for standardized game assets.

## Important architectural conclusion

No single source should be assumed to provide everything.

Use:

```text
API
+
export
+
ID mapping
+
game database
+
assets
+
snapshots
```

## API limitations discovered

The official API should not be treated as a source for:

- current resource balances
- every builder timer
- every exact completion timestamp
- all detailed village construction state

This is why the bot needs multiple data sources.

## Gemini conclusion

Gemini should be used for:

- natural-language understanding
- intent extraction
- tool selection
- explanations
- mode parsing

It should not calculate or invent Clash facts.

## Visual conclusion

Use actual Clash building/hero/equipment artwork like Clashify-style trackers rather than generic emoji-only cards.

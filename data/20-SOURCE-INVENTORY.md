# 20. Source Inventory

## External repositories/resources

| Resource | Purpose | Status |
|---|---|---|
| `chiefpansancolt/clash-of-clans-data` | Structured Clash game data and assets | Primary candidate |
| `Statscell/clash-of-clans-data` | Raw/normalized data research | Secondary |
| `ClashKingInc/ClashKingAssets` | Standardized Clash assets | Asset candidate |
| `SamBro2901/coc-upgrade-optimizer` | Scheduler/planner reference | Architecture reference |
| `pghant/.../cocMapping.json` gist | Export ID → name mapping | Mapping reference |
| Clashify Village Tracker | UX/behavior reference | Product reference |

## Important source URLs

- https://github.com/chiefpansancolt/clash-of-clans-data
- https://github.com/Statscell/clash-of-clans-data
- https://github.com/ClashKingInc/ClashKingAssets
- https://github.com/SamBro2901/coc-upgrade-optimizer
- https://gist.github.com/pghant/0717bb1e0e4e0d1373e90bdb3057d9dd
- https://clashify.app/village-tracker

## Verification policy

External sources can change.

Before production:

- verify repository structure
- verify current data version
- verify licenses/usage rights
- verify asset paths
- pin versions/commits where practical
- record source version in the database

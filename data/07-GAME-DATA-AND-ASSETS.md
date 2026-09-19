# 7. Game Data and Assets

## Primary researched repository

`chiefpansancolt/clash-of-clans-data`

GitHub:
https://github.com/chiefpansancolt/clash-of-clans-data

It was identified as a strong structured game-data source covering:

- Home Village
- Builder Base
- Clan Capital
- buildings
- defenses
- traps
- troops
- spells
- heroes
- hero equipment
- pets
- siege machines
- resource buildings

It contains structured per-level information, including upgrade-related data.

## Secondary researched repository

`Statscell/clash-of-clans-data`

GitHub:
https://github.com/Statscell/clash-of-clans-data

Useful as another data/reference pipeline and for understanding normalized/raw Supercell game data.

## Asset source

`ClashKingInc/ClashKingAssets`

GitHub:
https://github.com/ClashKingInc/ClashKingAssets

Useful for standardized Clash visual assets.

## Clashify research

Clashify's Village Tracker was investigated as a product reference.

Observed/concluded behavior:

```text
export JSON
→ map IDs
→ normalized village state
→ game data
→ remaining upgrades
→ resource/time calculations
→ tracker UI
```

Its proprietary internal implementation is not known. Do not present reconstructed behavior as confirmed source code.

## Asset philosophy

The bot should use actual Clash item artwork, not generic emoji, for:

- Cannon
- Archer Tower
- X-Bow
- Inferno Tower
- Eagle Artillery
- Scattershot
- Monolith
- Town Hall
- heroes
- troops
- spells
- pets
- equipment
- resources

## Asset resolver

Create:

```python
asset_service.get(
    category="building",
    key="cannon",
    level=19
)
```

Return a local cached path or validated remote asset.

## Caching

Do not download the same asset repeatedly.

Cache by:

```text
provider
item
category
level
version
```

## Data update validation

When updating game data:

1. download candidate dataset
2. validate schema
3. validate required categories
4. validate ID mapping
5. validate upgrade levels
6. validate asset references
7. run regression tests
8. only then activate new version

Never silently replace a working game-data version with malformed data.

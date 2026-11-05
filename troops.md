---
# Date the values below were read in the game (YYYY-MM-DD). Used by scripts/build_data.py.
as_of: 2026-10-21
---
# Troops Inventory & Formations

Detailed breakdown of military forces, training facilities, infirmary capacity, and configured march formations in [Kingshot](https://www.centurygames.com/games/kingshot/).

Dates in the **Updated** column, and in _(YYYY-MM-DD)_ after other values, show when each value was last uploaded to this repository.

## Current Troop Inventory

Standing forces are **Tier VIII (Elite)** units across the three military branches (Tier VII Brave on 24 Oct). Counts are from the Troops Preview screen, "All" tab (in town and out of town), of 2026-11-05; that screen lists only these three units, each with a "VIII" badge. Net Change is against the 2026-10-24 counts of the Tier VII units; the screens do not show whether the Tier VII troops were promoted to Tier VIII or trained new.

| Branch | Tier | Unit Name | Headcount | Distribution % | Status | Net Change | Updated |
| :--- | :---: | :--- | :---: | :---: | :--- | :---: | :---: |
| **Infantry** | VIII | Elite Infantry | 45,474 | 33.7% | All (in and out of town) | +11,323 | 2026-11-05 |
| **Cavalry** | VIII | Elite Cavalry | 46,298 | 34.3% | All (in and out of town) | +9,860 | 2026-11-05 |
| **Marksmen** | VIII | Elite Archer | 43,180 | 32.0% | All (in and out of town) | +8,040 | 2026-11-05 |
| **Total Military Force** | **VIII** | — | **134,952** | **100%** | **0 Injured** | +29,223 | 2026-11-05 |

## Army Statistics & Facility Caps

| Attribute | Value | Status / Notes | Updated |
| :--- | :---: | :--- | :---: |
| **Total Standing Troops** | 134,952 | Troops Preview, "All" tab: the sum of the three counts. The header reads "134.9K/134.9K" (5 Nov; 105.7K/105.7K on 24 Oct). On 22 Oct it read "1,278/98,409" with March Queue 2/4; on 23 and 24 Oct both numbers match and the queue reads 4/4, which suggests the first number counts troops in town (inferred; the screen does not say) | 2026-11-05 |
| **Single March Capacity** | 88,880 | `Be` and `Att` show 88,880 / 88,880 on the Deploy screen; `Gat` shows 88,410 / 88,410. The 470 difference equals Edwin's lower Troop Capacity (12,260 at Lv. 59 against 12,730 at Lv. 64), which suggests that a march holds a base amount plus its three heroes' Troop Capacity (inferred; the base would be 50,690). 79,275 for all three presets on 24 Oct | 2026-11-05 |
| **Available March Queues** | 4 / 4 | Shown as "March Queue 4/4" on the Troops Preview screen (5 Nov, as on 24 Oct). With the 22 Oct reading of 2/4 (when most troops were not counted in town), this suggests the first number is free queues (inferred; the screen does not say) | 2026-11-05 |
| **Infirmary Hospital Capacity** | 72,800 | 0 / 72,800 injured (38,600 on 24 Oct) | 2026-11-05 |
| **Overall Account Power** | Not recorded (kept in profile.md only, so this copy cannot fall behind) | See profile.md | 2026-10-22 |
| **Town Center Level** | Level 22 | 32/32 Citizens, 735 ATK / 1,470 DEF / 22,064 HP (27 Oct); the Governor Profile shows Lv. 22 on 5 Nov | 2026-11-05 |

## Saved March Formations

### Formation 1: Beast Hunting (`Be`) — PvE Preset
* **Formation Power:** 18,227,722 (9,840,959 on 24 Oct) _(2026-11-05)_
* **Total Troops:** 88,880 / 88,880 (Full March) _(2026-11-05)_
* **Assigned Heroes:** Diana (Lv. 64, Archer Lead), Gordon (Lv. 64, Cavalry), Forrest (Lv. 64, Infantry) _(2026-11-05)_
* **Tactical Objective:** High archer burst to eliminate map beasts and wandering monsters with minimal casualties, boosted by Diana's -18% Stamina Cost (Iron Constitution Lv. 4) and +60% Hunting March Speed. _(2026-10-21)_

| Branch | Unit Tier | Deployed Count | Available Count | Troop Ratio % | Updated |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Elite Infantry** | VIII | 31,108 | 45,474 | 35% | 2026-11-05 |
| **Elite Cavalry** | VIII | 17,776 | 46,298 | 20% | 2026-11-05 |
| **Elite Archer** | VIII | 39,996 | 43,180 | 45% | 2026-11-05 |

### Formation 2: Attack (`Att`) — PvP / Open-Field Preset
* **Formation Power:** 20,910,710 (11,279,258 on 24 Oct) _(2026-11-05)_
* **Total Troops:** 88,880 / 88,880 (Full March) _(2026-11-05)_
* **Assigned Heroes:** Howard (Lv. 64, Infantry Lead), Jabel (Lv. 64, Cavalry), Quinn (Lv. 64, Archer) _(2026-11-05)_
* **Tactical Objective:** Balanced frontline absorption and cavalry hammer for player battles and rally strikes. _(2026-10-21)_

| Branch | Unit Tier | Deployed Count | Available Count | Troop Ratio % | Updated |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Elite Infantry** | VIII | 44,440 | 45,474 | 50% | 2026-11-05 |
| **Elite Cavalry** | VIII | 26,664 | 46,298 | 30% | 2026-11-05 |
| **Elite Archer** | VIII | 17,776 | 43,180 | 20% | 2026-11-05 |

### Formation 3: Gathering (`Gat`) — Resource Preset
* **Formation Power:** 16,968,707 (9,161,177 on 24 Oct) _(2026-11-05)_
* **Total Troops:** 88,410 / 88,410 (Full March; 470 less than the other presets, see Single March Capacity) _(2026-11-05)_
* **Assigned Heroes:** Seth (Lv. 64, Infantry Lead), Edwin (Lv. 59, Cavalry), Amane (Lv. 64, Archer) _(2026-11-05)_
* **Tactical Objective:** Wilderness gathering. Only two of the three heroes have a gathering skill, each for one resource: Seth (Craftsmanship, +20% Iron Mining Speed) and Edwin (Stone Mining, +15%). Amane's expedition skills are Tri-Phalanx (+15% squad Attack) and Exorcism (infirmary). _(2026-10-24)_

| Branch | Unit Tier | Deployed Count | Available Count | Troop Ratio % | Updated |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Elite Infantry** | VIII | 45,089 | 45,474 | 51% | 2026-11-05 |
| **Elite Cavalry** | VIII | 43,321 | 46,298 | 49% | 2026-11-05 |
| **Elite Archer** | VIII | 0 | 43,180 | 0% | 2026-11-05 |

The Deploy screen shows preset tabs `Be`, `Att`, `Gat`, `4`, `5` and `6`, then locked tabs; `4` and `5` carry a flag icon like the named presets and `6` shows only its number. Presets 4 to 6 were not opened, so their heroes and troops are not recorded. _(2026-11-05)_

## Beast & Terror Hunting

The levels were told by the account owner on 2026-10-25 and match the two world-map screens of the same day (about 14:46 UTC). Map positions are not recorded.

| Target | Level | Attack type | Stamina | Recommended Power | Possible drops | Updated |
| :--- | :---: | :--- | :---: | :---: | :--- | :---: |
| **Lion** (beast) | **Lv. 21** (highest the account can take) | Attack (single march) | 10 | 3,012,128 | EXP ×410, bread ×78.5K, wood ×78.5K, stone ×15.7K | 2026-10-25 |
| **Alpha Black Panther** (Terror) | **Lv. 4** (highest the account can take) | **Rally only** | 25 | 37,797,400 | Hero shard ×1 (purple puzzle icon), gems ×25, an item ×20 (scroll icon; name not shown), 5-min speedup ×4 | 2026-10-25 |

* The Terror panel showed a timer of 05:54:37, read as the time before this Terror leaves the map (inferred; the screen does not say). _(2026-10-25)_
* Whether the stamina costs shown already include Diana's −18% (Iron Constitution) is not shown. _(2026-10-25)_
* For scale: the `Be` preset is 18,227,722 power (5 Nov; 9,840,959 on 24 Oct) against the Lion's recommended 3,012,128 (25 Oct); the strongest preset, `Att`, is 20,910,710 (5 Nov) against the Terror's recommended 37,797,400 (25 Oct), so a Terror rally still needs other players' marches. _(2026-11-05)_

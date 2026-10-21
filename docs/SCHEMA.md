# `KS_DATA` schema

`docs/index.html` renders every view from one JSON object, `KS_DATA`, found between
`/* KS_DATA:BEGIN */` and `/* KS_DATA:END */`. Replace only that block to update the dashboard.

## General rules

- **Missing = `null`.** The page shows "Not recorded" for any `null`/absent value. Never invent a value.
- **Dates** are ISO strings `YYYY-MM-DD`. Every section carries `asOf`; heroes carry their own `asOf`.
- **Never include the Player ID.** The page has no field for it.
- **Derived values are not stored.** Level caps, assignments, power sums, conflicts, the Drill Camp
  placement plan and feature states are computed by the page from the fields below.
- Hero lists, game features, recommendations and data-health items are arrays of any length
  (the hero UI is tested for 1–60 heroes).

## Top-level keys

| Key | Type | Used by |
|---|---|---|
| `meta` | object | Header data age, "New" badges, stale checks |
| `governor` | object | Header, Overview tiles, City |
| `townCenter` | object | Overview, City, level caps, feature unlock distances |
| `resources` | object | Overview (gems), City |
| `governorGear` | object | City |
| `army` | object | Overview, Army & marches |
| `rules` | object | Level caps, Drill Camp rule text, Gen 2 note (community rules, Unverified) |
| `heroes` | array | Heroes, drawer, Drill Camp, power checks |
| `drillCamp` | object \| null | Drill Camp |
| `lineups` | object | Army & marches, Defense & Arena, hero assignments |
| `recommendations` | array | Overview Top 5, Invest |
| `features` | array | Features |
| `dataHealth` | object | Data health (plus computed checks) |
| `codes` | object \| null | Codes |

## Field reference

### `meta`
| Field | Type | Notes |
|---|---|---|
| `schemaVersion` | number | Currently `1` |
| `snapshotAsOf` | date | Date shown in the header; sections older than this are flagged "older" |
| `staleAfterDays` | number | Sections older than this many days are flagged "stale" (default 7) |
| `previousSnapshot.asOf` | date \| null | When the previous hero list was taken |
| `previousSnapshot.heroes` | string[] | Hero names in the previous snapshot; heroes not in it get a "New" badge. Empty list = no badges |
| `lockedHeroesNotInData` | number \| null | Shown as a note under the hero grid |

### `governor`
`name`, `kingdom`, `alliance`, `vip`, `power`, `kills`, `stamina{current,max}`, `serverDay`, `asOf`.

### `townCenter`
`level`, `citizens{current,max}`, `attack`, `defense`, `health`,
`perks{unlocked,total,namesVerified}`, `asOf`. Perk names are intentionally not stored.

### `resources`
`bread`, `wood`, `stone`, `iron`, `gems`: each `{ "value": number, "rounded": boolean }` or `null`.
`rounded: true` means the game showed a rounded figure (e.g. 94.6M). Plus `asOf`.

### `governorGear`
`slotsTotal`, `slotsLocked`, `asOf`.

### `army`
| Field | Notes |
|---|---|
| `total`, `tier`, `injured`, `marchCapacity`, `infirmary` | Numbers / text |
| `queues{current,max}` | March queues |
| `classes[]` | `{ key, name, count, pct }`. `key` (`inf`/`cav`/`arc`) links to march `troops` keys and bar colours |
| `asOf` | date |

### `rules`
`source`, `confidence`, `heroLevelCapByTC` (`{"20": 54, ...}`), `drillCamp` (text),
`oneMarchPerHero` (text), `gen2Heroes{serverDay}`.

### `heroes[]`
| Field | Type | Notes |
|---|---|---|
| `name` | string | Required; the key used everywhere else |
| `rarity`, `cls`, `generation`, `role` | string \| null | Filter options are built from the values present |
| `level`, `stars`, `tier` | number \| null | |
| `shards` | `{have, need, to}` \| null | `to` = next step label (`"4★"`, `"T4"`); `null` shows "next step" |
| `power`, `gearPower` | number \| null | |
| `gear` | `{slots, note}` \| null | `slots` = `null` (not recorded) or `[{slot, state, quality?}]`; `state` is `"empty"`, `"plus0"` or free text. Empty and +0 slots are highlighted |
| `widget` | `{unlocked, name, level}` \| null | |
| `skills` | array \| null | `{name, status, level?, count?, all?, needs?, effect?, note?, confidence?}`; `status` is `capped`, `upgradeable`, `progress` or `locked` |
| `notes` | string[] | Shown in the drawer |
| `asOf` | date | |

### `drillCamp`
`asOf`, `instructors[{hero, level}]`, `slotsTotal`, `slotsOpen`, `slotted` (string[]),
`lockedSlots[{slot, requirement, tcLevel, note}]`, `testHero`.

### `lineups`
| Field | Notes |
|---|---|
| `marches[]` | `{name, purpose, heroes[{hero, lead?}], troops{inf,cav,arc}, ratioPct{inf,cav,arc}, power}` |
| `arena.attack`, `arena.defense` | `{power, front: string[], back: string[]}` |
| `guardStation` | `{heroes: string[]}` \| null |
| `barricades[]` | `{name, level, maxed, power, powerRounded, heroes: string[]}` |
| `asOf` | date |

### `recommendations[]`
| Field | Notes |
|---|---|
| `id` | Unique string |
| `priority` | Lower = higher; the first five feed "Top 5 moves now" |
| `type` | Invest group heading (groups are built from the values present) |
| `what`, `why` | Required text |
| `cost` | Text or `null` ("Not known") |
| `confidence` | Array of `"Verified"`, `"Inferred"`, `"Unverified"` |
| `heroes` | Hero names (clickable, also the Invest hero filter) |
| `evidence` | Strings citing the source data |
| `note` | Optional caveat |

### `features[]`
`{name, unlock, state, hasData, source, asOf, note}`.
`unlock` is `{type:"tc", level}`, `{type:"serverDay", day}` or `null`.
`state` (`"Active"`, `"Locked"`, `"Coming soon"`, `"Unknown"`) wins when set; when `null`, the page
computes it from `unlock` and labels it "(by rule)", or shows "Unknown".

### `dataHealth`
`conflicts[{area, title, detail}]` and `missing[{area, title}]`. The page adds computed items:
lineup power vs. sum of hero powers (>1% difference), Drill Camp level vs. hero level, per-field gaps
across the roster, and stale or undated sections.

### `codes`
`asOf`, `active[{code, redeemed}]`, `expired[{code, redeemed}]`, `expiredTotal`.

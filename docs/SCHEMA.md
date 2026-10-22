# `KS_DATA` schema

`docs/index.html` renders every view from one JSON object, `KS_DATA`, found between
`/* KS_DATA:BEGIN */` and `/* KS_DATA:END */`. Replace only that block to update the dashboard.

`scripts/build_data.py` generates this block from the five account `.md` files and
`data/manual.json` (see [Where each field comes from](#where-each-field-comes-from)) and writes it
into a copy of the page, `build/index.html`. The block inside `docs/index.html` itself stays
hand-written, so the file still works when opened directly.

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
`name`, `kingdom`, `alliance`, `vip`, `power`, `powerRounded`, `kills`, `stamina{current,max}`, `serverDay`, `asOf`.
`powerRounded: true` means the game showed a rounded figure (e.g. 11.4M); the Overview tile then shows it
rounded too instead of a precise-looking 11,400,000.

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
| `rarity`, `cls`, `role` | string \| null | Filter options are built from the values present |
| `generation` | number \| null | Shown as "Gen N"; also a filter |
| `level`, `stars`, `tier` | number \| null | |
| `shards` | `{have, need, to}` \| null | `to` = next step label (`"4★"`, `"T4"`); `null` shows "next step" |
| `power`, `gearPower` | number \| null | |
| `gear` | `{slots, slotsComplete?, note}` \| null | `slots` = `null` (not recorded) or `[{slot, state, quality?}]`; `state` is `"empty"`, `"plus0"` or free text such as `"+17"`. Empty and +0 slots are highlighted. `slotsComplete: true` means `slots` lists every slot (the drawer then says "All slots recorded."); absent or `false` means only some slots are listed ("Other slots: Not recorded.") |
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
| `steps` | Optional. Strings, one in-game action each; shown as a numbered list on Invest |
| `changes` | Optional. `[{where, before: string[], after: string[], note?}]`: the end state of each line-up, gear set or slot group the move touches. Overview Top 5 shows `where: after` with new entries in bold; Invest shows before (leaving entries struck out) and after (joining entries highlighted). An empty `before` shows "Empty". The generator warns on a malformed entry or a hero name not in `hero.md` |

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

## Where each field comes from

`scripts/build_data.py` builds `KS_DATA` from five Markdown files plus one hand-edited JSON file.
Rows are found by their **exact bold label**: renaming a label in a `.md` file turns that field
into `null` and prints a warning.

### Dates (`as_of` front matter)

Each `.md` file starts with the date its values were read in the game:

```
---
as_of: 2026-10-21
---
```

That date becomes the `asOf` of every section built from the file. A missing or malformed date gives
`null` (the page flags the section as undated) and a warning.

The per-value upload dates (the **Updated** table column and `_(YYYY-MM-DD)_` after other values) are
removed before parsing and not used, so they can never be read as a value.

### Field sources

| `KS_DATA` | Source | Rule |
|---|---|---|
| `meta.schemaVersion` | script | Constant `1` |
| `meta.snapshotAsOf` | front matter | Newest `as_of` of the five files |
| `meta.staleAfterDays`, `meta.previousSnapshot`, `meta.lockedHeroesNotInData` | `data/manual.json` | |
| `governor` | profile.md, "Governor Identity" table | Governor Name (optional row, not stored today, so `name` is `null` and the header shows "Governor: Not recorded"), Kingdom / Server, Alliance, VIP Level, Overall Account Power, Total Combat Kills, Stamina (`a / b`). `serverDay` is not recorded: `null` |
| `townCenter` | profile.md, "Town Center (TC)" section | Current Level, Citizens / Workforce Capacity, the Attack / Defense / Health table; perks from the heading `(6 / 7 Unlocked)`, checked against the perk table. `perks.namesVerified` comes from `data/manual.json` |
| `resources` | profile.md | Stored Food (Bread), Free Gems. A K/M/B suffix (`94.6M`) means `rounded: true`. Wood, stone, iron: `null` |
| `governorGear` | profile.md, "Governor Gear" | `6 / 6 Locked` = 6 locked of 6 slots |
| `army` | troops.md | `Tier VII (Brave)` → `"T7 Brave"`; inventory table (Infantry → `inf`, Cavalry → `cav`, Marksmen → `arc` "Archers"); the "Total Military Force" row gives total and injured; the caps table gives march capacity, queues and infirmary |
| `rules` | `data/manual.json` | Community rules (Unverified) |
| `heroes[]` | hero.md | See below |
| `drillCamp` | `data/manual.json` | |
| `lineups.marches` | troops.md, "Formation N: Purpose (`Tag`)" sections | Heroes (`Lead` marks the lead), deployed counts, ratios, power. lineups.md's preset table is only a cross-check |
| `lineups.arena` | lineups.md | "… Squad Power"; `Frontline` rows → `front`, `Backline` rows → `back` |
| `lineups.barricades` | lineups.md, "Barricade N" sections | `Level 10 (MAX)` → level 10, `maxed: true`; Combined Hero Power (`1.4M` → rounded) |
| `lineups.guardStation` | not recorded | `null` |
| `lineups.asOf` | front matter | Older of troops.md and lineups.md |
| `recommendations`, `features`, `dataHealth` | `data/manual.json` | |
| `codes` | codes.md | `[x]` = redeemed, `[ ]` = not; every row of both tables; `expiredTotal` = number of expired rows |

### Hero rules (hero.md)

- **List and order:** the "Active Hero Roster" table. Details come from each
  "In-Depth Hero Profile: Name" section; where both give a value (rarity, level, stars), the profile wins
  and a warning is printed.
- **name:** a bracketed alias is dropped (`Jabel (Jable)` → `Jabel`).
- **rarity:** `SSR / Mythic` → `Mythic`, `Rare (Blue)` → `Rare`. **generation:** `(Generation N)` in the
  profile's Rarity line. **role:** the bold label in the roster's role column (`**Core Carry:** …` → `Core Carry`).
- **shards:** `(Shards: have / need to X)`. `to` comes from X (`4-Star promotion` → `4★`,
  `Tier 5 promotion` → `T5`); when X is only "next promotion", from the preview heading
  (`… ➔ Tier 4` → `T4`); otherwise `null`.
- **gear.slots:** every row of the gear table (or the gear bullets): Helmet, Gauntlets → Gloves,
  Armor → Chest, Boots. `Base (+0)` → `plus0`, `None Equipped` → `empty`, otherwise the level (`+17`);
  `quality` from the rarity column; `slotsComplete: true`.
- **widget:** the "Exclusive Widget" line. `Unlocked (…)` gives `name: null` (the brackets describe the
  icon); no line gives `widget: null`.
- **skills:** one entry per row of every skill table. `Capped at …` → `capped` (`needs` from
  "Requires N-Star"); `In Progress (a/b …)` → `progress` with note `a/b …`, or `upgradeable` with
  `confidence: "Inferred"` when a ≥ b; `Locked` → `locked` (`needs` from "Unlocks at N-Star").
  Effect text is not copied.
- **gear.note, notes:** from `data/manual.json` → `heroes.<Name>.gearNote` / `notes`.

### `data/manual.json`

- Top-level keys use the `KS_DATA` names; `heroes` is keyed by hero name. Keys starting with `_` are ignored.
- It can only fill fields the `.md` files leave empty. Setting a field the `.md` files already
  provide stops the build, so every value has one home.

### Warnings and errors

- **Warning** (the build continues, the value is `null`): missing label, missing date, unknown
  skill status, roster/profile disagreement. Shown as annotations on the GitHub Actions run.
- **Error** (nothing is written): a missing `.md` file, no hero roster table, invalid `data/manual.json`,
  a manual/parsed collision, not exactly one `KS_DATA` block in the template, or the Player ID appearing
  anywhere in the output. The Player ID check runs only if profile.md has a "Player ID" row; the
  repository no longer stores the ID, so today there is nothing it could leak.

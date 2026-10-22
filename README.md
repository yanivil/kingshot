# Kingshot

A comprehensive guide and reference documentation for the mobile strategy survival game **Kingshot**, developed and published by [Century Games](https://www.centurygames.com/games/kingshot/).

## Overview

**Kingshot** is a free-to-play mobile strategy game that blends idle settlement survival with large-scale 4X multiplayer conquest. Set in a war-torn medieval realm, players step into the role of a Governor tasked with restoring a ruined province, rescuing refugees, assigning workers, and fending off rebel factions and dangerous beasts.

Mechanically, the game shares its progression framework and engine with Century Games' *Whiteout Survival*, retheming the survival-colony formula from a frozen wasteland into a medieval kingdom.

## Core Gameplay Mechanics

### 1. Settlement Survival and Colony Management
* **Refugee Rescue & Workforce:** Expand your settlement's population by rescuing refugees and assigning them to key production buildings (farms, sawmills, mines, and medical clinics).
* **Citizen Needs & Morale:** Balance shelter quality, food supplies, and clinic capacity to prevent disease outbreaks, declining morale, or population loss.
* **Keep Progression:** Upgrade the central Keep to unlock higher building tiers, advanced research, and larger troop capacities.

### 2. Hero Collection and Combat
* **Hero Roster:** Recruit and ascend heroes categorized into specialized roles (Combat, Gathering, and Garrison), each featuring unique skills and gear slots.
* **Unit Classes:** Train, promote, and customize armies across three core unit types (Infantry, Marksmen, and Cavalry) with rock-paper-scissors tactical advantages.
* **Tactical Minigames:** Progress through expedition levels and tower-defense combat stages to earn ascension materials, speedups, and rare equipment.

### 3. 4X World Map and Multiplayer Warfare
* **Wilderness Exploitation:** Scout the regional map for rebel encampments, beast dens, and high-yield resource tiles.
* **Alliances:** Join an alliance to construct shared territory banners, unlock alliance research perks, trade resources, and coordinate mutual defense.
* **Rallies & PvP:** Organize multi-player rally attacks against fortified enemy compounds, territorial shrines, and central kingdom wonders.
* **Kingdom vs. Kingdom (KvK):** Compete in state-level battle events and cross-server wars for dominance and governing privileges.

## Platform Availability

| Platform | Official Source |
| :--- | :--- |
| **Android** | [Kingshot on Google Play](https://play.google.com/store/apps/details?id=com.run.tower.defense&hl=en) |
| **iOS** | [Kingshot on the App Store](https://apps.apple.com/us/app/kingshot/id6739554056) |
| **Official Portal** | [Century Games Kingshot Page](https://www.centurygames.com/games/kingshot/) |
| **Official Web Store** | [Kingshot Web Top-Up Store](https://store.centurygames.com/kingshot) |

## Repository Scope

This repository provides:
* **`profile.md`**: Governor account identity, Kingdom #2508, Town Center Lv. 20 stats & perks.
* **`hero.md`**: Complete roster profiles, star ascensions, gear pieces, skill levels, and promotion milestones,
  plus heroes seen but not yet recruited (not shown on the dashboard).
* **`lineups.md`**: Arena 5v5 Offense & Defense squads, Barricades 1 & 2 (City Wall Guard), and saved March Presets (`Be` and `Att`).
* **`troops.md`**: Tier VII standing troop inventory, march capacities, and infirmary hospital caps.
* **`codes.md`**: Active promotional gift codes and expired codes archive.
* **`docs/index.html`**: The account dashboard (see below).
* **`docs/SCHEMA.md`**: Reference for the dashboard's data object and where each field comes from.
* **`data/manual.json`**: Hand-edited dashboard content that is not in the `.md` files (recommendations,
  data-health notes, community game rules, features, Drill Camp, a few hero notes).
* **`scripts/build_data.py`**: Generator that builds the dashboard data from the `.md` files
  (tests: `scripts/test_build_data.py`).
* **`.github/workflows/build-dashboard.yml`**: Builds and publishes the dashboard to GitHub Pages.
* **`design/dashboard-prototype.dc.html`**: The approved design prototype (design-canvas format; not runnable on its own).
* **`CHANGELOG.md`**: History of changes.

### Update dates

Every value in `profile.md`, `hero.md`, `lineups.md`, `troops.md` and `codes.md` carries the date it was
last uploaded: tables have an **Updated** column, and other values end with _(YYYY-MM-DD)_.
When you change a value, set its date to the day of the upload. Unchanged rows keep their old date.

These upload dates are separate from the `as_of:` line at the top of each file (the day the values were
read in the game). The dashboard generator uses only `as_of:` and ignores the upload dates.

## Account Dashboard

A phone-first dashboard that answers three questions: where the account stands, where it is weak,
and where the next resources should go. It has ten views (Overview, Heroes, Drill Camp,
Army & marches, Defense & Arena, City, Invest, Features, Data health, Codes) plus a hero detail drawer.

### Architecture

* **One self-contained file**, `docs/index.html`: styles, data and logic together; no framework.
  The only external request is the Google Fonts stylesheet (system fonts are the fallback).
* **Data is separate from layout.** Everything shown comes from one JSON object, `KS_DATA`, between
  `/* KS_DATA:BEGIN */` and `/* KS_DATA:END */`. Missing values are `null` and render as "Not recorded".
* **The data is generated.** `scripts/build_data.py` (Python 3, standard library only) parses
  `profile.md`, `hero.md`, `troops.md`, `lineups.md` and `codes.md`, adds `data/manual.json`, and writes
  `build/index.html`: a copy of `docs/index.html` with a generated `KS_DATA`. The repo copy keeps its
  hand-written block, so it still opens on its own. Field-by-field sources and parsing rules:
  [`docs/SCHEMA.md`](docs/SCHEMA.md#where-each-field-comes-from).
* **Published by GitHub Actions.** On every push to `main` that touches a root `.md` file,
  `data/manual.json`, `docs/`, `scripts/` or the workflow, `.github/workflows/build-dashboard.yml`
  runs the tests and the generator and deploys `build/` to GitHub Pages. It never commits to `main`.
* **Derived values are computed in the page**, not stored: hero level caps (from the Town Center rule
  table), assignments, lineup power checks, march conflicts, the Drill Camp placement plan, feature
  states and the data-health checks.
* Game rules come from community sources and are labelled **Unverified** wherever they are used.
* The Player ID is never displayed.

### Updating the data

1. **Game data:** edit the `.md` file and set its `as_of:` line (front matter at the top) to the date you
   read the values in the game. Keep the bold labels as they are: they are how the generator finds each value.
2. **Judgments and rules** (recommendations, data-health notes, rules, features, Drill Camp, hero notes):
   edit `data/manual.json`. It can only add what the `.md` files don't provide. A recommendation that
   moves a hero or a gear piece should say what replaces it: list the actions in `steps` and the end
   state in `changes` (`where`, `before`, `after`, or `rows` with `Front` / `Back` groups for the Arena).
   The dashboard shows the final line-up in the Top 5 and a Now / Suggested comparison on the Invest page.
3. Merge to `main`. The workflow rebuilds and republishes the dashboard; warnings (e.g. a renamed label)
   appear as annotations on the Actions run.

To check locally before pushing:

```
python3 -m unittest discover -s scripts -p "test_*.py"
python3 scripts/build_data.py --out build --json build/ks_data.json
```

then open `build/index.html`. `build/` is git-ignored.

### Viewing it

The published dashboard is at **https://yanivil.github.io/kingshot/** once GitHub Pages is set to
**Settings → Pages → Build and deployment → Source: GitHub Actions** (a one-time setting).
To re-publish without a code change, run the workflow from **Actions → Build and deploy dashboard → Run workflow**
on `main`.
The page carries `noindex`, but a GitHub Pages site is public to anyone with the link.

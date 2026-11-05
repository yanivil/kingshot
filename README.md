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
* **`profile.md`**: Governor account identity, Kingdom #2508, Town Center (Lv. 22 since 27 Oct) stats & perks, Governor Gear.
* **`hero.md`**: Complete roster profiles, star ascensions, gear pieces, skill levels, and promotion milestones
  (skill book counts are the shared stock of that book type on the date shown, not per-skill progress),
  plus heroes seen but not yet recruited (not shown on the dashboard).
* **`lineups.md`**: Arena 5v5 Offense & Defense squads, Barricades 1 & 2 (Wall Guard, against Rebel Invasions), and saved March Presets (`Be`, `Att` and `Gat`).
* **`troops.md`**: standing troop inventory (Tier VIII Elite since 5 Nov), march capacities, infirmary hospital caps, the
  `Be` / `Att` / `Gat` presets, and the highest beast and Terror (rally-only) levels the account can take.
* **`codes.md`**: gift codes in two lists: Active (still to redeem) and Expired (redeemed, marked ✓, or old). Restarted on 2026-11-05
  with only the account owner's current codes; older tracker codes are in `data/gift_codes_baseline.txt`.
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
When a screenshot shows a value, set its date to the day of the upload, whether the value changed or was
only re-confirmed (the date means "last seen in game", not "last changed"). A derived line, such as a gear
total, takes the new date only when every value it is built from was re-confirmed. Values not shown in the
upload keep their old date.

The dashboard dates come from these upload dates: each hero shows the newest date in its roster row and
profile; troop counts, each march preset, each Arena squad and each barricade show the newest date in their
own section (and each army tile its own row's date), because they are read from different screens; every
other section shows the newest date in its file. So updating a value's date is enough
to move the dashboard date forward. The `as_of:` line at the top of each file is only the fallback for a
section with no dates. Features on the Features page take the date of the file named as their source, or of the section named in
their `section` field (so Barricades and Arena, both in `lineups.md`, each keep their own date).

## Account Dashboard

A phone-first dashboard that answers three questions: where the account stands, where it is weak,
and where the next resources should go. It has ten views (Overview, Heroes, Drill Camp,
Army & marches, Defense & Arena, City, Invest, Features, Data health, Codes) plus a hero detail drawer.
The Overview opens with account power and total kills.

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
  states and the data-health checks. Data health flags a section as stale when it is more than 3 days old
  (`staleAfterDays` in `data/manual.json`) or has no date; the Drill Camp page says its reading is older than
  the hero data only when it trails it by more than the same number of days.
* Game rules come from community sources and are labelled **Unverified** wherever they are used.
* The Player ID is never displayed.
* **Gift codes.** The Codes page shows two read-only lists from `codes.md`: To redeem (the Active list) and
  Expired. Every redeemed code goes to Expired with ✓ in its **Redeemed** column (the account owner's rule,
  2026-11-05), and the page shows the ✓ next to it. Redeemed is a fact about the account, so it is recorded in
  `codes.md` and nowhere else; the per-browser "redeemed" marks of earlier versions were removed on 2026-11-05, and
  the page deletes their old `localStorage` key (`ks-code-marks`) once.

### Updating the data

1. **Game data:** edit the `.md` file and set the changed value's **Updated** date (or its _(YYYY-MM-DD)_)
   to today. Keep the bold labels as they are: they are how the generator finds each value.
   Account power is kept in `profile.md` only; `troops.md` does not repeat it.
2. **Judgments and rules** (recommendations, data-health notes, rules, features, Drill Camp, hero notes):
   edit `data/manual.json`. It can only add what the `.md` files don't provide. A recommendation that
   moves a hero or a gear piece should say what replaces it: list the actions in `steps` and the end
   state in `changes` (`where`, `before`, `after`, or `rows` with `Front` / `Back` groups for the Arena, or
   `Heroes` / `Troops` rows for a march formation, with exact troop numbers).
   The dashboard shows the final line-up in the Top 5 and a Now / Suggested comparison on the Invest page.
   Keep cards short: a short title (`what`, the suggestion itself) and a one- or two-sentence `summary`; the full
   reasoning goes in `why`, `steps`, `evidence` and `note`, which the page folds under Details.
   Give each recommendation one move only. When the account can't do it yet (not enough shards or books, or a
   stock not read), set `"ready": false` and say what is missing in `waitingFor`: the move then stays out of
   "Top 5 moves now" (which lists only moves that can be done today) and shows as "Not yet" on Invest.
3. Merge to `main`. The workflow rebuilds and republishes the dashboard; warnings (e.g. a renamed label)
   appear as annotations on the Actions run.

To check locally before pushing:

```
python3 -m unittest discover -s scripts -p "test_*.py"
python3 scripts/build_data.py --out build --json build/ks_data.json
```

then open `build/index.html`. `build/` is git-ignored.

### New gift-code check

Every two days (11:23 UTC on odd days of the month; GitHub may start it a little late),
`.github/workflows/check-gift-codes.yml` runs `scripts/check_gift_codes.py` (standard library only):

1. It reads the codes already in `codes.md` (Active and Expired lists) and in `data/gift_codes_baseline.txt`:
   old codes that trackers still list but that were never recorded (142 found on the first run, 4 Nov 2026).
2. It downloads a few community tracker pages (listed in `SOURCES` in the script) and picks out
   code-shaped words from the places those pages put codes (`<code>`, bold text, table cells, copy buttons,
   JSON `"code"` keys).
3. It drops codes already in `codes.md`, in the baseline, or named in an earlier `gift-codes` issue.
4. If anything is left, it opens **one issue** labelled `gift-codes` that mentions the repo owner (so GitHub
   sends a notification), split into codes seen on two or more trackers and on one tracker only.

It never commits: the codes are unverified until tried in the game, so `codes.md` still changes only through
a PR. The run summary on the Actions page lists every tracker, whether it downloaded, and how many recorded
codes it showed (from `codes.md` or the baseline); a tracker showing 0 has probably changed its page and needs
its entry fixed. To stop the check reporting a code that is old or not a real code, add it to the baseline file. The run fails
only when every tracker fails to download. To run it by hand: **Actions → Check for new gift codes →
Run workflow** (tick "dry run" to see the report without opening an issue).

### Viewing it

The published dashboard is at **https://yanivil.github.io/kingshot/** once GitHub Pages is set to
**Settings → Pages → Build and deployment → Source: GitHub Actions** (a one-time setting).
To re-publish without a code change, run the workflow from **Actions → Build and deploy dashboard → Run workflow**
on `main`.
The page carries `noindex`, but a GitHub Pages site is public to anyone with the link.

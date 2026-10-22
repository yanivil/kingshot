# Changelog

All notable changes to this repository are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `docs/index.html`: static, self-contained account dashboard for GitHub Pages with ten views
  (Overview, Heroes, Drill Camp, Army & marches, Defense & Arena, City, Invest, Features,
  Data health, Codes) and a hero detail drawer. Phone-first, light/dark/auto theme, no build step.
- All dashboard content lives in one `KS_DATA` JSON block (hand-written for now, snapshot of 21 Oct 2026),
  so a future generator can replace it without touching layout or logic.
- `docs/SCHEMA.md`: field-by-field reference for `KS_DATA`.
- `design/dashboard-prototype.dc.html`: the approved design prototype the page was built from.
- `scripts/build_data.py`: generator that builds `KS_DATA` from `profile.md`, `hero.md`, `troops.md`,
  `lineups.md`, `codes.md` and `data/manual.json`, and writes `build/index.html`. Missing values become
  `null` with a warning; a manual/parsed collision, a missing template block or a Player ID leak stops the
  build. Standard library only. Tests in `scripts/test_build_data.py`.
- `data/manual.json`: hand-edited content that is a judgment or a community rule rather than game data
  (recommendations, data-health notes, rules, features, Drill Camp, meta settings, hero notes), seeded
  with the values previously hand-written in `docs/index.html`.
- `.github/workflows/build-dashboard.yml`: on push to `main` (root `.md` files, `data/manual.json`,
  `docs/**`, `scripts/**`, the workflow) or manual run, tests and runs the generator and deploys `build/`
  to GitHub Pages. Read-only on the repository; never commits.
- `as_of:` front matter in the five `.md` files (2026-10-21 for all, as a placeholder until the
  in-game read dates are confirmed).
- `.gitignore` for `build/` and Python bytecode.

### Changed
- `hero.md`: Chenko promoted to 3-Star Tier 4; Gordon's Culinary Chaos and Amane's Exorcism reach Lv. 3;
  Yeonwoo and Saul equip Windbreaker Leatherwear in the empty chest slot.
- `lineups.md`: Arena offensive squad power is now 2,383,515, and Chenko is listed at 3-Star (T4).
- `docs/index.html`: `KS_DATA` updated to match these changes (Chenko, Gordon, Yeonwoo, Amane, Saul,
  Arena attack power), including the recommendation and data-health text that quoted the old values.
- Jabel: Lv. 54 (cap until Town Center Lv. 21), power 564,200, troop capacity +11,525, boots enhanced
  to +20; stats updated in `hero.md`, her level in `lineups.md` and `troops.md`, and her `KS_DATA` entry.
- `profile.md`, `hero.md`, `lineups.md`, `troops.md`, `codes.md`: every value now shows when it was last
  uploaded (an **Updated** column in tables, _(YYYY-MM-DD)_ after other values). Initial dates come from
  git history; all current values were uploaded on 2026-10-21. README documents the convention.
- `codes.md`: Kingshot888, VIP777, KS1005, WELLDONE and Hangul2026 marked redeemed, matching the dashboard.
- Dashboard data now comes from the generator, so it shows more of what the `.md` files hold: every hero's
  generation and role, all four gear slots, one entry per skill, the next promotion step for 14 of 15
  heroes, and all 22 expired codes.
- `docs/index.html`: the hero drawer says "All slots recorded." instead of "Other slots: Not recorded."
  when `gear.slotsComplete` is true.
- `docs/SCHEMA.md`: `gear.slotsComplete`, `generation` as a number, and a "Where each field comes from"
  section with every parsing rule.
- `README.md`: architecture, data-update steps and the GitHub Pages setting for the generator.
- Account data from new in-game screens (Troops Preview, Governor Profile):
  - `troops.md`: Infantry 30,756, Cavalry 33,127, Archers 33,045 (total 96,928; shares recomputed),
    infirmary capacity 38,600, account power 11.4M. The old "Net Change" values are cleared (not shown).
  - `profile.md`: account power 11.4M (the screen shows only the rounded figure), stamina 161 / 200.
- `hero.md`: Jabel's shards are 17 / 40 (were 0 / 40), from her hero screens of 2026-10-22. Level, power,
  stats, gear, widget, skills and promotion preview were re-checked and are unchanged.
- `hero.md`: Quinn from his hero screens of 2026-10-22: Lv. 52, power 485,610, troop capacity 11,140,
  8 escorts, shards 91 / 100, new hero and escort stats, Archer Health +20.74%, chest piece +17, 22 / 50
  manuals, and a new star-promotion preview section. The chest piece's power and conquest stats (and so the
  gear power total, 117,610) are inferred from the same item on Diana. Roster level updated to Lv. 52.
- From Diana's hero screens and the Drill Camp screen of 2026-10-22:
  - `hero.md`: Diana's XP counter 2,020 / 130,000 and 22 / 50 manuals; everything else re-checked, unchanged.
  - `profile.md`: gems 21,450 (gem counter on the Drill Camp screen).
  - `data/manual.json`: Drill Camp instructors are now Jabel 54, Saul 50, Chenko 49 (identified by
    appearance), Diana 49 and Quinn 52; 7 open slots, none filled; slot 8 needs Town Center 21. The
    drill-fill recommendation, the Drill Camp feature date and the stale "Drill Camp" missing item are updated.
- `data/manual.json`: Quinn's note "No star-preview data." removed (the preview is now recorded).
- `governor.powerRounded` (generator, `docs/index.html`, `docs/SCHEMA.md`): a rounded account power is shown
  as "11.4M" on the Overview tile instead of a precise-looking 11,400,000.

### Removed
- The Player ID, from `README.md` (the `profile.md` description) and from `profile.md` (the "Player ID" row).
  It remains in the git history of earlier commits.
- The governor name, from `profile.md` (the "Governor Name" row, now optional for the generator),
  `troops.md`, `README.md`, the hand-written `KS_DATA` in `docs/index.html` and the design prototype.
  The dashboard header shows "Governor: Not recorded". The name remains in the git history.

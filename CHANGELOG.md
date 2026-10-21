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

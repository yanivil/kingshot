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
- `hero.md`: Jabel's power 567,410 and new stats from 2026-10-22 (Hero Defense 1,497, Hero Health 14,853,
  Escort Defense 498, Escort Health 4,951, Cavalry Health +24.69%). A gear piece was upgraded, but the
  gear screen wasn't shared, so her gear rows and gear power (131,460) are still the 2026-10-21 values.
- `hero.md`: Jabel's Crusader's Gauntlets +7 → +11 (30,750 power, Hero +109 DEF / +549 HP, Escort +36 DEF /
  +183 HP, +11.31% Cavalry Health); gear power 134,670. This accounts exactly for her 2026-10-22 stat changes.
- From Diana's hero screens and the Drill Camp screen of 2026-10-22:
  - `hero.md`: Diana's XP counter 2,020 / 130,000 and 22 / 50 manuals; everything else re-checked, unchanged.
  - `profile.md`: gems 21,450 (gem counter on the Drill Camp screen).
  - `data/manual.json`: Drill Camp instructors are now Jabel 54, Saul 50, Chenko 49 (identified by
    appearance), Diana 49 and Quinn 52; 7 open slots, none filled; slot 8 needs Town Center 21. The
    drill-fill recommendation, the Drill Camp feature date and the stale "Drill Camp" missing item are updated.
- `hero.md`: Quinn from his hero, skill and gear screens of 2026-10-22 (later the same day): power 486,220,
  shards 95 / 100, XP counter 51,686 / 160,000, Hero Attack 1,558, Hero Health 9,628, Escort Health 3,208,
  Archer Lethality +20.74%, 25 / 50 manuals. Windbreaker Boots +16 → +17 (24,010 power, ATK +97 / HP +301,
  escort ATK +32 / HP +100, +8.38% Archer Lethality). The chest piece values, inferred until now, are confirmed
  by its own screen; gear power is 118,220. The boots upgrade accounts exactly for the stat and power changes.
- Recommendations now say what to do, not only what is wrong. Each move names the replacement and shows the
  end state:
  - `data/manual.json`: the seven moves are rewritten and re-ranked (free swaps first):
    1. Quinn replaces Amane in Arena attack, Arena defense, Barricade 1 and Att.
    2. Gordon replaces Jabel in Be.
    3. Seth's Epic gloves and boots go to Howard.
    4. Drill Camp: who to slot and reset, and where the XP goes.
    5. Fahd's two +0 pieces go to +12.
    6. Quinn's 4★ is first in the promotion order.
    7. Save manuals for Fahd's Eagle Wings.
  - New optional `steps` and `changes` fields (`docs/SCHEMA.md`). `docs/index.html` shows the final
    line-up under each Top 5 move and a before → after block plus numbered steps on the Invest page.
  - `scripts/build_data.py` warns when a recommendation names an unknown hero or has a malformed
    `steps`/`changes` entry (new test).
- `data/manual.json`: the Drill Camp rule now says which parts are in-game text (auto-level to the lowest
  instructor, Level Resets refund all Hero XP; 22 Oct screens) and which part is still community (a hero
  removed from the camp returns to its own level).
- `profile.md`: gems 21,550 (Drill Camp screen, 2026-10-22).
- `data/manual.json`: Quinn's note "No star-preview data." removed (the preview is now recorded).
- `governor.powerRounded` (generator, `docs/index.html`, `docs/SCHEMA.md`): a rounded account power is shown
  as "11.4M" on the Overview tile instead of a precise-looking 11,400,000.

### Removed
- The Player ID, from `README.md` (the `profile.md` description) and from `profile.md` (the "Player ID" row).
  It remains in the git history of earlier commits.
- The governor name, from `profile.md` (the "Governor Name" row, now optional for the generator),
  `troops.md`, `README.md`, the hand-written `KS_DATA` in `docs/index.html` and the design prototype.
  The dashboard header shows "Governor: Not recorded". The name remains in the git history.

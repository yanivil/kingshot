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
- Arena changes in recommendations are shown by row, Front and Back, as a Now / Suggested table on Invest and
  as "Front … · Back …" in the Top 5 (`changes[].rows`, `docs/SCHEMA.md`). The other changes read Now / Suggested
  instead of Before / After.
- Move 1 now also replaces Fahd with Gordon in the Arena defense front: Fahd is the weakest hero there, and the
  −12% skill he was picked for is an Expedition (march) skill. Move 7 now saves manuals for Gordon's Emergency
  Snack instead of Fahd's Arena skill, and move 5 no longer counts Fahd as an Arena hero.
- `hero.md`: Jabel's shards 19 / 40 (were 17), from her screens of 2026-10-22. Power, stats, promotion
  preview, skills and gear were re-checked and are unchanged.
- Saul from his screens of 2026-10-22: Lv. 54 (was 50), power 284,550, troop capacity 11,525, Hero 1,058 ATK / 876 DEF /
  6,556 HP, Escort 352 / 292 / 2,185. Shards (1 / 15), bonuses, promotion preview, skills and gear unchanged. This confirms
  all 5 Drill Camp instructors at Lv 54 (Saul's level was the last one inferred).
- Amane from her screens of 2026-10-22: Lv. 54 in a Drill Camp slot (was 46), power 286,390, troop capacity 11,525,
  8 escorts, Hero 1,113 ATK / 1,044 DEF / 6,624 HP, Escort 370 / 348 / 2,208, 25 / 30 manuals (the old 34 / 30 reading
  is replaced). Shards (0 / 40), bonuses, promotion preview, skill levels and gear (chest still empty) unchanged.
- Fahd from his screens of 2026-10-22: Lv. 54 in a Drill Camp slot (was 48), power 308,000, troop capacity 11,525,
  8 escorts, Hero 933 ATK / 1,104 DEF / 9,210 HP, Escort 310 / 368 / 3,070, 25 / 30 manuals (the old 34 / 30 reading is
  replaced). Shards, bonuses, promotion preview, skill levels and gear unchanged.
- Yeonwoo from her screens of 2026-10-22: Lv. 54 in a Drill Camp slot, power 323,360, troop capacity 11,525, 8 escorts,
  shards 8 / 40, Hero 1,132 ATK / 1,122 DEF / 6,974 HP, Escort 376 / 374 / 2,324. Bonuses, promotion preview, skills
  (capped until 3★) and gear unchanged.
- Edwin from his screens of 2026-10-22: Lv. 54, promoted to 3-Star Tier 3 (3 / 40 to T4), power 342,371, troop capacity
  11,525, 8 escorts, Hero 958 ATK / 1,386 DEF / 9,540 HP, Escort 318 / 462 / 3,180, Cavalry Attack/Defense +51.41%,
  40 / 50 Rare Expedition Books, new promotion preview. Gear unchanged. Edwin leaves the promotion move.
- Forrest from his screens of 2026-10-22: Lv. 54 in a Drill Camp slot, promoted to 3-Star Tier 4 (3 / 40 to T5), power
  371,073, troop capacity 11,525, 8 escorts, Hero 764 ATK / 1,458 DEF / 14,994 HP, Escort 254 / 485 / 4,998, Infantry
  Attack/Defense +54.31%, new promotion preview. Gear and skills unchanged. Level and tier updated in the roster,
  `lineups.md` and `troops.md`; Forrest leaves the promotion move.
- Olive from her screens of 2026-10-22: Lv. 54, power 372,601, troop capacity 11,525, 8 escorts, shards 16 / 40, Hero
  1,256 ATK / 1,446 DEF / 7,590 HP, Escort 418 / 482 / 2,529. Her Archer Health is +14.10% (gloves 8.10% + chest 6.00%),
  which settles the 8.10% / 14.10% conflict; the Data health note is removed. Promotion preview, skills and gear unchanged.
- Seth from his screens of 2026-10-22: Lv. 54 (levelled, not in the Drill Camp), power 408,649, troop capacity 11,525,
  8 escorts, shards 29 / 40, Hero 800 ATK / 1,482 DEF / 15,690 HP, Escort 266 / 494 / 5,229. Bonuses, promotion
  preview, gear (+15 / +15 / +15 / +16, still his Epic set) and skills (Lv 4, capped until 4★) unchanged.
- Gordon from his screens of 2026-10-22: Lv. 54 in a Drill Camp slot, power 435,470, troop capacity 11,525, 8 escorts,
  shards 10 / 40, Hero 1,198 ATK / 1,462 DEF / 12,000 HP, Escort 398 / 487 / 4,000, 25 / 50 manuals (the odd 6 / 50 on
  Culinary Chaos is replaced). Bonuses, promotion preview, skill levels and gear unchanged. Level updated in the
  roster, `lineups.md` and `troops.md`.
- Chenko from her screens of 2026-10-22 (the name on screen confirms the instructor identified by appearance): Lv. 54,
  power 440,920, troop capacity 11,525, 8 escorts, shards 10 / 40, Hero 1,202 ATK / 1,465 DEF / 12,030 HP, Escort
  400 / 488 / 4,010, 25 / 50 manuals. Bonuses, promotion preview and gear unchanged. Level updated in the roster and
  `lineups.md`; Saul is now the only instructor whose Lv 54 is inferred.
- `data/manual.json`: Drill Camp slots from the 22 Oct screen: Amane, Helga, Howard, Gordon, Yeonwoo, Fahd and Forrest
  (7 / 7 filled). The Drill Camp move is done and removed; 3 moves remain.
- `scripts/build_data.py`: a value written as "Not recorded (…)" or "Not shown (…)" is read as missing, so a number
  in the explanation (a date, a "+19") can't become the value (new test).
- Howard from his screens of 2026-10-22: Lv. 54 in a Drill Camp slot, promoted to 3-Star Tier 4 (9 / 40 to T5), power
  477,020, troop capacity 11,525, 8 escorts, new hero/escort stats, Infantry Attack/Defense +84.49%, Infantry Health
  +21.79%, new promotion preview. Chest piece +17 → +19 (12.99% Infantry Health from the stats total; power not shown,
  so gear power is not recorded). Level and tier updated in the roster, `lineups.md` and `troops.md`.
- `data/manual.json`: Drill Camp now records Howard as slotted and runs at Lv 54 (Chenko and Saul 54 inferred); the
  Drill Camp move becomes "fill the remaining slots"; Howard leaves the promotion list; Seth's gear move notes
  Howard's chest is +19.
- Diana from her screens of 2026-10-22: Lv. 54 (cap until Town Center 21), power 482,570, troop capacity 11,525,
  8 escorts, Hero 1,569 ATK / 1,534 DEF / 9,579 HP, Escort 522 / 510 / 3,192, 25 / 50 manuals. Shards (54 / 100),
  expedition bonuses, promotion preview and gear re-checked, unchanged. Her level is updated in the roster,
  `lineups.md`, `troops.md` and the Drill Camp instructors; the Drill Camp move now names Chenko (the only Lv 49
  instructor) as the one to level.
- Dashboard dates now follow the per-value upload dates (`scripts/build_data.py`, new test): each hero shows the
  newest date in its roster row and profile, other sections the newest date in their file. The front-matter
  `as_of` is only a fallback, so sections updated on 2026-10-22 no longer show 21 Oct. `README.md`,
  `docs/SCHEMA.md` and the Data health note about placeholder dates are updated.
- Quinn from his screens of 2026-10-22 (later): Lv. 54 (cap until Town Center 21), power 490,460, troop capacity
  11,525, shards 97 / 100, Hero 1,569 ATK / 1,566 DEF / 9,700 HP, Escort 522 / 521 / 3,232. Skills (25 / 50 manuals),
  gear and promotion preview unchanged. His level is updated in `hero.md`, `lineups.md`, `troops.md` and the Drill
  Camp instructors; the promotion move now says 3 shards.
- Line-ups as saved in game on 2026-10-22:
  - `lineups.md`: Arena attack back row has Quinn instead of Amane. Its power is not recorded yet.
  - Arena defense: front row Howard and Gordon, back row Jabel, Diana and Quinn; power 2,417,730.
  - Barricade 1: Howard, Jabel, Quinn (1.5M). Barricade 2: Gordon, Chenko, Diana (1.3M).
  - `Be`: Diana, Gordon, Forrest (9,195,741). `Att`: Howard, Jabel, Quinn (10,767,581).
  - `troops.md`: the two marches' troops and power. Tier VII counts are now 31,858 / 33,477 / 33,395 (98,730),
    plus 150 Veteran Cavalry and 150 Veteran Archers noted. March capacity is 77,785 (`Att`) or 75,960 (`Be`).
  - `profile.md` and `troops.md`: account power 11,537,653 (exact). `profile.md`: bread 104.5M.
  - `hero.md`: the roster's assignments for Jabel, Quinn, Gordon, Fahd and Amane.
  - `data/manual.json`: the applied moves (Quinn for Amane, Gordon for Fahd, Gordon for Jabel in `Be`) and
    Fahd's gear move (he is in no line-up now) are removed; 4 moves remain.
- `docs/index.html`: a rounded line-up power ("1.3M") is flagged on Data health only when it is off by more
  than its rounding (50,000), not by more than 1%.
- `data/manual.json`: the Drill Camp rule now says which parts are in-game text (auto-level to the lowest
  instructor, Level Resets refund all Hero XP; 22 Oct screens) and which part is still community (a hero
  removed from the camp returns to its own level).
- `profile.md`: gems 21,550 (Drill Camp screen, 2026-10-22).
- `hero.md`: new "Heroes Not Yet Recruited" table with Amadeus (SSR / Mythic infantry, 0 / 20 shards, 20,550
  shown power). The generator ignores it, so the dashboard still lists 15 heroes. Quinn's 5-shard need to 4★
  is confirmed in game; the promotion move no longer asks about the "Redeem 2" button.
- `data/manual.json`: Quinn's note "No star-preview data." removed (the preview is now recorded).
- `governor.powerRounded` (generator, `docs/index.html`, `docs/SCHEMA.md`): a rounded account power is shown
  as "11.4M" on the Overview tile instead of a precise-looking 11,400,000.

### Removed
- The Player ID, from `README.md` (the `profile.md` description) and from `profile.md` (the "Player ID" row).
  It remains in the git history of earlier commits.
- The governor name, from `profile.md` (the "Governor Name" row, now optional for the generator),
  `troops.md`, `README.md`, the hand-written `KS_DATA` in `docs/index.html` and the design prototype.
  The dashboard header shows "Governor: Not recorded". The name remains in the git history.

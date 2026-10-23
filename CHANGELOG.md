# Changelog

All notable changes to this repository are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Overview (`docs/index.html`): a "Total kills" tile next to Account power (kills were only on the City view).
  Documented in `docs/SCHEMA.md` and `README.md`.
- Codes page (`docs/index.html`): each code is now a toggle to mark it redeemed or not. Marks are saved in the
  browser (`localStorage` key `ks-code-marks`), shown with a "This device" tag, listed as "not in codes.md yet",
  and dropped once `codes.md` agrees; "Clear marks on this device" removes them. The lede counts active codes
  still to redeem. Works with storage blocked (marks then last for the visit). Documented in README and SCHEMA.
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
- Dates (`scripts/build_data.py`, `docs/index.html`): troop counts and march presets now have separate dates. The army
  is dated by the troop inventory and caps sections only, and each army tile by its own row (`army.fieldAsOf`), so
  march capacity read from a preset screen keeps its day. Each march preset, Arena squad and barricade carries its
  own `asOf`; the March presets and Barricades panels show their newest part and mark an older card with its own
  date, and each Arena panel shows its squad's date. `lineups.asOf` (Data age) is now the oldest part's date instead
  of the older of the two files' dates. Tests added; documented in `docs/SCHEMA.md` and `README.md`.
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
- `hero.md`: Helga's widget is **Bands of Tyre, locked** (was recorded as unlocked from the emblem icon); Saul's
  Rabbitgear Cannon, locked, is now recorded. `scripts/build_data.py` keeps a locked widget's name ("Locked — Name";
  new test; `docs/SCHEMA.md`).
- Helga from her screens of 2026-10-22: Lv. 54 in a Drill Camp slot (was 46), power 259,615, troop capacity 11,525,
  8 escorts, Hero 599 ATK / 743 DEF / 11,875 HP, Escort 198 / 247 / 3,958. Shards (0 / 5), bonuses, promotion preview,
  skills and gear unchanged. All 15 heroes now carry 2026-10-22 readings.
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
- `hero.md`: Howard's Praetorian's Shroud (+19) read from its gear screen: 37,890 power, DEF +124 / HP +931,
  escort DEF +41 / HP +310. His gear power is now 127,900 (was "Not recorded"), and the hero / escort stat sums
  from gear are filled in. Seven other gear screens from the same upload match the recorded values (2026-10-22).
- Date rule (README "Update dates", `docs/SCHEMA.md`): an upload date now means "last seen in game". A value
  re-confirmed by a screenshot takes the upload date even when it didn't change; a derived total moves only
  when all its parts were re-confirmed.
- `hero.md`: re-confirmed gear restamped to 2026-10-22: all four of Seth's pieces and his gear totals;
  Helga's helm, gloves, shroud and Infantry Health total; Saul's Berserker's Bracers; Olive's Berserker's
  Faceplate; Jabel's Brigader's Armet, Breastplate and Battle Boots. No values changed. Diana's, Quinn's and
  Howard's re-confirmed pieces already carried 2026-10-22.
- `hero.md`: Saul's Windbreaker Faceplate (+16), Windbreaker Boots (+16) and Archer Lethality total re-confirmed
  and restamped to 2026-10-22. The same upload re-confirmed Chenko's, Gordon's, Edwin's and Quinn's pieces,
  which already carried that date. No values changed.
- `hero.md`: re-confirmed and restamped to 2026-10-22: Forrest's Stonewall Gloves (+12), Shroud (+14), Greaves (+12)
  and Infantry Health total; Olive's and Yeonwoo's Windbreaker Bracers (+15). Gordon's Breastplate (+14) and
  Chenko's Breastplate and Battle Boots (+15) were re-confirmed too and already carried that date. No values changed.
- `data/manual.json`: recommendations re-checked against the 22 Oct gear uploads. The Seth → Howard gear move now
  sends Howard's freed Stonewall Gloves (+20) and Greaves (+19) to Forrest (Be march) instead of Seth, and Seth takes
  Forrest's +12 pieces. Howard's chest numbers (37,890; DEF +124 / HP +931) are in the evidence, each hero's gear
  power and troop bonuses before and after are shown, and the note says which parts are Verified, Inferred and
  Unverified. Quinn's promotion and Gordon's skill moves are unchanged (no new shard or manual data).
- `data/manual.json`: removed the "Hero XP readings differ" data-health conflict. All six readings it quoted were
  replaced by the 22 Oct Lv 54 hero updates, and no data file holds a Hero XP reading any more.
- `codes.md`: `lwaL5ZKx5`, `KSGW26JP` and `KSPRAWNING` added to the expired archive (could not be redeemed when
  tried on 2026-10-22; rewards not recorded). Kingshot888, VIP777, KS1017, VIP1017, CHALLENGE26 and IG200KS were
  re-checked the same day and restamped to 2026-10-22.
- `lineups.md`: Arena defense power is now 2,452,930 (Defensive Squad Lineup screen, 2026-10-22), exactly the sum of
  Howard's, Gordon's, Jabel's, Diana's and Quinn's recorded powers, which clears that Data-health conflict. Fresh
  Barricade screens with all six heroes at Lv 54 re-confirm 1.5M and 1.3M; Jabel's Arena-defense and Barricade 1 rows
  restamped.
- `profile.md` and `troops.md` (2026-10-22): account power 11,643,259, kills 338,672, stamina 199 / 200, bread 105.1M, gems 21,570;
  kingdom, alliance, VIP, governor gear, Town Center level and citizens re-confirmed. The governor name and Player ID
  on the profile screen are not recorded.
- Lineup power check (`docs/index.html`, `docs/SCHEMA.md`): a short figure such as "1.3M" is now treated as cut to one
  decimal (1,300,000 up to 1,399,999), not rounded. Barricade 2 showed 1.3M for heroes adding up to 1,358,960, which
  rounding would show as 1.4M. This clears the Barricade 2 conflict.
- `profile.md`: Town Center perks now use the in-game names and descriptions from the 22 Oct perk screens (Rapid Fire,
  Strength, Slash, Governor Health / Attack / Defense Enhancement; slot 7 locked, name not shown). The old names were
  interpretations and are gone. Town Center stats (584 / 1,168 / 17,523) re-confirmed. `data/manual.json`:
  `perks.namesVerified` is now true and the "Perk names look interpreted" conflict is removed, so Data health
  lists no conflicts.
- Data health (`docs/index.html`): the Conflicts panel says "No conflicts found." when the list is empty.
- `troops.md` (Troops Preview, "All" tab, 2026-10-22): Brave Infantry 30,988, Cavalry 33,903, Archer 33,518, total
  98,409 (−321 against the earlier Deploy-screen counts); 6 injured of 38,600; March Queue shown as 2 / 4. The 150
  Veteran Cavalry and 150 Veteran Archers (Tier IV) are no longer listed. The header's "1,278/98,409" is recorded
  as shown; the screen does not say what 1,278 counts.
- `profile.md`: new "Research Building (Institute)" section: Lv 20, +2.0% research speed, 94,996 building power
  (Lv 21: +2.1%, 107,624). Research levels are still not recorded. `data/manual.json`: the Research feature is
  Active with that note, and the Data-health gap is renamed "Research levels".
- Generator (`scripts/build_data.py`, `date_features`): a feature whose `source` is one of the five .md files now takes
  that file's newest upload date, so the Features page no longer shows 21 Oct for sections updated on 22 Oct. Test
  added; README and SCHEMA updated.
- `hero.md`: ten more gear screens (2026-10-22) re-confirmed recorded values; restamped to 2026-10-22: Saul's
  Leatherwear (+10), Archer Health total and gear attribute totals; Helga's Stonewall Greaves (+2), Infantry Lethality
  total and gear attribute totals; Yeonwoo's Leatherwear and Archer Health total; Olive's Leatherwear and Boots and all
  her gear totals. Fahd's, Amane's and Edwin's re-confirmed pieces already carried that date. No values changed.
- `hero.md`, Chenko (2026-10-22): Brigader's Breastplate enhanced +15 → +16 (23,400; DEF +79 / HP +396; escort DEF +26 /
  HP +132; +8.24% Cavalry Health). Hero power 441,520 (+600), gear power 92,400, Hero Defense 1,466, Hero Health
  12,036, Escort Health 4,012, Cavalry Health +16.48%; gear totals updated. Skill screens: exploration skills 27/50 Epic
  Expedition Manuals, expedition skills 28/50 Epic Conquest Books (expedition rows restamped from 21 Oct).
- `data/manual.json`: Gordon's Emergency Snack move now needs 3 more manuals (27 of 30), using Chenko's later reading of
  the shared stock (Inferred).
- `hero.md`, Quinn (2026-10-22): promoted to **4-Star (Tier 0)**, 1 / 100 shards; Berserker's Faceplate +16 → +17 (36,015;
  ATK +146 / HP +452; escort ATK +48 / HP +150; +12.57% Archer Lethality). Hero power 528,735 (= 490,460 + 37,360
  promotion + 915 Faceplate), gear power 119,135; new Hero Stats and the 4★ Tier 0 → Tier 1 preview; skill rows show
  28/50 Epic Expedition Manuals and 31/50 Epic Conquest Books. Roster row and the three `lineups.md` rows now say 4-Star.
- `data/manual.json`: the promotion move now lists the next promotions (Helga 5, Seth 11, Saul 14, Jabel 21) and drops
  to priority 3; Gordon's Emergency Snack move needs 2 more manuals (28 of 30) and moves to priority 2.
- `hero.md`, Gordon (2026-10-22): Emergency Snack is Lv. 3 (all five skills at Lv. 3), +2,520 power; BBQ Feast shows 5/50
  Epic Expedition Manuals. Brigader's Battle Boots +12 → +13 (21,630; ATK +75 / HP +378; escort ATK +25 / HP +126; +7.82%
  Cavalry Lethality; 20 / 75 toward +14, no enhancement materials left), +570 power. Hero power 438,560, gear power 89,440,
  Hero Stats 1,199 / 1,462 / 12,006, escort 399 / 487 / 4,002, Cavalry Lethality +15.92%; gear totals updated.
- `hero.md`, Edwin (2026-10-23): Shrapnel Load Lv. 3 → Lv. 4 (Attack × 182% AoE; Lv. 5 needs 4★); hero power 345,017
  (+2,646; stats and gear unchanged); shards 5 / 40 (Redeem shows 1); expedition skills show 34/50 Rare Development Books.
  Hero Stats, the promotion preview, all four gear pieces, Detonate, level, escorts and troop capacity re-confirmed; the
  whole Edwin section and his roster row are dated 2026-10-23.
- `hero.md`, Chenko (2026-10-23): Brigader's Gauntlets +16 → +20 and Battle Boots +15 → +20 (25,900 each; +8.80% Cavalry
  Health / Lethality). Gear power 98,000 and hero power 447,120 (both +5,600); Hero Stats 1,208 / 1,471 / 12,090, escort
  402 / 490 / 4,030, Cavalry Lethality +16.90%, Health +17.04%; gear totals updated. Shards 15 / 40; skill rows show 22/50
  Epic Expedition Manuals and 36/50 Epic Conquest Books. Whole section and roster row dated 2026-10-23.
- `data/manual.json`: the promotion move notes Chenko (25 shards) as the next lineup hero after Jabel.
- Data health (`docs/index.html`, `data/manual.json`, `docs/SCHEMA.md`): a section is flagged only when it is undated or
  more than 3 days old (`staleAfterDays` 7 → 3). The "Older than snapshot" flag, which listed every section not refreshed
  on the newest upload day, is removed.
- `data/manual.json`: the Gordon Emergency Snack move is done and removed; the promotion move is priority 2.
- `hero.md`, Saul (2026-10-23): promoted 1-Star (Tier 5) → 2-Star (Tier 0) (+15,400 base power); shards 0 / 15 to Tier 1
  (Redeem shows 1); new Tier 0 → Tier 1 preview (99,800 +13,300 power; Archer Attack / Defense +63.60% +4.60%). Berserker's
  Bracers +0 → +1 (23,175; DEF +91 / HP +344; escort DEF +30 / HP +114; +9.21% Archer Health), gear power 89,925 (+675).
  Hero power 284,550 → 310,975; +10,350 of that is not itemised on screen (presumably the skill changes; inferred).
  Hero Stats 1,124 / 931 / 6,968, escort 374 / 310 / 2,322, Archer Attack / Defense +63.60%, Health +16.61%; gear totals
  updated. Skills: Rapid Fire and Taskforce Training Lv. 3 (Lv. 4 needs 3★); Superior Techniques Lv. 2 and Positional
  Battler Lv. 1 (unlocked); Final Prayer and Resourceful Lv. 2 no longer capped. Book counts from the Upgrade buttons
  (0/30 and 1/30, 1/10); the book names are inferred from the icons and say so. Rabbitgear Cannon details recorded
  (locked, Unlock 0/5, 30,000 power). Whole section and roster row dated 2026-10-23.
- `profile.md` (2026-10-23): account power 11,942,479; bread 65.4M; gems 25,840; VIP 3, citizens 32 / 32 and the Saul
  avatar re-confirmed. Town Center Lv. 20 is upgrading to Lv. 21 (3d 07:41:54 left on the screenshot, so around 26 Oct,
  inferred; Finish costs 63,759 gems); building power 431,800, +57,400 at Lv. 21.
- `troops.md`: the "Overall Account Power" row no longer repeats the power (now "Not recorded (kept in profile.md only …)").
  The copy fell behind whenever the power changed on a day without troop screens, and updating it would have dated the
  troop data as newer than it is.
- `data/manual.json`: the promotion move now reads "Saul is 2★ and Quinn 4★" with Saul at 15 shards to Tier 1; Saul's
  hero notes show the new skill effects and that the book names are inferred.
- `hero.md`, Saul (later on 2026-10-23): Berserker's Bracers +1 → +13 (32,445; DEF +113 / HP +425; escort DEF +37 /
  HP +141; +11.73% Archer Health). Hero power 320,245 and gear power 99,195 (both +9,270, all from the Bracers). Hero
  Stats DEF 953 / HP 7,049, escort DEF 317 / HP 2,349, Archer Health +19.13%; gear totals updated. Redeem shows 6.
- `data/manual.json`: the promotion move shows Saul's Redeem count as 6.
- `profile.md` (2026-10-23, Governor Profile): total kills 338,672 → 345,632; stamina 171 / 200; kingdom, alliance and
  the 6 locked Governor Gear slots re-confirmed. The profile shows power as 11.9M, the same figure as the exact
  11,942,479 already recorded.
- `lineups.md` (2026-10-23): Arena attack power recorded, 2,502,855 (Squad Settings; was "Not recorded"), and Arena defense
  power 2,452,930 → 2,494,295 (Defensive Squad Lineup). Each equals the sum of its five heroes' current powers, so the
  Arena defense conflict in Data health is gone (0 conflicts). All ten Arena rows re-confirmed.
- `troops.md` (2026-10-23, Troops Preview): Brave Infantry 32,811, Cavalry 34,579, Archer 34,195; total 101,585
  (+3,176; the header shows 101.5K/101.5K); 0 injured; March Queue 4/4. The notes now say what the header's first
  number and the queue count probably mean (inferred from the 22 and 23 Oct readings). March formations are unchanged.
- `hero.md`, Fahd (2026-10-23): Brigader's Breastplate +0 → +6 (17,850; DEF +67 / HP +336; escort DEF +22 / HP +112;
  +6.84% Cavalry Health). Hero power 310,850 and gear power 74,410 (both +2,850, all from the Breastplate). Hero Stats
  DEF 1,111 / HP 9,246, escort DEF 370 / HP 3,082, Cavalry Health +12.84%; gear totals updated. Shards 12 / 40 (Redeem
  shows 0). Promotion preview, all five skills, the other three gear pieces, level, escorts and troop capacity
  re-confirmed; the whole section and roster row are dated 2026-10-23.
- `hero.md`, Yeonwoo (2026-10-23): Windbreaker Leatherwear +0 → +3 (16,380; DEF +63 / HP +238; escort DEF +21 / HP +79;
  +6.42% Archer Health). Hero power 324,740 and gear power 80,740 (both +1,380, all from the Leatherwear). Hero Stats
  DEF 1,125 / HP 6,987, escort DEF 375 / HP 2,328, Archer Health +14.52%; gear totals updated. Shards 11 / 40 (Redeem
  shows 0). All five skills (Lv. 3, capped until 3★), the promotion preview and the other three gear pieces re-confirmed,
  including the Faceplate +11 and Boots +12 last seen on 21 Oct; the whole section and roster row are dated 2026-10-23.
- `hero.md`, Diana (2026-10-23): Berserker's Boots +16 → +17 (36,015; ATK +146 / HP +452; escort ATK +48 / HP +150;
  +12.57% Archer Lethality). Hero power 483,485 and gear power 111,245 (both +915, all from the Boots). Hero Stats
  ATK 1,571 / HP 9,586, escort HP 3,194, Archer Lethality +20.95%. Incendiary Arrows shows 27/50 Epic Expedition
  Manuals. Promotion preview (54 / 100, Redeem 0), the other three gear pieces, level, escorts and troop capacity
  re-confirmed. Sharpshooter, Deadly Strike and the two expedition skills keep their dates (their panels were not opened).

### Removed
- The Player ID, from `README.md` (the `profile.md` description) and from `profile.md` (the "Player ID" row).
  It remains in the git history of earlier commits.
- The governor name, from `profile.md` (the "Governor Name" row, now optional for the generator),
  `troops.md`, `README.md`, the hand-written `KS_DATA` in `docs/index.html` and the design prototype.
  The dashboard header shows "Governor: Not recorded". The name remains in the git history.

### Fixed
- Defense & Arena (`docs/index.html`): a power difference whose percentage rounds to zero showed a plus sign, e.g.
  "−915 (+0%)". The sign now follows the value (+ above zero, − below, none at zero), so it reads "−915 (0%)", and an
  exact match reads "0 (0%)" instead of "+0 (+0%)".

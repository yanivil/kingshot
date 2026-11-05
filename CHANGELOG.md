# Changelog

All notable changes to this repository are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `data/gift_codes_baseline.txt`: 142 old codes the six trackers still list but that were never in `codes.md`, found by
  the first (dry) run of the gift-code check on 4 Nov. The check now ignores them, so it reports only codes that appear
  later. `scripts/check_gift_codes.py` gains `--baseline` (the workflow passes it) and two tests. README updated.
- `codes.md`: `KS1104` in Active Codes (not redeemed, unverified), found by that run on kingshot.net and kingshotmastery.com.
- New gift-code check that runs on GitHub itself: `.github/workflows/check-gift-codes.yml` runs
  `scripts/check_gift_codes.py` every two days (and by hand from the Actions tab, with a dry-run option). It reads
  community tracker pages, drops codes already in `codes.md` or already reported, and opens one `gift-codes` issue
  mentioning the owner when new codes appear. It never commits. Tests in `scripts/test_check_gift_codes.py` (no
  network). README section "New gift-code check" added. It replaces the Claude scheduled task set up on 4 Nov.
- `codes.md`: two new gift codes in Active Codes, not redeemed yet: `TREAT4U` (Halloween; trackers give an expiry of 4 or 5 Nov)
  and `KS1102` (listed only by kingshot.net). Taken from community trackers on 2 Nov and not yet tried in the game, so unverified.
- `codes.md`: two new gift codes in Active Codes, both not redeemed yet: `KS1025` (listed from 25 Oct) and `OFFICIALSTORE1023`
  (listed from 23 Oct). Taken from community trackers (kingshotmastery.com, kingshot.net, kingshotguide.org, kingshotwiki.com) on
  27 Oct and not yet tried in the game, so their rewards and status are unverified.
- `data/manual.json`: three strategy suggestions, asked for by the account owner on 27 Oct ("think out of the box"), each with
  confidence labels and the community sources it relies on:
  - Priority 3, "Troops": train Infantry next. The army is 32% Infantry (34,151 of 105,729), while community guides mostly use
    50 / 20 / 30 for attacks and rallies; the Att preset can reach at most 43% Infantry, so it is suggested as 43 / 27 / 30.
  - Priority 4, "Marches": save the free fourth march preset as "Join", led by Chenko (Stand of Arms, +15% Lethality), with Helga and
    Yeonwoo, because guides say a joining march adds only its lead hero's first expedition skill to the rally.
  - Priority 6, "Heroes": long-term focus. Mythic shards and books to Jabel first; Epic to Diana, Quinn and Howard plus the rally
    joiner; Helga and Saul last for combat; Generation 2 / 3 timing from community timelines, to be checked against the kingdom's age.
  - The other suggestions move down one or two places (be-swap-forrest 7, gat-match-resource 8). The skill-book suggestion names
    Chenko's Stand of Arms as the Conquest Book pick for players who mostly join rallies, and drops Fahd from the Lv. 2 list.
- `troops.md`: new "Beast & Terror Hunting" section: beasts up to Lv 21 and Terror (a huge beast that can only be rallied)
  up to Lv 4, as told by the account owner on 25 Oct (not from a screenshot). `data/manual.json` adds a "Beasts & Terror"
  feature row dated from that section. README updated.
- `data/manual.json`: suggestion priority 5 ("Skills"): which skill each book type should go to next, ranked. Epic Conquest
  Books → Howard's Defenders' Edge, then Gordon's Trash Talk, then Quinn's Precision Shot; Epic Expedition Manuals →
  Howard's Joint Defense, then Quinn's Headshot, then Diana's Incendiary Arrows; Mythic books → Jabel's Youthful Rage and
  Persistence. Uses the shared-stock rule; the order is Inferred and says what is unverified.
- Drill Camp screen of 2026-10-25: `data/manual.json` Drill Camp (and its feature date) is now 25 Oct. The 5 instructors are
  Jabel, Chenko, Saul, Quinn and Diana, all Lv 54 (Saul is confirmed as an instructor; heroes are identified by portrait,
  as the screen shows no names). Slots unchanged: Amane, Helga, Howard, Gordon, Yeonwoo, Fahd, Forrest; slot 8 needs Town
  Center Lv 21. The auto-level and Level Resets texts are re-confirmed. `profile.md`: gems 25,840 → 24,396.
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
- `profile.md` (Town Center screen, later on 2026-11-05): account power **17,818,524** exact from the city top bar
  (the Governor Profile showed 17.7M earlier that day), **VIP 4** (VIP 3 on 27 Oct), free gems 35,597, bread 104.1M;
  Town Center Lv. 22, citizens 32 / 32 and TC Attack / Defense / Health 735 / 1,470 / 22,064 re-confirmed; the same
  six perk icons (names not shown, dates kept).
- Stale notes fixed, found while validating the suggestions on 2026-11-05: the Governor Gear feature note in
  `data/manual.json` said 3 of 6 slots equipped (now 6 of 6 since 5 Nov, as `profile.md` shows), and README described
  `profile.md` as Town Center Lv. 20 (Lv. 22 since 27 Oct).
- `data/manual.json`, `rally-join-preset`: troop numbers for the Join preset (asked for by the account owner on
  2026-11-05). Bear Hunt: 8,888 Infantry / 36,812 Cavalry / 43,180 Archers = 88,880 (10 / 41 / 49%). The guides give a
  joiner 10 / 10 / 80 (kingshotworld.com, kingshotguides.com) or 10 / 30 / 60 for Generation 1 heroes
  (kingshotmastery.com), but the account has 43,180 Archers, so every Archer goes and Cavalry fills the rest; the
  guides say a full march matters more than the exact ratio. Terror: 44,440 / 17,776 / 26,664 (50 / 20 / 30,
  kingshotguides.com). The 88,880 march size is inferred from the other presets; the per-joiner cap a rally leader sets
  is not known. Shown as a second Now / Suggested block and in the Top 5.
- Formation advice checked against the full guide pages (the account owner allowed the guide sites on 2026-11-05; the
  pages were downloaded, stripped to text and every quote checked). Search-excerpt evidence is replaced by dated
  quotes. Corrections:
  - Barricades only fight Rebel Invasions; the Guard Station's heroes defend the city against players and in Viking
    Vengeance (a guide author's reply). `lineups.md` and README no longer call the Barricades city defense, and the
    Guard Station card no longer says it may be the Barricades screen.
  - The Viking Vengeance guide's home team for players who don't spend is Jabel, Howard and Quinn; Saul is only in its
    pay-to-win list (the earlier "Howard, Quinn and Saul" was wrong).
  - "Amane is not a gathering hero" is not on the cited page; removed (her own skills show no gathering skill).
  - Two rally pages cited before are gone (404); the joiner rules now cite kingshot.net, kingshotworld.com,
    kingshotguides.com and kingshotmastery.com. That Chenko's and Yeonwoo's skills add together is from
    kingshotmastery.com. The official X post is still read only as a search excerpt (x.com is not reachable).
  - The troop-mix card notes the Bear Hunt ratio for a Generation 1 host (10 / 30 / 60, kingshotmastery.com).
  - Unchanged: the suggestions themselves (Chenko in Arena defense; Jabel, Howard and Quinn for the Guard Station).
- `data/manual.json`: community formation advice, asked for by the account owner on 2026-11-05 ("based on the
  community, which heroes should be in my formations?"). The guide pages could be read only as search-result excerpts
  (the sites are not on the session's network allow-list), so every guide claim is labelled Unverified.
  - New ready move `arena-defense-chenko` (priority 2): Arena defense = the guides' Generation 1 F2P team, the same five
    as the attack squad, so Chenko takes Gordon's front-right place.
  - New waiting move `guard-station-heroes`: Jabel, Howard and Quinn for city defense, waiting for a screenshot of the
    Guard Station (its heroes are not recorded).
  - More evidence on `rally-join-preset` (the official Kingshot X account: rally leaders get all three heroes'
    skills, joiners only the 4 highest-levelled first skills; chance-based skills do not stack), `be-swap-forrest`,
    `gat-match-resource` and `att-troop-mix-test`.
  - Unchanged because the guides agree with them: the Arena attack squad, the Att rally team (Howard, Jabel, Quinn),
    the Chenko-led Join preset and Barricade 1 (Howard, Jabel, Quinn).
- Gift codes: every redeemed code goes to Expired with ✓ (the account owner's rule, 2026-11-05), so the separate
  Redeemed list is gone. `codes.md`: `FORTHEKINGDOM` moves to Expired with ✓; the file now has Active and Expired only.
  `scripts/build_data.py`: `codes` is `{asOf, active, expired, expiredTotal}`; rows left under an old "Redeemed Codes"
  heading are shown as Expired with ✓ and warn (new tests `test_leftover_redeemed_list`,
  `test_expired_without_redeemed_column`). Page: two panels (To redeem, Expired); the lede reads
  "0 to redeem · 11 expired (6 ✓ redeemed)"; older data with a `redeemed` list is folded into Expired the same way.
  `scripts/check_gift_codes.py` docstrings and its test, README and `docs/SCHEMA.md` updated.
- `hero.md`, Olive (Stats screens, later on 2026-11-05): Lv. 63 → **Lv. 64**, power 416,159 → **418,174** (+2,015,
  presumably the level; inferred), troop capacity 12,650 → 12,730, Hero ATK / DEF / HP 1,351 / 1,566 / 8,175 and
  escort 450 / 522 / 2,724; the Archer bonuses are unchanged. The next level needs Town Center Lv. 23. Her +15,107 since
  27 Oct is exactly +9,815 for Lv. 59 → 64 (as inferred for Seth and Forrest) plus two Rare skill upgrades of +2,646, so
  the earlier inferred split fits. The Drill Camp note in `data/manual.json` now says she showed Lv. 63 at the time.
- Codes page: ✓ marks the codes redeemed on this account, also in the Expired list (asked for by the account owner on
  2026-11-05). The Expired table in `codes.md` gains a **Redeemed** column. The ✓ is set for `KS1104` and `VIP777`
  (told on 5 Nov) and for `Kingshot888`, `KS1025` and `OFFICIALSTORE1023`, which the list marked redeemed before the
  5 Nov restart (confirmed by the owner on 5 Nov). `scripts/build_data.py` reads it into `codes.expired[].redeemed` and
  warns on any text other than ✓ / V / Yes (new test `test_expired_redeemed_mark`). The page shows ✓ on every Redeemed
  code and on marked Expired codes ("10 total · 5 ✓ redeemed"); README and `docs/SCHEMA.md` updated.
- `codes.md` (told by the account owner on 2026-11-05): `FORTHEKINGDOM` added to Redeemed (rewards not recorded).
  `VIP777` and `KS1104` move from Redeemed to Expired because the owner thinks they are old; their notes keep that
  they were redeemed on this account. `KS1102` was already Expired. The page's sample data matches. README and
  `docs/SCHEMA.md` now say that a redeemed code that becomes old moves to Expired.
- "Top 5 moves now" lists only moves the account can do today, one move per card (the account owner pointed out on
  2026-11-05 that card 1 bundled three shard plans and none of them had enough shards: Amane needs 20 more with 4 Epic
  Redeem shards, Jabel 64 with 36 Mythic, Olive 24 with 4 Rare).
  - New optional recommendation fields `ready` (boolean) and `waitingFor` (text). A move with `ready: false` ranks after
    every ready move, stays out of the Top 5, and shows "Not yet" plus a "Needs" line on Invest. Under the Top 5 a line
    counts the waiting moves and opens Invest. `scripts/build_data.py` warns when `ready` is not a boolean or when a
    waiting move has no `waitingFor`; new test `test_ready_flag_checks`. `docs/SCHEMA.md` and README updated.
  - `data/manual.json`: `near-promo` is split into `epic-shards-amane`, `mythic-shards-jabel` and `rare-shards-olive`;
    `skill-books-order` into `expedition-manuals-howard` (21 more manuals needed: 29 of 50) and `conquest-books-gordon`
    (stock not read). These five and `hero-focus-long-term` are marked `ready: false`.
  - New Top 5: the rally Join preset, the Be-march test with Helga, gathering presets per resource, the Stonewall
    Greaves +24 to Forrest, and the optional 50 / 20 / 30 test, now in the Att preset itself, because the Join, Stone
    and Bread presets would fill the three spare tabs.
- `data/manual.json`: the Top 5 shows only open moves (asked for by the account owner on 2026-11-05). Every suggestion now
  describes only what is left; "done" steps and "(done)" changes are removed (the history stays in this changelog and in
  hero.md). The two suggestions whose main move is finished keep only a small optional step and move to the bottom:
  the gear swap becomes `greaves-to-forrest` (priority 8: Seth's Stonewall Greaves +24 to Forrest) and the troop
  suggestion becomes `att-troop-mix-test` (priority 7: optional 50 / 20 / 30 test). New order: promotions, rally Join
  preset, skill books, long-term focus, Be-march test, gathering presets, troop test, Forrest's greaves.
- Later on 2026-11-05 (Gear and promotion screens):
  - `hero.md`, Howard and Seth: they swapped boots. Howard now wears Seth's Epic Praetorian's Greaves +20 (gear 148,035 →
    158,325; Infantry Lethality 22.77% → 26.61%) and Seth Howard's Rare Stonewall Greaves +24 (gear 155,400 → 145,110). Each
    piece kept its + level, which settles that the level moves with the piece. Hero Stats and power were not re-read; the
    expected changes (±10,290 power) are noted as inferred.
  - `hero.md`, Diana: **4★ Tier 2** with 20 Epic Redeem shards (24 → 4). Power 599,698 → 635,778 and stats up by exactly the
    preview; Archer Attack / Defense +86.25%. New preview to Tier 3 (+36,080, +4.96%); roster row updated.
  - `hero.md`, Jabel: a stray closing parenthesis in her power line (from the 5 Nov update) is removed.
  - `data/manual.json`: the gear swap (priority 1) is marked done for Howard, with one optional step left (Seth's +24
    Greaves to Forrest, or to Helga if she replaces Forrest); the promotion suggestion (priority 2) marks Diana's Tier 2
    done and points the next Epic shards at Amane's 3★ (needs 20) or Quinn's Tier 2; Seth's gear note no longer says
    "Full Epic set".
- Gift codes restarted (asked for by the account owner on 2026-11-05):
  - `codes.md` now holds only the owner's current codes, in three lists with no checkbox column: **Active** (not redeemed
    yet; empty for now; new codes go here), **Redeemed** (`KS1104`, `VIP777`) and **Expired** (`KS1102`, `TREAT4U`,
    `OFFICIALSTORE1023`, `KS1025`, `Kingshot888`, `lwaL5ZKx5`, `KSPRAWNING`, `KS1017`). Known rewards are kept.
  - The 22 older codes dropped from `codes.md` (e.g. `HAPPYCATDAY`, `WELLDONE`, `KS1005`) were added to
    `data/gift_codes_baseline.txt`, so the gift-code check does not report them as new.
  - Dashboard: the per-browser "tap to mark redeemed" feature is removed, because redeemed is a fact about the account,
    not a browser. The Codes page shows three read-only lists (To redeem, Redeemed, Expired) and deletes the old
    `ks-code-marks` browser key once.
  - `scripts/build_data.py`: `codes` is now `{asOf, active, redeemed, expired, expiredTotal}` with `{code}` entries; it
    warns when a code is in two lists. `scripts/check_gift_codes.py` reads rows whose first cell is a backticked code
    (and still the old checkbox rows). Tests: three parser tests, two checker tests (old layout, dropped codes stay
    ignored); 53 tests in all.
  - README and `docs/SCHEMA.md` describe the three lists.
- `codes.md`: `KS1104` is ticked as redeemed (told by the account owner on 5 Nov; rewards not shown, so "Not recorded").
- `data/manual.json`: an audit of all eight suggestions against the 5 Nov data (asked for by the account owner) found older details
  in five and brings them up to date:
  - Be-march test (priority 7): hero power now Helga 306,455 / Forrest 438,984; the Be preset evidence is the 5 Nov split
    (35 / 20 / 45); the link to the gear swap now names the Stonewall Greaves +24, which go to Helga if she replaces Forrest
    (her own Greaves are +8); Saul's Lethality reads +15% (Positional Battler Lv 3), not +5%.
  - Rally Join preset (priority 4) and gathering presets (priority 8): the evidence uses the 5 Nov presets and march queues, and
    the steps point to the free preset tabs 4 to 6, whose contents were not shown.
  - Promotions (priority 2): "no line-up" now says "no combat line-up" where the hero is in the `Gat` gathering preset.
  - Skill books (priority 5): the Epic Expedition Manual evidence lists every 5 Nov screen that shows 29.
- `troops.md` (2026-11-05 Troops Preview and Deploy screens):
  - All troops are now **Tier VIII (Elite)**: Infantry 45,474, Cavalry 46,298, Archers 43,180, **134,952** in all (105,729 Tier VII
    on 24 Oct). Infirmary 0 / 72,800 (38,600). March queues 4 / 4.
  - March size **88,880** for `Be` and `Att`, 88,410 for `Gat`; the 470 gap equals Edwin's lower Troop Capacity at Lv 59, which
    suggests a base plus the three heroes' Troop Capacity (inferred).
  - Presets: `Be` 18,227,722 power, 35 / 20 / 45; `Att` 20,910,710, **50 / 30 / 20**; `Gat` 16,968,707, 51 / 49 / 0; heroes now
    Lv 64 (Edwin 59). Preset tabs 4, 5 and 6 exist but were not opened. `lineups.md`'s preset table updated to match.
- `profile.md` (2026-11-05 Governor Profile): power **17.7M** (the profile truncates; 13,969,554 exact on 27 Oct), kills 658,745,
  stamina 124 / 200, Kingdom #2508 and Alliance SPQ re-read. Governor Gear is now **6 / 6**: Plain Hood (Uncommon 1-Star, 306,000,
  Cavalry +12.75%), Modest Cloak (Infantry +9.35%) and Oakheart Ring (Archer +9.35%) fill the three empty slots; totals Cavalry
  +22.10%, Infantry and Archer +18.70% Attack and Defense, 1,428,000 gear power. The governor name and Player ID shown on the
  screen are not recorded.
- `data/manual.json`: the troop suggestion (priority 3) records that the Infantry goal is met (Att 50% Infantry on Tier VIII) and
  now offers the guides' 50 / 20 / 30 in Att only as an optional test; the rally suggestion notes the preset tabs 4 to 6.
- README and `docs/SCHEMA.md`: troop tier wording updated (Tier VIII Elite; `Gat` listed among the presets).
- `hero.md`, Amane and Helga (2026-11-05), the last two heroes still on 27 Oct data:
  - Amane: Lv 64 (drill slot), 20 / 40 to 3★, gear unchanged, **all three exploration skills Lv 2 → 3** (Sakura Blossom now capped
    until 3★). Power 313,060 → 332,700 = +12,080 levels + 7,560 skills (both inferred), exactly.
  - Helga: Lv 64 (drill slot), 1★ (0 / 5), Gloves +0 → +10, Shroud +3 → +9, Greaves +2 → +8 (gear 92,905 → 107,845). Power
    274,905 → 306,455 = +14,940 gear + 16,610 levels (inferred), exactly. She still wears her own Praetorian's Gloves and Shroud, so
    Howard's Epic gloves and Forrest's Epic Shroud are other pieces; their notes now say so.
  - Seth's and Olive's level notes and roster rows record that Seth replaced Olive as a Drill Camp instructor.
- `data/manual.json`, same date:
  - Drill Camp: new reading from the 5 Nov Drill Camp screen. The instructors are Jabel, Chenko, Seth, Quinn and Diana, all Lv 64
    (identified by portrait and confirmed as the only five heroes at Lv 64 outside a drill slot). The same 8 slotted heroes are all
    Lv 64, and the screen text again states the lowest-instructor rule. This replaces the 27 Oct reading and the inference about Olive.
  - Promotions: Amane's 3★ also needs 20 Epic shards, the same as Diana's Tier 2. The 24 in stock cover one of the two; Diana stays
    first (in line-ups) with Amane as the stated alternative (her 3★ lifts Tri-Phalanx, a rally-joiner skill, and Exorcism).
  - Skill books, rally, long-term and Be-march suggestions use the new Amane and Helga numbers.
- `hero.md`, Gordon, Seth, Saul, Forrest, Edwin, Olive, Yeonwoo and Fahd (2026-11-05):
  - Gordon: **4★ Tier 0** (5 / 100). Armet is now a Brigader's Armet +25 with exactly the stats Jabel's had on 27 Oct (presumably the
    same piece, inferred); the other three pieces +20. Power 475,780 → 539,750 = +37,360 4★ + 14,530 gear + 12,080 levels (inferred).
  - Seth: **3★ Tier 5** (39 / 100), all four Epic Praetorian's pieces +20 (gear 155,400). Power 438,369 → 481,924 = +18,785 Tier 5
    + 14,955 gear + 9,815 levels (inferred). He still wears his own Epic gloves, so Howard's +21 pair is a different one.
  - Saul: **2★ Tier 5** (0 / 40 to 3★), gear +26 (Bracers +25), **Positional Battler Lv 3**. Power 416,030 → 474,025 = +16,300 Tier 5
    + 23,445 gear + 18,250 levels and the skill (inferred). Roster role text updated (+9% construction, +15% Lethality).
  - Forrest: 59 / 100 to 4★; an Epic Praetorian's Shroud +19 replaced the Stonewall Shroud, and the other pieces went up (gear
    84,830 → 112,460). Power 401,539 → 438,984 = +27,630 gear + 9,815 levels (inferred, the same as Seth's).
  - Edwin: still Lv 59 (not in a drill slot; the hero XP stock of 414,898 covers the next level), **3★ Tier 3 → Tier 5** (7 / 100),
    Armet +11 → +20. Power 354,052 → 396,177 = +36,725 base (two promotions) + 5,400 gear, exactly.
  - Olive: Lv 59 → **63** with a working Upgrade button (412,898 / 420,000 XP), 76 / 100 to 4★, gear unchanged, **Green Thumb and
    Forager's Luck Lv 4** (+20%). Power 403,067 → 416,159 (+13,092, levels and the two skills, inferred). Roster role text updated.
  - Yeonwoo: Lv 64 (drill slot), 13 / 40 to Tier 1, Leatherwear +3 → +9, **On Guard Lv 4** (+20% Lethality). Power 361,910 → 380,548
    = +3,030 gear + 12,080 levels + 3,528 the skill (the last two inferred), exactly. Roster role text updated.
  - Fahd: Lv 64 (drill slot), **2★ Tier 5 → 3★** (17 / 40), Armet +11 → +20. Power 329,530 → 368,930 = +21,920 3★ (the preview)
    + 5,400 gear + 12,080 levels (inferred), exactly. The 3★ lifts his Lv 3 skill caps (Sandstorm now shows 29 / 50).
  - The stat changes split the same way; new previews where they changed.
- `data/manual.json`, same date: the gear swap now uses Seth's Greaves +20 and Forrest's 5 Nov gear (Howard +10,290, Forrest
  +4,550, Seth −14,840); promotions add Gordon (4★), Seth, Edwin and Olive (all Rare heroes are now Tier 5; Olive is closest to 4★,
  needs 24), Saul (Tier 5), Forrest and Yeonwoo; skill books mark Saul's Positional Battler and Yeonwoo's On Guard done; the rally,
  gathering, long-term and Be-march suggestions use the new numbers; Saul's hand-written skill notes were out of date (+6% / +10%)
  and are fixed; a sentence in the promotion suggestion had lost its commas in the Chenko update and is rewritten.
- `data/manual.json` Drill Camp: the instructor levels go back to the 27 Oct reading (Diana 61, Chenko 59). The Diana and Chenko
  updates had put their 5 Nov levels into a reading dated 27 Oct, mixing two dates; the page already flags each instructor whose
  own screen shows a different level and asks for a re-read. The note now records the 5 Nov evidence: the drill-slot heroes show
  Lv 64 while Olive shows Lv 63 and can be levelled, so she is presumably no longer an instructor (Seth, Lv 64, is the likeliest
  replacement; inferred). A new Drill Camp screenshot would settle it.
- `hero.md`, Chenko (2026-11-05): Lv 59 → **64** (cap, "Requirement: Town Center Lv. 23"), **4★ Tier 0** (8 / 100). The Rare
  Brigader's Armet +15 was replaced by the Mythic **Judicator's Armet +22** (68,025; +22.70% Cavalry Lethality) and the Breastplate is
  +20, so gear is 98,000 → 145,725. **Stand of Arms reached Lv 4.** Power 481,360 → 582,053: +37,360 4★ (the preview), +47,725
  gear, +12,080 presumably the levels and +3,528 presumably the skill (inferred); the stat changes split the same way. New
  promotion preview (T0 → T1: +32,560, +6.31%); roster row updated. Jabel's 5 Nov screens also show a Judicator's Armet (+23);
  whether there are two is not shown.
- `data/manual.json`, same date: Chenko is a 4★ in the promotion suggestion; the rally suggestion and the skill-book suggestion
  mark Stand of Arms Lv 4 as done; the Drill Camp instructor level for Chenko is 64. Two hand-written gear notes were out of date
  and are fixed: Chenko's said "All Rare gear.", and Jabel's still listed her 27 Oct gear (missed in the 5 Nov Jabel update).
- `hero.md`, Jabel, Diana, Quinn and Howard (2026-11-05 screenshots):
  - Jabel: **3★ Tier 5** (36 / 100 to 4★; Mythic Redeem 36). Power 653,530 → 764,215: +28,900 Tier 5 (the 27 Oct preview),
    +72,965 gear (Rare Brigader's Armet +25 replaced by the Mythic Judicator's Armet +23; Gauntlets +25; Breastplate +30), and
    +8,820 presumably Persistence and Youthful Rage reaching Lv 4 (inferred). Gear 237,155. Gallant Throw is capped until 4★.
  - Diana: Lv 61 → **64**, **4★ Tier 1** (80 / 100 to Tier 2). Power 502,893 → 599,698: +69,920 base (4★ and Tier 1, both
    previews), +19,525 gear (Faceplate +0 → +20, Leatherwear and Boots +20), +7,360 presumably the levels (inferred). Iron
    Constitution's Lv 4 cap is lifted.
  - Quinn: **4★ Tier 1** (32 / 100 to Tier 2). Power 551,935 → 597,520: +32,560 Tier 1 (the preview) and +13,025 gear (Faceplate
    and Bracers Epic +20, Leatherwear +20, Boots +24) add up exactly. Archer Attack / Defense +103.45% (the preview said +103.44%).
  - Howard: Lv 59 → **64** (still drill-locked), **4★ Tier 0** (2 / 100). Rare Stonewall Gloves +20 replaced by Epic Praetorian's
    Gloves +21; Helm and Shroud +21; Greaves +24 (gear 128,860 → 148,035). Shielded Strike and Weaken reached **Lv 4** (Shielded
    Strike Lv 5 costs 75 Epic Expedition Manuals). Power 515,748 → 591,419: +37,360 4★ (the preview), +19,175 gear, +12,080
    presumably the levels and +7,056 presumably the two skills (inferred); the stat changes split the same way.
  - New promotion previews for all four; roster rows updated.
- `data/manual.json`, same date:
  - Gear swap (priority 1): the gloves half is done; the suggestion now covers only the boots (Seth's Epic Greaves +16 for
    Howard's Rare +24). Seth's and Forrest's gear was not re-checked.
  - Promotions (priority 2): redeem 20 of the 24 Epic shards for Diana's Tier 2 now; keep the 36 Mythic shards for Jabel's 4★
    (needs 64).
  - Skill books (priority 5): Howard's Weaken and Shielded Strike and Jabel's Persistence and Youthful Rage are marked done;
    Epic Expedition Manual stock 29.
  - Long-term focus (priority 6): Jabel's next step is 4★, not Tier 5.
  - Drill Camp: Diana's instructor level is 64; the note records that Howard at Lv 64 implies all instructors are presumably 64
    (inferred; Olive and Chenko stay at 59 until their screens are re-sent).
- `data/manual.json`: the long-term hero suggestion records that the account has no Zoe, Hilde or Marlin (told by the account owner on
  28 Oct; kingdom age unknown), so Generation 2 has presumably not arrived (inferred); its last step now says to watch the Hero
  Roulette and Hall of Heroes events instead of asking for the kingdom age.
- `hero.md`, Saul (later on 2026-10-27): Superior Techniques Lv 2 → **Lv 3** (+20% Attack Speed; capped until 3★, "To upgrade:
  ascend to 3-Star"). Power 412,880 → 416,030 (+3,150) with stats, gear and preview unchanged, so presumably that skill (inferred).
  `data/manual.json`: the skill-book suggestion no longer lists Saul's Lv. 2 skills.
- `codes.md`: `KS1025` and `OFFICIALSTORE1023` are ticked as redeemed; the account owner confirmed both worked on 27 Oct
  (their rewards were not shown, so they stay "Not recorded").
- `hero.md`, Amane and Helga (2026-10-27):
  - Amane: Lv 59 (Drill Camp level); the empty chest slot now holds a Windbreaker Leatherwear (+0, 15,000) and the Faceplate is
    +11, so gear power is 65,500 and all 4 slots are filled (Archer Health 12.00%, Lethality 13.54%). Power 286,390 → 313,060:
    +15,550 gear and +11,120 levels (inferred) add up exactly. Stats 1,144 / 1,134 / 7,033, escort 381 / 378 / 2,344. Shards 0 →
    10 / 40 to 3★. Sakura Blossom shows 10 / 30 manuals.
  - Helga: Lv 59 (Drill Camp level), power 259,615 → 274,905 with gear (92,905), skills and preview unchanged, so presumably the
    levels (inferred). Stats 625 / 773 / 12,370, escort 205 / 257 / 4,123. Still 1★ Tier 0, 0 / 5; Antler Assault capped until 2★.
- `hero.md`, Fahd (2026-10-27): Lv 59 (Drill Camp level), power 310,850 → 329,530 with gear (74,410) and preview unchanged;
  presumably +11,120 levels and +7,560 for Sandstorm, Eagle Wings and Dune General reaching Lv 3 (inferred). Sandstorm Lv 3
  is capped until 3★ ("To upgrade: ascend to 3-Star"). Stats 957 / 1,141 / 9,486, escort 318 / 380 / 3,162. Shards 12 → 21 / 40
  to 3★, Epic Redeem 27. `data/manual.json`: the promotion suggestion notes the 27 Epic shards could cover Fahd's 3★ (19), though
  he is in no line-up.
- `hero.md`, Yeonwoo (2026-10-27): **promoted to 3-Star** with 25 Epic Redeem shards (the shared Epic stock went 52 → 27, told by
  the account owner). Lv 59 (Drill Camp level), Faceplate +11 → +18 (gear 84,870), power 324,740 → 361,910: +21,920 promotion
  (exactly the 23 Oct preview) + 4,130 Faceplate + 11,120 levels (inferred, Chenko's and Gordon's gain) add up exactly. Stats
  1,249 / 1,233 / 7,667, escort 416 / 411 / 2,555, Archer Attack / Defense 66.44%, Lethality 16.20%. The 3-Star promotion lifts
  her Lv. 3 skill cap: Petalbloom now shows 10 / 50 manuals; On Guard and her other skills are marked In Progress. New
  3★ T0 → T1 preview. `data/manual.json`: the promotion suggestion now starts with Edwin (1 Rare shard) and keeps the 27 Epic
  shards for Diana (needs 45).
- `hero.md`, Edwin (2026-10-27): Lv 59 (not in a drill slot), 12,260 troop capacity. Power 345,017 → 354,052 (+9,035) with gear
  (79,360), skills and preview unchanged, so presumably the levels (inferred; the same +9,035 as Seth). Stats 977 / 1,416 /
  9,735, escort 324 / 472 / 3,245. Shards 5 → **39 / 40** to Tier 4, Rare Redeem 2. Olive's and Forrest's unexplained +11,681
  now reads as +9,035 for the levels (Seth, Edwin) plus +2,646 for a skill reaching Lv 4 (Edwin's Shrapnel Load on 23 Oct);
  still inferred. `data/manual.json`: the promotion suggestion now says 1 of the 2 Rare Redeem shards promotes Edwin to Tier 4
  (+17,940 base power), the other goes to Seth.
- `hero.md`, Forrest (2026-10-27): Lv 59 (Drill Camp level), **Tier 4 → Tier 5** (+18,785, exactly the 22 Oct preview), power
  371,073 → 401,539 with gear unchanged (84,830); the other +11,681 is presumably levels plus Master Woodcutter reaching Lv 4
  (inferred; Olive shows the same +30,466 for the same changes). Stats 809 / 1,548 / 15,871, escort 268 / 515 / 5,290,
  Infantry Attack / Defense 57.22%. Shards 3 / 100 to 4★, Rare Redeem 2. New Tier 5 → 4★ preview. `data/manual.json`: the
  gathering suggestion uses Forrest's +20% wood, the gear-swap evidence cites his 27 Oct gear screens, and the Drill Camp
  note lists him as confirmed by his own screen.
- Drill Camp screen of 2026-10-27 (`data/manual.json`): instructors now Lv 64 / 61 / 59 / 59 / 64, so slotted heroes run at
  **Lv 59**. Instructors: Jabel 64, Diana 61, **Olive** 59, Chenko 59, Quinn 64. **Saul left the instructors and fills the
  new slot 8**: his own screen says he cannot be levelled within a Drill Camp. Olive's own screen (green hood, Lv 59) matches
  the fifth instructor. 8 of 15 slots are open and filled; slot 9 needs Town Center 23. The Drill Camp feature date is 27 Oct.
- `hero.md`, Saul (2026-10-27): Lv 59 (drill slot), **2-Star Tier 0 → Tier 4** (base power 99,800 → 158,900), Bracers
  +14 → +20 and Leatherwear +15 → +18 (gear 110,280), power 326,215 → 412,880 (+59,100 tiers, +7,365 gear, +20,200 presumably
  levels plus Final Prayer and Resourceful reaching Lv 3; inferred). Stats 1,372 / 1,179 / 8,662, escort 457 / 393 / 2,887,
  Archer Attack / Defense 82.02%, Health 21.72%. Shards 0 / 15 to Tier 5, Mythic Redeem 2. New Tier 4 → 5 preview.
- `hero.md`, Olive (2026-10-27): Lv 59 (Drill Camp instructor), **Tier 4 → Tier 5** (+18,785, exactly the 22 Oct preview),
  power 372,601 → 403,067 with gear unchanged; the other +11,681 is presumably levels plus Target Lock reaching Lv 4
  (inferred). Stats 1,328 / 1,536 / 8,028, escort 442 / 512 / 2,675, Archer Attack / Defense 57.22%. Shards 20 / 100 to 4★,
  Rare Redeem 2. New Tier 5 → 4★ preview.
- `data/manual.json` suggestions: Saul's promotion count (0 / 15 to Tier 5) and the Mythic book stock notes (not re-read since
  Saul's Final Prayer and Resourceful reached Lv 3).
- `hero.md`, Seth (2026-10-27): Lv 54 → **Lv 59** (not in a drill slot: the Upgrade button shows the shared hero XP), 12,260
  troop capacity. Power 429,334 → 438,369 (+9,035) with all four Praetorian's pieces (140,445), skills and preview
  unchanged, so presumably the levels (inferred). Stats 845 / 1,577 / 16,608, escort 280 / 525 / 5,535. Shards 0 → **31 / 40**
  to Tier 5, Redeem 2 (Rare). Hammer Burn says "To upgrade: ascend to 4-Star". `data/manual.json`: the promotion suggestion
  adds Seth (9 shards from Tier 5, +18,785 base power; in no combat lineup), and the Seth → Howard gear suggestion uses
  Howard's Shroud +20 of 27 Oct (Howard 128,860 → 147,000 gear power; Infantry Health 22.00% → 25.35%).
- `hero.md`, Gordon (2026-10-27): Lv 54 → **Lv 59** (Drill Camp level), 12,260 troop capacity. Armet +15 → **+16**
  (23,400; +8.24% Cavalry Lethality, total 16.62%); gear power 92,420. Power 464,060 → 475,780: +600 from the Armet and
  +11,120 presumably from the levels (inferred; the same gain as Chenko for Lv 54 → 59, which also backs the split of
  Howard's gain). Stats 1,277 / 1,552 / 12,756, escort 424 / 517 / 4,252. Shards 4 → 22 / 100, Redeem 52; BBQ Feast shows
  10 Epic Expedition Manuals. `data/manual.json`: the promotion and skill-book suggestions add Gordon's counts.
- `hero.md`, Howard, Chenko and Diana (2026-10-27):
  - Howard: Lv 54 → **Lv 59** (Drill Camp level), 12,260 troop capacity. Shroud +19 → +20 (38,850; +13.20% Infantry
    Health, total 22.00%); gear power 128,860. Power 500,140 → 515,748: +960 from the Shroud, and the other +14,648 is
    presumably the levels (+11,120, as Chenko) plus Defenders' Edge reaching Lv. 4 (+3,528, the same gain as Diana's Iron
    Constitution Lv. 4); both inferred. Defenders' Edge now **Lv. 4** (from the skill icon; the panel was not opened).
    Stats 1,016 / 1,608 / 19,917, escort 337 / 536 / 6,639. Shards 24 / 100, Redeem 52.
  - Chenko: Lv 54 → **Lv 59** (Drill Camp instructor), 12,260 troop capacity. Power 470,240 → 481,360 (+11,120) with gear
    (98,000), skill levels and preview unchanged, so presumably the levels (inferred). Stats 1,280 / 1,561 / 12,810,
    escort 426 / 520 / 4,270. Shards 1 → 27 / 100, Redeem 52.
  - Diana: Lv 54 → **Lv 61** (Drill Camp instructor), **9 escorts**, 12,470 troop capacity. Helmet swapped from
    Windbreaker Faceplate Rare +18 (24,630) to **Berserker's Faceplate Epic** (22,500; +9.00% Archer Lethality, total
    21.78%); gear power 111,285. Power 489,183 → 502,893: −2,130 from the swap and +15,840 presumably from the levels
    (inferred). Stats 1,626 / 1,577 / 9,886, escort 541 / 525 / 3,295. Shards 54 → 55 / 100, Redeem 52.
  - All three show 10 Epic Expedition Manuals in stock, as Quinn's screen did.
  - `data/manual.json`: the promotion suggestion now says Diana needs 45 of the 52 Epic Redeem shards (7 left for
    Quinn) and lists Chenko and Howard; the skill-book suggestion marks Howard's Defenders' Edge done, so Gordon's Trash
    Talk is the next Epic Conquest Books pick, and says the Conquest Book stock has not been read since.
- `hero.md`, Quinn (2026-10-27): Lv 54 → **Lv 64** (capped until Town Center 23), 9 escorts, 12,730 troop capacity. Power
  528,735 → 551,935 (+23,200) with all four gear pieces re-confirmed unchanged, so presumably the levels (inferred);
  Hero Stats 1,735 / 1,734 / 10,715, escort 576 / 577 / 3,570. Shards 30 → 53 / 100 to 4★ Tier 1; **Redeem 12 → 52**
  (Epic). Headshot shows 10 Epic Expedition Manuals in stock (26 on 25 Oct). `data/manual.json`: the promotion
  suggestion now says 46 of the 52 Epic Redeem shards can promote Diana to 4★ (the rest to Quinn); the skill-book
  suggestion uses the new manual stock.
- `hero.md`, Jabel (2026-10-27): Lv 54 → **Lv 64**, capped until Town Center 23 (the game's "Requirement: Town Center Lv.
  23"; this matches the community cap of 64 at TC 22). 9 escorts, 12,730 troop capacity. Gear: Armet and Breastplate +19
  → +25 (29,250 each; +9.50%), Gauntlets +20 → +24 (42,840; +14.04% Cavalry Health), Boots +20 → +30 (32,850; +10.20%
  Cavalry Lethality); gear power 164,190 with the widget. Power 605,610 → 653,530: +18,920 from gear and +29,000 not
  itemised (presumably the levels; inferred). Hero Stats 1,614 / 1,651 / 16,326, escort 538 / 550 / 5,442, Lethality
  +24.70%, Health +28.54%; after the gear, each stat rose by a uniform +60 / +60 / +600 (escort +20 / +20 / +200).
  Shards 2 → 21 / 40 to Tier 5, Redeem 11 → 2. `data/manual.json`: Jabel's notes and the promotion suggestion (Jabel 19
  to Tier 5; 2 Mythic Redeem left, not enough for Helga; 12 Epic to Diana) are updated.
- Redeem shards (`data/manual.json`, `hero.md`): the Redeem count on a promotion screen is a shared stock of shards per
  rarity, confirmed by the account owner on 27 Oct (`rules.redeemShards`). The promotion suggestion (priority 2) now
  uses it: 5 of the 11 Mythic shards finish Helga's 1★ Tier 1 now, the other 6 go to Jabel (Tier 5), and the 12 Epic
  shards go to Diana (4★); Inferred order, with the 1-to-1 conversion and Helga's 22 Oct count marked unverified.
  SCHEMA documents the rule.
- `profile.md` (later screens of 2026-10-27): power is **13,969,554**, the exact figure behind the Governor Profile's 13.9M
  (the game cuts the digits off rather than rounding); the 13,296,354 on the first Town Center screens was earlier the
  same day. Gems 35,666, bread 1.7M. Town Center Lv 22 and its stats, kills, stamina and Governor Gear re-confirmed.
- Governor Profile and Town Center screens of 2026-10-27 (`profile.md`): Town Center Lv 20 → **Lv 22** (both upgrades
  done; stats 735 / 1,470 / 22,064); power **13.9M** on the Governor Profile (rounded) while the Town Center screens show
  13,296,354 in the top bar (which is later is not known); kills 443,382 → 592,690; stamina 200 / 200; gems 30,166;
  bread 1.6M; citizens 32 / 32; VIP 3. Governor Gear is open: 3 / 6 equipped (Charmstone, Plain Breeches, Shortstaff,
  Uncommon, 224,400 power and +9.35% Attack / Defense for cavalry, infantry and archers); the crown, chest and ring
  slots are grey. Perks: the 6 shown re-confirmed; Governor Defense Enhancement is now +300% (was +250%). The Governor
  Name and Player ID on these screens are not stored. `data/manual.json`: Governor Gear feature Active; Jabel's
  level note says her level has not been read since the Town Center reached Lv 22 `troops.md`'s Town Center cross-check row
  matches (Level 22).
- Drill Camp page (`docs/index.html`): "older than the hero data" now follows the stale rule. It shows only when the
  reading trails the hero data by more than `staleAfterDays` (3) days, as the account owner asked on 25 Oct. README and
  SCHEMA updated.
- Skill book rule (`data/manual.json` `rules.skillBooks`, `hero.md`): each rarity has its own books (Epic heroes share
  Epic books, Mythic heroes share Mythic books), confirmed by the account owner on 25 Oct.
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
- `hero.md`, Diana (later on 2026-10-23): Windbreaker Faceplate and Leatherwear +17 → +18 (24,630 each, +8.52%) and
  Berserker's Boots +17 → +18 (36,945, +12.78% Lethality); gear power 113,415 (+2,170). Iron Constitution Lv. 3 → Lv. 4
  (skill icon; 18% stamina reduction from the earlier preview). Hero power 489,183: +2,170 from gear and +3,528 not
  itemised on screen (presumably the skill; inferred). Hero Stats 1,575 / 1,535 / 9,603, escort 524 / 511 / 3,201,
  Lethality +21.30%, Health +17.60%, each change matching the gear. Incendiary Arrows 33/50 manuals. Roster row and the
  `Be` march note now say −18% stamina.
- `profile.md` (Governor Profile, later on 2026-10-23): kills 345,632 → 443,382; stamina 100 / 200. Power shows 11.9M;
  the exact 11,942,479 is kept (the profile does not show the exact figure).
- `hero.md`, Seth (2026-10-24): promoted 3-Star Tier 3 → Tier 4 (+17,940 base power); shards 0 / 40 to Tier 5 (Redeem
  shows 1); new Tier 4 → Tier 5 preview (199,290 +18,785). Praetorian's Shroud +15 → +18 (36,945; DEF +122 / HP +918;
  escort DEF +40 / HP +306; +12.78% Infantry Health); gear power 140,445. Hero power 408,649 → 429,334, exactly the
  promotion plus the Shroud. Hero Stats 830 / 1,547 / 16,316, escort 276 / 515 / 5,438, Infantry Attack / Defense +54.31%,
  Health +24.93%; gear totals updated. Hammer Burn Lv. 4 re-confirmed; the other skills keep their dates.
- `data/manual.json`: the gear-swap move uses Seth's Shroud +18 (his gear power 140,445 → 113,265; the moved pieces are
  unchanged, so Howard's and Forrest's numbers stand). The promotion move drops Seth (now Tier 4, 40 shards to Tier 5).
- `troops.md` (2026-10-24): Brave Infantry 34,151, Cavalry 36,438, Archer 35,140; total 105,729 (+4,144; header
  105.7K/105.7K); 0 injured; queues 4/4. March capacity 79,275 (all three presets full). `Be` 9,840,959 power with
  21,269 / 22,866 / 35,140 (27 / 29 / 44%); `Att` 11,279,258 with 32,605 / 26,446 / 20,224 (41 / 33 / 26%). New
  Formation 3, Gathering (`Gat`): Seth (lead), Edwin, Amane; 28,813 / 36,438 / 14,024 (36 / 46 / 18%), 9,161,177 power.
- `lineups.md`: the preset table matches (Be and Att updated, Gat added).
- `data/manual.json`: two new suggestions under a "Marches" group. Priority 3: test Helga instead of Forrest in the `Be`
  march (Forrest's expedition skills are wood-only). Priority 4: lead gathering marches with the hero whose skill matches
  the resource (Seth iron, Edwin stone, Forrest wood, Olive bread). Both say which parts are verified and which are not;
  the Be suggestion notes its link to the priority-1 gear move (which gives Forrest Rare gear because he is in Be).
- `hero.md`, Saul (2026-10-24): Berserker's Bracers +13 → +14 (33,315; +11.94% Archer Health) and Windbreaker Leatherwear
  +10 → +15 (22,800; +8.10%); gear power 102,915 (+3,720). Positional Battler Lv. 1 → Lv. 2 (+10% squad Lethality; 12/30
  Mythic Conquest Books to Lv. 3). Hero power 326,215: +3,720 from gear, +2,250 not itemised (presumably the skill;
  inferred). Hero Stats DEF 961 / HP 7,078, escort DEF 320 / HP 2,359, Archer Health +20.04%, each change matching the
  gear. Redeem shows 11. Roster row and `data/manual.json` notes updated.
- `hero.md`, Howard (2026-10-24): promoted 3-Star Tier 4 → Tier 5 (+23,120 base power, as the 22 Oct preview said);
  shards 2 / 100 to 4-Star (Redeem shows 7); new Tier 5 → 4-Star preview (268,400 +37,360). Hero power 477,020 →
  500,140, exactly the promotion. Hero Stats 997 / 1,576 / 19,543, escort 332 / 525 / 6,514, Infantry Attack / Defense
  +89.01% (the old preview said +89.00%; the 0.01% gap is not explained), Lethality +21.86% and Health +21.79%
  re-confirmed. Level 54, 8 escorts and 11,525 troop capacity re-confirmed; gear and skills not shown, so they keep their
  dates.
- `hero.md`, Gordon (2026-10-25): promoted 3-Star Tier 4 → Tier 5 (+23,120 base power, as the 22 Oct preview said);
  shards 4 / 100 to 4-Star (Redeem shows 11); new Tier 5 → 4-Star preview (268,400 +37,360). Brigader's Battle Boots
  +13 → +17 (24,010; ATK +80 / HP +402; escort ATK +26 / HP +134; +8.38% Cavalry Lethality); gear power 91,820. Hero power
  438,560 → 464,060, exactly the promotion plus the boots. Hero Stats 1,252 / 1,522 / 12,510, escort 416 / 507 / 4,170,
  Cavalry Attack / Defense +89.01%, Lethality +16.48%, Health +16.06%, each change matching. Armet, Gauntlets and
  Breastplate re-confirmed. BBQ Feast Lv. 3 re-confirmed with 23/50 manuals; the other skills show only their badges and
  keep their dates.
- `hero.md`, Jabel (2026-10-25): promoted 3-Star Tier 3 → Tier 4 (+27,600 base power, as the 21 Oct preview said);
  shards 2 / 40 to Tier 5 (Redeem shows 11); new Tier 4 → Tier 5 preview (306,600 +28,900). Crusader's Gauntlets +11 →
  +20 (38,850; +13.20% Cavalry Health), Brigader's Armet and Breastplate +17 → +19 (25,260 each; +8.66%), Battle Boots +20
  re-confirmed; gear power 145,270 with the widget (widget not re-shown). Hero power 567,410 → 605,610, exactly the
  promotion plus the gear (+10,600). Hero Stats 1,534 / 1,576 / 15,558, escort 511 / 525 / 5,186, Cavalry Attack / Defense
  +120.71%, Lethality +22.46%, Health +26.86%, each change matching. All six skills re-read: Persistence 22/50 and
  Youthful Rage 17/50; the four Lv. 4 skills still need 4★.
- `data/manual.json`: the promotion suggestion drops Jabel (now 38 to Tier 5) and names Chenko (25 to Tier 5) as the
  closest lineup hero; Jabel's gear note is updated.
- `hero.md`, Quinn (2026-10-25): shards 1 → 30 / 100 to 4★ Tier 1 (Redeem shows 12). Power 528,735, Hero Stats, Level
  54 (Town Center 21 cap), 8 escorts, 11,525 troop capacity and the Tier 1 preview re-confirmed unchanged. All five skills
  still Lv. 3; their book counts went down (manuals 28 → 26, Conquest Books 31 → 28), recorded as shown with the cause
  marked unknown. All four gear pieces (Faceplate +17, Bracers +16, Leatherwear +17, Boots +17; 119,135) re-confirmed.
- `hero.md`, Howard (2026-10-25): shards 2 → 6 / 100 to 4★ (Redeem shows 12). Power 500,140, Hero Stats, Level 54
  (Drill Camp), 8 escorts, 11,525 troop capacity, the 4★ preview and all four gear pieces (Helm +20, Gloves +20, Shroud
  +19, Greaves +19; 127,900) re-confirmed unchanged. All five skills still Lv. 3; shared book stock 26 Epic Expedition
  Manuals and 28 Epic Conquest Books, the same as on Quinn's screens of the same day.
- `hero.md`, Diana (2026-10-25): Iron Constitution Lv. 4 is capped until 4★ (the panel shows 18% and "To upgrade: ascend
  to 4-Star"; it was recorded as in progress with the cost not shown). Redeem shows 12 (was 0). Power 489,183, shards 54 /
  100, Hero Stats, Level 54 (Town Center 21 cap), 8 escorts, 11,525 troop capacity, the 4★ preview and all four gear
  pieces (Faceplate +18, Bracers +22, Leatherwear +18, Boots +18; 113,415) re-confirmed unchanged. Other skills still Lv.
  3; shared book stock 26 Epic Expedition Manuals and 28 Epic Conquest Books.
- `hero.md`, Chenko (2026-10-25): promoted 3-Star Tier 4 → Tier 5 (+23,120 base power, as the 23 Oct preview said);
  shards 1 / 100 to 4★ (Redeem shows 12); new Tier 5 → 4★ preview (268,400 +37,360). Hero power 447,120 → 470,240, exactly
  the promotion. Hero Stats 1,256 / 1,531 / 12,570, escort 418 / 510 / 4,190, Cavalry Attack / Defense +89.01%; Lethality
  +16.90% and Health +17.04% unchanged; all four gear pieces (Armet +15, Gauntlets +20, Breastplate +16, Boots +20;
  98,000) re-confirmed on the gear screens. All five skills still Lv. 3; shared
  book stock 26 / 28. `data/manual.json`: the promotion suggestion drops Chenko and names Jabel (38 to Tier 5) as the
  closest lineup hero.
- World-map screens of 2026-10-25: `troops.md` "Beast & Terror Hunting" is now a table read from the screens: Lv 21 Lion
  (attack, 10 stamina, recommended power 3,012,128, drops) and Lv 4 Alpha Black Panther Terror (rally only, 25 stamina,
  recommended power 37,797,400, drops), confirming the owner's levels; map positions are not recorded. `profile.md`: power
  11,942,479 → 12,464,731, bread 65.4M → 96.1M, gems 24,421, VIP 3 re-confirmed. The Features note is updated.

### Removed
- The Player ID, from `README.md` (the `profile.md` description) and from `profile.md` (the "Player ID" row).
  It remains in the git history of earlier commits.
- The governor name, from `profile.md` (the "Governor Name" row, now optional for the generator),
  `troops.md`, `README.md`, the hand-written `KS_DATA` in `docs/index.html` and the design prototype.
  The dashboard header shows "Governor: Not recorded". The name remains in the git history.

### Fixed
- Governor Gear (`scripts/build_data.py`, `docs/index.html`): the generator only understood "6 / 6 Locked". It now also
  reads "3 / 6 Equipped" (`governorGear.slotsEquipped`), dates the block by its own row, and the City view shows
  "3 of 6 slots equipped". SCHEMA documented; test added.
- Overview tile dates (`scripts/build_data.py`, `docs/index.html`): Account power, Total kills, VIP, Stamina, Town
  Center and Gems took the newest date in `profile.md`'s section, so when power was read on 25 Oct, kills (read on 23
  Oct) also showed "as of 25 Oct". `governor`, `townCenter` and `resources` now carry `fieldAsOf` from each row's or
  bullet's own date (new `bullet_dates()` helper), and each tile uses it. Documented in SCHEMA; test added.
- Drill Camp slot summary (`docs/index.html`, `data/manual.json`): it said "0 open · 7 filled · 15 locked · 15 total" because
  `slotsOpen` was 0 while the page reads it as unlocked slots. `slotsOpen` is now 7 (25 Oct screen), the summary counts
  empty and locked slots from it (now "0 open · 7 filled · 8 locked · 15 total"), and SCHEMA documents the field.
- Skill book counts (`scripts/build_data.py`, `docs/index.html`, `hero.md`): the a/b on a skill's Upgrade button is the
  shared stock of that book type, not progress saved on that skill (confirmed by the account owner, 25 Oct). Skill notes
  now read "a in stock / b needed · Books · read D Mon", the "In progress" status is now "Needs books", and the hero
  drawer explains the rule (`rules.skillBooks` in `data/manual.json`). `hero.md` states the rule under the date note,
  and Quinn's falling counts are explained by it. Documented in README and SCHEMA; test updated.
- `data/manual.json`: the promotion suggestion referred to Chenko as "he"; Chenko is female, so it now says "her".
- Defense & Arena (`docs/index.html`): a power difference whose percentage rounds to zero showed a plus sign, e.g.
  "−915 (+0%)". The sign now follows the value (+ above zero, − below, none at zero), so it reads "−915 (0%)", and an
  exact match reads "0 (0%)" instead of "+0 (+0%)".
- Features page dates (`scripts/build_data.py`, `data/manual.json`): a feature can name a `section` of its source
  file and then takes that section's newest date instead of the whole file's. Set for Town Center & buildings,
  Research, Troops, Arena, Barricades, Governor Gear and Alliance. Barricades now shows 22 Oct (its last upload) instead
  of 23 Oct, and Research 22 Oct instead of 23 Oct. Test added; documented in `docs/SCHEMA.md` and `README.md`.

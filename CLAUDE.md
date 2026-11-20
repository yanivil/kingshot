# Instructions for Claude

This repository is a Kingshot (mobile game) account dashboard. The account owner sends game screens; Claude records
the values in the Markdown data files and `data/manual.json`, and `scripts/build_data.py` builds the page published at
https://yanivil.github.io/kingshot/ on every push to `main`.

## Privacy (never break these)

- Never write the **Player ID** or the **governor name** (it starts with the alliance tag) into any file, commit
  message, pull request, issue or comment. Before each commit, search the staged diff for both, as they appear on the
  Governor Profile screen; there must be no hits.
- Do not record map coordinates, other players' names or chat, or anything in a private overlay on a screenshot.
- Never paste or store tokens or passwords.
- Screenshots stay out of git: save them under `phone_shots/` (ignored by `.gitignore`) and delete them once recorded.

## Reading the game from the Android phone (adb)

The phone is an Android device connected to the owner's iMac by USB. Run these from a Claude Code session on the iMac. `scripts/phone.sh` wraps them (screenshots, taps with the
Kingshot-in-front check, crops); use it instead of a temporary copy, which a session restart can delete:

1. Check the connection: `adb devices` must list the phone as `device` (not `unauthorized`; if so, ask the owner to
   accept the "Allow USB debugging" prompt on the phone).
2. Find the game's package: `adb shell pm list packages | grep -i -e king -e century`, and ask the owner if it is not
   clear. Open it with `adb shell monkey -p <package> 1`.
3. Screenshot: `adb exec-out screencap -p > phone_shots/<name>.png`, then read the image.
4. Move between screens with `adb shell input tap <x> <y>` and `adb shell input keyevent 4` (Back). Get the screen size
   from `adb shell wm size` and pick coordinates from the latest screenshot.

**Read-only, except the owner's play tasks.** Only open screens, switch tabs, scroll and close panels. Never tap
anything that spends, upgrades, promotes, ascends, buys, redeems, trains, sends a march, joins a rally, or sends a
message, and never confirm a dialog that does, **unless the action is a task in `play_tasks.md`**: since 2026-11-18 the
owner wants Claude to play these tasks for them and repeat them when they are available ("I want you to play instead
of me"). A task is added to that file only from the owner's own words in chat, and its limits there always apply. If a
tap would do anything not listed, or the result is unclear, stop and ask the owner. Many games forbid automated input;
the owner accepted that risk.

### Phone notes (learned on 17–18 Nov)

- **Connection.** The phone is a Samsung. Its **Auto Blocker** (Settings → Security and privacy) blocks USB debugging
  and has switched itself back on before: if `adb devices` shows only the emulator, ask the owner to turn it off and
  re-enable USB debugging. The game's package is `com.run.tower.defense`.
- **The owner may be using the phone.** Before every tap, check that the game is in front
  (`adb shell dumpsys activity activities | grep topResumedActivity` must show `com.run.tower.defense`) and stop if it
  is not. Never record anything from another app; delete such a screenshot at once.
- **Owner's tasks** (the only taps beyond reading) are in `play_tasks.md`: for example, Confirm on the "Welcome back!"
  popup, the alliance-help handshake and the storehouse chest. Trying gift codes (Redeem) needs the owner's OK each time.
- **Back** on the city screen opens "Quit game?": press **Cancel**.
- **Checking every 30 seconds** (owner, 2026-11-20): run `python3 scripts/phone_watch.py watch` in the background. It
  taps the help hand itself (task 2) and stops when a rally, Mail or a full round needs Claude; after each stop, do
  that task and start it again. Samsung Game Booster's **Touch Protection** can cover the game: it darkens the screen and
  blocks touches. It is a phone setting, so ask the owner to clear it.
- **One tap at a time:** after each tap, take a screenshot and check the screen before the next tap; never chain taps
  on screens not yet seen (a chained batch pressed Share in a battle report on 2026-11-18).

Where each value is read (coordinates are for the 1440 × 3120 screen; the city map pans, so buildings are found by
screenshot):

| Data | Route | File |
| :--- | :--- | :--- |
| Power, gems, bread, citizens, VIP | City top bar | `profile.md` |
| Kills, stamina, governor gear | Avatar (top left, ~87, 212); tap each gear icon. The screen shows the governor name and Player ID, which are never recorded | `profile.md` |
| Troop counts, march queue, infirmary | Avatar → **Squad** (~546, 3001) = Troops Preview | `troops.md` |
| March presets | Troops Preview → **Formations** (Deploy); tap each tab at the top. Never press Save, Clear All, Equalize or Balance | `troops.md`, `lineups.md` |
| Gift codes | Avatar → Settings (~1239, 3001) → Gift Code. No history list | `codes.md` |
| Town Center level and stats | The "Upgrade Town Center" quest bar (~468, 2661) | `profile.md` |
| Heroes | Heroes (~381, 3042) → a hero. Tabs Stats (~265, 3042), Skills (~718, 3042), Gear (~1170, 3042); Hero Stats panel (~1232, 2777); promotion preview (~1232, 2309); next hero (~1335, 1966). Grey heroes at the end of the list are not recruited | `hero.md` |
| Drill Camp | Heroes → **Drill Camp** | `data/manual.json` |
| Arena defense, standing | The building with crowns → Arena of Glory → **Def. Lineup**. Never press Challenge (starts a battle); the attack squad has not been read | `lineups.md` |
| Guard Station | The building labelled "Guard Station" → City Defense | `lineups.md` |
| Barricades 1 and 2 | Tap the wall gate (the arch between two square towers); each Barricade is a different gate | `lineups.md` |
| Conquest stage | Conquest (~140, 3042). Never press Conquer or Claim | `profile.md` |
| Current research, queues | Side panel tab on the left edge (~37, 1395) | `profile.md` |
| Research totals | Side panel → Tech Research arrow → Academy → **Research**; the list button at the top left is the Tech Bonus Overview. Never press Finish or Speedups | `profile.md` |
| Wood, stone, iron, speedups, Hero XP | Backpack (~605, 3033) → chart button at the top right (Overview: Resources & Speedups) | `profile.md` |
| Events | Events icon at the top right (~1323, 437) → Calendar tab; Hall of Governors tab | `profile.md` |

Never press on hero screens: Upgrade, Ascend, Quick Equip, Gear Enhancement, Mastery Forging; on buildings: Upgrade,
Finish, Speedups; anywhere: Recruit, Dispatch All, Quick Deploy.

## Recording rules

- Never invent a value. Label claims **Verified** (read on a screen), **Inferred** (worked out from screens) or
  **Unverified** (from guides). Say which screen a value came from.
- A value read on a screen gets the date of that reading, as `YYYY-MM-DD` in the `Updated` column or `_(YYYY-MM-DD)_`
  after the value. Keep the old value in the note ("764,215 on 5 Nov").
- When a value changes, explain the change from what the screens show (promotion previews, gear, skill levels) and
  label any unexplained part as inferred.
- Follow the existing formats in each file; the generator parses them. After editing, run
  `python3 -m unittest scripts.test_build_data` and `python3 scripts/build_data.py`; both must pass with 0 warnings.

## Suggestions (`data/manual.json` → `recommendations`)

- Every suggestion made in chat is also added as a card. Title (`what`) at most 60 characters, `summary` at most 200;
  details go in `why`, `steps`, `evidence` and `note`.
- Formation cards give exact heroes and troop counts, never general advice.
- Remove a card when the owner has done it.
- Standing account plans to respect in every card and play task (told by the owner on 2026-11-18): **no speedups
  until 2026-12-01** (alliance request), and **no upgrades other than research until 2026-12-01** (buildings including
  Town Center 24, hero levels, skills, stars, gear); the owner finishes research first. The alliance's KvK save list
  (announcement, 2026-11-18) is in `play_tasks.md`: speedups; gems, Roulette spins, hero shards; Mithril, Widgets,
  Forgehammers; Governor Charm and Governor Gear items; Taming Marks, pet food and items. Remove a line once its date has passed or the
  owner says it no longer applies.

## Git

- Never commit to `main`. Work on `feature/<desc>` or `fix/<desc>`, open a draft pull request with the sections Title,
  Context / Why, Summary of Changes, Test Steps and Doc Impact, then mark it ready and squash-merge it.
- Keep `README.md`, `CHANGELOG.md` (`[Unreleased]`) and `docs/SCHEMA.md` up to date with every change.
- Code gets docstrings and comments that explain why.

## Replies to the owner

Short and concrete: the answer first, then the evidence. Ask one question at a time. End every reply with
`Dashboard: https://yanivil.github.io/kingshot/`.

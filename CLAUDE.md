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

The phone is an Android device connected to the owner's iMac by USB. Run these from a Claude Code session on the iMac:

1. Check the connection: `adb devices` must list the phone as `device` (not `unauthorized`; if so, ask the owner to
   accept the "Allow USB debugging" prompt on the phone).
2. Find the game's package: `adb shell pm list packages | grep -i -e king -e century`, and ask the owner if it is not
   clear. Open it with `adb shell monkey -p <package> 1`.
3. Screenshot: `adb exec-out screencap -p > phone_shots/<name>.png`, then read the image.
4. Move between screens with `adb shell input tap <x> <y>` and `adb shell input keyevent 4` (Back). Get the screen size
   from `adb shell wm size` and pick coordinates from the latest screenshot.

**Read-only.** Only open screens, switch tabs, scroll and close panels. Never tap anything that spends, upgrades,
promotes, ascends, buys, redeems, trains, sends a march, joins a rally, or sends a message, and never confirm a dialog
that does. If a tap would do any of these or the result is unclear, stop and ask the owner. Many games forbid
automated input; the owner accepted that risk only for reading screens.

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

## Git

- Never commit to `main`. Work on `feature/<desc>` or `fix/<desc>`, open a draft pull request with the sections Title,
  Context / Why, Summary of Changes, Test Steps and Doc Impact, then mark it ready and squash-merge it.
- Keep `README.md`, `CHANGELOG.md` (`[Unreleased]`) and `docs/SCHEMA.md` up to date with every change.
- Code gets docstrings and comments that explain why.

## Replies to the owner

Short and concrete: the answer first, then the evidence. Ask one question at a time. End every reply with
`Dashboard: https://yanivil.github.io/kingshot/`.

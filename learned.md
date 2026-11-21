# What Claude has learned

This file collects what Claude learned about the game, the server timeline website and the owner's phone while it read
and played Kingshot for the owner on 17–21 Nov 2026. The data values themselves live in the data files
(`profile.md`, `hero.md`, `lineups.md`, `troops.md`, `codes.md`, `data/manual.json`). This file explains how things
work and where to find them. Labels follow `CLAUDE.md`:

- **Verified:** seen on a game screen.
- **Inferred:** worked out from screens.
- **Unverified:** from the website or a guide.

Add to this file when something new is learned, and correct it when the game shows otherwise.

## 1. The server timeline website

- **Link:** https://kingshotmastery.com/tools/server-timeline?kingdom_num=2508#result. The owner asked for it to be used
  whenever possible (20 Nov).
- **How to read it:** use the built-in browser's `get_page_text`. The page needs no sign-in.
- **What it shows:** the kingdom's day, its open date and the tracked unlocks reached. It also shows the next unlock, the
  events of the next 7 days and the whole list of future unlocks with dates.
- **Where it is recorded:** the "Kingdom Opened" row and the "Server timeline" table in `profile.md`. The dashboard works out
  the server day from the open date.

### How the site counts days

- **Open date:** Kingdom 2508 opened on Sep 20, 2026 at 14:45 UTC. On 20 and 21 Nov the site showed 11 of 32 tracked unlocks reached.
- **Day count:** the site showed Day 62 on 20 Nov and Day 63 on 21 Nov (UTC). That is the days since opening plus one, so
  the opening day counts as Day 1.
  - The site's own FAQ says "Day 0" is the open date. The dashboard follows the number the site displays
    (`server_day` in `scripts/build_data.py`).
- **Two lists that disagree:** the site has a generic day list at the bottom of the page and a timeline for this kingdom.
  - For Kingdom 2508 the timeline is 7 days earlier than the generic list:

    | Unlock | Generic list | Timeline for 2508 |
    | :--- | :---: | :---: |
    | Gen 3 heroes and the Master Academy | Day 113 | Day 106 |
    | Cassia | Day 155 | Day 148 |
    | Gen 4 | Day 197 | Day 190 |
    | War Academy | Day 225 | Day 218 |
    | Gen 5 | Day 281 | Day 274 |
    | Olander and Catherine | Day 365 | Day 358 |

  - The site gives no reason for the difference (the offset is inferred by comparing the two lists).
  - Use the kingdom's timeline. Generation 2 heroes are only in the generic list, at Day 50.
- **Accuracy:** the site says fixed unlocks are accurate to within 1–2 days and that event dates can shift. Check the
  game's Event Center before spending anything.

### Timeline for Kingdom 2508 (read 21 Nov 2026, Unverified)

| Day | Date (UTC) | Unlock | The site's advice |
| :---: | :--- | :--- | :--- |
| 48–52 | 6–10 Nov 2026 | King's Castle, first Castle Battle (reached) | |
| 55 | 13 Nov 2026 | Generation 1 Pets (reached) | |
| 59–69 | 17–27 Nov 2026 | Age of Truegold begins: Truegold research needs Town Center 30 (this account is at 23) | Push Town Center 30 |
| 70–79 | 28 Nov – 7 Dec 2026 | **First Kingdom of Power (KvK)**: matchmaking to the end of the event; a matchmaking bye can delay the first battle | Save speedups, Truegold, hero shards, pet materials and gear upgrades |
| 72 | 30 Nov 2026 | Generation 2 Pets: Cheetah and Moose in the Beast Cage | Hold pet food and upgrade materials |
| 106 | 4 Jan 2027 | Generation 3 Heroes and Pets (Lion, Grizzly Bear; the Lion makes Truegold and Forgehammers); Master Academy with Valora, Pan and Roman | Stockpile gems and pet food |
| 148 | 15 Feb 2027 | Truegold Level 5 and the Truegold Crucible; Cassia (4th Master) | |
| 190 | 29 Mar 2027 | Generation 4 Heroes and Pets (Giant Rhino, Mighty Bison); Wilson and Guinevere | Save gems a few weeks ahead |
| 218 | 26 Apr 2027 | War Academy (needs Town Center 30; T11 troop research) | Town Center 30 ready |
| 274 | 21 Jun 2027 | Generation 5 Heroes and Pets (Great Moose, Alpha Black Panther); Aena and Isnor | |
| 316 | 2 Aug 2027 | Truegold Level 8 and Tempered Truegold | |
| 358 | 13 Sep 2027 | Generation 6 Heroes and Pets (Regal White Lion, Ironclad War Elephant); Olander and Catherine | |
| 442 | 6 Dec 2027 | Generation 7 Heroes and the Ironclad War Bear | |
| 484 | 17 Jan 2028 | Advanced Truegold Research | |
| 533 | 5 Mar 2028 | Generation 8 Heroes (Diego, Liz, Luna) | |
| 617 | 28 May 2028 | Generation 9 Heroes; Governor Gear Infusion | |
| 652 | 3 Jul 2028 | Truegold Level 9–10 | |

The site's "next 7 days" list on 21 Nov included:

- Alliance Championship and Hall of Governors, both ending on 22 Nov.
- Hero Rally, ending on 29 Nov.
- All Out on 20–21 Nov, and again on 27–28 Nov.
- Alliance Championship again, 23–29 Nov.
- Sanctuary Battle, 24–27 Nov.
- Desert Trial, 25–27 Nov.

Viking Vengeance (24–26 Nov) and "Defeat nearby beasts" (24–25 Nov) were in the 20 Nov list but not in the 21 Nov one.

The site has other tools that have not been used yet: an Event Calendar (Bear Hunt, the Mystic Trial rotation and more), a VIP calculator and a Hero
Ascension calculator.

## 2. Game rules seen on the screens

### Heroes

- **Level cap:** a hero's level is capped by the Town Center. At Town Center 23 the cap is Lv 69: Jabel's screen says her
  next level needs Town Center 24. Community tables give Lv 74 at Town Center 24 (Unverified; see `data/manual.json`
  rules).
- **Drill Camp:**
  - Heroes in a Drill Camp slot auto-level to the lowest of the five instructors (the "Level Minimum").
  - Their own screen says "You cannot level up a hero within a Drill Camp!", so Hero XP only matters for the instructors and
    the heroes outside the camp.
  - Slot 10 needs Town Center 25.
- **Shared stocks:** skill books and Redeem shards are one shared stock per rarity (Epic, Mythic, Rare).
- **Skill caps:** a skill's level is capped at the hero's stars plus one. Lv 5 needs 4 stars (guide).

### Marches and presets

- **March size:** a preset's march size is a base plus its heroes' Troop Capacity.
  - The base was 56,600 on 20 Nov. It rose by 1,000 when the research total Troops Deployment Capacity went from +7,100 to
    +8,100 (inferred; the numbers match exactly).
  - The gathering presets send 55% of their capacity (61% for `Bre`).
- **One march per hero:** a hero can be in only one march at a time (community rule). `Ter` and `Att` share Jabel and
  Howard but take turns: troops.md marks `Att` "Alternative to: `Ter`", so the dashboard does not count them as a
  conflict (21 Nov). With 47,795 Infantry each and 69,530 in total, they cannot both go out full anyway. Quinn in
  `Iro` and `Att` is a real clash; the card "Iron preset: Amane instead of Quinn" fixes it.

### Arena, Barricades and Guard Station

- **Arena challenges:**
  - **Challenge** opens the Challenge List.
  - With "Daily challenges: 0", its swords buttons are grey and the Squad Settings screen does not open. The attack squad can then
    be read from a replay in Arena → **History**, which shows both squads.
  - With a challenge left, Squad Settings shows the squad and its power. On 21 Nov the owner sent that screen: 3,682,672,
    exactly the sum of the five heroes' powers.
  - **Fight** starts a battle. Only the owner presses it.
- **Squad power:** an Arena squad's power, attack or defense, is exactly the sum of its heroes' powers.
- **Barricades:**
  - They fight only in Rebel Invasions: "Assigned hero will fight alongside the governor in Rebel Invasion."
  - Barricade 1 is the wall gate right of the Town Center. Barricade 2 is the gate below the Arena and the Guard Station.
  - The gate by the cliff is not a Barricade.
- **Guard Station:** it defends the city. Its box "Garrisoned heroes cannot be deployed" is unticked, so its heroes can
  still march.

### Resources, rallies and other screens

- **Backpack Overview:** "In stock" is the city's storage plus the resource items in the backpack. The amount stored in
  the city is stock minus items; for bread this matched the top bar.
- **Rallies:**
  - The red skull on the city screen counts the open rallies.
  - A rally whose troops are at the maximum, or that is already marching, cannot be joined.
  - The game's "Auto-joining…" timer does not work well (owner, 20 Nov).
- **Troop losses:** between 18 and 20 Nov, Infantry fell by 1,446 while kills rose by 28,816. The loss is inferred to come
  from the rallies.
- **Alliance help hand:** it disappears within seconds of showing.
- **Hero Recruitment:**
  - The building is the golden one with a red carpet.
  - A white key bubble above it means keys are waiting. The keys show at the top of the screen: silver for Advanced, gold for Epic.
  - On 20 Nov, 2 silver keys gave "Recruit 2 times".
- **Mail:** inside an opened battle report, the spot of **Read & Claim All** is the **Share** button.
- **Alliance tech:** the tech with the thumbs-up changes place. On 20 Nov it was at (374, 765), not (374, 850).
- **Gift codes:**
  - Avatar → Settings → Gift Code. The screen keeps no history.
  - An expired code says "Cannot be redeemed outside of redemption period!" (HELLOWORLD25, 20 Nov).
- **Quit game:** Back on the city screen opens "Quit game?". Press **Cancel**.

## 3. Playing on the phone

Taps are in the 1000-px-high preview frame used by `scripts/phone.sh` (multiply by 3.12 for the 1440 × 3120 screen).
Take one tap at a time and look at the screen before the next one.

### Taps that work

| Action | Taps |
| :--- | :--- |
| Join a rally (task 12) | Skull (≈ 421, 372) → War → Rally tab → green **+** on the rally card (≈ 410, 281) → the march screen opens with `Ter` loaded → **Deploy** (≈ 351, 957) |
| Alliance help (task 2) | The hand (≈ 340, 899), straight after the screenshot that shows it |
| Mail (task 11) | Envelope (≈ 421, 848; at y 890 the tap hits the chat bar). The X at the top right (≈ 434, 57) closes Mail and the chat |
| Heal (task 4) | The green **+** above the infirmary → **Heal**. Never **Finish** |
| Arena attack squad | Arena → History → a replay (when the daily challenges are 0) |

### The 30-second watcher

- **Running it:** `python3 scripts/phone_watch.py watch` runs in the background. It taps the help hand itself, then stops
  with an event:
  - `rally`, `mail`, `periodic` (after 10 minutes), `gone`, `dark` or `check`;
  - Claude handles the event and starts the watcher again.
  - `--quiet-rally N` ignores a rally already found full for N seconds.
  - Help taps are logged in `phone_shots/watch.log`.
- **Thresholds**, measured on real screens on 20 Nov (`stats` prints the current values):

  | Icon | Shown | Not shown |
  | :--- | :--- | :--- |
  | Rally skull | 0.149 red, 0.108 white | 0, 0 |
  | Help hand | 0.111 green, 0.187 white, 0.130 peach | 0, 0.029, 0 |
  | Mail count | 0.04 red | 0 |
  | World button (city screen) | over 0.07 green | |

- **Stopping it:** stopping it with `pkill` reports exit code 144. This is expected.
- **Reading the screen:** `adb exec-out screencap` without `-p` gives a 16-byte header and then raw RGBA. No image library is needed.

### Phone problems and their fixes

- **Samsung Auto Blocker:** it switches USB debugging off. The owner turns it off while Claude plays, and back on afterwards.
- **Game Booster's Touch Protection:** it darkens the game and blocks touches. Only the owner can clear it. The watcher
  reports it as `dark`.
- **Lost connection:** the phone can drop off `adb`. The owner reconnects it.

### Mistakes not to repeat

- **18 Nov, chained taps:** a chained batch of taps in Mail pressed **Share** in a battle report.
- **20 Nov, late taps:**
  - A late tap on the help hand opened the alliance chat. It was closed with the X and nothing was typed.
  - A Mail tap at y 890 opened the alliance chat.
- **Wrong buildings:**
  - The Hero Recruitment building was taken for the Arena. Back was pressed and nothing was recruited.
  - The gate by the cliff was taken for a Barricade.
- **Wrong icon:** the key bubble was taken for a hammer (an upgrade). The owner pointed it out (20 Nov).

## 4. How the owner wants Claude to work

- **What to play:** only the tasks in `play_tasks.md`, added from the owner's own words.
  - Help and join rallies first, at once (20 Nov).
  - Join with `Ter`; if its heroes are busy, join with what is free.
- **When to play:** check every 30 seconds with the watcher (20 Nov). When the owner says "when done, stop playing"
  (20 Nov), finish the current task and stop the watcher.
- **Merging:** split data updates into small chunks and merge each one (20 Nov).
- **Gift codes:** trying a gift code needs the owner's OK each time.
- **Server age and events:** use the server timeline link above.
- **Standing plans:**
  - No speedups until 1 Dec (alliance request).
  - No upgrades other than research until 1 Dec.
  - Keep everything on the alliance's KvK save list (see `play_tasks.md`).
  - The first KvK (28 Nov – 7 Dec, Unverified) starts before 1 Dec. The suggestion card "First KvK 28 Nov – 7 Dec" asks the
    owner to check with the alliance.

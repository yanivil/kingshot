# Play tasks

Tasks Claude does in the game for the account owner, on the Android phone (see `CLAUDE.md`, "Reading the game from the
Android phone"), with `scripts/phone.sh`. Since 2026-11-18 the owner wants Claude to play these for them and repeat each one whenever it is
available. A task is added, changed or removed here only from the owner's own words in chat; the date says when.

## Limits (always apply)

- Never spend real money: no Shop, Deals, packs, top-ups or anything with a price in a currency.
- Never spend gems unless a task below says so.
- **No speedups until 2026-12-01** (alliance request, told by the owner on 2026-11-18).
- **Save for KvK** (alliance announcement "KVK: WHAT TO SAVE", read on 2026-11-18): 1. all speedups; 2. gems, Roulette
  spins, hero shards; 3. Mithril, Widgets, Forgehammers; 4. Governor Charm and Governor Gear items; 5. Taming Marks, pet
  food and items. No task uses any of these.
- **No upgrades other than research until 2026-12-01** (buildings including Town Center 24, hero levels, skills,
  stars, gear; told by the owner on 2026-11-18).
- Never write in chat or mail, start a rally, attack, scout, teleport, or change alliance, unless a task says so.
  Joining an alliance rally is task 12.
- Before every tap, check that Kingshot is the app in front; stop if it is not (the owner may be using the phone).
- If a tap would do something not listed here, or its result is unclear, stop and ask the owner.
- **One tap at a time:** tap, take a screenshot, check the screen is the one expected, then the next tap. Never chain
  taps on screens not yet seen. On 2026-11-18 a chained batch in Mail opened an old battle report, where the spot of
  "Read & Claim All" is the **Share** button, and Share was pressed 2–3 times (the share window was closed without
  choosing anyone).

## Tasks

| # | Task | When available | How | Added |
| :---: | :--- | :--- | :--- | :---: |
| 1 | Close the "Welcome back!" popup | On opening the game | Press the green **Confirm** button (not the X) | 2026-11-18 |
| 2 | Alliance help | Every time the help icon shows: a hand / handshake bubble at the bottom right, above the Alliance button (about 339, 896 in the 1000-px frame) | Press it once ("press on it each time you are seeing it", owner, 18 Nov). `scripts/phone_watch.py` (checking every 30 seconds, owner, 20 Nov) taps it by itself and checks the city screen afterwards. Otherwise tap it straight after the screenshot that shows it: it disappears within seconds, and on 20 Nov a late tap hit the chat bar under it and opened the alliance chat (closed with the X; nothing typed). If you see one, help at once, before other tasks (owner, 20 Nov) | 2026-11-18 |
| 3 | Storehouse chest | When a chest bubble shows above the storehouse (the next one came after 10 minutes, then after about an hour, on 18 Nov) | Press the chest; the reward screen ("Next Chest Ready In") closes with a tap | 2026-11-18 |
| 4 | Heal injured soldiers | When a green **+** bubble shows above the infirmary | Press the +, then the teal **Heal** button (costs resources; 46 injured took 1:26 on 18 Nov). Never press **Finish** (costs gems) or use speedups | 2026-11-18 |
| 5 | Ask the alliance for help | When a hand / handshake bubble shows above a building that is working (healing, training, research) | Press it once; the game says "Ally help request sent!" | 2026-11-18 |
| 6 | Alliance loot chests | When the Alliance button or its Chests tile shows a red count | Alliance (bottom bar) → **Chests** → Loot Chest tab → **Claim All** (161 / 500 of the daily limit on 18 Nov) | 2026-11-18 |
| 7 | Big alliance box | Only when the big box at the top of the Chests screen is shining (glow and a red count) | Press the box; tap to close the rewards | 2026-11-18 |
| 8 | Alliance gifts | When the Alliance Gift tab has gifts not yet claimed | Alliance → Chests → **Alliance Gift** tab: claim each gift **one by one**, never Claim All (owner, 18 Nov). Never press **Go** (it opens a purchase) or tick "Send Anonymous Alliance Gift" | 2026-11-18 |
| 9 | Alliance tech contributions | When the Contribute (iron) attempts are not used up: up to 25, one more every few minutes | Alliance → **Tech** → the tech with a **thumbs-up** → the teal **Contribute** until the attempts reach 0; it costs a resource (iron, wood, stone or bread: any is fine; 1,250 iron on 18 Nov). **Never the orange Contribute** (10 gems). With no thumbs-up anywhere: if fewer than 20 attempts are waiting, wait for later; with 20 or more, choose any tech and contribute (owner, 18 Nov). 18 attempts on Archer Lethality I on 18 Nov | 2026-11-18 |
| 10 | Alliance Triumph chest | When a chest on the Activity Triumph screen is shining | Alliance → **Triumph** (bottom) → press a chest only if it shines (the weekly chest or the Personal Activity Triumph Chest); otherwise go back (owner, 18 Nov). Neither shone on 18 Nov: the personal chest (bottom) was open at 1,400 / 800 and a tap only showed its contents, so it had been claimed that day | 2026-11-18 |
| 11 | Mail | When the envelope (bottom right) shows a red count | Envelope → for each tab with a red count (Wars, Alliance, System, Reports, Starred): open the tab, check it is the list (not an open mail), press **Read & Claim All**, tap to close the rewards. Never press **Delete Read**, and inside an open mail never press Delete, Star or **Share** (owner, 18 Nov) | 2026-11-18 |
| 12 | Join alliance rallies | Whenever a red skull icon with a timer shows on the city screen (right side, about 421, 372 in the 1000-px frame; a number on it counts the rallies) or Alliance → **War** → Rally tab has a red count | **At once, before any other task** ("If you see a rally or help request, you immediately help and/or join the rally", owner, 20 Nov). Tap the skull: it opens War → **Rally**. For each rally that is not full and not yet marching: Join, choose the `Ter` preset, March. Do not rely on the game's "Auto-joining…" timer at the bottom of that screen ("auto join is not working well", owner, 20 Nov). A rally whose troop count is at its maximum, or that is already marching, cannot be joined. Never start a rally, never use speedups or gems on a march, and leave the **Solo** tab alone (enemy marches on members). `Ter` is the first formation, for Terror and Beasts, as the owner asked ("join with the first formation for Terror and Beasts", 20 Nov). First join on 20 Nov: a Lv. 6 Ironclad War Elephant rally, `Ter` with Jabel, Diana and Howard and 95,590 troops, by the green **+** on the rally card, then **Deploy**. If `Ter`'s heroes are busy (for example still in an earlier rally), join with what is free ("If there is another rally and Ter is not available, then use what you have", owner, 20 Nov) | 2026-11-20 |

More tasks follow as the owner names them.

#!/usr/bin/env python3
"""Watch the Kingshot city screen on the owner's phone and report what needs a play task.

Why it exists: the owner wants Claude to check the game every 30 seconds ("keep playing - check each 30 seconds",
2026-11-20) and to help and join rallies at once (play_tasks.md, tasks 2 and 12). Looking at a screenshot every
30 seconds would cost a model turn each time, so this script does the looking with plain pixel tests and only
stops (which wakes Claude, who runs it in the background) when something needs Claude:

    rally     the red rally skull on the right side of the city screen (task 12)
    mail      a red count on the envelope (task 11)
    periodic  the time limit passed: Claude does a full round (map bubbles, alliance chests and tech)
    gone      the phone left adb (Auto Blocker or the cable)
    dark      Samsung Game Booster's "Touch Protection" window covers the game and blocks touches
    check     the automatic help tap did not end on the city screen as expected

The help hand (task 2) disappears within seconds, so the script taps it itself: one tap at the hand's fixed spot,
then a new capture to check that the hand is gone and the city screen is still there; otherwise it stops with
"check". Every tap first checks that Kingshot is the app in front (the owner may be using the phone).

It reads the raw framebuffer (`adb exec-out screencap` without -p: a 16-byte header, then RGBA) so it needs no
image library. Regions are in the 1000-px-high preview frame used by scripts/phone.sh (x and y times 3.12).

Usage:
    python3 scripts/phone_watch.py watch [--every 30] [--limit 600]
    python3 scripts/phone_watch.py stats          # print the region measurements of the current screen
"""
import argparse
import datetime
import os
import struct
import subprocess
import sys
import time

PACKAGE = "com.run.tower.defense"
SCALE = 3.12
LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "phone_shots", "watch.log")

# Preview-frame boxes (x0, y0, x1, y1). The HUD moves a little when the chat bar changes height, so the boxes are
# a bit larger than the icons.
SKULL = (398, 340, 446, 400)      # rally skull, below Deals on the right
HAND = (318, 870, 362, 925)       # help hand bubble above the Alliance button
HAND_TAP = (340, 899)
MAIL = (430, 815, 452, 900)       # red count at the envelope's top right
WORLD = (400, 940, 455, 975)      # the World button's map icon: about 14% green on the city screen (20 Nov)


def serial():
    out = subprocess.run(["adb", "devices"], capture_output=True, text=True).stdout
    for line in out.splitlines()[1:]:
        parts = line.split()
        if len(parts) == 2 and parts[1] == "device" and not parts[0].startswith("emulator"):
            return parts[0]
    return None


def in_front(s):
    out = subprocess.run(["adb", "-s", s, "shell", "dumpsys", "activity", "activities"],
                         capture_output=True, text=True).stdout
    for line in out.splitlines():
        if "topResumedActivity" in line:
            return PACKAGE in line
    return False


def capture(s):
    raw = subprocess.run(["adb", "-s", s, "exec-out", "screencap"], capture_output=True).stdout
    if len(raw) < 16:
        return None
    w, h = struct.unpack("<II", raw[:8])
    return w, h, raw


def classes(img, box, step=3):
    """Share of pixels in a preview-frame box that are red, green, white or peach (the icons' colours)."""
    w, h, raw = img
    x0, y0, x1, y1 = (int(v * SCALE) for v in box)
    n = red = green = white = peach = 0
    for y in range(y0, min(y1, h), step):
        row = 16 + y * w * 4
        for x in range(x0, min(x1, w), step):
            i = row + x * 4
            r, g, b = raw[i], raw[i + 1], raw[i + 2]
            n += 1
            if r > 185 and g < 90 and b < 90:
                red += 1
            elif g > 140 and g - r > 45 and g - b > 25:
                green += 1
            elif r > 232 and g > 232 and b > 232:
                white += 1
            elif r > 215 and 150 < g < 215 and 110 < b < 185 and r - b > 50:
                peach += 1
    n = max(n, 1)
    return {"red": red / n, "green": green / n, "white": white / n, "peach": peach / n}


def in_city(img):
    """True when the bottom bar shows the World button, i.e. the city screen (not chat, mail or a menu)."""
    return classes(img, WORLD)["green"] > 0.07


def brightness(img, step=97):
    """Mean brightness (0-255) of a sparse sample of the whole screen."""
    w, h, raw = img
    total = n = 0
    for i in range(16, len(raw) - 4, 4 * step):
        total += raw[i] + raw[i + 1] + raw[i + 2]
        n += 3
    return total / max(n, 1)


def dark_screen(s):
    """True when the screen is darkened by a window above the game, such as Samsung Game Booster's "Touch
    Protection", which blocks touches (seen on 20 Nov). That is a phone setting, so the owner clears it."""
    out = subprocess.run(["adb", "-s", s, "shell", "dumpsys", "window", "windows"], capture_output=True, text=True).stdout
    return "TouchProtection" in out


def detect(img):
    sk, hd, ml = classes(img, SKULL), classes(img, HAND), classes(img, MAIL)
    found = {
        # Skull shown (night, 20 Nov): 0.149 red / 0.108 white; no skull: 0 / 0. The first 0.25 missed it.
        "rally": sk["red"] > 0.07 and sk["white"] > 0.04,
        # Measured on 20 Nov: hand shown 0.111 green / 0.187 white / 0.130 peach, gone 0 / 0.029 / 0;
        # envelope with a count 0.04 red, without 0.0.
        "help": hd["green"] > 0.06 and hd["white"] > 0.10 and hd["peach"] > 0.06,
        "mail": ml["red"] > 0.02,
    }
    return found, {"skull": sk, "hand": hd, "mail": ml}


def log(msg):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a") as f:
        f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {msg}\n")


def tap(s, x, y):
    subprocess.run(["adb", "-s", s, "shell", "input", "tap", str(int(x * SCALE)), str(int(y * SCALE))])


def watch(every, limit, quiet_rally=0):
    """Loop until something needs Claude. quiet_rally: seconds from the start in which a rally skull is ignored, for
    a rally Claude has already found full or marching (it stays on screen until it leaves, about 2-5 minutes)."""
    start = time.time()
    while True:
        s = serial()
        if not s:
            print("EVENT gone: the phone is not on adb")
            return
        if in_front(s) and dark_screen(s):
            print("EVENT dark: Game Booster Touch Protection covers the game; the owner must clear it")
            return
        if in_front(s):
            img = capture(s)
            if img and in_city(img):
                found, m = detect(img)
                if found["rally"] and time.time() - start > quiet_rally:
                    print("EVENT rally", m["skull"])
                    return
                if found["help"]:
                    tap(s, *HAND_TAP)
                    time.sleep(1.5)
                    after = capture(s)
                    still, _ = detect(after) if after else ({"help": True}, None)
                    log("help hand tapped" + (" (still shown after the tap)" if still["help"] else ""))
                    if still["help"] or not in_front(s) or not (after and in_city(after)):
                        print("EVENT check: after the help tap the city screen is not as expected")
                        return
                if found["mail"]:
                    print("EVENT mail", m["mail"])
                    return
        if time.time() - start > limit:
            print("EVENT periodic")
            return
        time.sleep(every)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("mode", choices=["watch", "stats"])
    ap.add_argument("--every", type=float, default=30)
    ap.add_argument("--limit", type=float, default=600)
    ap.add_argument("--quiet-rally", type=float, default=0,
                    help="ignore the rally skull for this many seconds (a rally already found full)")
    a = ap.parse_args()
    # The thresholds were measured on 20 Nov on screens with and without each icon. "stats" prints the measurements so they can be checked again.
    if a.mode == "stats":
        s = serial()
        if not s:
            sys.exit("no phone")
        found, m = detect(capture(s))
        img = capture(s)
        print("front:", in_front(s), "touch protection:", dark_screen(s), "brightness:", round(brightness(img)))
        for k, v in m.items():
            print(k, {c: round(x, 3) for c, x in v.items()})
        print("city:", in_city(capture(s)), "found:", found)
    else:
        watch(a.every, a.limit, a.quiet_rally)


if __name__ == "__main__":
    main()

#!/bin/zsh
# Phone helper for reading and playing Kingshot on the owner's Android phone over adb (macOS: uses `sips`).
#
# Why it lives in the repo: a copy in a session's temporary folder was lost when the session restarted, so every
# session (and every restart) uses this one. See CLAUDE.md, "Reading the game from the Android phone", and
# play_tasks.md for what may be tapped.
#
# Coordinates are given in a 1000-px-high "preview" frame and scaled by 3.12 to the phone's 1440 x 3120 screen, so a
# point read from a screenshot shrunk to 1000 px can be tapped directly.
#
# Usage:
#   scripts/phone.sh shot NAME [HEIGHT]        screenshot -> phone_shots/NAME.png and NAME_s.png (HEIGHT px high)
#   scripts/phone.sh tap X Y [WAIT]            tap, then wait WAIT seconds (default 1.5)
#   scripts/phone.sh tapshot X Y NAME [WAIT]   tap, wait, screenshot
#   scripts/phone.sh swipe X1 Y1 X2 Y2 [MS]    swipe (pans the city map)
#   scripts/phone.sh back [WAIT]               Android Back key
#   scripts/phone.sh crop NAME X Y W H         full-resolution crop of phone_shots/NAME.png -> NAME_crop.png
#   scripts/phone.sh front                     exit 0 if Kingshot is the app in front, 3 if not
#
# Every input command first checks that Kingshot is in front and stops (exit 3) if not: the owner may be using the
# phone, and a tap must never land in another app. Screenshots go to phone_shots/, which .gitignore keeps out of git;
# delete them once their values are recorded.

SERIAL=${KS_PHONE_SERIAL:-$(adb devices | awk '$2=="device" && $1 !~ /^emulator/ {print $1; exit}')}
PACKAGE=com.run.tower.defense
SHOTS=${0:A:h:h}/phone_shots
mkdir -p "$SHOTS"

[[ -z $SERIAL ]] && { echo "No phone found: check 'adb devices' (Samsung Auto Blocker off, USB debugging on)"; exit 2; }

# Scale a preview-frame coordinate to screen pixels.
sc() { echo $(( $1 * 312 / 100 )); }

# Save a screenshot and a copy shrunk to HEIGHT px (default 1000) for reading.
shot() {
  local h=${2:-1000}
  adb -s $SERIAL exec-out screencap -p > "$SHOTS/$1.png" && sips -Z $h "$SHOTS/$1.png" --out "$SHOTS/$1_s.png" >/dev/null && echo "$SHOTS/$1_s.png"
}

# Stop unless Kingshot is the app in front.
guard() {
  adb -s $SERIAL shell dumpsys activity activities | grep -m1 topResumedActivity | grep -q $PACKAGE \
    || { echo "STOP: Kingshot is not in front"; exit 3; }
}

case $1 in
  shot) shot $2 $3 ;;
  front) guard; echo "Kingshot is in front" ;;
  tap) guard; adb -s $SERIAL shell input tap $(sc $2) $(sc $3); sleep ${4:-1.5} ;;
  tapshot) guard; adb -s $SERIAL shell input tap $(sc $2) $(sc $3); sleep ${5:-1.8}; shot $4 ;;
  swipe) guard; adb -s $SERIAL shell input swipe $(sc $2) $(sc $3) $(sc $4) $(sc $5) ${6:-400}; sleep 1.2 ;;
  back) guard; adb -s $SERIAL shell input keyevent 4; sleep ${2:-1.2} ;;
  crop) sips -c $(sc $6) $(sc $5) --cropOffset $(sc $4) $(sc $3) "$SHOTS/$2.png" --out "$SHOTS/$2_crop.png" >/dev/null \
          && echo "$SHOTS/$2_crop.png" ;;
  *) sed -n '2,24p' "$0"; exit 1 ;;
esac

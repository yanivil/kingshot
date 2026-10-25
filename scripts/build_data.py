#!/usr/bin/env python3
"""Build the dashboard's KS_DATA object from the account Markdown files.

The dashboard (docs/index.html) renders everything from one JSON object,
KS_DATA, stored between the lines ``/* KS_DATA:BEGIN */`` and
``/* KS_DATA:END */``. This script:

1. parses profile.md, hero.md, troops.md, lineups.md and codes.md
   (each carries an ``as_of:`` date in YAML front matter);
2. merges in data/manual.json, the hand-edited file for content that is a
   judgment or a community game rule rather than data read in the game
   (recommendations, data-health notes, rules, features, Drill Camp, ...);
3. writes a copy of docs/index.html with the generated KS_DATA into an
   output folder (default: build/). The repository copy is never modified.

Rules (agreed before this script was written, see docs/SCHEMA.md):

* A value that is not in the files becomes ``null``. Nothing is invented.
* Rows are found by their exact bold label (e.g. ``Overall Account Power``). A renamed
  label turns the field into ``null`` and prints a warning.
* data/manual.json may only fill fields the parser left empty; setting a field
  the .md files already provide stops the build.
* If profile.md has a "Player ID" row, it is read only to make sure the ID
  never reaches the output. (The row is optional and currently absent.)

Usage::

    python3 scripts/build_data.py                  # writes build/index.html
    python3 scripts/build_data.py --out site       # another output folder
    python3 scripts/build_data.py --json ks.json   # also save KS_DATA as JSON

Exit status: 0 on success (warnings go to stderr), 1 on a build error.
Only the Python 3 standard library is used.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Constants
# Why: every file name, label and marker the parser depends on lives here, so
# a change to the Markdown layout is a one-line change in one place.
# ---------------------------------------------------------------------------

SCHEMA_VERSION = 1
SOURCE_FILES = ("profile.md", "hero.md", "troops.md", "lineups.md", "codes.md")
MANUAL_FILE = Path("data") / "manual.json"
TEMPLATE_FILE = Path("docs") / "index.html"

# Anchored to whole lines: the page's header comment mentions both markers on
# one line, and that comment must not be mistaken for the data block.
MARKER_RE = re.compile(r"^/\* KS_DATA:BEGIN \*/$.*?^/\* KS_DATA:END \*/$", re.S | re.M)

# Top-level keys in the order docs/SCHEMA.md lists them; the output keeps it.
TOP_LEVEL_KEYS = (
    "meta", "governor", "townCenter", "resources", "governorGear", "army",
    "rules", "heroes", "drillCamp", "lineups", "recommendations", "features",
    "dataHealth", "codes",
)

# hero.md slot labels -> the names the dashboard already uses.
SLOT_NAMES = {"Helmet": "Helmet", "Gauntlets": "Gloves", "Armor": "Chest", "Boots": "Boots"}

# troops.md branch / unit words -> (march key, display name). "Marksmen" and
# "Archer" both mean the archer class; the page shows it as "Archers".
CLASS_WORDS = (
    ("Infantry", "inf", "Infantry"),
    ("Cavalry", "cav", "Cavalry"),
    ("Marksmen", "arc", "Archers"),
    ("Archer", "arc", "Archers"),
)

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
BULLET_RE = re.compile(r"^\*\s+\*\*(.+?):\*\*\s*(.*?)\s*$")
AMOUNT_RE = re.compile(r"(\d[\d,]*(?:\.\d+)?)([KMB])?(?!\w)")
PAIR_RE = re.compile(r"(\d[\d,]*)\s*/\s*(\d[\d,]*)")
LEVEL_RE = re.compile(r"Lv\.\s*(\d+)")
STARS_RE = re.compile(r"(\d+)-Star\s*\((?:Tier\s*|T)(\d+)\)")
SHARDS_RE = re.compile(r"Shards:\s*(\d[\d,]*)\s*/\s*(\d[\d,]*)\s*to\s+([^)]*)\)")
PREVIEW_RE = re.compile(r"Star Promotion Milestone Preview \(.*?➔\s*([^)]+)\)")
# "Last uploaded" stamp after a value, e.g. "**94.6M** _(2026-10-21)_". It is
# repository bookkeeping, not game data, and must never be read as a number.
UPLOAD_DATE_RE = re.compile(r"\s*_\(\d{4}-\d{2}-\d{2}\)_")
# Any ISO date in the text: the per-value upload stamps (_(YYYY-MM-DD)_ and the
# "Updated" table column). The newest one dates a section; see newest_date().
ISO_DATE_RE = re.compile(r"(?<![\d-])(\d{4}-\d{2}-\d{2})(?![\d-])")
SUFFIX = {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000}


class BuildError(Exception):
    """A structural problem that makes the output untrustworthy; the build stops."""


@dataclass
class BuildLog:
    """Collects non-fatal warnings so one run reports every problem at once.

    Attributes:
        warnings: Messages in the order they were raised.
    """

    warnings: List[str] = field(default_factory=list)

    def warn(self, source: str, message: str) -> None:
        """Record a warning.

        Args:
            source: File or area the warning is about (e.g. ``"hero.md"``).
            message: What is missing or inconsistent.

        Returns:
            None.
        """
        self.warnings.append(f"{source}: {message}")


# ---------------------------------------------------------------------------
# Markdown reading helpers
# Why: the .md files are written for people, not machines. These helpers turn
# the three shapes the files use (headings, bold-label bullets, pipe tables)
# into plain Python structures; everything else ignores Markdown entirely.
# ---------------------------------------------------------------------------


@dataclass
class Section:
    """A heading and the lines under it.

    Attributes:
        level: Heading depth (1 for ``#``, 2 for ``##``, ...).
        title: Heading text with Markdown emphasis removed.
        lines: Every line until the next heading of the same or higher level,
            so a ``##`` section includes its ``###`` subsections.
        own: Lines until the next heading of any level.
    """

    level: int
    title: str
    lines: List[str]
    own: List[str]


@dataclass
class Table:
    """A Markdown pipe table.

    Attributes:
        header: Column names with Markdown emphasis removed.
        rows: One dict per row, mapping column name to the raw cell text
            (emphasis kept, because some rules read the bold part of a cell).
    """

    header: List[str]
    rows: List[Dict[str, str]]


def strip_md(text: Optional[str]) -> str:
    """Remove bold, italic and code markers, upload-date stamps, and collapse whitespace.

    Args:
        text: Raw Markdown text; ``None`` is treated as empty.

    Returns:
        The plain text.
    """
    if not text:
        return ""
    plain = UPLOAD_DATE_RE.sub("", text).replace("**", "").replace("`", "")
    # Only *wrapped* italics are removed: "Attack * 65%" in skill text is a
    # multiplication sign with spaces around it and must stay.
    plain = re.sub(r"\*([^*\s][^*]*?)\*", r"\1", plain)
    return re.sub(r"\s+", " ", plain).strip()


def drop_parenthetical(text: str) -> str:
    """Remove every ``(...)`` group, e.g. ``"Jabel (Jable)"`` -> ``"Jabel"``.

    Args:
        text: Plain text.

    Returns:
        The text without parenthetical groups, trimmed.
    """
    return re.sub(r"\s*\([^)]*\)", "", text).strip()


def read_source(path: Path, log: BuildLog) -> Tuple[Optional[str], str]:
    """Read a source .md file and its ``as_of`` front-matter date.

    Args:
        path: File to read.
        log: Collects a warning when the date is missing or malformed.

    Returns:
        ``(as_of, body)``: the ISO date string or ``None``, and the Markdown
        body without the front matter.

    Raises:
        BuildError: If the file does not exist.
    """
    if not path.is_file():
        raise BuildError(f"{path.name}: file not found")
    text = path.read_text(encoding="utf-8")
    front: Dict[str, str] = {}
    body = text
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end == -1:
            log.warn(path.name, "front matter has no closing '---'; ignoring it")
        else:
            for line in text[4:end].splitlines():
                line = line.strip()
                # Comment lines document the field for whoever edits the file.
                if not line or line.startswith("#") or ":" not in line:
                    continue
                key, value = line.split(":", 1)
                front[key.strip()] = value.strip().strip("'\"")
            body = text[end + len("\n---\n"):]
    raw = front.get("as_of", "")
    if not raw:
        log.warn(path.name, "no as_of date in front matter; its sections will show as undated")
        return None, body
    try:
        return dt.date.fromisoformat(raw).isoformat(), body
    except ValueError:
        log.warn(path.name, f"as_of '{raw}' is not a YYYY-MM-DD date; treating it as missing")
        return None, body


def newest_date(text: str, fallback: Optional[str] = None) -> Optional[str]:
    """Return the newest valid ISO date in ``text``, or ``fallback``.

    Why: every value in the .md files carries the date it was last uploaded,
    so the newest stamp in a section says how fresh that section is. The
    front-matter ``as_of`` is only the fallback for text without stamps.

    Args:
        text: Markdown text (a section, a table row, or a whole file body).
        fallback: Date to return when the text holds no valid date.

    Returns:
        ``YYYY-MM-DD`` or ``fallback``.
    """
    found = []
    for raw in ISO_DATE_RE.findall(text):
        try:
            found.append(dt.date.fromisoformat(raw).isoformat())
        except ValueError:
            continue  # e.g. "2026-13-40" is not a date
    return max(found) if found else fallback


def section_date(sec: Optional[Section], fallback: Optional[str]) -> Optional[str]:
    """Return the newest upload date inside one section (subsections included).

    Why: one .md file can hold parts read from screens uploaded on different
    days (troop counts and march presets in troops.md; Arena squads and
    barricades in lineups.md), so each part is dated by its own stamps rather
    than by the newest stamp anywhere in the file.

    Args:
        sec: The section, or ``None`` when it was not found.
        fallback: Date to return when the section is missing or has no stamp.

    Returns:
        ``YYYY-MM-DD`` or ``fallback``.
    """
    if sec is None:
        return fallback
    return newest_date("\n".join(sec.lines), fallback)


def oldest_part_date(parts: Iterable[Optional[Dict[str, Any]]]) -> Optional[str]:
    """Return the oldest ``asOf`` among dated parts.

    Why: the "Lineups & marches" row of Data age should say how old the
    stalest lineup is, so one fresh Arena screen does not hide an old march.

    Args:
        parts: Marches, Arena squads and barricades (``None`` entries and
            parts without a date are skipped).

    Returns:
        ``YYYY-MM-DD``, or ``None`` when no part is dated.
    """
    dated = [p["asOf"] for p in parts if p and p.get("asOf")]
    return min(dated) if dated else None


def split_sections(body: str) -> List[Section]:
    """Split a Markdown body into heading sections.

    Args:
        body: Markdown text without front matter.

    Returns:
        Sections in document order.
    """
    lines = body.splitlines()
    heads: List[Tuple[int, int, str]] = []
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match:
            heads.append((index, len(match.group(1)), strip_md(match.group(2))))
    sections = []
    for pos, (start, level, title) in enumerate(heads):
        own_end = heads[pos + 1][0] if pos + 1 < len(heads) else len(lines)
        block_end = len(lines)
        for later_start, later_level, _ in heads[pos + 1:]:
            if later_level <= level:
                block_end = later_start
                break
        sections.append(Section(level, title, lines[start + 1:block_end], lines[start + 1:own_end]))
    return sections


def find_section(sections: Iterable[Section], pattern: str) -> Optional[Section]:
    """Return the first section whose title matches a regular expression.

    Args:
        sections: Sections to search.
        pattern: Regular expression searched in each title.

    Returns:
        The matching section, or ``None``.
    """
    regex = re.compile(pattern)
    return next((s for s in sections if regex.search(s.title)), None)


def find_sections(sections: Iterable[Section], pattern: str) -> List[Section]:
    """Return every section whose title matches a regular expression.

    Args:
        sections: Sections to search.
        pattern: Regular expression searched in each title.

    Returns:
        Matching sections in document order.
    """
    regex = re.compile(pattern)
    return [s for s in sections if regex.search(s.title)]


def parse_tables(lines: List[str]) -> List[Table]:
    """Find every pipe table in a list of lines.

    Args:
        lines: Markdown lines.

    Returns:
        Tables in document order. A block of ``|`` lines without a
        ``---`` separator row is not a table and is skipped.
    """
    tables: List[Table] = []
    index = 0
    while index < len(lines):
        if not lines[index].lstrip().startswith("|"):
            index += 1
            continue
        block = []
        while index < len(lines) and lines[index].lstrip().startswith("|"):
            block.append(lines[index])
            index += 1
        cells = [[c.strip() for c in row.strip().strip("|").split("|")] for row in block]
        if len(cells) < 2 or not all(re.fullmatch(r":?-{3,}:?", c) for c in cells[1]):
            continue
        header = [strip_md(c) for c in cells[0]]
        rows = []
        for row in cells[2:]:
            # Short rows are padded so a missing trailing cell reads as empty.
            row = row + [""] * (len(header) - len(row))
            rows.append(dict(zip(header, row)))
        tables.append(Table(header, rows))
    return tables


def find_table(lines: List[str], *columns: str) -> Optional[Table]:
    """Return the first table whose header has columns starting with each name.

    Args:
        lines: Markdown lines to search.
        *columns: Column-name prefixes that must all be present.

    Returns:
        The table, or ``None``.
    """
    for table in parse_tables(lines):
        if all(any(h.startswith(c) for h in table.header) for c in columns):
            return table
    return None


def cell(row: Dict[str, str], prefix: str) -> str:
    """Return the raw cell whose column name starts with ``prefix``.

    Args:
        row: A table row.
        prefix: Column-name prefix, e.g. ``"Upgrade Status"``.

    Returns:
        The raw cell text, or ``""`` if no such column exists.
    """
    for name, value in row.items():
        if name.startswith(prefix):
            return value
    return ""


def bullets(lines: List[str]) -> Dict[str, str]:
    """Read top-level ``* **Label:** value`` bullets.

    Args:
        lines: Markdown lines.

    Returns:
        Label -> raw value without its ``_(YYYY-MM-DD)_`` upload stamp.
        Indented (nested) bullets are ignored, and when a label repeats the
        first one wins.
    """
    found: Dict[str, str] = {}
    for line in lines:
        match = BULLET_RE.match(line)
        if match:
            label = strip_md(match.group(1))
            if label not in found:
                found[label] = UPLOAD_DATE_RE.sub("", match.group(2))
    return found


def bullet_dates(lines: List[str], fallback: Optional[str]) -> Dict[str, Optional[str]]:
    """Read the date of each top-level ``* **Label:** value`` bullet.

    ``bullets()`` drops the ``_(YYYY-MM-DD)_`` stamp from the value; this keeps
    it, so a tile can show the day its own value was read.

    Args:
        lines: Markdown lines.
        fallback: Date for a bullet without a stamp (usually the section date).

    Returns:
        Label -> newest ISO date in that bullet, else ``fallback``. When a
        label repeats, the first one wins (as in ``bullets()``).
    """
    found: Dict[str, Optional[str]] = {}
    for line in lines:
        match = BULLET_RE.match(line)
        if match:
            label = strip_md(match.group(1))
            if label not in found:
                found[label] = newest_date(match.group(2), fallback)
    return found


# ---------------------------------------------------------------------------
# Value parsers
# Why: the files mix exact numbers ("11,110,919"), rounded game figures
# ("94.6M"), ratios ("240 / 200") and ranks ("3-Star (Tier 3)"). Each shape is
# parsed in exactly one place so the rules stay consistent.
# ---------------------------------------------------------------------------


def parse_amount(text: Optional[str]) -> Optional[Dict[str, Any]]:
    """Parse the first number in a text, honouring K/M/B suffixes.

    ``"11,110,919 (11.1M)"`` gives the exact 11110919; ``"94.6M"`` gives
    94600000 marked as rounded, because the game showed a rounded figure.

    Args:
        text: Raw cell or bullet text.

    Returns:
        ``{"value": int, "rounded": bool}``, or ``None`` if there is no number.
    """
    plain = strip_md(text)
    # "Not recorded (…)" / "Not shown (…)" mark a missing value; a number in
    # the explanation (a date, a "+19") must not be read as the value.
    if re.match(r"\s*not\s+(recorded|shown)\b", plain, re.IGNORECASE):
        return None
    match = AMOUNT_RE.search(plain)
    if not match:
        return None
    number = Decimal(match.group(1).replace(",", ""))
    suffix = match.group(2)
    if suffix:
        return {"value": int(number * SUFFIX[suffix]), "rounded": True}
    # Edge case: a plain decimal ("30.1") is kept as a float, not truncated.
    value: Any = int(number) if number == number.to_integral_value() else float(number)
    return {"value": value, "rounded": False}


def parse_number(text: Optional[str]) -> Optional[Any]:
    """Return just the value of :func:`parse_amount`.

    Args:
        text: Raw text.

    Returns:
        The number, or ``None``.
    """
    amount = parse_amount(text)
    return amount["value"] if amount else None


def parse_pair(text: Optional[str]) -> Optional[Tuple[int, int]]:
    """Parse ``"a / b"`` into two integers.

    Args:
        text: Raw text such as ``"32 / 32"``.

    Returns:
        ``(a, b)`` or ``None``.
    """
    match = PAIR_RE.search(strip_md(text))
    if not match:
        return None
    return int(match.group(1).replace(",", "")), int(match.group(2).replace(",", ""))


def parse_stars(text: Optional[str]) -> Tuple[Optional[int], Optional[int]]:
    """Parse ``"3-Star (Tier 3)"`` or ``"3-Star (T3)"``.

    Args:
        text: Raw text.

    Returns:
        ``(stars, tier)``; both ``None`` if the pattern is absent.
    """
    match = STARS_RE.search(strip_md(text))
    if not match:
        return None, None
    return int(match.group(1)), int(match.group(2))


def parse_level(text: Optional[str]) -> Optional[int]:
    """Parse the first ``"Lv. N"`` in a text.

    Args:
        text: Raw text.

    Returns:
        The level, or ``None``.
    """
    match = LEVEL_RE.search(strip_md(text))
    return int(match.group(1)) if match else None


def step_label(text: str) -> Optional[str]:
    """Turn a promotion target into the dashboard's short label.

    Args:
        text: E.g. ``"4-Star promotion"``, ``"Tier 5 promotion"``, ``"Tier 4"``.

    Returns:
        ``"4★"``, ``"T5"``, ... or ``None`` when the text names no target
        (e.g. ``"next promotion"``).
    """
    star = re.search(r"(\d+)-Star", text)
    if star:
        return f"{star.group(1)}★"
    tier = re.search(r"\bTier\s*(\d+)", text)
    if tier:
        return f"T{tier.group(1)}"
    return None


def rarity_label(text: str) -> Optional[str]:
    """Normalise a rarity cell: ``"SSR / Mythic"`` -> ``"Mythic"``, ``"Rare (Blue)"`` -> ``"Rare"``.

    Args:
        text: Raw rarity text.

    Returns:
        The rarity name, or ``None`` if the cell is empty.
    """
    plain = drop_parenthetical(strip_md(text))
    if "/" in plain:
        plain = plain.split("/")[-1].strip()
    return plain or None


def class_key(text: str) -> Optional[Tuple[str, str]]:
    """Map a troop branch or unit name to ``(key, display name)``.

    Args:
        text: E.g. ``"Marksmen"`` or ``"Brave Archer"``.

    Returns:
        ``("arc", "Archers")`` etc., or ``None`` for an unknown class.
    """
    for word, key, name in CLASS_WORDS:
        if word in text:
            return key, name
    return None


def roman_to_int(numeral: str) -> int:
    """Convert a Roman numeral such as ``"VII"`` to an integer.

    Args:
        numeral: Upper-case Roman numeral.

    Returns:
        Its value.
    """
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
    total = 0
    for pos, char in enumerate(numeral):
        value = values[char]
        # Subtractive notation: a smaller numeral before a larger one (IV, IX).
        if pos + 1 < len(numeral) and values[numeral[pos + 1]] > value:
            total -= value
        else:
            total += value
    return total


def label_value(found: Dict[str, str], label: str, source: str, log: BuildLog) -> Optional[str]:
    """Look up a labelled value and warn when the label is missing.

    Args:
        found: Label -> raw value (from a table or bullets).
        label: Exact label text.
        source: File name for the warning.
        log: Warning collector.

    Returns:
        The raw value, or ``None``.
    """
    if label not in found:
        log.warn(source, f"label '{label}' not found; value set to null")
        return None
    return found[label]


# ---------------------------------------------------------------------------
# profile.md -> governor, townCenter, resources, governorGear
# ---------------------------------------------------------------------------


def parse_profile(body: str, as_of: Optional[str], log: BuildLog) -> Dict[str, Any]:
    """Parse the governor profile and Town Center.

    Args:
        body: profile.md without front matter.
        as_of: The file's date.
        log: Warning collector.

    Returns:
        ``{"governor", "townCenter", "resources", "governorGear", "playerId"}``.
        ``playerId`` is used only by the leak check and is never written out.
    """
    src = "profile.md"
    sections = split_sections(body)
    identity: Dict[str, str] = {}
    identity_rows: Dict[str, Dict[str, str]] = {}
    sec = find_section(sections, r"^Governor Identity")
    table = find_table(sec.lines, "Attribute", "Value") if sec else None
    if table:
        identity = {strip_md(r["Attribute"]): r["Value"] for r in table.rows}
        identity_rows = {strip_md(r["Attribute"]): r for r in table.rows}
    else:
        log.warn(src, "Governor Identity table not found")

    stamina = parse_pair(label_value(identity, "Stamina", src, log))
    gear_text = label_value(identity, "Governor Gear", src, log)
    gear_pair = parse_pair(gear_text)
    # "6 / 6 Locked" reads as 6 locked out of 6; without the word the meaning is unclear.
    if gear_pair and "Locked" not in strip_md(gear_text):
        log.warn(src, "Governor Gear value does not say 'Locked'; slot counts set to null")
        gear_pair = None
    player_id = identity.get("Player ID")

    power = parse_amount(label_value(identity, "Overall Account Power", src, log))
    governor = {
        # Optional row: the name is deliberately not stored in this public repo,
        # so its absence is expected and not a warning.
        "name": strip_md(identity.get("Governor Name")) or None,
        "kingdom": parse_number(label_value(identity, "Kingdom / Server", src, log)),
        "alliance": strip_md(label_value(identity, "Alliance", src, log)) or None,
        "vip": parse_number(label_value(identity, "VIP Level", src, log)),
        "power": power["value"] if power else None,
        # The profile screen may show only "11.4M"; the page then shows it rounded too.
        "powerRounded": power["rounded"] if power else None,
        "kills": parse_number(label_value(identity, "Total Combat Kills", src, log)),
        "stamina": {"current": stamina[0], "max": stamina[1]} if stamina else None,
        "serverDay": None,  # Not recorded in any .md file.
        "asOf": as_of,
    }

    # Per-tile dates: rows of the identity table are read on different days
    # (power from the city top bar, kills from the Governor Profile), so each
    # Overview tile gets its own row's Updated date instead of the newest one.
    def row_date(label: str) -> Optional[str]:
        """Date of one identity row (its Updated cell), else the file date."""
        row = identity_rows.get(label)
        return newest_date(" | ".join(row.values()), as_of) if row else as_of

    governor["fieldAsOf"] = {
        "power": row_date("Overall Account Power"),
        "kills": row_date("Total Combat Kills"),
        "vip": row_date("VIP Level"),
        "stamina": row_date("Stamina"),
    }

    tc_sec = find_section(sections, r"^Town Center \(TC\)")
    tc_lines = tc_sec.lines if tc_sec else []
    if not tc_sec:
        log.warn(src, "Town Center section not found")
    tc_bullets = bullets(tc_lines)
    tc_dates = bullet_dates(tc_lines, as_of)
    citizens = parse_pair(label_value(tc_bullets, "Citizens / Workforce Capacity", src, log))
    stats_table = find_table(tc_lines, "Attribute", "Base Value")
    stats = {strip_md(r["Attribute"]): r["Base Value"] for r in stats_table.rows} if stats_table else {}

    perks = None
    perk_sec = find_section(sections, r"Town Center Perks \(")
    if perk_sec:
        match = re.search(r"\((\d+)\s*/\s*(\d+) Unlocked\)", perk_sec.title)
        perk_table = find_table(perk_sec.lines, "Slot", "Status")
        if match:
            perks = {"unlocked": int(match.group(1)), "total": int(match.group(2))}
            if perk_table:
                counted = sum(1 for r in perk_table.rows if strip_md(r["Status"]) == "Unlocked")
                if counted != perks["unlocked"] or len(perk_table.rows) != perks["total"]:
                    log.warn(src, "perk heading count disagrees with the perk table; using the heading")
    else:
        log.warn(src, "Town Center Perks heading not found")

    town_center = {
        "level": parse_number(label_value(tc_bullets, "Current Level", src, log)),
        "citizens": {"current": citizens[0], "max": citizens[1]} if citizens else None,
        "attack": parse_number(label_value(stats, "Attack", src, log)),
        "defense": parse_number(label_value(stats, "Defense", src, log)),
        "health": parse_number(label_value(stats, "Health", src, log)),
        "perks": perks,
        "asOf": as_of,
        # The level bullet's own date; other bullets in the section (gems) change more often.
        "fieldAsOf": {"level": tc_dates.get("Current Level", as_of)},
    }
    resources = {
        "bread": parse_amount(label_value(tc_bullets, "Stored Food (Bread)", src, log)),
        "wood": None, "stone": None, "iron": None,  # Not recorded in any .md file.
        "gems": parse_amount(label_value(tc_bullets, "Free Gems", src, log)),
        "asOf": as_of,
        "fieldAsOf": {"bread": tc_dates.get("Stored Food (Bread)", as_of), "gems": tc_dates.get("Free Gems", as_of)},
    }
    governor_gear = {
        "slotsTotal": gear_pair[1] if gear_pair else None,
        "slotsLocked": gear_pair[0] if gear_pair else None,
        "asOf": as_of,
    }
    return {
        "governor": governor, "townCenter": town_center, "resources": resources,
        "governorGear": governor_gear, "playerId": strip_md(player_id) or None,
    }


# ---------------------------------------------------------------------------
# troops.md -> army, lineups.marches
# Why marches come from here: troops.md is the only file with per-class troop
# counts; lineups.md repeats the presets and is used as a cross-check.
# ---------------------------------------------------------------------------


def parse_march_heroes(text: str) -> List[Dict[str, Any]]:
    """Parse ``"Diana (Lv. 49, Archer Lead), Jabel (Lv. 54, Cavalry)"``.

    Args:
        text: Raw "Assigned Heroes" value.

    Returns:
        ``[{"hero": "Diana", "lead": True}, {"hero": "Jabel"}, ...]``.
    """
    heroes = []
    for match in re.finditer(r"([A-Z][\w' -]*?)\s*\(([^)]*)\)", strip_md(text)):
        entry: Dict[str, Any] = {"hero": match.group(1).strip()}
        if re.search(r"\bLead\b", match.group(2)):
            entry["lead"] = True
        heroes.append(entry)
    return heroes


def parse_troops(body: str, as_of: Optional[str], log: BuildLog) -> Dict[str, Any]:
    """Parse the troop inventory, army caps and saved march formations.

    Args:
        body: troops.md without front matter.
        as_of: The front-matter date, used for a part without upload dates.
        log: Warning collector.

    Returns:
        ``{"army": {...}, "marches": [...], "crossCheck": {...}}``.
    """
    src = "troops.md"
    sections = split_sections(body)
    tier_match = re.search(r"\*\*Tier ([IVXLC]+) \(([^)]+)\)\*\*", body)
    tier = f"T{roman_to_int(tier_match.group(1))} {tier_match.group(2)}" if tier_match else None
    if not tier_match:
        log.warn(src, "troop tier sentence ('Tier VII (Brave)') not found")

    classes, total, injured = [], None, None
    total_row: Optional[Dict[str, str]] = None
    inv_sec = find_section(sections, r"^Current Troop Inventory")
    inv = find_table(inv_sec.lines, "Branch", "Headcount") if inv_sec else None
    if inv:
        for row in inv.rows:
            branch = strip_md(row["Branch"])
            if branch.startswith("Total"):
                total_row = row
                total = parse_number(row["Headcount"])
                injured_match = re.search(r"(\d[\d,]*)\s+Injured", strip_md(row.get("Status", "")))
                injured = int(injured_match.group(1).replace(",", "")) if injured_match else None
                continue
            mapped = class_key(branch)
            if not mapped:
                log.warn(src, f"unknown troop branch '{branch}' skipped")
                continue
            pct = parse_number(cell(row, "Distribution"))
            classes.append({"key": mapped[0], "name": mapped[1], "count": parse_number(row["Headcount"]),
                            "pct": float(pct) if pct is not None else None})
    else:
        log.warn(src, "troop inventory table not found")

    caps: Dict[str, str] = {}
    caps_rows: Dict[str, Dict[str, str]] = {}
    caps_sec = find_section(sections, r"^Army Statistics")
    caps_table = find_table(caps_sec.lines, "Attribute", "Value") if caps_sec else None
    if caps_table:
        caps_rows = {strip_md(r["Attribute"]): r for r in caps_table.rows}
        caps = {name: r["Value"] for name, r in caps_rows.items()}
    queues = parse_pair(label_value(caps, "Available March Queues", src, log))
    standing = parse_number(caps.get("Total Standing Troops"))
    if total is not None and standing is not None and standing != total:
        log.warn(src, f"Total Standing Troops ({standing}) differs from inventory total ({total})")

    # The army is dated by the troop counts and caps only; the march presets
    # below carry their own dates, as they come from other screens.
    army_date = newest_date("\n".join((inv_sec.lines if inv_sec else []) + (caps_sec.lines if caps_sec else [])), as_of)

    def row_date(row: Optional[Dict[str, str]]) -> Optional[str]:
        """Date of one table row (its Updated cell), else the army date."""
        return newest_date(" | ".join(row.values()), army_date) if row else army_date

    army = {
        "total": total, "tier": tier, "injured": injured, "classes": classes,
        "marchCapacity": parse_number(label_value(caps, "Single March Capacity", src, log)),
        "queues": {"current": queues[0], "max": queues[1]} if queues else None,
        "infirmary": parse_number(label_value(caps, "Infirmary Hospital Capacity", src, log)),
        "asOf": army_date,
        # Rows of one table can be read on different days (march capacity
        # comes from the preset screens), so each tile gets its row's date.
        "fieldAsOf": {
            "total": row_date(total_row),
            "injured": row_date(total_row),
            "marchCapacity": row_date(caps_rows.get("Single March Capacity")),
            "queues": row_date(caps_rows.get("Available March Queues")),
            "infirmary": row_date(caps_rows.get("Infirmary Hospital Capacity")),
        },
    }

    marches = []
    for sec in find_sections(sections, r"^Formation \d+:"):
        head = re.search(r"^Formation \d+:\s*(.+?)\s*\(([^)]+)\)", sec.title)
        if not head:
            log.warn(src, f"formation heading '{sec.title}' not understood; skipped")
            continue
        info = bullets(sec.lines)
        troops: Dict[str, Any] = {"inf": None, "cav": None, "arc": None}
        ratio: Dict[str, Any] = {"inf": None, "cav": None, "arc": None}
        table = find_table(sec.lines, "Branch", "Deployed Count")
        for row in table.rows if table else []:
            mapped = class_key(strip_md(row["Branch"]))
            if mapped:
                troops[mapped[0]] = parse_number(row["Deployed Count"])
                ratio[mapped[0]] = parse_number(cell(row, "Troop Ratio"))
        marches.append({
            "name": head.group(2).strip(),
            "purpose": head.group(1).strip(),
            "heroes": parse_march_heroes(label_value(info, "Assigned Heroes", src, log) or ""),
            "troops": troops,
            "ratioPct": ratio,
            "power": parse_number(label_value(info, "Formation Power", src, log)),
            "asOf": section_date(sec, as_of),
        })
    if not marches:
        log.warn(src, "no saved march formations found")
    return {
        "army": army, "marches": marches,
        "crossCheck": {"power": parse_number(caps.get("Overall Account Power")),
                       "tcLevel": parse_number(caps.get("Town Center Level"))},
    }


# ---------------------------------------------------------------------------
# lineups.md -> lineups.arena, lineups.barricades (+ march cross-check)
# ---------------------------------------------------------------------------


def parse_arena(sec: Optional[Section], name: str, log: BuildLog,
                as_of: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Parse one Arena squad section.

    Args:
        sec: The squad's section, or ``None`` if it was not found.
        name: ``"attack"`` or ``"defense"``, for warnings.
        log: Warning collector.
        as_of: lineups.md's front-matter date, used when the section has no stamp.

    Returns:
        ``{"power", "front", "back", "asOf"}`` or ``None``.
    """
    src = "lineups.md"
    if not sec:
        log.warn(src, f"Arena {name} section not found")
        return None
    power_label = next((k for k in bullets(sec.lines) if k.endswith("Squad Power")), None)
    if not power_label:
        log.warn(src, f"Arena {name}: 'Squad Power' bullet not found")
    front, back = [], []
    table = find_table(sec.lines, "Grid Position", "Hero")
    for row in table.rows if table else []:
        position, hero = strip_md(row["Grid Position"]), strip_md(row["Hero"])
        if position.startswith("Frontline"):
            front.append(hero)
        elif position.startswith("Backline"):
            back.append(hero)
        else:
            log.warn(src, f"Arena {name}: position '{position}' is neither Frontline nor Backline")
    return {"power": parse_number(bullets(sec.lines).get(power_label)) if power_label else None,
            "front": front, "back": back, "asOf": section_date(sec, as_of)}


def parse_lineups(body: str, as_of: Optional[str], log: BuildLog) -> Dict[str, Any]:
    """Parse Arena squads, barricades and the march preset summary.

    Args:
        body: lineups.md without front matter.
        as_of: The front-matter date, used for a part without upload dates.
        log: Warning collector.

    Returns:
        ``{"arena", "barricades", "presets"}``; ``presets`` is only used to
        cross-check troops.md.
    """
    src = "lineups.md"
    sections = split_sections(body)
    arena = {
        "attack": parse_arena(find_section(sections, r"Arena Offensive Squad"), "attack", log, as_of),
        "defense": parse_arena(find_section(sections, r"Arena Defensive Squad"), "defense", log, as_of),
    }

    barricades = []
    for sec in find_sections(sections, r"^Barricade \d+"):
        info = bullets(sec.lines)
        status = strip_md(label_value(info, "Status", src, log))
        level = re.search(r"Level\s+(\d+)", status)
        power = parse_amount(label_value(info, "Combined Hero Power", src, log))
        table = find_table(sec.lines, "Slot", "Hero")
        barricades.append({
            "name": drop_parenthetical(sec.title),
            "level": int(level.group(1)) if level else None,
            "maxed": ("MAX" in status.upper()) if status else None,
            "power": power["value"] if power else None,
            "powerRounded": power["rounded"] if power else None,
            "heroes": [strip_md(r["Hero"]) for r in table.rows] if table else [],
            "asOf": section_date(sec, as_of),
        })
    if not barricades:
        log.warn(src, "no barricade sections found")

    presets = {}
    preset_sec = find_section(sections, r"^Saved March Deployment Presets")
    preset_table = find_table(preset_sec.lines, "Preset Name", "Tag") if preset_sec else None
    for row in preset_table.rows if preset_table else []:
        ratios = re.findall(r"(\d+)%\s*(Inf|Cav|Arc)", strip_md(row.get("Troop Allocation", "")))
        presets[strip_md(row["Tag"])] = {
            "heroes": [drop_parenthetical(strip_md(cell(row, c))) for c in ("Primary Lead", "Deputy 1", "Deputy 2")],
            "ratioPct": {k.lower(): int(v) for v, k in ratios},
            "power": parse_number(row.get("Combat Power")),
        }
    return {"arena": arena, "barricades": barricades, "presets": presets}


def cross_check_marches(marches: List[Dict[str, Any]], presets: Dict[str, Any], log: BuildLog) -> None:
    """Warn when troops.md and lineups.md describe a march preset differently.

    Args:
        marches: Marches parsed from troops.md (the source used).
        presets: Preset summary parsed from lineups.md.
        log: Warning collector.

    Returns:
        None. Nothing is changed; troops.md stays the source.
    """
    for march in marches:
        preset = presets.get(march["name"])
        if not preset:
            log.warn("lineups.md", f"march '{march['name']}' from troops.md is not in the preset table")
            continue
        names = [h["hero"] for h in march["heroes"]]
        if names != preset["heroes"]:
            log.warn("lineups.md", f"march '{march['name']}': heroes {preset['heroes']} differ from troops.md {names}")
        if preset["power"] != march["power"]:
            log.warn("lineups.md", f"march '{march['name']}': power {preset['power']} differs from troops.md {march['power']}")
        if preset["ratioPct"] and preset["ratioPct"] != march["ratioPct"]:
            log.warn("lineups.md", f"march '{march['name']}': troop ratio differs from troops.md")


# ---------------------------------------------------------------------------
# hero.md -> heroes[]
# Why two sources: the roster table is the list of heroes (and the only place
# with class and role); each "In-Depth Hero Profile" adds the detail. When
# both give a value (level, stars), the profile wins and a warning is printed.
# ---------------------------------------------------------------------------

# Month names for short dates in skill notes ("25 Oct"); a fixed list so the
# output does not depend on the machine's locale.
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def short_date(iso: str) -> str:
    """Format an ISO date as a short day-month string.

    Args:
        iso: A date such as ``"2026-10-25"``.

    Returns:
        The date as ``"25 Oct"``.

    Raises:
        ValueError: If ``iso`` is not a valid ISO date.
    """
    day = dt.date.fromisoformat(iso)
    return f"{day.day} {MONTHS[day.month - 1]}"


def parse_skill(row: Dict[str, str]) -> Dict[str, Any]:
    """Turn one skill-table row into a dashboard skill entry.

    The "a/b Books" count on an upgrade button is the player's shared stock
    of that book type (every hero using the same books draws on it), not
    progress saved on this skill, so the note says "in stock" and, when the
    row has an "Updated" date, the day it was read.

    Args:
        row: A row from a table with "Skill Name" and "Upgrade Status" columns
            (and usually an "Updated" column).

    Returns:
        ``{"name", "level"?, "status", "needs"?, "note"?, "confidence"?}``.
        ``status`` is ``capped``, ``progress``, ``upgradeable``, ``locked`` or
        ``None`` when the status text is not one of the known forms.
    """
    status_text = strip_md(cell(row, "Upgrade Status"))
    skill: Dict[str, Any] = {"name": strip_md(row["Skill Name"])}
    level = parse_level(cell(row, "Current Level"))
    if level is not None:
        skill["level"] = level
    if status_text.startswith("Capped"):
        skill["status"] = "capped"
        needs = re.search(r"Requires (\d+)-Star", status_text)
    elif status_text.startswith("Locked"):
        skill["status"] = "locked"
        needs = re.search(r"Unlocks at (\d+)-Star", status_text)
    elif status_text.startswith("In Progress"):
        needs = None
        books = re.search(r"\((\d+)\s*/\s*(\d+)\s+(.+?)(?:\s+to\b[^)]*)?\)", status_text)
        skill["status"] = "progress"
        if books:
            have, need = int(books.group(1)), int(books.group(2))
            note = f"{have} in stock / {need} needed · {books.group(3)}"
            # The stock changes whenever any hero spends or gains these books,
            # so an older reading may no longer hold; show when it was read.
            read_on = ISO_DATE_RE.search(cell(row, "Updated"))
            if read_on:
                note += f" · read {short_date(read_on.group(1))}"
            skill["note"] = note
            # Edge case: more books than the next level needs (e.g. 34/30)
            # suggests the upgrade was affordable when read, but the screen did
            # not say so, and the same stock may have gone to another hero.
            if have >= need:
                skill["status"] = "upgradeable"
                skill["confidence"] = "Inferred"
    else:
        needs = None
        skill["status"] = None
    if needs:
        skill["needs"] = f"{needs.group(1)}★"
    return skill


def parse_gear(sec: Optional[Section], hero: str, log: BuildLog) -> Optional[List[Dict[str, Any]]]:
    """Read a hero's gear slots from a gear table or, for Jabel's layout, bullets.

    Args:
        sec: The "Equipped Hero Gear" section, or ``None``.
        hero: Hero name, for warnings.
        log: Warning collector.

    Returns:
        ``[{"slot", "state", "quality"?}]`` in file order, or ``None`` if the
        hero has no gear section. ``state`` is ``"plus0"`` for a piece at +0,
        ``"empty"`` for an empty slot, otherwise the level text (``"+17"``).
    """
    if not sec:
        log.warn("hero.md", f"{hero}: no 'Equipped Hero Gear' section; gear slots set to null")
        return None
    slots = []
    table = find_table(sec.lines, "Slot", "Item Name")
    if table:
        for row in table.rows:
            label = strip_md(row["Slot"])
            item = strip_md(row["Item Name"])
            quality = strip_md(cell(row, "Rarity"))
            slot: Dict[str, Any] = {"slot": SLOT_NAMES.get(label, label)}
            if re.search(r"none equipped", item, re.I):
                slot["state"] = "empty"
            else:
                slot["state"] = gear_state(strip_md(row.get("Level", "")), hero, label, log)
                if quality and quality != "—":
                    slot["quality"] = quality
            slots.append(slot)
        return slots
    # Bullet layout: "* **Gauntlets:** **Crusader's Gauntlets (+7, Epic Purple)** — 27,540 Power".
    for label, value in bullets(sec.lines).items():
        if label not in SLOT_NAMES:
            continue  # e.g. "Exclusive Widget", read by parse_widget
        match = re.search(r"\((\+\d+)\s*,\s*(\w+)", strip_md(value))
        slot = {"slot": SLOT_NAMES[label]}
        if match:
            slot["state"] = gear_state(match.group(1), hero, label, log)
            slot["quality"] = match.group(2)
        else:
            slot["state"] = None
            log.warn("hero.md", f"{hero}: gear '{label}' level not understood")
        slots.append(slot)
    return slots or None


def gear_state(level_text: str, hero: str, label: str, log: BuildLog) -> Optional[str]:
    """Map a gear level cell to a slot state.

    Args:
        level_text: Plain text such as ``"+17"`` or ``"Base (+0)"``.
        hero: Hero name, for warnings.
        label: Slot label, for warnings.
        log: Warning collector.

    Returns:
        ``"plus0"``, ``"+N"``, or ``None`` if no level is given.
    """
    match = re.search(r"\+(\d+)", level_text)
    if not match:
        log.warn("hero.md", f"{hero}: gear '{label}' has no level ('{level_text}')")
        return None
    return "plus0" if int(match.group(1)) == 0 else f"+{match.group(1)}"


def parse_widget(info: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """Read the "Exclusive Widget" bullet.

    Args:
        info: Bullets of the hero profile.

    Returns:
        ``{"unlocked", "name", "level"}``, or ``None`` when no widget line is
        recorded (unknown, not "locked").
    """
    raw = info.get("Exclusive Widget")
    if raw is None:
        return None
    text = strip_md(raw)
    if text.startswith("Locked"):
        # "Locked — Bands of Tyre (note)": the name after the dash, if given.
        named = re.match(r"Locked\s*[—-]\s*([^(]+)", text)
        return {"unlocked": False, "name": named.group(1).strip() if named else None, "level": None}
    if text.startswith("Unlocked"):
        # "Unlocked (Purple Stag/Antler Emblem)": the brackets describe the
        # icon, they are not the widget's name.
        return {"unlocked": True, "name": None, "level": None}
    level = re.search(r"\(\+(\d+)\)", text)
    name = re.split(r"\s*\(|\s+—", text)[0].strip() or None
    return {"unlocked": True, "name": name, "level": int(level.group(1)) if level else None}


def parse_shards(info: Dict[str, str], block: List[Section]) -> Optional[Dict[str, Any]]:
    """Read shard progress and the next promotion step.

    Args:
        info: Bullets of the hero profile.
        block: Sections inside the profile (for the promotion-preview heading).

    Returns:
        ``{"have", "need", "to"}`` or ``None``. ``to`` comes from the bullet
        ("to 4-Star promotion"); when the bullet only says "next promotion",
        from the preview heading ("3-Star Tier 3 ➔ Tier 4"); else ``None``.
    """
    match = SHARDS_RE.search(strip_md(info.get("Star Tier", "")))
    if not match:
        return None
    target = step_label(match.group(3))
    if target is None:
        for sec in block:
            preview = PREVIEW_RE.search(sec.title)
            if preview:
                target = step_label(preview.group(1))
                break
    return {"have": int(match.group(1).replace(",", "")), "need": int(match.group(2).replace(",", "")), "to": target}


def parse_heroes(body: str, as_of: Optional[str], log: BuildLog) -> List[Dict[str, Any]]:
    """Parse the roster table and every hero profile.

    Args:
        body: hero.md without front matter.
        as_of: The file's date (used for every hero).
        log: Warning collector.

    Returns:
        Heroes in roster order, with every schema field present.

    Raises:
        BuildError: If the roster table is missing or empty.
    """
    src = "hero.md"
    sections = split_sections(body)
    roster_sec = find_section(sections, r"^Active Hero Roster")
    roster = find_table(roster_sec.lines, "Hero", "Rarity") if roster_sec else None
    if not roster or not roster.rows:
        raise BuildError("hero.md: 'Active Hero Roster' table not found or empty")

    profiles: Dict[str, Section] = {}
    for sec in find_sections(sections, r"^In-Depth Hero Profile:"):
        profiles[drop_parenthetical(sec.title.split(":", 1)[1].strip())] = sec

    heroes = []
    for row in roster.rows:
        name = drop_parenthetical(strip_md(row["Hero"]))
        stars, tier = parse_stars(cell(row, "Stars"))
        role = re.match(r"\s*\*\*([^*]+?):\*\*", cell(row, "Combat"))
        hero: Dict[str, Any] = {
            "name": name,
            "rarity": rarity_label(row["Rarity"]),
            "cls": strip_md(row.get("Class")) or None,
            "generation": None,
            "role": role.group(1).strip() if role else None,
            "level": parse_level(row.get("Level")),
            "stars": stars, "tier": tier,
            "shards": None, "power": None, "gearPower": None,
            "gear": {"slots": None, "note": None},
            "widget": None, "skills": None, "notes": None,
            "asOf": as_of,
        }
        profile = profiles.pop(name, None)
        # A hero is as fresh as the newest value recorded for it (roster row
        # plus its profile section); the file date is only the fallback.
        hero["asOf"] = newest_date(" ".join(row.values()) + "\n" + ("\n".join(profile.lines) if profile else ""), as_of)
        if profile is None:
            log.warn(src, f"{name}: no In-Depth Hero Profile; detail fields set to null")
            heroes.append(hero)
            continue
        info = bullets(profile.own)
        block = split_sections("\n".join(profile.lines))

        rarity_text = info.get("Rarity", "")
        generation = re.search(r"Generation\s+(\d+)", strip_md(rarity_text))
        hero["generation"] = int(generation.group(1)) if generation else None
        profile_values = {
            "rarity": rarity_label(rarity_text) if rarity_text else None,
            "level": parse_level(info.get("Current Level")),
        }
        profile_values["stars"], profile_values["tier"] = parse_stars(info.get("Star Tier"))
        for key, value in profile_values.items():
            if value is None:
                continue
            if hero[key] is not None and hero[key] != value:
                log.warn(src, f"{name}: roster {key} {hero[key]!r} differs from profile {value!r}; using the profile")
            hero[key] = value

        hero["shards"] = parse_shards(info, block)
        hero["power"] = parse_number(label_value(info, "Total Hero Power", src, log))
        hero["gearPower"] = parse_number(label_value(info, "Total Equipped Gear Power", src, log))
        gear_sec = find_section(block, r"Equipped Hero Gear")
        slots = parse_gear(gear_sec, name, log)
        hero["gear"] = {"slots": slots, "note": None}
        if slots:
            # Tells the page the list is the full set, not just the problem slots.
            hero["gear"]["slotsComplete"] = True
        widget_info = dict(info)
        if gear_sec:
            widget_info.update({k: v for k, v in bullets(gear_sec.lines).items() if k == "Exclusive Widget"})
        hero["widget"] = parse_widget(widget_info)

        skills = []
        for table in parse_tables(profile.lines):
            if any(h.startswith("Skill Name") for h in table.header) and any(h.startswith("Upgrade Status") for h in table.header):
                for skill_row in table.rows:
                    skill = parse_skill(skill_row)
                    if skill["status"] is None:
                        log.warn(src, f"{name}: skill '{skill['name']}' status not understood")
                    skills.append(skill)
        hero["skills"] = skills or None
        heroes.append(hero)

    for orphan in profiles:
        log.warn(src, f"profile for '{orphan}' has no row in the roster table; skipped")
    return heroes


# ---------------------------------------------------------------------------
# codes.md -> codes
# ---------------------------------------------------------------------------


def parse_code_rows(table: Optional[Table], area: str, log: BuildLog) -> List[Dict[str, Any]]:
    """Read ``| [x] | `CODE` | ...`` rows.

    Args:
        table: The codes table, or ``None``.
        area: ``"active"`` or ``"expired"``, for warnings.
        log: Warning collector.

    Returns:
        ``[{"code", "redeemed"}]``; ``redeemed`` is ``None`` when the box is
        neither ``[ ]`` nor ``[x]``.
    """
    if not table:
        log.warn("codes.md", f"{area} codes table not found")
        return []
    rows = []
    for row in table.rows:
        box = strip_md(cell(row, "Redeemed")).lower()
        redeemed = True if box == "[x]" else False if box == "[ ]" else None
        if redeemed is None:
            log.warn("codes.md", f"{area} code '{strip_md(cell(row, 'Gift Code'))}': checkbox '{box}' not understood")
        rows.append({"code": strip_md(cell(row, "Gift Code")) or None, "redeemed": redeemed})
    return rows


def parse_codes(body: str, as_of: Optional[str], log: BuildLog) -> Dict[str, Any]:
    """Parse active and expired gift codes.

    Args:
        body: codes.md without front matter.
        as_of: The file's date.
        log: Warning collector.

    Returns:
        The ``codes`` object.
    """
    sections = split_sections(body)
    active_sec = find_section(sections, r"^Active Codes")
    expired_sec = find_section(sections, r"Expired Codes")
    active = parse_code_rows(find_table(active_sec.lines, "Redeemed") if active_sec else None, "active", log)
    expired = parse_code_rows(find_table(expired_sec.lines, "Redeemed") if expired_sec else None, "expired", log)
    return {"asOf": as_of, "active": active, "expired": expired, "expiredTotal": len(expired)}


# ---------------------------------------------------------------------------
# data/manual.json merge
# Why strict: one value must have one home. If manual.json could override the
# .md files, the dashboard could silently disagree with them.
# ---------------------------------------------------------------------------


def merge_manual(target: Dict[str, Any], extra: Dict[str, Any], path: str) -> None:
    """Merge hand-written values into parsed ones, refusing to overwrite data.

    Args:
        target: Parsed object, changed in place.
        extra: Values from manual.json for the same object.
        path: Dotted path for error messages.

    Returns:
        None.

    Raises:
        BuildError: If manual.json sets a field the parser already filled.
    """
    for key, value in extra.items():
        if key.startswith("_"):
            continue  # documentation keys inside manual.json
        where = f"{path}.{key}" if path else key
        current = target.get(key)
        if current is None:
            target[key] = value
        elif isinstance(current, dict) and isinstance(value, dict):
            merge_manual(current, value, where)
        else:
            raise BuildError(f"data/manual.json sets '{where}', which the .md files already provide")


def apply_manual(ks: Dict[str, Any], manual: Dict[str, Any], log: BuildLog) -> None:
    """Apply data/manual.json to the parsed KS_DATA.

    Args:
        ks: Parsed KS_DATA, changed in place.
        manual: Decoded manual.json.
        log: Warning collector.

    Returns:
        None.

    Raises:
        BuildError: On a field collision (see :func:`merge_manual`).
    """
    heroes_by_name = {h["name"]: h for h in ks["heroes"]}
    for name, extra in (manual.get("heroes") or {}).items():
        hero = heroes_by_name.get(name)
        if hero is None:
            log.warn("data/manual.json", f"hero '{name}' is not in hero.md; entry ignored")
            continue
        for key, value in extra.items():
            if key == "gearNote":
                merge_manual(hero["gear"], {"note": value}, f"heroes.{name}.gear")
            elif key == "notes":
                merge_manual(hero, {"notes": value}, f"heroes.{name}")
            else:
                log.warn("data/manual.json", f"hero '{name}': unknown key '{key}' ignored")
    for key, value in manual.items():
        if key.startswith("_") or key == "heroes":
            continue
        if key not in TOP_LEVEL_KEYS:
            log.warn("data/manual.json", f"unknown top-level key '{key}' ignored")
            continue
        if isinstance(value, dict) and isinstance(ks.get(key), dict):
            merge_manual(ks[key], value, key)
        else:
            merge_manual(ks, {key: value}, "")


# ---------------------------------------------------------------------------
# Assembly, privacy check and output
# ---------------------------------------------------------------------------


def build_ks_data(root: Path, log: BuildLog) -> Tuple[Dict[str, Any], Optional[str]]:
    """Build the complete KS_DATA object.

    Args:
        root: Repository root containing the .md files and data/manual.json.
        log: Warning collector.

    Returns:
        ``(ks_data, player_id)``: KS_DATA with top-level keys in schema order,
        and the Player ID from profile.md (only so the caller can check the
        final page for it; it is never part of KS_DATA).

    Raises:
        BuildError: On a missing file, invalid manual.json, a field collision,
            or if the Player ID would appear in the output.
    """
    dates: Dict[str, Optional[str]] = {}
    bodies: Dict[str, str] = {}
    front_dates: Dict[str, Optional[str]] = {}
    for name in SOURCE_FILES:
        front_dates[name], bodies[name] = read_source(root / name, log)
        # The newest per-value stamp wins over the front-matter date, so a
        # section's date moves forward as soon as one of its values is updated.
        dates[name] = newest_date(bodies[name], front_dates[name])

    profile = parse_profile(bodies["profile.md"], dates["profile.md"], log)
    # These two files are dated part by part; a part without stamps falls back
    # to the front-matter date, never to a newer stamp elsewhere in the file.
    troops = parse_troops(bodies["troops.md"], front_dates["troops.md"], log)
    lineups = parse_lineups(bodies["lineups.md"], front_dates["lineups.md"], log)
    heroes = parse_heroes(bodies["hero.md"], front_dates["hero.md"], log)
    codes = parse_codes(bodies["codes.md"], dates["codes.md"], log)
    cross_check_marches(troops["marches"], lineups["presets"], log)

    # Duplicated facts: profile.md is the source; troops.md only cross-checks.
    if troops["crossCheck"]["power"] not in (None, profile["governor"]["power"]):
        log.warn("troops.md", "account power differs from profile.md (profile.md is used)")
    if troops["crossCheck"]["tcLevel"] not in (None, profile["townCenter"]["level"]):
        log.warn("troops.md", "Town Center level differs from profile.md (profile.md is used)")

    known_dates = [d for d in dates.values() if d]
    # Every march, Arena squad and barricade carries its own date; the section
    # date is the stalest of them, so Data age shows the oldest lineup.
    lineup_parts = list(troops["marches"]) + list(lineups["arena"].values()) + list(lineups["barricades"])
    ks: Dict[str, Any] = {key: None for key in TOP_LEVEL_KEYS}
    ks.update({
        "meta": {"schemaVersion": SCHEMA_VERSION, "snapshotAsOf": max(known_dates) if known_dates else None},
        "governor": profile["governor"],
        "townCenter": profile["townCenter"],
        "resources": profile["resources"],
        "governorGear": profile["governorGear"],
        "army": troops["army"],
        "heroes": heroes,
        "lineups": {
            "asOf": oldest_part_date(lineup_parts),
            "marches": troops["marches"],
            "arena": lineups["arena"],
            "guardStation": None,  # Not recorded in any .md file.
            "barricades": lineups["barricades"],
        },
        "codes": codes,
    })

    manual_path = root / MANUAL_FILE
    if manual_path.is_file():
        try:
            manual = json.loads(manual_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as err:
            raise BuildError(f"data/manual.json is not valid JSON: {err}") from err
        apply_manual(ks, manual, log)
    else:
        log.warn("data/manual.json", "file not found; recommendations, rules, features and Drill Camp will be empty")

    # Fallbacks so list-shaped fields are lists even when nothing supplied them.
    for hero in ks["heroes"]:
        if hero["notes"] is None:
            hero["notes"] = []
    for key in ("recommendations", "features"):
        if ks[key] is None:
            ks[key] = []
    if ks["dataHealth"] is None:
        ks["dataHealth"] = {"conflicts": [], "missing": []}
    date_features(ks["features"], dates, bodies, log)
    check_recommendations(ks, log)

    check_player_id(json.dumps(ks, ensure_ascii=False), profile["playerId"])
    return ks, profile["playerId"]


def date_features(features: List[Dict[str, Any]], dates: Dict[str, Optional[str]],
                  bodies: Optional[Dict[str, str]] = None, log: Optional[BuildLog] = None) -> None:
    """Date each feature from the file (or the section of it) it names as its source.

    Why: features are hand-written in manual.json, so a typed ``asOf`` goes
    stale as soon as the source file gets a newer upload date. A feature whose
    ``source`` is one of the parsed .md files takes that file's newest upload
    date instead; features with no source (or another source) keep their own.
    One file can hold parts read on different days (Arena squads and
    barricades in lineups.md), so a feature may also name a ``section``
    (a heading pattern) and then takes the newest date in that section.

    Args:
        features: ``ks["features"]``, changed in place.
        dates: Newest upload date per source file name (``"profile.md"`` → ISO date or None).
        bodies: Source file bodies by name; needed only for ``section``.
        log: Warning collector; a ``section`` that matches no heading is reported.

    Returns:
        None.
    """
    for feature in features:
        src = feature.get("source") if isinstance(feature, dict) else None
        # Only a parsed file with a known date wins; anything else keeps the typed value.
        if not (src in dates and dates[src]):
            continue
        feature["asOf"] = dates[src]
        pattern = feature.get("section")
        if pattern and bodies and src in bodies:
            sec = find_section(split_sections(bodies[src]), pattern)
            if sec is None:
                # Edge case: a renamed heading keeps the file date and says so.
                if log:
                    log.warn("data/manual.json", f"feature '{feature.get('name')}': section '{pattern}' not found in {src}")
                continue
            feature["asOf"] = section_date(sec, dates[src])


def check_recommendations(ks: Dict[str, Any], log: BuildLog) -> None:
    """Warn about recommendations the page would show wrongly.

    Why: recommendations are hand-written in manual.json, so a misspelled hero
    name or a malformed ``changes`` entry would otherwise reach the page
    silently (an unclickable hero, an empty before/after row).

    Args:
        ks: KS_DATA after manual.json was applied.
        log: Warning collector.

    Returns:
        None.
    """
    known = {h["name"] for h in ks["heroes"]}
    for rec in ks["recommendations"]:
        rid = rec.get("id") or rec.get("what") or "?"
        for name in rec.get("heroes") or []:
            if name not in known:
                log.warn("data/manual.json", f"recommendation '{rid}': hero '{name}' is not in hero.md")
        steps = rec.get("steps")
        if steps is not None and not (isinstance(steps, list) and all(isinstance(s, str) for s in steps)):
            log.warn("data/manual.json", f"recommendation '{rid}': 'steps' must be a list of strings")
        for change in rec.get("changes") or []:
            # Each change needs a label and either two string lists ("before"
            # may be empty, e.g. filling empty Drill Camp slots) or "rows":
            # labelled groups such as Arena Front / Back, each with the same.
            ok = isinstance(change, dict) and isinstance(change.get("where"), str)
            if ok and "rows" in change:
                rows = change["rows"]
                ok = isinstance(rows, list) and bool(rows) and all(
                    isinstance(row, dict) and isinstance(row.get("label"), str) and _string_lists(row)
                    for row in rows)
            elif ok:
                ok = _string_lists(change)
            if not ok:
                log.warn("data/manual.json",
                         f"recommendation '{rid}': each change needs 'where' and 'before'/'after' (or 'rows')")


def _string_lists(obj: Dict[str, Any]) -> bool:
    """Return True when ``obj['before']`` and ``obj['after']`` are lists of strings.

    Args:
        obj: A change or one of its rows.

    Returns:
        Whether both keys hold lists of strings.
    """
    return all(isinstance(obj.get(k), list) and all(isinstance(x, str) for x in obj[k])
               for k in ("before", "after"))


def check_player_id(text: str, player_id: Optional[str]) -> None:
    """Stop the build if the Player ID appears in the generated text.

    Args:
        text: Serialised KS_DATA or the finished HTML page.
        player_id: The ID read from profile.md, or ``None`` if absent.

    Returns:
        None.

    Raises:
        BuildError: If the ID is present.
    """
    if player_id and player_id in text:
        raise BuildError("the Player ID would appear in the dashboard; refusing to write it")


def render_block(ks: Dict[str, Any]) -> str:
    """Serialise KS_DATA as the script block that sits between the markers.

    Args:
        ks: KS_DATA.

    Returns:
        The text from ``/* KS_DATA:BEGIN */`` to ``/* KS_DATA:END */``.
    """
    payload = json.dumps(ks, ensure_ascii=False, indent=2)
    # "</" inside a <script> could close the tag early (e.g. "</script>" in a note).
    payload = payload.replace("</", "<\\/")
    return ("/* KS_DATA:BEGIN */\n"
            "// Generated by scripts/build_data.py. Edit the .md files or data/manual.json, not this block.\n"
            f"var KS_DATA = {payload};\n"
            "/* KS_DATA:END */")


def inject(template: str, ks: Dict[str, Any]) -> str:
    """Replace the KS_DATA block in the page template.

    Args:
        template: Contents of docs/index.html.
        ks: KS_DATA.

    Returns:
        The page with the generated block.

    Raises:
        BuildError: Unless the template has exactly one marker pair.
    """
    found = MARKER_RE.findall(template)
    if len(found) != 1:
        raise BuildError(f"docs/index.html must contain exactly one KS_DATA block (found {len(found)})")
    block = render_block(ks)
    # A function replacement, so backslashes in the data are not read as regex escapes.
    return MARKER_RE.sub(lambda _match: block, template, count=1)


def report(level: str, message: str) -> None:
    """Print a warning or error, as an annotation when running in GitHub Actions.

    Args:
        level: ``"warning"`` or ``"error"``.
        message: Text to show.

    Returns:
        None.
    """
    if os.environ.get("GITHUB_ACTIONS") == "true":
        # Workflow command: shows on the run's summary page, not only in the log.
        print(f"::{level} title=build_data::{message}")
    else:
        print(f"{level}: {message}", file=sys.stderr)


def main(argv: Optional[List[str]] = None) -> int:
    """Command-line entry point.

    Args:
        argv: Arguments (defaults to ``sys.argv[1:]``).

    Returns:
        Process exit status: 0 on success, 1 on a build error.
    """
    parser = argparse.ArgumentParser(description="Build KS_DATA from the account .md files.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="repository root (default: the folder above scripts/)")
    parser.add_argument("--out", type=Path, default=Path("build"),
                        help="output folder for index.html (default: build)")
    parser.add_argument("--json", type=Path, help="also write KS_DATA as JSON to this file")
    args = parser.parse_args(argv)

    log = BuildLog()
    try:
        ks, player_id = build_ks_data(args.root, log)
        template_path = args.root / TEMPLATE_FILE
        if not template_path.is_file():
            raise BuildError("docs/index.html not found")
        page = inject(template_path.read_text(encoding="utf-8"), ks)
        # Checked again on the whole page: the template itself must not carry it either.
        check_player_id(page, player_id)
    except BuildError as err:
        for warning in log.warnings:
            report("warning", warning)
        report("error", str(err))
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "index.html").write_text(page, encoding="utf-8")
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(ks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for warning in log.warnings:
        report("warning", warning)
    print(f"wrote {args.out / 'index.html'} ({len(ks['heroes'])} heroes, {len(log.warnings)} warnings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

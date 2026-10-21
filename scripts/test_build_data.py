#!/usr/bin/env python3
"""Tests for scripts/build_data.py (standard library ``unittest`` only).

Run from the repository root::

    python3 -m unittest discover -s scripts -p "test_*.py"
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

# The script is not a package; make it importable from its own folder.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_data as bd  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Value parsers: each agreed parsing rule has a test, so a change to a rule
# shows up as a failing test rather than as a quietly different dashboard.
# ---------------------------------------------------------------------------


class ValueParserTests(unittest.TestCase):
    """Number, ratio, rank and label rules."""

    def test_exact_number_ignores_rounded_hint(self) -> None:
        """``11,110,919 (11.1M)`` keeps the exact figure."""
        self.assertEqual(bd.parse_amount("**11,110,919** (11.1M)"), {"value": 11110919, "rounded": False})

    def test_suffix_marks_rounded(self) -> None:
        """A K/M/B suffix scales the number and marks it rounded."""
        self.assertEqual(bd.parse_amount("**94.6M**"), {"value": 94600000, "rounded": True})
        self.assertEqual(bd.parse_amount("1.4M"), {"value": 1400000, "rounded": True})

    def test_plain_decimal_and_missing(self) -> None:
        """Decimals stay floats; text without a number gives None."""
        self.assertEqual(bd.parse_number("30.1%"), 30.1)
        self.assertIsNone(bd.parse_amount("Not recorded"))

    def test_pair_and_stars(self) -> None:
        """Ratios and both star notations."""
        self.assertEqual(bd.parse_pair("**240 / 200**"), (240, 200))
        self.assertEqual(bd.parse_stars("3-Star (Tier 4)"), (3, 4))
        self.assertEqual(bd.parse_stars("2-Star (T5)"), (2, 5))
        self.assertEqual(bd.parse_stars("none"), (None, None))

    def test_step_label(self) -> None:
        """Promotion targets map to 4★ / T5; vague text maps to None."""
        self.assertEqual(bd.step_label("4-Star promotion"), "4★")
        self.assertEqual(bd.step_label("Tier 5 promotion"), "T5")
        self.assertIsNone(bd.step_label("next promotion"))
        self.assertIsNone(bd.step_label("next tier advancement"))

    def test_rarity_and_names(self) -> None:
        """Rarity keeps the readable word; aliases in brackets are dropped."""
        self.assertEqual(bd.rarity_label("SSR / Mythic"), "Mythic")
        self.assertEqual(bd.rarity_label("**Rare (Blue)**"), "Rare")
        self.assertEqual(bd.drop_parenthetical("Jabel (Jable)"), "Jabel")

    def test_roman_numerals(self) -> None:
        """Troop tiers are written in Roman numerals."""
        self.assertEqual(bd.roman_to_int("VII"), 7)
        self.assertEqual(bd.roman_to_int("IX"), 9)

    def test_strip_md_keeps_multiplication_sign(self) -> None:
        """``Attack * 65%`` is not italics and must survive."""
        self.assertEqual(bd.strip_md("**Attack * 65%** and *italic*"), "Attack * 65% and italic")

    def test_upload_date_stamp_is_never_data(self) -> None:
        """A trailing ``_(YYYY-MM-DD)_`` stamp is removed before any value is read."""
        self.assertEqual(bd.rarity_label("**SSR / Mythic** (Generation 1) _(2026-10-21)_"), "Mythic")
        self.assertEqual(bd.parse_amount("**94.6M** _(2026-10-21)_"), {"value": 94600000, "rounded": True})
        # A value line holding only a stamp has no value; it must not become 2026.
        self.assertIsNone(bd.parse_amount("_(2026-10-21)_"))
        self.assertEqual(bd.bullets(["* **Free Gems:** **17,030** _(2026-10-21)_"]), {"Free Gems": "**17,030**"})


class FrontMatterTests(unittest.TestCase):
    """``as_of`` front matter handling."""

    def _read(self, text: str) -> tuple:
        """Write ``text`` to a temporary .md file and read it back.

        Args:
            text: File contents.

        Returns:
            ``(as_of, body, warnings)``.
        """
        log = bd.BuildLog()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.md"
            path.write_text(text, encoding="utf-8")
            as_of, body = bd.read_source(path, log)
        return as_of, body, log.warnings

    def test_valid_date_with_comment(self) -> None:
        """Comment lines are skipped and the body starts after the closing ---."""
        as_of, body, warnings = self._read("---\n# note\nas_of: 2026-10-21\n---\n# Title\n")
        self.assertEqual((as_of, body, warnings), ("2026-10-21", "# Title\n", []))

    def test_missing_or_bad_date_warns(self) -> None:
        """No date, or a malformed one, gives None plus a warning."""
        for text in ("# Title\n", "---\nas_of:\n---\n", "---\nas_of: 21/10/2026\n---\n"):
            as_of, _, warnings = self._read(text)
            self.assertIsNone(as_of)
            self.assertEqual(len(warnings), 1)

    def test_missing_file_is_an_error(self) -> None:
        """A missing source file stops the build."""
        with self.assertRaises(bd.BuildError):
            bd.read_source(Path("/nonexistent/profile.md"), bd.BuildLog())


class HeroRuleTests(unittest.TestCase):
    """Skill, gear and widget rules."""

    def test_skill_statuses(self) -> None:
        """Capped, in progress, affordable (Inferred) and locked skills."""
        row = lambda level, status: {"Skill Name": "**S**", "Current Level": level, "Upgrade Status & Next Rank": status}
        self.assertEqual(bd.parse_skill(row("**Lv. 4**", "**Capped at Lv. 4** (Requires 4-Star ascension for Lv. 5: x)")),
                         {"name": "S", "level": 4, "status": "capped", "needs": "4★"})
        self.assertEqual(bd.parse_skill(row("**Lv. 3**", "**In Progress** (13/50 Mythic Expedition Manuals to reach Lv. 4: y)")),
                         {"name": "S", "level": 3, "status": "progress", "note": "13/50 Mythic Expedition Manuals"})
        self.assertEqual(bd.parse_skill(row("**Lv. 2**", "**In Progress** (34/30 Epic Expedition Manuals to Lv. 3: z)")),
                         {"name": "S", "level": 2, "status": "upgradeable", "note": "34/30 Epic Expedition Manuals",
                          "confidence": "Inferred"})
        self.assertEqual(bd.parse_skill(row("**Lv. 1 (Locked)**", "**Locked** (Unlocks at 2-Star ascension; w)")),
                         {"name": "S", "level": 1, "status": "locked", "needs": "2★"})
        self.assertIsNone(bd.parse_skill(row("**Lv. 1**", "Something new"))["status"])

    def test_gear_table(self) -> None:
        """+0 pieces, empty slots and upgraded pieces from a gear table."""
        lines = [
            "| Slot | Item Name | Class Synergy | Rarity / Tier | Level | Item Power |",
            "| :--- | :--- | :---: | :---: | :---: | :--- |",
            "| **Helmet** | **A** | Archer | **Rare** | **+17** | 1 |",
            "| **Armor** | *None Equipped* | — | — | — | — |",
            "| **Gauntlets**| **B** | Archer | **Epic** | **Base (+0)** | 1 |",
        ]
        section = bd.Section(3, "3. Equipped Hero Gear", lines, lines)
        self.assertEqual(bd.parse_gear(section, "X", bd.BuildLog()), [
            {"slot": "Helmet", "state": "+17", "quality": "Rare"},
            {"slot": "Chest", "state": "empty"},
            {"slot": "Gloves", "state": "plus0", "quality": "Epic"},
        ])

    def test_gear_bullets_and_widget(self) -> None:
        """Jabel's bullet layout: gear slots plus the widget line."""
        lines = [
            "* **Exclusive Widget:** **Banner of Faith (+1)** — 30,000 Power  ",
            "* **Gauntlets:** **Crusader's Gauntlets (+7, Epic Purple)** — 27,540 Power  ",
        ]
        section = bd.Section(3, "3. Equipped Hero Gear & Widget", lines, lines)
        self.assertEqual(bd.parse_gear(section, "Jabel", bd.BuildLog()), [{"slot": "Gloves", "state": "+7", "quality": "Epic"}])
        self.assertEqual(bd.parse_widget(bd.bullets(lines)), {"unlocked": True, "name": "Banner of Faith", "level": 1})
        self.assertEqual(bd.parse_widget({"Exclusive Widget": "Unlocked (Purple Stag/Antler Emblem)"}),
                         {"unlocked": True, "name": None, "level": None})
        self.assertIsNone(bd.parse_widget({}))


class MergeAndOutputTests(unittest.TestCase):
    """manual.json merge, page injection and the Player ID guard."""

    def test_manual_fills_empty_fields_only(self) -> None:
        """manual.json may fill nulls and add keys, never replace parsed data."""
        target = {"meta": {"schemaVersion": 1}, "rules": None}
        bd.merge_manual(target, {"meta": {"staleAfterDays": 7}, "rules": {"a": 1}, "_readme": "x"}, "")
        self.assertEqual(target, {"meta": {"schemaVersion": 1, "staleAfterDays": 7}, "rules": {"a": 1}})
        with self.assertRaises(bd.BuildError):
            bd.merge_manual(target, {"meta": {"schemaVersion": 2}}, "")

    def test_inject_replaces_only_the_line_anchored_block(self) -> None:
        """The header comment naming both markers on one line is left alone."""
        template = ("<!-- change only /* KS_DATA:BEGIN */ and /* KS_DATA:END */ -->\n<script>\n"
                    "/* KS_DATA:BEGIN */\nvar KS_DATA = {};\n/* KS_DATA:END */\n</script>")
        page = bd.inject(template, {"note": "</script><b>"})
        self.assertIn("<!-- change only /* KS_DATA:BEGIN */ and /* KS_DATA:END */ -->", page)
        self.assertIn('"note": "<\\/script><b>"', page)
        self.assertEqual(page.count("var KS_DATA ="), 1)

    def test_inject_needs_exactly_one_block(self) -> None:
        """Zero or two blocks is a structural error."""
        block = "/* KS_DATA:BEGIN */\nvar KS_DATA = {};\n/* KS_DATA:END */"
        for template in ("<script></script>", block + "\n" + block):
            with self.assertRaises(bd.BuildError):
                bd.inject(template, {})

    def test_player_id_guard(self) -> None:
        """The build refuses to write text containing the Player ID."""
        bd.check_player_id("nothing here", "123456789")
        bd.check_player_id("anything", None)
        with self.assertRaises(bd.BuildError):
            bd.check_player_id('{"x": "123456789"}', "123456789")


class RepositoryTests(unittest.TestCase):
    """End-to-end run on the real files: structure and privacy, not values."""

    @classmethod
    def setUpClass(cls) -> None:
        """Build once from the repository files.

        Returns:
            None.
        """
        cls.log = bd.BuildLog()
        cls.ks, cls.player_id = bd.build_ks_data(ROOT, cls.log)

    def test_top_level_keys_in_schema_order(self) -> None:
        """Every documented top-level key is present, in order."""
        self.assertEqual(tuple(self.ks), bd.TOP_LEVEL_KEYS)

    def test_player_id_never_in_output(self) -> None:
        """Neither KS_DATA nor the finished page contains the Player ID."""
        if not self.player_id:
            # Removing the ID from profile.md is fine; there is then nothing to leak.
            self.skipTest("profile.md records no Player ID")
        page = bd.inject((ROOT / bd.TEMPLATE_FILE).read_text(encoding="utf-8"), self.ks)
        self.assertNotIn(self.player_id, json.dumps(self.ks, ensure_ascii=False))
        self.assertNotIn(self.player_id, page)

    def test_heroes_and_codes_are_well_formed(self) -> None:
        """Each hero has a unique name; each code has a boolean or null redeemed."""
        names = [h["name"] for h in self.ks["heroes"]]
        self.assertTrue(names)
        self.assertEqual(len(names), len(set(names)))
        for code in self.ks["codes"]["active"] + self.ks["codes"]["expired"]:
            self.assertIn(code["redeemed"], (True, False, None))
        self.assertEqual(self.ks["codes"]["expiredTotal"], len(self.ks["codes"]["expired"]))


if __name__ == "__main__":
    unittest.main()

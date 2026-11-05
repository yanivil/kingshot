#!/usr/bin/env python3
"""Tests for scripts/check_gift_codes.py (standard library ``unittest`` only).

No network: pages are small hand-written HTML samples.

Run from the repository root::

    python3 -m unittest discover -s scripts -p "test_*.py"
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_gift_codes as gc  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class LooksLikeCodeTests(unittest.TestCase):
    """Which words count as code-shaped."""

    def test_real_codes_qualify(self) -> None:
        """Codes already on record pass the shape test."""
        for code in ("KS1025", "TREAT4U", "VIP777", "Kingshot888", "lwaL5ZKx5", "WELLDONE", "HAPPYCATDAY"):
            self.assertTrue(gc.looks_like_code(code), code)

    def test_page_words_do_not(self) -> None:
        """Plain words, numbers, quantities and stop words are rejected."""
        for word in ("Gems", "2026", "500K", "10x", "5min", "21st", "EXPIRED", "Active", "NEW", "Copy"):
            self.assertFalse(gc.looks_like_code(word), word)


class ExtractTests(unittest.TestCase):
    """Where on a page codes are looked for."""

    def test_tags_attributes_and_json(self) -> None:
        """Codes in <code>, table cells, copy buttons and JSON are found; body text is not."""
        html = """
        <p>Redeem ABC123X today for rewards</p>
        <table><tr><td><strong>TREAT4U</strong></td><td>500 Gems, 5min speedup</td></tr></table>
        <code>KS1102</code>
        <button data-clipboard-text="VIP777">Copy</button>
        <script>{"code":"OFFICIALSTORE1023","status":"active"}</script>
        """
        self.assertEqual(gc.extract_candidates(html), {"TREAT4U", "KS1102", "VIP777", "OFFICIALSTORE1023"})

    def test_broken_html_does_not_raise(self) -> None:
        """Malformed markup still yields what it can."""
        self.assertIn("KS1102", gc.extract_candidates("<td><code>KS1102</td><div"))


class KnownCodesTests(unittest.TestCase):
    """Reading codes.md."""

    def test_reads_every_list(self) -> None:
        """The Expired list of the repo's codes.md (redeemed and old codes) is read, case-folded."""
        known = gc.load_known_codes((ROOT / "codes.md").read_text(encoding="utf-8"))
        for code in ("forthekingdom", "ks1104", "vip777", "kingshot888", "ks1017", "treat4u"):
            self.assertIn(code, known)

    def test_sample(self) -> None:
        """Rows whose first cell is a backticked code count; the header row does not."""
        md = "| Gift Code | Rewards |\n| `VIP777` | 200 Gems |\n| `KS1017` | x |\n| Code | other |"
        self.assertEqual(gc.load_known_codes(md), {"vip777", "ks1017"})

    def test_old_checkbox_layout(self) -> None:
        """The layout used until 2026-11-05 ("| [x] | `CODE` |") is still read."""
        md = "| [x] | `VIP777` | 200 Gems |\n| [ ] | `KS1017` | x |"
        self.assertEqual(gc.load_known_codes(md), {"vip777", "ks1017"})

    def test_dropped_codes_stay_ignored(self) -> None:
        """Codes dropped from codes.md on 2026-11-05 are in the baseline, so the check does not report them again."""
        known = gc.load_known_codes((ROOT / "codes.md").read_text(encoding="utf-8"))
        base = gc.load_baseline((ROOT / "data" / "gift_codes_baseline.txt").read_text(encoding="utf-8"))
        for code in ("happycatday", "welldone", "hangul2026", "ks1005", "ksgw26jp"):
            self.assertNotIn(code, known)
            self.assertIn(code, base)


class BaselineTests(unittest.TestCase):
    """The baseline of old codes."""

    def test_comments_and_blanks_are_skipped(self) -> None:
        """Only code lines count, case-folded."""
        self.assertEqual(gc.load_baseline("# note\n\nXMAS2024\n  KS0803  \n"), {"xmas2024", "ks0803"})

    def test_repo_baseline_loads(self) -> None:
        """The committed baseline has codes and does not hold KS1104 (recorded in codes.md instead)."""
        base = gc.load_baseline((ROOT / "data" / "gift_codes_baseline.txt").read_text(encoding="utf-8"))
        self.assertIn("xmas2024", base)
        self.assertNotIn("ks1104", base)


class FindNewTests(unittest.TestCase):
    """Combining pages into new codes."""

    PAGES = {
        "a": "<code>VIP777</code><code>TREAT4U</code><code>KS1102</code>",
        "b": "<td>vip777</td><td>treat4u</td>",
    }

    def test_new_codes_and_sources(self) -> None:
        """Known codes are dropped; spelling with more capitals is kept; sources listed."""
        new, known_seen = gc.find_new_codes(self.PAGES, {"vip777"}, set())
        self.assertEqual(new, {"TREAT4U": ["a", "b"], "KS1102": ["a"]})
        self.assertEqual(known_seen, {"a": 1, "b": 1})

    def test_already_reported_is_skipped(self) -> None:
        """A code named in an earlier issue is not reported again."""
        new, _ = gc.find_new_codes(self.PAGES, {"vip777"}, {"treat4u"})
        self.assertEqual(new, {"KS1102": ["a"]})

    def test_codes_in_issue_text(self) -> None:
        """Backticked words in an issue body are read back."""
        self.assertEqual(gc.codes_in_text("| `TREAT4U` | a |\nsee `codes.md`"), {"treat4u"})


class ReportTests(unittest.TestCase):
    """The issue body."""

    def test_groups_and_mention(self) -> None:
        """Likely and single-tracker codes are listed apart; the owner is mentioned."""
        text = gc.build_report({"TREAT4U": ["a", "b"], "KS1102": ["a"]}, {"kingshot.net": "ok"},
                               {"kingshot.net": 3}, "2026-11-05", notify="owner")
        self.assertTrue(text.startswith("@owner"))
        self.assertIn("### Seen on two or more trackers", text)
        self.assertIn("| `TREAT4U` | a, b |", text)
        self.assertIn("### Seen on one tracker only (less certain)", text)
        self.assertIn("| kingshot.net | ok | 3 |", text)

    def test_nothing_new(self) -> None:
        """With nothing new there is no mention and no code table."""
        text = gc.build_report({}, {}, {}, "2026-11-05")
        self.assertIn("found no new codes", text)
        self.assertNotIn("@", text)
        self.assertNotIn("| Code |", text)


if __name__ == "__main__":
    unittest.main()

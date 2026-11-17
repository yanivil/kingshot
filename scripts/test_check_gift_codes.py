#!/usr/bin/env python3
"""Tests for scripts/check_gift_codes.py (standard library ``unittest`` only).

No network: pages are small hand-written HTML samples.

Run from the repository root::

    python3 -m unittest discover -s scripts -p "test_*.py"
"""

from __future__ import annotations

import io
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_data as bd  # noqa: E402
import check_gift_codes as gc  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# A made-up code: no tracker lists it, so it can only come from these tests.
FAKE = "FAKE2026ZQ"


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

    def test_says_merge_adds_to_dashboard(self) -> None:
        """The next step tells the owner that merging puts the codes on the dashboard."""
        text = gc.build_report({"TREAT4U": ["a"]}, {}, {}, "2026-11-05")
        self.assertIn("To redeem", text)
        self.assertIn("Active", text)


SAMPLE_CODES_MD = """---
as_of: 2026-11-05
---
# Codes

## Active Codes

Still to redeem. None right now (2026-11-05).

| Gift Code | Rewards | Source / Notes | Updated |
| :--- | :--- | :--- | :---: |

## Expired Codes

| Gift Code | Redeemed | Rewards | Source / Notes | Updated |
| :--- | :---: | :--- | :--- | :---: |
| `VIP777` | ✓ | 200 Gems | Starter | 2026-11-05 |
"""


class AddToActiveTests(unittest.TestCase):
    """Writing new codes into the Active table of codes.md."""

    NEW = {"TREAT4U": ["a", "b"], "KS1102": ["a"]}

    def test_rows_go_into_the_active_table(self) -> None:
        """Rows land between the Active header and the Expired heading; Expired is untouched."""
        out = gc.add_to_active(SAMPLE_CODES_MD, self.NEW, "2026-11-18")
        active, expired = out.split("## Expired Codes")
        self.assertIn("| `TREAT4U` | Not recorded | Unverified: found by the automated gift-code check on 18 Nov, "
                      "listed on 2 trackers (a, b); not tried in the game yet | 2026-11-18 |", active)
        self.assertIn("| `KS1102` |", active)
        self.assertEqual(expired, SAMPLE_CODES_MD.split("## Expired Codes")[1])
        # Two-tracker codes come first, as in the report.
        self.assertLess(active.index("TREAT4U"), active.index("KS1102"))

    def test_single_tracker_is_marked_less_certain(self) -> None:
        """A code seen on one tracker only says so in its note."""
        out = gc.add_to_active(SAMPLE_CODES_MD, {"KS1102": ["a"]}, "2026-11-18")
        self.assertIn("listed on one tracker only (a), so less certain", out)

    def test_none_right_now_is_dropped(self) -> None:
        """The "None right now" sentence goes once the list has codes."""
        out = gc.add_to_active(SAMPLE_CODES_MD, self.NEW, "2026-11-18")
        self.assertNotIn("None right now", out)
        self.assertIn("Still to redeem.\n", out)

    def test_appends_after_existing_rows(self) -> None:
        """Codes already in Active stay first; new rows follow them."""
        md = SAMPLE_CODES_MD.replace("| :--- | :--- | :--- | :---: |\n",
                                     "| :--- | :--- | :--- | :---: |\n| `OLD1234` | x | y | 2026-11-10 |\n", 1)
        out = gc.add_to_active(md, {"KS1102": ["a"]}, "2026-11-18")
        self.assertLess(out.index("OLD1234"), out.index("KS1102"))
        self.assertLess(out.index("KS1102"), out.index("## Expired Codes"))

    def test_nothing_new_changes_nothing(self) -> None:
        """No new codes leave the file as it was."""
        self.assertEqual(gc.add_to_active(SAMPLE_CODES_MD, {}, "2026-11-18"), SAMPLE_CODES_MD)

    def test_missing_active_table_raises(self) -> None:
        """Without an Active table the run fails instead of dropping the codes."""
        with self.assertRaises(ValueError):
            gc.add_to_active("# Codes\n\n## Expired Codes\n", self.NEW, "2026-11-18")

    def test_added_codes_count_as_known(self) -> None:
        """The next run reads the added rows as recorded, so it does not report them again."""
        out = gc.add_to_active(SAMPLE_CODES_MD, self.NEW, "2026-11-18")
        self.assertTrue({"treat4u", "ks1102"} <= gc.load_known_codes(out))


class DashboardTests(unittest.TestCase):
    """A code added by the check reaches the dashboard's "To redeem" list."""

    def test_repo_codes_md_builds_with_the_new_code(self) -> None:
        """The repo's codes.md plus a fake code builds with the code in Active and no new warning.

        Why compare with a build of the unchanged copy rather than expect no
        warnings at all: this test also runs before every scheduled check, and
        an unrelated warning (say in hero.md) must not stop the gift-code check.
        """
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in bd.SOURCE_FILES:
                shutil.copy(ROOT / name, root / name)
            (root / "data").mkdir()
            shutil.copy(ROOT / "data" / "manual.json", root / "data" / "manual.json")
            before = bd.BuildLog()
            bd.build_ks_data(root, before)
            path = root / "codes.md"
            path.write_text(gc.add_to_active(path.read_text(encoding="utf-8"), {FAKE: ["a", "b"]}, "2026-11-18"),
                            encoding="utf-8")
            after = bd.BuildLog()
            ks, _ = bd.build_ks_data(root, after)
        self.assertIn({"code": FAKE}, ks["codes"]["active"])
        self.assertNotIn(FAKE, [c["code"] for c in ks["codes"]["expired"]])
        self.assertEqual(after.warnings, before.warnings)


class MainTests(unittest.TestCase):
    """The whole run, with the network replaced by a sample page."""

    def run_main(self, tmp: Path, *extra: str) -> str:
        """Run main() on a copy of the sample codes.md; return what it printed."""
        page = f"<code>{FAKE}</code><code>VIP777</code>"
        env = {"GITHUB_OUTPUT": str(tmp / "out.txt"), "GITHUB_TOKEN": "", "GITHUB_STEP_SUMMARY": ""}
        buf = io.StringIO()
        with mock.patch.object(gc, "fetch", return_value=(page, "ok")), \
                mock.patch.dict(os.environ, env), redirect_stdout(buf):
            self.assertEqual(gc.main(["--codes", str(tmp / "codes.md"), "--baseline", str(tmp / "none.txt"),
                                      "--report-file", str(tmp / "report.md"), *extra]), 0)
        return buf.getvalue()

    def test_add_to_codes_writes_rows_report_and_count(self) -> None:
        """--add-to-codes puts the new code in Active; the report and the count are written for the workflow."""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            (tmp / "codes.md").write_text(SAMPLE_CODES_MD, encoding="utf-8")
            self.run_main(tmp, "--add-to-codes")
            codes = (tmp / "codes.md").read_text(encoding="utf-8")
            self.assertIn(f"| `{FAKE}` |", codes.split("## Expired Codes")[0])
            self.assertIn(f"`{FAKE}`", (tmp / "report.md").read_text(encoding="utf-8"))
            self.assertIn("new_codes=1", (tmp / "out.txt").read_text(encoding="utf-8"))

    def test_without_flag_codes_md_is_untouched(self) -> None:
        """Without --add-to-codes the run only reports."""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            (tmp / "codes.md").write_text(SAMPLE_CODES_MD, encoding="utf-8")
            self.run_main(tmp)
            self.assertEqual((tmp / "codes.md").read_text(encoding="utf-8"), SAMPLE_CODES_MD)
            self.assertIn("new_codes=1", (tmp / "out.txt").read_text(encoding="utf-8"))

    def test_nothing_new_writes_zero(self) -> None:
        """A run with nothing new writes new_codes=0, so the workflow opens no pull request."""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            (tmp / "codes.md").write_text(SAMPLE_CODES_MD.replace("`VIP777`", f"`{FAKE}`"), encoding="utf-8")
            (tmp / "none.txt").write_text("VIP777\n", encoding="utf-8")
            self.run_main(tmp, "--add-to-codes")
            self.assertIn("new_codes=0", (tmp / "out.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Look for new Kingshot gift codes on community tracker sites.

Run by ``.github/workflows/check-gift-codes.yml`` every two days on GitHub's
runners (standard library only, no installs). It:

1. reads the codes already recorded in ``codes.md`` (Active, and Expired, which
   also holds the redeemed ones) and in ``data/gift_codes_baseline.txt`` (old
   codes trackers still list);
2. downloads a handful of community tracker pages;
3. picks out code-shaped words from the places those pages usually put codes
   (``<code>``, ``<strong>``, table cells, copy buttons, JSON ``"code"`` keys);
4. drops anything already in ``codes.md``, in the baseline, or already reported
   in an earlier ``gift-codes`` issue or pull request;
5. writes a report of what is left, split into codes seen on two or more
   trackers (likely) and on one tracker only (less certain);
6. with ``--add-to-codes``, adds those codes to the Active table of
   ``codes.md`` as unverified rows.

The workflow then commits ``codes.md`` to a ``gift-codes/...`` branch and opens
a pull request with the report as its body; merging it puts the codes on the
dashboard's "To redeem" list. Why a pull request: on 9 Nov the check reported
11OFFICIALSTORE08 in an issue only, nothing copied it into ``codes.md``, and it
expired before anyone tried it. The codes are still unverified (tracker pages
are written by third parties), so they reach ``main`` only when the owner
merges, and each row says so until the code is tried in the game.

Usage::

    python3 scripts/check_gift_codes.py --codes codes.md            # report only
    python3 scripts/check_gift_codes.py --codes codes.md --add-to-codes \\
        --github-repo owner/name --notify owner --report-file report.md

Environment: ``GITHUB_TOKEN`` (optional; reads earlier gift-code issues and
pull requests so their codes are not reported twice), ``GITHUB_STEP_SUMMARY``
(optional; the report is appended there), ``GITHUB_OUTPUT`` (optional;
``new_codes=<count>`` is written there for the workflow's next steps).

Exit status: 0 normally; 1 when every tracker failed to download, so a broken
check shows up as a failed workflow run instead of silently finding nothing.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple

# ---------------------------------------------------------------------------
# Settings. Tracker pages that listed Kingshot codes on 2 Nov 2026; any of
# them may move or block automated requests, which the report then shows.
# ---------------------------------------------------------------------------

SOURCES: Dict[str, str] = {
    "kingshot.net": "https://kingshot.net/gift-codes",
    "kingshotoptimizer.com": "https://kingshotoptimizer.com/gift-codes/",
    "kingshotguide.org": "https://www.kingshotguide.org/gift-codes",
    "kingshotguide.com": "https://www.kingshotguide.com/gift-codes",
    "kingshotmastery.com": "https://kingshotmastery.com/gift-codes",
    "boostbot.org": "https://boostbot.org/blog/kingshot-gift-codes/",
}

ISSUE_LABEL = "gift-codes"
USER_AGENT = "Mozilla/5.0 (compatible; kingshot-gift-code-check/1.0)"
TIMEOUT_SECONDS = 25

# Tags whose text often holds a code on tracker pages, and attributes that
# copy-to-clipboard buttons use for the code itself.
CODE_TAGS = {"code", "kbd", "strong", "b", "td", "th", "li", "button", "h2", "h3", "h4", "span"}
CODE_ATTRS = {"data-code", "data-clipboard-text", "data-copy", "data-gift-code"}

# A code is 4–24 letters and digits. Examples on record: KS1025, TREAT4U,
# VIP777, Kingshot888, lwaL5ZKx5, WELLDONE, HAPPYCATDAY.
TOKEN_RE = re.compile(r"[A-Za-z0-9]{4,24}")
# Quantities and ordinals such as 500K, 10x, 5min, 21st are reward text, not codes.
QUANTITY_RE = re.compile(r"^\d+(x|k|m|b|h|hr|hrs|min|mins|d|day|days|st|nd|rd|th|pcs)$", re.IGNORECASE)
# Next.js / Nuxt pages often ship their data as JSON: {"code":"TREAT4U", ...}.
JSON_CODE_RE = re.compile(r'"(?:code|giftCode|gift_code|redeemCode|redeem_code)"\s*:\s*"([A-Za-z0-9]{4,24})"')
# Codes already recorded: the backticked code in the first cell of a table row ("| `CODE` | ...").
# The older layout with a checkbox cell first ("| [x] | `CODE` | ...", used until 2026-11-05) is
# still read, so an old copy of codes.md cannot make the check report recorded codes as new.
KNOWN_CODE_RE = re.compile(r"^\|\s*(?:\[[ xX]\]\s*\|\s*)?`([^`]+)`", re.MULTILINE)

# All-capital words of six or more letters that trackers print but that are
# not codes (lower-case page text never qualifies without a digit).
STOPWORDS = {
    w.casefold() for w in """
    ACTIVE EXPIRED EXPIRES REDEEM REDEEMED REWARD REWARDS STATUS UNKNOWN UPDATED
    VERIFIED WORKING INVALID LIMITED COPIED CLAIMED PERMANENT KINGSHOT CENTURY
    DISCORD FACEBOOK INSTAGRAM YOUTUBE TWITTER REDDIT TIKTOK ANDROID IPHONE
    SPEEDUP SPEEDUPS MYTHIC LEGENDARY STAMINA RESOURCES GOVERNOR PLAYER SERVER
    KINGDOM SETTINGS CONFIRM SUBMIT ENTRIES LATEST RECENT ARCHIVE CHECKED
    JANUARY FEBRUARY MARCH APRIL AUGUST SEPTEMBER OCTOBER NOVEMBER DECEMBER
    MONDAY TUESDAY WEDNESDAY THURSDAY FRIDAY SATURDAY SUNDAY
    """.split()
}


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def load_known_codes(codes_md: str) -> Set[str]:
    """Return the codes already in ``codes.md``, case-folded.

    Args:
        codes_md: The text of ``codes.md``.

    Returns:
        Case-folded codes from every table row whose first cell is a
        backticked code: the Active and Expired lists alike, and any older
        list such as Redeemed (an expired or redeemed code is not news either).
    """
    return {m.group(1).strip().casefold() for m in KNOWN_CODE_RE.finditer(codes_md)}


def load_baseline(text: str) -> Set[str]:
    """Return the case-folded codes in the baseline file.

    Why: trackers keep listing old codes that were never recorded in
    ``codes.md``; the baseline keeps the check from reporting them.

    Args:
        text: The file's text: one code per line, ``#`` lines are comments.

    Returns:
        Case-folded codes.
    """
    return {line.strip().casefold() for line in text.splitlines()
            if line.strip() and not line.lstrip().startswith("#")}


def looks_like_code(token: str) -> bool:
    """Decide whether a word could be a gift code.

    Args:
        token: A run of 4–24 letters and digits.

    Returns:
        True when it mixes letters and digits (KS1025, TREAT4U) or is a capital
        word of six or more letters (WELLDONE), and is not a quantity
        (500K, 5min) or a known non-code word (EXPIRED).
    """
    if not TOKEN_RE.fullmatch(token) or token.isdigit():
        return False
    if QUANTITY_RE.match(token) or token.casefold() in STOPWORDS:
        return False
    has_digit = any(c.isdigit() for c in token)
    has_letter = any(c.isalpha() for c in token)
    # Edge case: a year glued to a word (e.g. "2026Q4") still qualifies here;
    # the two-tracker split in the report keeps such one-offs apart.
    return (has_digit and has_letter) or (token.isupper() and len(token) >= 6)


class _CodeTextParser(HTMLParser):
    """Collect text inside code-bearing tags and code-bearing attributes."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth = 0  # how many CODE_TAGS we are inside
        self.chunks: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        for name, value in attrs:
            if name in CODE_ATTRS and value:
                self.chunks.append(value)
        if tag in CODE_TAGS:
            self.depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in CODE_TAGS and self.depth:
            self.depth -= 1

    def handle_data(self, data: str) -> None:
        if self.depth:
            self.chunks.append(data)


def extract_candidates(html: str) -> Set[str]:
    """Pick code-shaped words out of one tracker page.

    Args:
        html: The page source.

    Returns:
        Words that pass ``looks_like_code``, from code-bearing tags and
        attributes and from JSON ``"code"`` keys, with their original case.
    """
    parser = _CodeTextParser()
    try:
        parser.feed(html)
        parser.close()
    except Exception:  # noqa: BLE001 - a malformed page must not stop the run
        pass
    words = set()
    for chunk in parser.chunks:
        words.update(TOKEN_RE.findall(chunk))
    words.update(JSON_CODE_RE.findall(html))
    return {w for w in words if looks_like_code(w)}


def find_new_codes(
    pages: Dict[str, str], known: Set[str], already_reported: Set[str]
) -> Tuple[Dict[str, List[str]], Dict[str, int]]:
    """Combine the pages into new codes and the trackers that list each one.

    Args:
        pages: Tracker name → page HTML (only the pages that downloaded).
        known: Case-folded codes already in ``codes.md``.
        already_reported: Case-folded codes named in earlier gift-code issues.

    Returns:
        ``(new, known_seen)``: ``new`` maps each new code to the sorted tracker
        names listing it; ``known_seen`` counts, per tracker, how many
        ``codes.md`` codes it showed. A tracker with 0 is a sign this script
        no longer reads that page correctly.
    """
    seen: Dict[str, Set[str]] = {}
    spelling: Dict[str, str] = {}
    known_seen: Dict[str, int] = {}
    for source, html in pages.items():
        found = extract_candidates(html)
        known_seen[source] = len({w.casefold() for w in found} & known)
        for word in found:
            key = word.casefold()
            if key in known or key in already_reported:
                continue
            seen.setdefault(key, set()).add(source)
            # Keep the spelling with more capitals: trackers sometimes lower-case codes.
            if sum(c.isupper() for c in word) >= sum(c.isupper() for c in spelling.get(key, "")):
                spelling[key] = word
    new = {spelling[k]: sorted(v) for k, v in seen.items()}
    return new, known_seen


def codes_in_text(text: str) -> Set[str]:
    """Return the case-folded backticked words in ``text`` (used for issue and pull request bodies)."""
    return {m.casefold() for m in re.findall(r"`([A-Za-z0-9]{4,24})`", text or "")}


def split_by_certainty(new: Dict[str, List[str]]) -> Tuple[List[str], List[str]]:
    """Return ``(likely, single)``: codes on two or more trackers, then on one, each sorted."""
    likely = sorted((c for c, s in new.items() if len(s) >= 2), key=str.casefold)
    single = sorted((c for c, s in new.items() if len(s) == 1), key=str.casefold)
    return likely, single


# ---------------------------------------------------------------------------
# codes.md update
# ---------------------------------------------------------------------------

# The "## Active Codes" heading, and the sentence its paragraph carries while the list is empty.
ACTIVE_HEADING_RE = re.compile(r"^##\s+Active Codes\b", re.MULTILINE)
NONE_RIGHT_NOW_RE = re.compile(r"\s*None right now \(\d{4}-\d{2}-\d{2}\)\.")


def add_to_active(codes_md: str, new: Dict[str, List[str]], today: str) -> str:
    """Add new codes as unverified rows at the end of the Active table of ``codes.md``.

    Why here and not only in an issue: the dashboard's "To redeem" list is built
    from this table, so a code that is only in an issue never shows there.

    Args:
        codes_md: The text of ``codes.md``.
        new: New code → tracker names (from ``find_new_codes``).
        today: Date of the run (YYYY-MM-DD); it goes in the Updated column.

    Returns:
        The new text. Rows follow the Active table's columns (Gift Code,
        Rewards, Source / Notes, Updated); two-tracker codes come first. The
        paragraph's "None right now (date)." is dropped, since the list is no
        longer empty. With nothing new the text is returned unchanged.

    Raises:
        ValueError: When there is no Active Codes table, so the run fails
            loudly instead of losing the codes.
    """
    if not new:
        return codes_md
    lines = codes_md.splitlines(keepends=True)
    heading = next((i for i, line in enumerate(lines) if ACTIVE_HEADING_RE.match(line)), None)
    if heading is None:
        raise ValueError("codes.md has no '## Active Codes' heading")
    # The section ends at the next heading of the same or a higher level.
    end = next((i for i in range(heading + 1, len(lines)) if re.match(r"^#{1,2}\s", lines[i])), len(lines))
    header = next((i for i in range(heading + 1, end) if lines[i].startswith("| Gift Code")), None)
    if header is None or header + 1 >= end or not lines[header + 1].startswith("|"):
        raise ValueError("codes.md has no Active Codes table")
    last = header + 1  # the | :--- | separator row
    while last + 1 < end and lines[last + 1].startswith("|"):
        last += 1

    day = dt.date.fromisoformat(today)
    when = f"{day.day} {day:%b}"  # "18 Nov", as in the notes already in codes.md
    rows = []
    likely, single = split_by_certainty(new)
    for code in likely + single:
        sources = new[code]
        seen = (f"listed on {len(sources)} trackers ({', '.join(sources)})" if len(sources) >= 2
                else f"listed on one tracker only ({sources[0]}), so less certain")
        rows.append(f"| `{code}` | Not recorded | Unverified: found by the automated gift-code check on {when}, "
                    f"{seen}; not tried in the game yet | {today} |\n")
    # Edge case: a file without a final newline must not glue the first new row to the last old one.
    if not lines[last].endswith("\n"):
        lines[last] += "\n"
    intro = [NONE_RIGHT_NOW_RE.sub("", line) for line in lines[heading:header]]
    return "".join(lines[:heading] + intro + lines[header:last + 1] + rows + lines[last + 1:])


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------


def build_report(
    new: Dict[str, List[str]],
    status: Dict[str, str],
    known_seen: Dict[str, int],
    today: str,
    notify: Optional[str] = None,
) -> str:
    """Write the Markdown used for the issue body and the run summary.

    Args:
        new: New code → tracker names (from ``find_new_codes``).
        status: Tracker name → "ok" or the download error.
        known_seen: Tracker name → recorded codes (codes.md or baseline) it showed.
        today: Date of the run (YYYY-MM-DD).
        notify: GitHub login to mention so the owner gets a notification.

    Returns:
        Markdown text.
    """
    likely, single = split_by_certainty(new)
    lines = []
    if notify:
        lines.append(f"@{notify}")
        lines.append("")
    if new:
        lines.append(f"The scheduled check on {today} found codes that are not in `codes.md` yet. "
                     "They come from community trackers and have not been tried in the game, so they are unverified.")
    else:
        lines.append(f"The scheduled check on {today} found no new codes.")
    for title, group in (("Seen on two or more trackers", likely), ("Seen on one tracker only (less certain)", single)):
        if group:
            lines += ["", f"### {title}", "", "| Code | Trackers |", "| --- | --- |"]
            lines += [f"| `{c}` | {', '.join(new[c])} |" for c in group]
    lines += ["", "### Trackers checked", "", "| Tracker | Download | Recorded codes seen |", "| --- | --- | :---: |"]
    for source in SOURCES:
        lines.append(f"| {source} | {status.get(source, 'not tried')} | {known_seen.get(source, '—')} |")
    lines += ["", "Recorded codes are those in `codes.md` or `data/gift_codes_baseline.txt`. A tracker that downloads "
              "but shows 0 of them has probably changed its page; codes it lists may be missed."]
    if new:
        lines += ["", "Next step: merge the pull request that adds these codes to the Active list in `codes.md` "
                  "(marked unverified), so the dashboard shows them under To redeem. Then try them in the game and "
                  "tell Claude how each one went, so its row is moved to Expired. A code that is old or not real: "
                  "delete its row and add it to `data/gift_codes_baseline.txt`."]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Network
# ---------------------------------------------------------------------------


def fetch(url: str) -> Tuple[Optional[str], str]:
    """Download one page.

    Returns:
        ``(html, "ok")`` or ``(None, short error)``; never raises.
    """
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            return resp.read().decode("utf-8", errors="replace"), "ok"
    except urllib.error.HTTPError as exc:
        return None, f"HTTP {exc.code}"
    except Exception as exc:  # noqa: BLE001 - DNS, TLS, timeout: report and move on
        return None, type(exc).__name__


def _github(method: str, path: str, token: str, body: Optional[dict] = None) -> Tuple[int, object]:
    """Call the GitHub REST API; returns ``(status, parsed JSON or None)``."""
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        data=json.dumps(body).encode() if body is not None else None,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            raw = resp.read()
            return resp.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        return exc.code, None


def reported_codes(repo: str, token: str) -> Set[str]:
    """Codes named in any earlier issue or pull request with the gift-codes label (open, closed or merged).

    Why pull requests count too: the issues endpoint lists pull requests as
    well, so a code the owner turned down by closing its pull request is not
    proposed again on the next run.
    """
    status, issues = _github("GET", f"/repos/{repo}/issues?labels={ISSUE_LABEL}&state=all&per_page=100", token)
    if status != 200 or not isinstance(issues, list):
        return set()
    found: Set[str] = set()
    for issue in issues:
        found |= codes_in_text(issue.get("body") or "")
    return found


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: Optional[Iterable[str]] = None) -> int:
    """Run the check; see the module docstring for arguments and exit status."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--codes", default="codes.md", help="path to codes.md")
    ap.add_argument("--baseline", default="data/gift_codes_baseline.txt",
                    help="codes not to report (one per line); skipped if the file is missing")
    ap.add_argument("--github-repo", help="owner/name; skip codes named in its earlier gift-codes issues and PRs")
    ap.add_argument("--notify", help="GitHub login to mention in the report")
    ap.add_argument("--add-to-codes", action="store_true",
                    help="add the new codes to the Active table of the --codes file, marked unverified")
    ap.add_argument("--report-file", help="also write the report here (the workflow uses it as the PR body)")
    args = ap.parse_args(list(argv) if argv is not None else None)

    codes_path = Path(args.codes)
    codes_md = codes_path.read_text(encoding="utf-8")
    known = load_known_codes(codes_md)
    baseline_path = Path(args.baseline)
    # Edge case: a missing baseline is not an error; the check then reports old codes too.
    if baseline_path.is_file():
        known |= load_baseline(baseline_path.read_text(encoding="utf-8"))
    token = os.environ.get("GITHUB_TOKEN", "")

    pages: Dict[str, str] = {}
    status: Dict[str, str] = {}
    for source, url in SOURCES.items():
        html, status[source] = fetch(url)
        if html is not None:
            pages[source] = html

    already = reported_codes(args.github_repo, token) if args.github_repo and token else set()
    new, known_seen = find_new_codes(pages, known, already)
    # UTC, like the runner and the workflow's `date -u`, so the row date and the commit message agree.
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    report = build_report(new, status, known_seen, today, args.notify if new else None)

    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(report)
    if args.report_file:
        Path(args.report_file).write_text(report, encoding="utf-8")
    # Why the file is written even on a dry run: it only changes the runner's
    # checkout, and the workflow shows the diff; only the push needs a real run.
    if args.add_to_codes and new:
        codes_path.write_text(add_to_active(codes_md, new, today), encoding="utf-8")
        print(f"Added {len(new)} code(s) to the Active table of {codes_path}.")
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as fh:
            fh.write(f"new_codes={len(new)}\n")

    if not pages:
        print("Every tracker failed to download.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

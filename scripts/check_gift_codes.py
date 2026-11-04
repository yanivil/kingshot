#!/usr/bin/env python3
"""Look for new Kingshot gift codes on community tracker sites.

Run by ``.github/workflows/check-gift-codes.yml`` every two days on GitHub's
runners (standard library only, no installs). It:

1. reads the codes already recorded in ``codes.md`` (active and expired);
2. downloads a handful of community tracker pages;
3. picks out code-shaped words from the places those pages usually put codes
   (``<code>``, ``<strong>``, table cells, copy buttons, JSON ``"code"`` keys);
4. drops anything already in ``codes.md`` or already reported in an earlier
   ``gift-codes`` issue;
5. opens one GitHub issue listing what is left, split into codes seen on two or
   more trackers (likely) and on one tracker only (less certain).

Why an issue and not a pull request: tracker pages are written by third
parties and change without notice, so whatever this finds is unverified. A
person (or Claude, when asked) tries the codes in the game and then records
them in ``codes.md`` through the usual pull request.

Usage::

    python3 scripts/check_gift_codes.py --codes codes.md            # report only
    python3 scripts/check_gift_codes.py --codes codes.md \\
        --github-repo owner/name --notify owner                     # also open an issue

Environment: ``GITHUB_TOKEN`` (needed to read and open issues),
``GITHUB_STEP_SUMMARY`` (optional; the report is appended there),
``DRY_RUN=true`` (optional; report but do not open an issue).

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
# Codes already recorded: the backticked code after the checkbox in a table row.
KNOWN_CODE_RE = re.compile(r"^\|\s*\[[ xX]\]\s*\|\s*`([^`]+)`", re.MULTILINE)

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
        Case-folded codes from every table row that starts with a checkbox,
        active and expired alike (an expired code is not news either).
    """
    return {m.group(1).strip().casefold() for m in KNOWN_CODE_RE.finditer(codes_md)}


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
    """Return the case-folded backticked words in ``text`` (used for issue bodies)."""
    return {m.casefold() for m in re.findall(r"`([A-Za-z0-9]{4,24})`", text or "")}


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
        known_seen: Tracker name → recorded codes it showed.
        today: Date of the run (YYYY-MM-DD).
        notify: GitHub login to mention so the owner gets a notification.

    Returns:
        Markdown text.
    """
    likely = sorted((c for c, s in new.items() if len(s) >= 2), key=str.casefold)
    single = sorted((c for c, s in new.items() if len(s) == 1), key=str.casefold)
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
    lines += ["", "A tracker that downloads but shows 0 recorded codes has probably changed its page; "
              "codes it lists may be missed."]
    if new:
        lines += ["", "Next step: try the codes in the game, then tell Claude which ones worked so `codes.md` is updated "
                  "through a pull request. Close this issue when done."]
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
    """Codes named in any earlier issue with the gift-codes label (open or closed)."""
    status, issues = _github("GET", f"/repos/{repo}/issues?labels={ISSUE_LABEL}&state=all&per_page=100", token)
    if status != 200 or not isinstance(issues, list):
        return set()
    found: Set[str] = set()
    for issue in issues:
        found |= codes_in_text(issue.get("body") or "")
    return found


def open_issue(repo: str, token: str, title: str, body: str) -> Optional[str]:
    """Open the issue (creating the label first if needed); return its URL."""
    _github("POST", f"/repos/{repo}/labels", token,
            {"name": ISSUE_LABEL, "color": "d4a72c", "description": "New Kingshot gift codes found by the scheduled check"})
    status, issue = _github("POST", f"/repos/{repo}/issues", token, {"title": title, "body": body, "labels": [ISSUE_LABEL]})
    return issue.get("html_url") if status == 201 and isinstance(issue, dict) else None


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: Optional[Iterable[str]] = None) -> int:
    """Run the check; see the module docstring for arguments and exit status."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--codes", default="codes.md", help="path to codes.md")
    ap.add_argument("--github-repo", help="owner/name; open an issue there when new codes are found")
    ap.add_argument("--notify", help="GitHub login to mention in the issue")
    args = ap.parse_args(list(argv) if argv is not None else None)

    known = load_known_codes(Path(args.codes).read_text(encoding="utf-8"))
    token = os.environ.get("GITHUB_TOKEN", "")
    dry_run = os.environ.get("DRY_RUN", "").lower() == "true"

    pages: Dict[str, str] = {}
    status: Dict[str, str] = {}
    for source, url in SOURCES.items():
        html, status[source] = fetch(url)
        if html is not None:
            pages[source] = html

    already = reported_codes(args.github_repo, token) if args.github_repo and token else set()
    new, known_seen = find_new_codes(pages, known, already)
    today = dt.date.today().isoformat()
    report = build_report(new, status, known_seen, today, args.notify if new else None)

    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(report)

    if not pages:
        print("Every tracker failed to download.", file=sys.stderr)
        return 1
    if new and args.github_repo and token and not dry_run:
        url = open_issue(args.github_repo, token, f"New Kingshot gift codes ({today})", report)
        print(f"Opened issue: {url}" if url else "Could not open the issue.")
    elif new and dry_run:
        print("Dry run: no issue opened.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

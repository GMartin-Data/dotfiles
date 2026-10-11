#!/usr/bin/env python3
"""Check where every web source's date in a tech-watch report comes from (K6 / E8).

Usage: python3 -I check-dates.py <report.md> <transcript.jsonl>

Covers the ranked entries (a `🔗` line followed by a `📅` line) and the Primary
sources block (one line: `**Title** — 🔗 URL — 📅 date`). For each source whose
URL is not a Tier 1 domain (arxiv.org, github.com, youtube.com), the date on its
`📅` line is classified as:
  unverified      - the allowed value when nothing could be established
  url             - the date appears in the URL path (e.g. /2026/07/16/)
  fetched         - the date appears, year included, in a WebFetch result for
                    that URL (ISO, 10/7/2026, October 7, 2026, Oct 07, 2026,
                    7 October 2026, ...)
  fetched-month   - the report gives a month only (YYYY-MM) and the fetched page
                    shows that month
  fetched-noyear  - the fetched page shows the day and month but no year: the
                    year in the report was inferred
  search          - the date appears in a WebSearch result (snippet), which the
                    skill rule does NOT accept as a source
  UNSOURCED       - found nowhere above: invented or estimated
Exit code 1 if any source is UNSOURCED or search-derived. `fetched-noyear` is
reported, not failed: whether an inferred year is acceptable is an open point
(final replay 2026-10-11).
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

TIER1 = ("arxiv.org", "github.com", "youtube.com", "youtu.be")
MONTHS = [
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December",
]
UNVERIFIED_PREFIXES = ("unverified", "undated", "unknown", "n/a")

# A source: `🔗 URL` then `📅 date`, either on the same line (Primary sources
# block) or within the next three lines (ranked entries).
SOURCE = re.compile(r"🔗\s*(\S+)(?:[^\n]*?|\n(?:[^\n]*\n){0,2}?)📅\s*([^|\n]+)")
FULL_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
MONTH_ONLY = re.compile(r"\d{4}-\d{2}(?!-\d)")


def _month_names(month: int) -> tuple[str, str]:
    """Full and abbreviated month name, e.g. ("October", "Oct")."""
    name = MONTHS[month - 1]
    return name, name[:3]


def full_date_patterns(d: date) -> list[re.Pattern[str]]:
    """Spellings of a full date, year included, as seen in fetched pages."""
    month, mon = _month_names(d.month)
    day2 = f"{d.day:02d}"
    return [
        re.compile(p)
        for p in (
            rf"{d.year}-{d.month:02d}-{day2}",
            rf"{d.year}/{d.month:02d}/{day2}",
            rf"\b(?:{month}|{mon})\.? 0?{d.day}(?:st|nd|rd|th)?,? {d.year}\b",
            rf"\b0?{d.day} (?:{month}|{mon})\.? {d.year}\b",
            rf"\b0?{d.month}/0?{d.day}/{d.year}\b",
        )
    ]


def noyear_patterns(d: date) -> list[re.Pattern[str]]:
    """Day and month without a year right after (`Oct 5`, `October 5`, `5 Oct`)."""
    month, mon = _month_names(d.month)
    return [
        re.compile(rf"\b(?:{month}|{mon})\.? 0?{d.day}(?:st|nd|rd|th)?\b(?!,? ?\d{{4}})"),
        re.compile(rf"\b0?{d.day} (?:{month}|{mon})\.?\b(?! \d{{4}})"),
    ]


def month_patterns(year: int, month_num: int) -> list[re.Pattern[str]]:
    """Spellings of a month without a day (`October 2026`, `2026-10`, `10/2026`)."""
    month, mon = _month_names(month_num)
    return [
        re.compile(rf"\b(?:{month}|{mon})\.? {year}\b"),
        re.compile(rf"\b{year}-{month_num:02d}\b"),
        re.compile(rf"\b0?{month_num}/{year}\b"),
    ]


def normalize_url(url: str) -> str:
    """Comparable form of a URL: no scheme, no `www.`, no fragment, no trailing slash."""
    url = url.split("#")[0].rstrip("/")
    for prefix in ("https://", "http://"):
        url = url.removeprefix(prefix)
    return url.removeprefix("www.")


def tool_texts(transcript: str, tool: str) -> list[tuple[dict, str]]:
    """(input, result text) for every call of `tool` in a stream-json transcript."""
    calls: dict[str, dict] = {}
    results: dict[str, str] = {}
    with Path(transcript).open(encoding="utf-8") as fh:
        for line in fh:
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            content = (ev.get("message") or {}).get("content") or []
            if not isinstance(content, list):
                continue
            for block in content:
                if ev.get("type") == "assistant" and block.get("type") == "tool_use" and block.get("name") == tool:
                    calls[block["id"]] = block.get("input") or {}
                elif ev.get("type") == "user" and block.get("type") == "tool_result" and block.get("tool_use_id") in calls:
                    raw = block.get("content")
                    if isinstance(raw, list):
                        text = "\n".join(b.get("text", "") for b in raw if isinstance(b, dict))
                    else:
                        text = str(raw)
                    results[block["tool_use_id"]] = text
    return [(calls[k], results.get(k, "")) for k in calls]


def _any(patterns: list[re.Pattern[str]], text: str) -> bool:
    return any(p.search(text) for p in patterns)


def classify(url: str, shown: str, page_text: str, search_text: str) -> str:
    """Verdict for one source, given the fetched text of its own URL and all snippets."""
    if shown.lower().startswith(UNVERIFIED_PREFIXES):
        return "unverified"

    full = FULL_DATE.search(shown)
    if full:
        d = date.fromisoformat(full.group(0))
        if f"/{d.year}/{d.month:02d}/{d.day:02d}" in url or full.group(0) in url:
            return "url"
        if _any(full_date_patterns(d), page_text):
            return "fetched"
        if _any(noyear_patterns(d), page_text):
            return "fetched-noyear"
        if _any(full_date_patterns(d), search_text):
            return "search"
        return "UNSOURCED"

    month = MONTH_ONLY.search(shown)
    if month:
        year, month_num = int(month.group(0)[:4]), int(month.group(0)[5:7])
        if f"/{year}/{month_num:02d}/" in url:
            return "url"
        if _any(month_patterns(year, month_num), page_text):
            return "fetched-month"
        if _any(month_patterns(year, month_num), search_text):
            return "search"
        return "UNSOURCED"

    # Neither ISO nor unverified: look for the literal text.
    if shown in page_text:
        return "fetched"
    if shown in search_text:
        return "search"
    return "UNSOURCED"


def main() -> int:
    """Print one verdict per web source and return 1 when any is UNSOURCED or search-derived."""
    report, transcript = sys.argv[1], sys.argv[2]
    text = Path(report).read_text(encoding="utf-8")
    search_text = "\n".join(t for _, t in tool_texts(transcript, "WebSearch"))
    fetched: dict[str, str] = {}
    for inp, out in tool_texts(transcript, "WebFetch"):
        key = normalize_url(inp.get("url") or "")
        fetched[key] = fetched.get(key, "") + "\n" + out

    bad = 0
    noyear = 0
    print(f"{'verdict':<15} {'date':<12} url")
    for url, raw_date in SOURCE.findall(text):
        if any(d in url for d in TIER1):
            continue
        shown = raw_date.strip()
        verdict = classify(url, shown, fetched.get(normalize_url(url), ""), search_text)
        bad += verdict in ("search", "UNSOURCED")
        noyear += verdict == "fetched-noyear"
        print(f"{verdict:<15} {shown:<12} {url}")
    print(f"\nWebFetch calls in transcript: {len(fetched)} distinct URLs")
    if noyear:
        print(f"Year inferred on {noyear} source(s) (fetched-noyear): reported, not failed.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

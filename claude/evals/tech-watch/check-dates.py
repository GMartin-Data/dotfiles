#!/usr/bin/env python3
"""Check where every web source's date in a tech-watch report comes from (K6 / E8).

Usage: python3 -I check-dates.py <report.md> <transcript.jsonl>

For each source whose URL is not a Tier 1 domain (arxiv.org, github.com,
youtube.com), the date on its `📅` line is classified as:
  unverified   - the allowed value when nothing could be established
  url          - the date appears in the URL path (e.g. /2026/07/16/)
  fetched      - the date appears in a WebFetch result for that URL
  search       - the date appears in a WebSearch result (snippet), which the
                 skill rule does NOT accept as a source
  UNSOURCED    - found nowhere above: invented or estimated
Exit code 1 if any source is UNSOURCED or search-derived.
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


def date_variants(iso: str) -> list[str]:
    """ISO date -> spellings to look for in page or snippet text."""
    try:
        d = date.fromisoformat(iso)
    except ValueError:
        return [iso]
    month = MONTHS[d.month - 1]
    return [
        iso,
        f"{month} {d.day}, {d.year}",
        f"{month[:3]} {d.day}, {d.year}",
        f"{d.day} {month} {d.year}",
        f"{d.day} {month[:3]} {d.year}",
        f"{d.year}/{d.month:02d}/{d.day:02d}",
        f"{d.year}-{d.month:02d}",
    ]


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


def main() -> int:
    report, transcript = sys.argv[1], sys.argv[2]
    text = Path(report).read_text(encoding="utf-8")
    search_text = "\n".join(t for _, t in tool_texts(transcript, "WebSearch"))
    fetches = tool_texts(transcript, "WebFetch")

    # Each source: a 🔗 line followed (within a few lines) by a 📅 line.
    pattern = re.compile(r"🔗\s*(\S+)\s*\n(?:[^\n]*\n){0,2}?📅\s*([^|\n]+)")
    bad = 0
    print(f"{'verdict':<11} {'date':<12} url")
    for url, raw_date in pattern.findall(text):
        if any(d in url for d in TIER1):
            continue
        shown = raw_date.strip()
        if shown.lower().startswith(("unverified", "undated", "unknown", "n/a")):
            verdict = "unverified"
        else:
            iso = re.search(r"\d{4}-\d{2}-\d{2}", shown)
            variants = date_variants(iso.group(0)) if iso else [shown]
            path_hit = iso and (
                f"/{iso.group(0)[:4]}/{iso.group(0)[5:7]}/{iso.group(0)[8:10]}" in url
                or iso.group(0) in url
            )
            fetched_hit = any(
                (inp.get("url") or "").split("#")[0].rstrip("/") == url.split("#")[0].rstrip("/")
                and any(v in out for v in variants)
                for inp, out in fetches
            )
            search_hit = any(v in search_text for v in variants)
            if path_hit:
                verdict = "url"
            elif fetched_hit:
                verdict = "fetched"
            elif search_hit:
                verdict = "search"
                bad += 1
            else:
                verdict = "UNSOURCED"
                bad += 1
        print(f"{verdict:<11} {shown:<12} {url}")
    print(f"\nWebFetch calls in transcript: {len(fetches)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

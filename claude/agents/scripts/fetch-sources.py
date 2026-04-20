#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "feedparser",
#     "requests",
# ]
# ///
"""
fetch-sources.py — Deterministic source fetcher for the tech-watch pipeline.

Calls arXiv and GitHub APIs directly (no LLM, no API key required).
Produces raw-sources.json consumed by the tech-watch-scorer agent.

Usage:
    uv run fetch-sources.py "topic" [--days 20] [--max 30] [--output tech-watch/raw-sources.json]
    uv run fetch-sources.py "MCP server security" --days 30
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

import feedparser  # pyright: ignore[reportMissingImports]
import requests

# ---------------------------------------------------------------------------
# arXiv
# ---------------------------------------------------------------------------


def fetch_arxiv(query: str, days: int, max_results: int = 30) -> list[dict]:
    """Fetch recent papers from arXiv API. Free, no key required.

    Args:
        query: Free-text search query (passed to arXiv `all:` field).
        days: Only keep papers published within the last N days.
        max_results: Upper bound on results requested from arXiv.

    Returns:
        List of source dicts with keys: title, url, published, source,
        type, summary, authors, tags, engagement. Empty list on request
        failure.
    """
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  [arXiv] Request failed: {e}", file=sys.stderr)
        return []

    feed = feedparser.parse(resp.content)
    cutoff = datetime.now(UTC) - timedelta(days=days)
    results = []

    for entry in feed.entries:
        pub_date = datetime(*entry.published_parsed[:6], tzinfo=UTC)
        if pub_date < cutoff:
            continue

        authors = (
            ", ".join(a.name for a in entry.authors)
            if hasattr(entry, "authors")
            else ""
        )
        categories = (
            [t["term"] for t in entry.tags][:5] if hasattr(entry, "tags") else []
        )

        results.append(
            {
                "title": entry.title.replace("\n", " ").strip(),
                "url": entry.id,
                "published": pub_date.strftime("%Y-%m-%d"),
                "source": "arXiv",
                "type": "paper",
                "summary": entry.summary[:600].replace("\n", " ").strip(),
                "authors": authors,
                "tags": categories,
                "engagement": {},
            }
        )

    print(f"  [arXiv] {len(results)} papers in last {days} days", file=sys.stderr)
    return results


# ---------------------------------------------------------------------------
# GitHub
# ---------------------------------------------------------------------------


def fetch_github(query: str, days: int, max_results: int = 20) -> list[dict]:
    """Fetch recent/trending repos from GitHub Search API. No key = 10 req/min.

    Args:
        query: Free-text search query (combined with `pushed:>` filter).
        days: Only keep repos pushed within the last N days.
        max_results: Upper bound on results requested from GitHub (capped at 30).

    Returns:
        List of source dicts with keys: title, url, published, source,
        type, summary, authors, tags, engagement (stars/forks/watchers).
        Empty list on request failure.
    """
    cutoff = datetime.now(UTC) - timedelta(days=days)
    cutoff_str = cutoff.strftime("%Y-%m-%d")

    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"{query} pushed:>{cutoff_str}",
        "sort": "stars",
        "order": "desc",
        "per_page": min(max_results, 30),
    }
    headers = {"Accept": "application/vnd.github.v3+json"}

    # Use token from env if available (optional, higher rate limit)
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  [GitHub] Request failed: {e}", file=sys.stderr)
        return []

    data = resp.json()
    results = []

    for item in data.get("items", []):
        updated = item.get("pushed_at", item.get("updated_at", ""))
        if updated:
            updated_str = updated[:10]  # YYYY-MM-DD
        else:
            updated_str = ""

        results.append(
            {
                "title": item["full_name"],
                "url": item["html_url"],
                "published": updated_str,
                "source": "GitHub",
                "type": "repository",
                "summary": (item.get("description") or "No description")[:600],
                "authors": item.get("owner", {}).get("login", ""),
                "tags": (item.get("topics") or [])[:5],
                "engagement": {
                    "stars": item.get("stargazers_count", 0),
                    "forks": item.get("forks_count", 0),
                    "watchers": item.get("watchers_count", 0),
                },
            }
        )

    print(f"  [GitHub] {len(results)} repos in last {days} days", file=sys.stderr)
    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def deduplicate(sources: list[dict]) -> list[dict]:
    """Remove duplicate URLs, preserving first-seen order.

    Args:
        sources: List of source dicts, each expected to have a `url` key.

    Returns:
        List of sources with duplicate URLs removed.
    """
    seen: set[str] = set()
    unique = []
    for s in sources:
        url = s["url"]
        if url not in seen:
            seen.add(url)
            unique.append(s)
    return unique


def main():
    parser = argparse.ArgumentParser(
        description="Fetch raw sources for tech-watch pipeline"
    )
    parser.add_argument("topic", help="Search topic (e.g. 'MCP server security')")
    parser.add_argument(
        "--days", type=int, default=20, help="Look back N days (default: 20)"
    )
    parser.add_argument(
        "--max", type=int, default=30, help="Max results per source (default: 30)"
    )
    parser.add_argument(
        "--output", default="tech-watch/raw-sources.json", help="Output path"
    )
    args = parser.parse_args()

    print(
        f"Fetching sources for: '{args.topic}' (last {args.days} days)", file=sys.stderr
    )

    all_sources: list[dict] = []

    # arXiv
    all_sources.extend(fetch_arxiv(args.topic, args.days, args.max))
    time.sleep(1)  # Polite delay between APIs

    # GitHub
    all_sources.extend(fetch_github(args.topic, args.days, args.max))

    # Deduplicate
    all_sources = deduplicate(all_sources)

    # Build output
    output = {
        "topic": args.topic,
        "fetched_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "days_lookback": args.days,
        "source_counts": {
            "arxiv": sum(1 for s in all_sources if s["source"] == "arXiv"),
            "github": sum(1 for s in all_sources if s["source"] == "GitHub"),
        },
        "total": len(all_sources),
        "sources": all_sources,
    }

    # Write
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))

    print(f"Done: {len(all_sources)} sources → {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()

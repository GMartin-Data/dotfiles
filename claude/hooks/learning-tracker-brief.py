#!/usr/bin/env python3
"""SessionStart hook: display a compact learning dashboard.

Reads ~/.claude/agent-memory/learning-tracker/MEMORY.md and prints a brief
summary of active learning topics. Silent if nothing relevant to show.

Exit code is always 0 — a hook must never block session startup.
"""
from __future__ import annotations

import re
import sys
from datetime import date, datetime
from pathlib import Path

MEMORY_PATH = Path.home() / ".claude" / "agent-memory" / "learning-tracker" / "MEMORY.md"

FRESH_DAYS = 3
STALE_DAYS = 14


def parse_memory(text: str) -> tuple[dict[str, int], list[dict[str, str]]]:
    """Parse MEMORY.md into meta counters and a list of active topics.

    Returns (meta, active_topics). active_topics is a list of dicts with
    keys: name, last_contact (str or ''), next_step (str or '').
    """
    meta = {"active": 0, "completed": 0, "archived": 0}
    meta_match = re.search(
        r"Sujets actifs\s*:\s*(\d+)\s*\|\s*Compl[eé]t[eé]s\s*:\s*(\d+)\s*\|\s*Archiv[eé]s\s*:\s*(\d+)",
        text,
    )
    if meta_match:
        meta["active"] = int(meta_match.group(1))
        meta["completed"] = int(meta_match.group(2))
        meta["archived"] = int(meta_match.group(3))

    topics: list[dict[str, str]] = []
    blocks = re.split(r"^###\s+", text, flags=re.MULTILINE)[1:]
    for block in blocks:
        header_line, _, rest = block.partition("\n")
        if "[ACTIF]" not in header_line:
            continue
        name = header_line.split("[")[0].strip()
        last_contact = ""
        next_step = ""
        for line in rest.splitlines():
            m_contact = re.match(r"\s*-\s*Dernier contact\s*:\s*(\S+)", line)
            if m_contact:
                last_contact = m_contact.group(1).strip()
                continue
            m_next = re.match(r"\s*-\s*Prochaine [eé]tape\s*:\s*(.+)", line)
            if m_next:
                next_step = m_next.group(1).strip()
        topics.append({"name": name, "last_contact": last_contact, "next_step": next_step})
    return meta, topics


def days_since(iso_date: str) -> int | None:
    """Return days between iso_date (YYYY-MM-DD) and today, or None if unparseable."""
    try:
        d = datetime.strptime(iso_date, "%Y-%m-%d").date()
    except ValueError:
        return None
    return (date.today() - d).days


def color_for(days: int | None) -> str:
    if days is None:
        return "🟡"
    if days <= FRESH_DAYS:
        return "🟢"
    if days < STALE_DAYS:
        return "🟡"
    return "🔴"


def format_dashboard(meta: dict[str, int], topics: list[dict[str, str]]) -> str:
    today = date.today().isoformat()
    header = (
        f"📊 LEARNING — {today} "
        f"({meta['active']} actif{'s' if meta['active'] > 1 else ''} | "
        f"{meta['archived']} archivé{'s' if meta['archived'] > 1 else ''})"
    )
    lines = [header, ""]
    for t in topics:
        days = days_since(t["last_contact"])
        color = color_for(days)
        if days is None:
            freshness = "date inconnue"
        elif days == 0:
            freshness = "touché aujourd'hui"
        elif days == 1:
            freshness = "touché hier"
        elif days < STALE_DAYS:
            freshness = f"{days} jours"
        else:
            freshness = f"stale depuis {days} jours"
        lines.append(f"{color} {t['name']} — {freshness}")
        if t["next_step"]:
            lines.append(f"   → Prochaine étape : {t['next_step']}")
    return "\n".join(lines)


def should_display(topics: list[dict[str, str]]) -> bool:
    """Display only if at least one active topic has last_contact older than today."""
    if not topics:
        return False
    for t in topics:
        days = days_since(t["last_contact"])
        if days is None or days >= 1:
            return True
    return False


def main() -> int:
    if not MEMORY_PATH.exists():
        return 0
    try:
        text = MEMORY_PATH.read_text(encoding="utf-8")
    except OSError:
        return 0
    try:
        meta, topics = parse_memory(text)
    except Exception:
        return 0
    if not should_display(topics):
        return 0
    print(format_dashboard(meta, topics))
    return 0


if __name__ == "__main__":
    sys.exit(main())

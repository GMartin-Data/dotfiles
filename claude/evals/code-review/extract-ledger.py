#!/usr/bin/env python3
"""Print the final result text (the ledger) of one or more campaign transcripts.

Usage: extract-ledger.py <run-dir> [<run-dir> ...]
For each run dir, reads transcript.jsonl and prints the `result` event's text,
plus the cwd-check marker — the grading material for the truth table in README.
"""
import json
import pathlib
import sys

for run in sys.argv[1:]:
    run_path = pathlib.Path(run)
    transcript = run_path / "transcript.jsonl"
    print(f"\n{'=' * 72}\n== {run_path.name}")
    cwd_check = run_path / "cwd-check"
    print(f"== cwd-check: {cwd_check.read_text().strip() if cwd_check.exists() else 'absent'}")
    if not transcript.exists():
        print("== transcript absent")
        continue
    result = None
    n_events = 0
    for line in transcript.read_text().splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        n_events += 1
        if ev.get("type") == "result":
            result = ev
    if result is None:
        print(f"== pas d'event result ({n_events} events)")
        continue
    usage = result.get("usage", {})
    print(
        f"== events: {n_events} · duration: {result.get('duration_ms', 0) / 1000:.0f}s"
        f" · turns: {result.get('num_turns')} · out_tokens: {usage.get('output_tokens')}"
    )
    print(result.get("result", "(champ result vide)"))

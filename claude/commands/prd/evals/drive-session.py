#!/usr/bin/env python3
"""Turn-based driver for automated claude -p B sessions.

Feeds user message N+1 only after turn N's `result` event appears on stdout,
so the interview is exercised one turn at a time (unlike a naive full pipe,
which delivers every queued message at once).

Usage: drive-session.py <input.jsonl> <output.jsonl> <cwd> [extra claude flags...]
"""
import json
import subprocess
import sys
import threading

infile, outfile, cwd, *extra = sys.argv[1:]
with open(infile) as f:
    messages = [line for line in f if line.strip()]

cmd = [
    "claude", "-p",
    "--input-format", "stream-json",
    "--output-format", "stream-json",
    "--verbose",
    *extra,
]

proc = subprocess.Popen(
    cmd, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL, text=True, bufsize=1,
)
stdin, stdout = proc.stdin, proc.stdout
assert stdin is not None and stdout is not None

turn_done = threading.Event()

with open(outfile, "w") as out:

    def pump() -> None:
        for line in stdout:
            out.write(line)
            out.flush()
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") == "result":
                turn_done.set()

    reader = threading.Thread(target=pump, daemon=True)
    reader.start()

    for i, msg in enumerate(messages):
        turn_done.clear()
        stdin.write(msg)
        stdin.flush()
        if not turn_done.wait(timeout=420):
            print(f"TIMEOUT waiting for result after message {i + 1}", file=sys.stderr)
            proc.kill()
            sys.exit(1)
        print(f"turn {i + 1}/{len(messages)} done", file=sys.stderr)

    stdin.close()
    proc.wait(timeout=60)
    reader.join(timeout=10)

print(f"exit={proc.returncode}", file=sys.stderr)
sys.exit(proc.returncode or 0)

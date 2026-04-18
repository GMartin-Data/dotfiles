#!/usr/bin/env python3
"""PreToolUse hook to block access to sensitive .env files.

Template files (.env.example, .env.sample, .env.template, .env.dist) are
allowed, since they contain placeholders rather than secrets. The allowlist
is fail-closed: any unknown suffix is blocked by default.
"""
from __future__ import annotations

import json
import re
import sys

SAFE_ENV_SUFFIXES: frozenset[str] = frozenset({"example", "sample", "template", "dist"})

_ENV_FILE_PATTERN = re.compile(r'(?:^|[\s/\'"`])(\.env(?:\.[a-zA-Z0-9_-]+)?)\b')


def main() -> None:
    input_data = json.load(sys.stdin)
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    if tool_name in ("Read", "Edit", "Write"):
        file_path = tool_input.get("file_path", "")
        if is_env_file(file_path):
            print(f"BLOCKED: Access to '{file_path}' denied.", file=sys.stderr)
            sys.exit(2)

    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if references_env_file(command):
            print("BLOCKED: Bash command references sensitive .env file.", file=sys.stderr)
            sys.exit(2)

    sys.exit(0)


def is_env_file(path: str) -> bool:
    """Return True if the path points to a sensitive .env file.

    Template files matching the safe-suffix allowlist are excluded.

    Args:
        path: File path to inspect. Only the basename is considered.

    Returns:
        True if the file is considered sensitive and should be blocked.
    """
    filename = path.rstrip("/").split("/")[-1]

    if filename == ".env":
        return True

    if filename.startswith(".env."):
        suffix = filename[len(".env."):]
        return suffix not in SAFE_ENV_SUFFIXES

    return False


def references_env_file(command: str) -> bool:
    """Return True if the bash command references a sensitive .env file.

    Scans for .env[.suffix] tokens and applies the same safe-suffix
    allowlist as file-based tools, so a single source of truth drives both.

    Args:
        command: Bash command line to inspect.

    Returns:
        True if the command references a sensitive .env file.
    """
    for match in _ENV_FILE_PATTERN.finditer(command):
        token = match.group(1)
        if is_env_file(token):
            return True
    return False


def _self_test() -> None:
    """Run assertion-based tests. Invoke via: python3 protect_env.py --test"""
    assert is_env_file(".env") is True
    assert is_env_file(".env.local") is True
    assert is_env_file(".env.prod") is True
    assert is_env_file(".env.production") is True
    assert is_env_file(".env.example") is False
    assert is_env_file(".env.sample") is False
    assert is_env_file(".env.template") is False
    assert is_env_file(".env.dist") is False
    assert is_env_file(".environment") is False
    assert is_env_file("path/to/.env") is True
    assert is_env_file("path/to/.env.example") is False
    assert is_env_file("") is False

    assert references_env_file("cat .env") is True
    assert references_env_file("cat .env.example") is False
    assert references_env_file("cat path/to/.env.prod") is True
    assert references_env_file("cat 'quoted/.env'") is True
    assert references_env_file("cat .environment") is False
    assert references_env_file("echo hello") is False
    assert references_env_file("grep API_KEY .env.local") is True
    assert references_env_file("grep API_KEY .env.sample") is False

    print("All tests passed ✓")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        _self_test()
    else:
        main()

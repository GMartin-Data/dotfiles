#!/usr/bin/env python3
"""PreToolUse hook to block access to sensitive .env files.

Template files (.env.example, .env.sample, .env.template, .env.dist) are
allowed, since they contain placeholders rather than secrets. The allowlist
is fail-closed: any unknown suffix is blocked by default.

Bash commands are blocked only when the referenced token resolves (against
the session cwd) to an existing file — mentioning .env in prose (a commit
message, an echo) is allowed. Residual gaps are accepted (globs, variable
expansion, `cd` mid-command resolving against the starting cwd): this hook
is a guardrail against inadvertent access, not a sandbox.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SAFE_ENV_SUFFIXES: frozenset[str] = frozenset({"example", "sample", "template", "dist"})

_ENV_FILE_PATTERN = re.compile(
    r'(?:^|[\s\'"`])((?:[\w~.-]+/|/)*\.env(?:\.[a-zA-Z0-9_-]+)?)\b'
)


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
        cwd = input_data.get("cwd", "")
        if references_env_file(command, cwd):
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


def references_env_file(command: str, cwd: str) -> bool:
    """Return True if the bash command references a sensitive .env file.

    Scans for path tokens ending in .env[.suffix] and applies the same
    safe-suffix allowlist as file-based tools, so a single source of truth
    drives both. A token only counts as a reference if it resolves to an
    existing file — prose mentions are not references.

    Args:
        command: Bash command line to inspect.
        cwd: Directory the command runs in, used to resolve relative tokens.

    Returns:
        True if the command references a sensitive .env file that exists.
    """
    for match in _ENV_FILE_PATTERN.finditer(command):
        token = match.group(1)
        if is_env_file(token) and _points_to_existing_file(token, cwd):
            return True
    return False


def _points_to_existing_file(token: str, cwd: str) -> bool:
    """Return True if the token resolves to an existing file.

    Args:
        token: Path token extracted from the command (may be relative or ~).
        cwd: Base directory for resolving relative tokens.

    Returns:
        True if a file exists at the resolved path.
    """
    path = Path(token).expanduser()
    if not path.is_absolute():
        path = Path(cwd or ".") / path
    return path.is_file()


def _hook_exit_code(tool_name: str, tool_input: dict, cwd: str) -> int:
    """Invoke the hook end-to-end as Claude Code does: JSON on stdin, exit code out."""
    import subprocess

    payload = json.dumps({"tool_name": tool_name, "tool_input": tool_input, "cwd": cwd})
    result = subprocess.run(
        [sys.executable, __file__], input=payload, capture_output=True, text=True
    )
    return result.returncode


def _self_test() -> None:
    """Run assertion-based tests. Invoke via: python3 protect_env.py --test"""
    import tempfile
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

    # End-to-end Bash cases: block only when the referenced file actually
    # exists on disk — a token in prose (commit message, echo) is not a file.
    with tempfile.TemporaryDirectory() as with_env, \
            tempfile.TemporaryDirectory() as without_env:
        root = Path(with_env)
        for name in (".env", ".env.example", ".env.local", ".env.sample",
                     ".environment"):
            (root / name).touch()
        for sub in ("sub", "quoted"):
            (root / sub).mkdir()
        (root / "sub" / ".env.prod").touch()
        (root / "quoted" / ".env").touch()

        def bash(command: str, cwd: str) -> int:
            return _hook_exit_code("Bash", {"command": command}, cwd)

        assert bash("cat .env", with_env) == 2
        assert bash('bash -c "cat .env"', with_env) == 2
        assert bash("cat sub/.env.prod", with_env) == 2
        assert bash(f"cat {with_env}/.env", without_env) == 2
        assert bash("cat 'quoted/.env'", with_env) == 2
        assert bash("grep API_KEY .env.local", with_env) == 2
        assert bash("cat .env.example", with_env) == 0
        assert bash("grep API_KEY .env.sample", with_env) == 0
        assert bash("cat .environment", with_env) == 0
        assert bash("echo hello", with_env) == 0
        assert bash("cat .env", without_env) == 0
        assert bash('git commit -m "drop rules for .env files"', without_env) == 0

    print("All tests passed ✓")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        _self_test()
    else:
        main()

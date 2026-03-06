#!/usr/bin/env python3
"""PreToolUse hook to block all access to .env files."""

import json
import re
import sys


def main() -> None:
    input_data = json.load(sys.stdin)
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Check file-based tools (Read, Edit, Write)
    if tool_name in ("Read", "Edit", "Write"):
        file_path = tool_input.get("file_path", "")
        if is_env_file(file_path):
            print(f"BLOCKED: Access to '{file_path}' denied.", file=sys.stderr)
            sys.exit(2)

    # Check Bash commands (cat, grep, head, etc.)
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if references_env_file(command):
            print("BLOCKED: Bash command references .env file.", file=sys.stderr)
            sys.exit(2)

    sys.exit(0)


def is_env_file(path: str) -> bool:
    """Check if a path points to a .env file."""
    filename = path.rstrip("/").split("/")[-1]
    return filename == ".env" or filename.startswith(".env.")


def references_env_file(command: str) -> bool:
    """Check if a bash command references .env files."""
    return bool(re.search(r"\.env\b", command))


if __name__ == "__main__":
    main()

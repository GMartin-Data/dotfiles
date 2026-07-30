#!/usr/bin/env python3
"""Pre-commit hook: every staged dbt model must declare its partition column.

Blocks any staged .sql file that does not contain exactly one
`-- partition:` directive.
"""

import re
import subprocess
import sys

DIRECTIVE = re.compile(r"--\s*partition:")


def staged_sql_files() -> list[str]:
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return [f for f in out.splitlines() if f.endswith(".sql")]


def main() -> int:
    errors = []
    for path in staged_sql_files():
        with open(path, encoding="utf-8") as fh:
            # BUG under test (eval fixture): counts every match in the file,
            # including prose comments that merely mention "-- partition:".
            hits = DIRECTIVE.findall(fh.read())
        if len(hits) != 1:
            errors.append(
                f"{path}: expected exactly one '-- partition:' directive, found {len(hits)}"
            )
    for err in errors:
        print(err, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

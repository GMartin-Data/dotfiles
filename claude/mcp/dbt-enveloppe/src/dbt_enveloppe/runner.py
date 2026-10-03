"""Subprocess layer: the project's dbt, the canonical argv, no shell.

Every dbt call goes through ``uv run --project <dir> --no-sync dbt`` (plan
§1.2), with ``--project-dir``, ``--profiles-dir ~/.dbt`` and ``--target``
appended by the envelope (plan §3). Arguments are passed as a list.
"""

from __future__ import annotations

import subprocess
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from dbt_enveloppe.conditions import RefusalError

DEFAULT_TIMEOUT_S = 120.0


@dataclass(frozen=True)
class Result:
    """Captured outcome of one subprocess call.

    Attributes:
        argv: The exact command run.
        returncode: Exit code, or None when the call timed out.
        stdout: Captured standard output (dbt writes its errors there too).
        stderr: Captured standard error.
        duration_s: Wall-clock duration.
        timed_out: Whether the process was killed on timeout.
    """

    argv: tuple[str, ...]
    returncode: int | None
    stdout: str
    stderr: str
    duration_s: float
    timed_out: bool = False


def resolve_project_dir(env: Mapping[str, str]) -> Path:
    """Locate the dbt project from ``CLAUDE_PROJECT_DIR``, never from the cwd.

    Raises:
        RefusalError: If the variable is missing, the directory has no
            ``dbt_project.yml``, or ``.venv/bin/dbt`` is absent (run ``uv sync``).
    """
    raw = env.get("CLAUDE_PROJECT_DIR")
    if not raw:
        raise RefusalError(
            "CLAUDE_PROJECT_DIR is not set: the envelope only runs inside a project opened in Claude Code"
        )
    project_dir = Path(raw)
    if not (project_dir / "dbt_project.yml").is_file():
        raise RefusalError(f"no dbt_project.yml in {project_dir}: not a dbt project")
    if not (project_dir / ".venv" / "bin" / "dbt").exists():
        raise RefusalError(
            f"no .venv/bin/dbt in {project_dir}: run `uv sync` in the project first"
        )
    return project_dir


def dbt_argv(
    project_dir: Path,
    command: str,
    args: Sequence[str] = (),
    *,
    target: str = "dev",
) -> list[str]:
    """Build the canonical argv for one dbt command.

    ``--quiet`` is added to every command except ``debug`` (D1).
    ``--project-dir``, ``--profiles-dir`` and ``--target`` are appended last.
    """
    argv = [
        "uv",
        "run",
        "--project",
        str(project_dir),
        "--no-sync",
        "dbt",
        "--no-use-colors",
    ]
    if command != "debug":
        argv.append("--quiet")
    argv.append(command)
    argv.extend(args)
    argv.extend(
        [
            "--project-dir",
            str(project_dir),
            "--profiles-dir",
            str(Path.home() / ".dbt"),
            "--target",
            target,
        ]
    )
    return argv


def run(argv: Sequence[str], cwd: Path, timeout_s: float = DEFAULT_TIMEOUT_S) -> Result:
    """Run ``argv`` without a shell, stdin closed, and capture everything.

    A timeout kills the process and yields a ``Result`` with
    ``timed_out=True`` instead of raising.
    """
    start = time.monotonic()
    try:
        completed = subprocess.run(
            list(argv),
            cwd=cwd,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        # On POSIX the partial output carried by the exception is bytes even in text mode.
        return Result(
            tuple(argv),
            None,
            _as_text(exc.stdout),
            _as_text(exc.stderr),
            time.monotonic() - start,
            timed_out=True,
        )
    return Result(
        tuple(argv),
        completed.returncode,
        completed.stdout,
        completed.stderr,
        time.monotonic() - start,
    )


def _as_text(output: str | bytes | None) -> str:
    if output is None:
        return ""
    if isinstance(output, bytes):
        return output.decode(errors="replace")
    return output

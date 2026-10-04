"""Subprocess layer: project resolution, canonical argv, capture."""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from dbt_enveloppe.conditions import RefusalError
from dbt_enveloppe.runner import dbt_argv, resolve_project_dir, run

# --- resolve_project_dir ----------------------------------------------------


def test_resolve_requires_claude_project_dir() -> None:
    with pytest.raises(RefusalError, match="CLAUDE_PROJECT_DIR"):
        resolve_project_dir({})


def test_resolve_requires_dbt_project_yml(tmp_path: Path) -> None:
    with pytest.raises(RefusalError, match=r"dbt_project\.yml"):
        resolve_project_dir({"CLAUDE_PROJECT_DIR": str(tmp_path)})


def test_resolve_requires_the_project_venv(tmp_path: Path) -> None:
    (tmp_path / "dbt_project.yml").write_text("name: x\n")
    with pytest.raises(RefusalError, match="uv sync"):
        resolve_project_dir({"CLAUDE_PROJECT_DIR": str(tmp_path)})


def test_resolve_returns_the_project(project_dir: Path) -> None:
    assert resolve_project_dir({"CLAUDE_PROJECT_DIR": str(project_dir)}) == project_dir


# --- dbt_argv ---------------------------------------------------------------


def test_argv_is_the_canonical_call_through_the_project_uv(project_dir: Path) -> None:
    argv = dbt_argv(project_dir, "parse", ["--no-partial-parse", "--warn-error"])
    assert argv[:6] == ["uv", "run", "--project", str(project_dir), "--no-sync", "dbt"]
    assert argv[6:9] == ["--no-use-colors", "--quiet", "parse"]
    assert argv[9:11] == ["--no-partial-parse", "--warn-error"]
    assert argv[11:] == [
        "--project-dir",
        str(project_dir),
        "--profiles-dir",
        str(Path.home() / ".dbt"),
        "--target",
        "dev",
    ]


def test_argv_debug_is_never_quiet(project_dir: Path) -> None:
    argv = dbt_argv(project_dir, "debug")
    assert "--quiet" not in argv
    assert argv[argv.index("dbt") + 1 :][:2] == ["--no-use-colors", "debug"]


def test_argv_target_is_appended_as_given(project_dir: Path) -> None:
    argv = dbt_argv(project_dir, "show", ["--inline", "select 1"], target="ro")
    assert argv[-2:] == ["--target", "ro"]
    assert "select 1" in argv


# --- run --------------------------------------------------------------------


def test_run_captures_code_stdout_stderr(tmp_path: Path) -> None:
    result = run(["sh", "-c", "echo out; echo err >&2; exit 3"], cwd=tmp_path)
    assert result.returncode == 3
    assert result.stdout == "out\n"
    assert result.stderr == "err\n"
    assert not result.timed_out
    assert result.duration_s >= 0


def test_run_times_out_without_raising(tmp_path: Path) -> None:
    result = run(["sh", "-c", "echo partial; sleep 5"], cwd=tmp_path, timeout_s=0.3)
    assert result.timed_out
    assert result.returncode is None
    assert result.duration_s < 3


def test_run_timeout_kills_the_grandchild_too(tmp_path: Path) -> None:
    """`uv run` forks dbt: killing uv alone would leave dbt running on the warehouse."""
    marker = tmp_path / "survived"
    script = f"sh -c 'sleep 1; touch {marker}'; true"
    result = run(["sh", "-c", script], cwd=tmp_path, timeout_s=0.3)
    assert result.timed_out
    time.sleep(1.5)
    assert not marker.exists()


def test_run_refuses_when_the_launcher_cannot_start(tmp_path: Path) -> None:
    with pytest.raises(RefusalError, match="no-such-launcher"):
        run(["no-such-launcher", "run", "dbt"], cwd=tmp_path)


def test_run_uses_cwd_and_closes_stdin(tmp_path: Path) -> None:
    result = run(["sh", "-c", "pwd; cat"], cwd=tmp_path, timeout_s=5)
    assert result.stdout.strip() == str(tmp_path.resolve())
    assert result.returncode == 0

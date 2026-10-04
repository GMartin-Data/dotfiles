"""CLI: project from the environment, JSON outcome, session persisted in target/."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from conftest import COMPILE_DIM_CUSTOMERS, DEBUG_OK, LS_TWO_VIEWS, FakeRun

from dbt_enveloppe.cli import SESSION_FILE, main


def invoke(
    capsys: pytest.CaptureFixture[str],
    argv: list[str],
    fake: FakeRun,
    project_dir: Path | None,
) -> tuple[int, dict]:
    env = {"CLAUDE_PROJECT_DIR": str(project_dir)} if project_dir else {}
    code = main(argv, run=fake, env=env)
    out = capsys.readouterr().out
    return code, json.loads(out)


def test_missing_project_dir_is_a_json_refusal(
    capsys: pytest.CaptureFixture[str], fake_run: FakeRun
) -> None:
    code, outcome = invoke(capsys, ["parse"], fake_run, None)
    assert code == 1
    assert outcome["ok"] is False
    assert "CLAUDE_PROJECT_DIR" in outcome["error"]
    assert fake_run.calls == []


def test_parse_prints_the_outcome_and_exits_zero(
    capsys: pytest.CaptureFixture[str], fake_run: FakeRun, project_dir: Path
) -> None:
    fake_run.script("parse", 0, "")
    code, outcome = invoke(capsys, ["parse"], fake_run, project_dir)
    assert code == 0
    assert outcome == {"ok": True, "data": None, "error": None}


def test_failure_exits_one(
    capsys: pytest.CaptureFixture[str], fake_run: FakeRun, project_dir: Path
) -> None:
    fake_run.script("parse", 2, "Compilation Error\n")
    code, outcome = invoke(capsys, ["parse"], fake_run, project_dir)
    assert code == 1
    assert outcome["ok"] is False
    assert "Compilation Error" in outcome["error"]


def test_session_persists_across_invocations(
    capsys: pytest.CaptureFixture[str], fake_run: FakeRun, project_dir: Path
) -> None:
    fake_run.script("debug", 0, DEBUG_OK)
    fake_run.script("parse", 0, "")
    fake_run.script("ls", 0, LS_TWO_VIEWS)
    fake_run.script(
        "compile", 0, COMPILE_DIM_CUSTOMERS.replace("dim_customers", "stg_orders")
    )
    assert invoke(capsys, ["debug"], fake_run, project_dir)[0] == 0
    assert invoke(capsys, ["parse"], fake_run, project_dir)[0] == 0
    assert (project_dir / SESSION_FILE).exists()
    code, outcome = invoke(
        capsys,
        [
            "ls",
            "--select",
            "stg_orders stg_customers",
            "--expected",
            "stg_orders,stg_customers",
        ],
        fake_run,
        project_dir,
    )
    assert code == 0
    assert outcome["data"][0]["name"] == "stg_orders"
    code, outcome = invoke(
        capsys, ["compile", "--name", "stg_orders"], fake_run, project_dir
    )
    assert code == 0
    assert outcome["data"]["compiled"].startswith("select")


def test_refusal_is_reported_without_a_dbt_call(
    capsys: pytest.CaptureFixture[str], fake_run: FakeRun, project_dir: Path
) -> None:
    code, outcome = invoke(
        capsys, ["show", "--name", "tag:nightly"], fake_run, project_dir
    )
    assert code == 1
    assert outcome["ok"] is False
    assert fake_run.calls == []


def test_show_inline_and_codegen_arguments(
    capsys: pytest.CaptureFixture[str], fake_run: FakeRun, project_dir: Path
) -> None:
    fake_run.script("debug", 0, DEBUG_OK)
    fake_run.script("parse", 0, "")
    fake_run.script("show", 0, '{"show": [{"X": 1}]}')
    fake_run.script("run-operation", 0, "select 1 as id\n")
    fake_run.script("parse", 0, "")
    invoke(capsys, ["debug"], fake_run, project_dir)
    invoke(capsys, ["parse"], fake_run, project_dir)
    code, outcome = invoke(
        capsys,
        ["show-inline", "--sql", "select 1 as x", "--limit", "2"],
        fake_run,
        project_dir,
    )
    assert code == 0
    assert outcome["data"]["rows"] == [{"X": 1}]
    code, outcome = invoke(
        capsys,
        [
            "codegen",
            "--macro",
            "generate_base_model",
            "--args",
            '{"source_name": "tpch", "table_name": "ORDERS"}',
            "--output",
            "models/base_orders.sql",
        ],
        fake_run,
        project_dir,
    )
    assert code == 0
    assert outcome["data"]["path"] == "models/base_orders.sql"


def test_corrupt_session_file_starts_fresh(
    capsys: pytest.CaptureFixture[str], fake_run: FakeRun, project_dir: Path
) -> None:
    (project_dir / "target").mkdir()
    (project_dir / SESSION_FILE).write_text("{not json")
    fake_run.script("parse", 0, "")
    code, _ = invoke(capsys, ["parse"], fake_run, project_dir)
    assert code == 0

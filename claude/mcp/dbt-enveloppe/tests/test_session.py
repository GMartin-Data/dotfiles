"""Session: canonical calls per tool, preconditions (S1, L2, D3), state."""

from __future__ import annotations

import json
from pathlib import Path

from conftest import (
    COMPILE_DIM_CUSTOMERS,
    DEBUG_OK,
    LS_TWO_VIEWS,
    MODEL_YAML_DIM_CUSTOMERS,
    MODEL_YAML_UNBUILT,
    SHOW_DIM_CUSTOMERS,
    FakeRun,
    make_ready,
    run_results,
    write_run_results,
)

from dbt_enveloppe.session import Session, changed_files, fingerprint

# --- fingerprint ------------------------------------------------------------


def test_fingerprint_ignores_dbt_output_dirs_and_hidden_entries(
    project_dir: Path,
) -> None:
    for name in ("target", "logs", "dbt_packages"):
        (project_dir / name).mkdir(exist_ok=True)
        (project_dir / name / "noise.json").write_text("{}")
    (project_dir / ".user.yml").write_text("id: 1\n")
    files = fingerprint(project_dir).files
    assert set(files) == {
        "dbt_project.yml",
        "models/stg_orders.sql",
        "models/stg_customers.sql",
    }


def test_changed_files_detects_add_remove_modify(project_dir: Path) -> None:
    before = fingerprint(project_dir)
    (project_dir / "models" / "stg_orders.sql").write_text("select 2 as id, 'x' as y\n")
    (project_dir / "models" / "stg_customers.sql").unlink()
    (project_dir / "models" / "dim_customers.sql").write_text("select 1\n")
    changed = changed_files(before, fingerprint(project_dir))
    assert set(changed) == {
        "models/stg_orders.sql",
        "models/stg_customers.sql",
        "models/dim_customers.sql",
    }
    assert changed_files(before, before) == []


# --- dbt output paths -------------------------------------------------------


def _write_under(project_dir: Path, *relatives: str) -> None:
    for relative in relatives:
        path = project_dir / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("x")


def test_custom_output_paths_from_the_project_file_are_not_file_changes(
    project_dir: Path, fake_run: FakeRun
) -> None:
    (project_dir / "dbt_project.yml").write_text(
        "name: testbed\nversion: '1.0'\n"
        "target-path: build/dbt\nlog-path: build/logs\npackages-install-path: packages\n"
    )
    session = Session(project_dir, fake_run, env={})
    make_ready(session, fake_run)
    _write_under(
        project_dir, "build/dbt/manifest.json", "build/logs/dbt.log", "packages/u/m.sql"
    )
    fake_run.script("ls", 0, LS_TWO_VIEWS)
    assert session.ls("stg_orders stg_customers", ["stg_orders", "stg_customers"]).ok


def test_env_target_path_wins_over_the_project_file(
    project_dir: Path, fake_run: FakeRun
) -> None:
    (project_dir / "dbt_project.yml").write_text(
        "name: testbed\nversion: '1.0'\ntarget-path: build\n"
    )
    session = Session(project_dir, fake_run, env={"DBT_ENGINE_TARGET_PATH": "out"})
    make_ready(session, fake_run)
    _write_under(project_dir, "out/manifest.json")
    fake_run.script("ls", 0, LS_TWO_VIEWS)
    assert session.ls("stg_orders stg_customers", ["stg_orders", "stg_customers"]).ok
    _write_under(project_dir, "build/manifest.json")
    outcome = session.ls("stg_orders stg_customers", ["stg_orders", "stg_customers"])
    assert not outcome.ok
    assert "build/manifest.json" in outcome.error


def test_build_reads_run_results_from_the_custom_target_path(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run, env={"DBT_ENGINE_TARGET_PATH": "out"})
    make_ready(session, fake_run)
    document = run_results({"stg_orders": "success", "stg_customers": "success"})

    def write_out() -> None:
        (project_dir / "out").mkdir(exist_ok=True)
        (project_dir / "out" / "run_results.json").write_text(json.dumps(document))

    fake_run.script("build", 0, "", side_effect=write_out)
    assert session.build("stg_orders stg_customers").ok


# --- canonical calls --------------------------------------------------------


def test_ls_canonical_call(project_dir: Path, fake_run: FakeRun) -> None:
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run, ls_select="tag:nightly")
    argv = fake_run.argv_for("ls")
    i = argv.index("ls")
    assert argv[i - 1] == "--quiet"
    assert argv[i + 1 :][:9] == [
        "--select",
        "tag:nightly",
        "--resource-type",
        "model",
        "--output",
        "json",
        "--output-keys",
        "name config.materialized",
        "--warn-error",
    ]


def test_compile_canonical_call_and_data(project_dir: Path, fake_run: FakeRun) -> None:
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run)
    fake_run.script(
        "compile", 0, COMPILE_DIM_CUSTOMERS.replace("dim_customers", "stg_orders")
    )
    outcome = session.compile("stg_orders", full_refresh=True)
    assert outcome.ok
    assert outcome.data["materialized"] == "view"
    argv = fake_run.argv_for("compile")
    i = argv.index("compile")
    assert argv[i + 1 :][:6] == [
        "--select",
        "stg_orders",
        "--no-introspect",
        "--output",
        "json",
        "--full-refresh",
    ]
    assert argv[-2:] == ["--target", "ro"]


def test_show_canonical_call_joins_materialization(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run)
    fake_run.script(
        "show", 0, SHOW_DIM_CUSTOMERS.replace("dim_customers", "stg_orders")
    )
    outcome = session.show("stg_orders", limit=3)
    assert outcome.ok
    assert outcome.data["materialized"] == "view"
    argv = fake_run.argv_for("show")
    i = argv.index("show")
    assert argv[i + 1 :][:6] == [
        "--select",
        "stg_orders",
        "--limit",
        "3",
        "--output",
        "json",
    ]
    assert argv[-2:] == ["--target", "ro"]


def test_show_inline_canonical_call(project_dir: Path, fake_run: FakeRun) -> None:
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run)
    fake_run.script("show", 0, '{"show": [{"X": 1}]}')
    assert session.show_inline("select 1 as x;", limit=-1).ok
    argv = fake_run.argv_for("show")
    i = argv.index("show")
    assert argv[i + 1 :][:6] == [
        "--inline",
        "select 1 as x",
        "--limit",
        "-1",
        "--output",
        "json",
    ]
    assert argv[-2:] == ["--target", "ro"]


def test_build_canonical_call(project_dir: Path, fake_run: FakeRun) -> None:
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run)
    document = run_results(
        {"stg_orders": "success", "stg_customers": "success"}, invocation_id="inv-new"
    )
    fake_run.script(
        "build", 0, "", side_effect=lambda: write_run_results(project_dir, document)
    )
    assert session.build("stg_orders stg_customers", full_refresh=True).ok
    argv = fake_run.argv_for("build")
    i = argv.index("build")
    assert argv[i - 1] == "--quiet"
    assert argv[i + 1 :][:3] == [
        "--select",
        "stg_orders stg_customers",
        "--full-refresh",
    ]
    assert argv[-2:] == ["--target", "dev"]


# --- preconditions: no dbt call on refusal ----------------------------------


def test_ls_requires_a_parse(project_dir: Path, fake_run: FakeRun) -> None:
    outcome = Session(project_dir, fake_run).ls("stg_orders", ["stg_orders"])
    assert not outcome.ok
    assert "parse" in outcome.error.lower()
    assert fake_run.calls == []


def test_compile_requires_debug_then_parse_then_ls(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run)
    assert "debug" in session.compile("stg_orders").error.lower()
    fake_run.script("debug", 0, DEBUG_OK)
    assert session.debug().ok
    assert "parse" in session.compile("stg_orders").error.lower()
    fake_run.script("parse", 0, "")
    assert session.parse().ok
    assert "ls" in session.compile("stg_orders").error.lower()
    assert [c for c in fake_run.calls if "compile" in c] == []


def test_failed_debug_blocks_the_connected_tools(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run)
    fake_run.script(
        "debug",
        1,
        "17:55:09    Connection test: [ERROR]\n\n17:55:09  1 check failed:\n",
    )
    fake_run.script("parse", 0, "")
    assert not session.debug().ok
    assert session.parse().ok
    assert not session.show_inline("select 1").ok
    assert "debug" in session.show_inline("select 1").error.lower()


def test_unsupported_dbt_version_blocks_the_connected_tools(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run)
    fake_run.script(
        "debug", 0, DEBUG_OK.replace("dbt version: 1.12.5", "dbt version: 1.11.0")
    )
    fake_run.script("parse", 0, "")
    fake_run.script("ls", 0, LS_TWO_VIEWS)
    assert session.debug().ok
    assert session.parse().ok
    assert session.ls("stg_orders stg_customers", ["stg_orders", "stg_customers"]).ok
    outcome = session.compile("stg_orders")
    assert not outcome.ok
    assert "1.11.0" in outcome.error


def test_file_change_since_parse_is_refused_and_named(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run)
    (project_dir / "models" / "stg_orders.sql").write_text(
        "select 2 as id, 'changed' as y\n"
    )
    outcome = session.compile("stg_orders")
    assert not outcome.ok
    assert "models/stg_orders.sql" in outcome.error
    assert "parse" in outcome.error.lower()


def test_a_new_parse_resets_validated_selections(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run)
    fake_run.script("parse", 0, "")
    assert session.parse().ok
    outcome = session.compile("stg_orders")
    assert not outcome.ok
    assert "ls" in outcome.error.lower()


def test_build_requires_the_exact_validated_selection(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run, ls_select="tag:nightly")
    outcome = session.build("stg_orders")
    assert not outcome.ok
    assert "ls" in outcome.error.lower()
    assert [c for c in fake_run.calls if "build" in c] == []


def test_selection_is_normalized_between_ls_and_build(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run, ls_select=" stg_orders stg_customers ")
    assert fake_run.argv_for("ls")[fake_run.argv_for("ls").index("--select") + 1] == (
        "stg_orders stg_customers"
    )
    document = run_results({"stg_orders": "success", "stg_customers": "success"})
    fake_run.script(
        "build", 0, "", side_effect=lambda: write_run_results(project_dir, document)
    )
    assert session.build(" stg_orders stg_customers").ok
    argv = fake_run.argv_for("build")
    assert argv[argv.index("--select") + 1] == "stg_orders stg_customers"


def test_failed_ls_does_not_validate_anything(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run)
    fake_run.script("debug", 0, DEBUG_OK)
    fake_run.script("parse", 0, "")
    fake_run.script("ls", 0, LS_TWO_VIEWS)
    session.debug()
    session.parse()
    assert not session.ls("stg_orders stg_customers", ["stg_orders"]).ok
    assert "ls" in session.compile("stg_orders").error.lower()


# --- build ------------------------------------------------------------------


def test_build_detects_a_stale_run_results(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run)
    stale = run_results(
        {"stg_orders": "success", "stg_customers": "success"}, invocation_id="inv-old"
    )
    write_run_results(project_dir, stale)
    fake_run.script("build", 0, "")
    outcome = session.build("stg_orders stg_customers")
    assert not outcome.ok
    assert "run_results.json" in outcome.error


def test_build_reports_model_materializations_from_ls(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run)
    document = run_results(
        {"stg_orders": "success", "stg_customers": "success"}, invocation_id="inv-new"
    )
    fake_run.script(
        "build", 0, "", side_effect=lambda: write_run_results(project_dir, document)
    )
    outcome = session.build("stg_orders stg_customers")
    assert outcome.ok
    assert {m["materialized"] for m in outcome.data["models"]} == {"view"}


# --- codegen ----------------------------------------------------------------


def test_codegen_writes_the_file_reparses_and_hides_the_content(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run)
    fake_run.script("run-operation", 0, MODEL_YAML_DIM_CUSTOMERS)
    fake_run.script("parse", 0, "")
    outcome = session.codegen(
        "generate_model_yaml",
        {"model_names": ["dim_customers"]},
        "models/dim_customers.yml",
    )
    assert outcome.ok
    assert outcome.data == {
        "path": "models/dim_customers.yml",
        "bytes": len(MODEL_YAML_DIM_CUSTOMERS),
        "columns": 4,
    }
    assert (
        project_dir / "models" / "dim_customers.yml"
    ).read_text() == MODEL_YAML_DIM_CUSTOMERS
    argv = fake_run.argv_for("run-operation")
    i = argv.index("run-operation")
    assert argv[i + 1] == "generate_model_yaml"
    assert argv[i + 2] == "--args"
    assert json.loads(argv[i + 3]) == {"model_names": ["dim_customers"]}
    assert argv[-2:] == ["--target", "ro"]
    assert fake_run.calls[-1] is fake_run.argv_for("parse")
    assert "columns" in outcome.data and "content" not in outcome.data


def test_codegen_removes_the_file_when_the_parse_fails(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run)
    fake_run.script("run-operation", 0, MODEL_YAML_DIM_CUSTOMERS)
    fake_run.script(
        "parse", 2, "Compilation Error\n  patch for unknown model 'dim_customers'\n"
    )
    outcome = session.codegen(
        "generate_model_yaml",
        {"model_names": ["dim_customers"]},
        "models/dim_customers.yml",
    )
    assert not outcome.ok
    assert "unknown model" in outcome.error
    assert not (project_dir / "models" / "dim_customers.yml").exists()


def test_codegen_removes_the_file_when_columns_are_empty(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run)
    fake_run.script("run-operation", 0, MODEL_YAML_UNBUILT)
    outcome = session.codegen(
        "generate_model_yaml", {"model_names": ["unbuilt_model"]}, "models/unbuilt.yml"
    )
    assert not outcome.ok
    assert not (project_dir / "models" / "unbuilt.yml").exists()
    assert [
        c for c in fake_run.calls if "parse" in c and c is not fake_run.calls[1]
    ] == []


def test_codegen_refuses_an_existing_path_without_calling_dbt(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run)
    calls_before = len(fake_run.calls)
    outcome = session.codegen(
        "generate_base_model",
        {"source_name": "tpch", "table_name": "ORDERS"},
        "models/stg_orders.sql",
    )
    assert not outcome.ok
    assert len(fake_run.calls) == calls_before
    assert (project_dir / "models" / "stg_orders.sql").read_text() == "select 1 as id\n"


def test_codegen_generate_source_always_asks_for_columns(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run)
    source_yaml = (
        "version: 2\nsources:\n  - name: tpch\n    tables:\n"
        "      - name: ORDERS\n        columns:\n          - name: O_ORDERKEY\n"
    )
    fake_run.script("run-operation", 0, source_yaml)
    fake_run.script("parse", 0, "")
    assert session.codegen(
        "generate_source", {"schema_name": "TPCH_SF1"}, "models/sources.yml"
    ).ok
    argv = fake_run.argv_for("run-operation")
    args = json.loads(argv[argv.index("--args") + 1])
    assert args == {"schema_name": "TPCH_SF1", "generate_columns": True}


def test_codegen_failed_run_operation_returns_the_message(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run)
    fake_run.script(
        "run-operation",
        2,
        "17:59:00  [ERROR]: Encountered an error:\n  dbt could not find a macro with the name 'generate_source'\n",
    )
    outcome = session.codegen(
        "generate_source", {"schema_name": "X"}, "models/sources.yml"
    )
    assert not outcome.ok
    assert "could not find a macro" in outcome.error
    assert not (project_dir / "models" / "sources.yml").exists()


# --- persistence ------------------------------------------------------------


def test_round_trip_keeps_the_session_ready(
    project_dir: Path, fake_run: FakeRun
) -> None:
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run)
    restored = Session.from_dict(
        project_dir, json.loads(json.dumps(session.to_dict())), fake_run
    )
    fake_run.script(
        "compile", 0, COMPILE_DIM_CUSTOMERS.replace("dim_customers", "stg_orders")
    )
    assert restored.compile("stg_orders").ok

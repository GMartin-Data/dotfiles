"""One explicit failure per line of principle 2 (spec part I).

Each test names its line of the principle 2 table. Where the envelope's
answer is structural (an option always added or never added), the test
checks the argv the session builds; where it is a judgement on the output,
the test checks the condition function.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from conftest import (
    DEBUG_OK,
    MODEL_YAML_UNBUILT,
    PARSE_WARNING,
    SHOW_INLINE_CREATE_TABLE,
    FakeRun,
    make_ready,
)

from dbt_enveloppe.conditions import (
    RefusalError,
    check_codegen_output,
    check_compile,
    check_debug,
    check_ls,
    check_parse,
    check_show,
    normalize_inline_sql,
    validate_codegen_request,
    validate_node_name,
)
from dbt_enveloppe.session import Session


def test_line1_ls_empty_selection_is_a_failure() -> None:
    """Line 1: ``ls`` on an empty selection or a bare wildcard exits 0, prints nothing."""
    outcome = check_ls(0, "", ["stg_orders"])
    assert not outcome.ok
    assert "no model" in outcome.error.lower()


def test_line2_show_refuses_tag_and_multiple_selections() -> None:
    """Line 2: ``show`` with ``tag:x`` or a list exits 0 without a preview."""
    for name in (
        "tag:nightly",
        "stg_orders stg_customers",
        "stg_orders+",
        "+stg_orders",
    ):
        with pytest.raises(RefusalError):
            validate_node_name(name)
    # And if such an output ever reaches the check: no `show` key = failure.
    assert not check_show(0, "").ok
    assert not check_show(0, '{"node": "stg_orders"}').ok


def test_line3_show_zero_rows_on_built_incremental_is_flagged() -> None:
    """Line 3: a built ``incremental`` model shows 0 rows; the envelope says why (H3)."""
    outcome = check_show(
        0, '{"node": "fct_orders", "show": []}', materialized="incremental"
    )
    assert outcome.ok
    assert outcome.data["row_count"] == 0
    assert "incremental" in outcome.data["note"].lower()


def test_line4_compile_without_sql_is_a_failure() -> None:
    """Line 4: ``compile`` with ``tag:x`` exits 0 but prints no SQL."""
    assert not check_compile(0, "").ok
    assert not check_compile(0, '{"node": "stg_orders", "compiled": ""}').ok


def test_line5_parse_cache_cannot_mask_a_warning(
    project_dir: Path, fake_run: FakeRun
) -> None:
    """Line 5: the second ``parse --warn-error`` exits 0 because the cache masks the warning."""
    fake_run.script("parse", 0, "")
    Session(project_dir, fake_run).parse()
    argv = fake_run.argv_for("parse")
    assert "--no-partial-parse" in argv
    assert "--warn-error" in argv
    assert argv.index("--quiet") < argv.index("parse")
    # A warning that does come through is a failure even with exit code 0.
    assert not check_parse(0, PARSE_WARNING).ok


def test_line6_model_yaml_without_columns_is_a_failure() -> None:
    """Line 6: ``generate_model_yaml`` on an unbuilt model exits 0 with empty ``columns:``."""
    outcome = check_codegen_output("generate_model_yaml", MODEL_YAML_UNBUILT)
    assert not outcome.ok
    assert "column" in outcome.error.lower()


def test_line7_codegen_log_header_is_refused(
    project_dir: Path, fake_run: FakeRun
) -> None:
    """Line 7: ``codegen`` without ``--quiet`` writes a file whose YAML is invalid."""
    polluted = "17:50:20  Running with dbt=1.12.5\n17:50:20  Registered adapter: snowflake=1.12.1\nversion: 2\nmodels: []\n"
    assert not check_codegen_output("generate_model_yaml", polluted).ok
    # Structural: the envelope puts --quiet before run-operation (G2).
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run)
    fake_run.script("run-operation", 0, "select 1 as id\n")
    fake_run.script("parse", 0, "")
    session.codegen(
        "generate_base_model",
        {"source_name": "tpch", "table_name": "ORDERS"},
        "models/base.sql",
    )
    argv = fake_run.argv_for("run-operation")
    assert argv.index("--quiet") < argv.index("run-operation")


def test_line8_run_operation_outside_the_whitelist_is_refused(
    project_dir: Path,
) -> None:
    """Line 8: ``run-operation --sql`` writes to the warehouse; only codegen macros exist here."""
    for macro in ("t_exec", "t_rows", "drop_everything", ""):
        with pytest.raises(RefusalError):
            validate_codegen_request(macro, "models/out.yml", project_dir)
    assert not hasattr(Session, "run_operation")


def test_line9_debug_is_never_quiet_and_an_empty_failure_is_explicit(
    project_dir: Path, fake_run: FakeRun
) -> None:
    """Line 9: ``debug --quiet`` on an unreachable database exits 1 with 0 bytes."""
    fake_run.script("debug", 0, DEBUG_OK)
    Session(project_dir, fake_run).debug()
    assert "--quiet" not in fake_run.argv_for("debug")
    outcome = check_debug(1, "")
    assert not outcome.ok
    assert "1" in outcome.error


def test_line10_show_inline_accepts_select_only_and_detects_a_statement_result(
    project_dir: Path, fake_run: FakeRun
) -> None:
    """Line 10: ``show --inline "create table ..."`` exits 0 and persists the table."""
    with pytest.raises(RefusalError):
        normalize_inline_sql("create table t as select 1 as id")
    with pytest.raises(RefusalError):
        normalize_inline_sql("select 1; drop table t")
    # Real T3 output under the writer role: a status row, not a query result.
    assert not check_show(0, SHOW_INLINE_CREATE_TABLE).ok
    # Structural: the read-only target is imposed (H7).
    session = Session(project_dir, fake_run)
    make_ready(session, fake_run)
    fake_run.script("show", 0, '{"show": [{"X": 1}]}')
    session.show_inline("select 1 as x")
    argv = fake_run.argv_for("show")
    assert argv[argv.index("--target") + 1] == "ro"

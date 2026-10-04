"""Conditions of success (spec III §D, plan §1.1 and §3) beyond principle 2."""

from __future__ import annotations

from pathlib import Path

import pytest
from conftest import (
    COMPILE_DIM_CUSTOMERS,
    DEBUG_CONNECTION_FAILED,
    DEBUG_OK,
    LS_TWO_VIEWS,
    MODEL_YAML_DIM_CUSTOMERS,
    RO_INSUFFICIENT_PRIVILEGES,
    SHOW_DIM_CUSTOMERS,
    run_results,
)

from dbt_enveloppe.conditions import (
    MESSAGE_TRUNCATION,
    RefusalError,
    check_build,
    check_codegen_output,
    check_compile,
    check_debug,
    check_ls,
    check_parse,
    check_show,
    normalize_inline_sql,
    validate_codegen_request,
    validate_dbt_version,
    validate_limit,
    validate_node_name,
    validate_select,
)

# --- debug ------------------------------------------------------------------


def test_debug_keeps_verdict_lines_and_versions_only() -> None:
    outcome = check_debug(0, DEBUG_OK)
    assert outcome.ok
    assert outcome.data["dbt_version"] == "1.12.5"
    assert outcome.data["adapter_version"] == "1.12.1"
    lines = outcome.data["lines"]
    assert any("[OK found and valid]" in line for line in lines)
    assert any("[OK connection ok]" in line for line in lines)
    assert "All checks passed!" in lines
    joined = "\n".join(lines)
    for secret in ("account:", "user:", "warehouse:", "role:", "ORG-ACCOUNT"):
        assert secret not in joined
    assert not any(line[:2].isdigit() and line[2] == ":" for line in lines)


def test_debug_failure_keeps_error_lines_and_explanation() -> None:
    outcome = check_debug(1, DEBUG_CONNECTION_FAILED)
    assert not outcome.ok
    assert "[ERROR]" in outcome.error
    assert "unable to connect" in outcome.error
    assert "account:" not in outcome.error


def test_debug_nonzero_with_all_ok_lines_is_still_a_failure() -> None:
    assert not check_debug(2, DEBUG_OK).ok


# --- parse ------------------------------------------------------------------


def test_parse_silent_success() -> None:
    outcome = check_parse(0, "")
    assert outcome.ok
    assert outcome.data is None


def test_parse_whitespace_only_output_is_success() -> None:
    assert check_parse(0, "\n").ok


def test_parse_error_returns_the_message() -> None:
    outcome = check_parse(
        2, "Compilation Error\n  Model 'x' depends on 'y' which was not found\n"
    )
    assert not outcome.ok
    assert "depends on 'y'" in outcome.error


# --- ls ---------------------------------------------------------------------


def test_ls_matching_list_in_dbt_order() -> None:
    outcome = check_ls(0, LS_TWO_VIEWS, ["stg_customers", "stg_orders"])
    assert outcome.ok
    assert outcome.data == [
        {"name": "stg_orders", "materialized": "view"},
        {"name": "stg_customers", "materialized": "view"},
    ]


def test_ls_mismatch_names_missing_and_unexpected() -> None:
    outcome = check_ls(0, LS_TWO_VIEWS, ["stg_orders", "dim_customers"])
    assert not outcome.ok
    assert "dim_customers" in outcome.error
    assert "stg_customers" in outcome.error


def test_ls_rejects_empty_expected() -> None:
    assert not check_ls(0, LS_TWO_VIEWS, []).ok


def test_ls_rejects_non_json_output() -> None:
    assert not check_ls(
        0, "17:58:03  Running with dbt=1.12.5\n" + LS_TWO_VIEWS, ["stg_orders"]
    ).ok


def test_ls_nonzero_is_a_failure_with_message() -> None:
    outcome = check_ls(
        2,
        "17:58:03  [ERROR]: The selection criterion 'x' does not match any nodes\n",
        ["x"],
    )
    assert not outcome.ok
    assert "does not match" in outcome.error


# --- compile ----------------------------------------------------------------


def test_compile_returns_node_and_sql() -> None:
    outcome = check_compile(0, COMPILE_DIM_CUSTOMERS)
    assert outcome.ok
    assert outcome.data["node"] == "dim_customers"
    assert outcome.data["compiled"].startswith("select")


def test_compile_nonzero_is_a_failure_with_message() -> None:
    outcome = check_compile(
        2, "Compilation Error in model x\n  'undefined_macro' is undefined\n"
    )
    assert not outcome.ok
    assert "undefined_macro" in outcome.error


# --- show -------------------------------------------------------------------


def test_show_returns_rows_and_materialization() -> None:
    outcome = check_show(0, SHOW_DIM_CUSTOMERS, materialized="table")
    assert outcome.ok
    assert outcome.data["node"] == "dim_customers"
    assert outcome.data["materialized"] == "table"
    assert outcome.data["row_count"] == 1
    assert outcome.data["rows"][0]["CUSTOMER_ID"] == 1
    assert outcome.data["note"] is None


def test_show_truncates_to_max_rows_with_a_note() -> None:
    rows = ", ".join(f'{{"X": {i}}}' for i in range(60))
    outcome = check_show(0, f'{{"node": "m", "show": [{rows}]}}', max_rows=50)
    assert outcome.ok
    assert len(outcome.data["rows"]) == 50
    assert outcome.data["row_count"] == 60
    assert "truncated" in outcome.data["note"].lower()


def test_show_zero_rows_on_a_table_has_no_note() -> None:
    outcome = check_show(0, '{"node": "m", "show": []}', materialized="table")
    assert outcome.ok
    assert outcome.data["note"] is None


def test_show_nonzero_is_a_failure_with_message() -> None:
    outcome = check_show(2, RO_INSUFFICIENT_PRIVILEGES)
    assert not outcome.ok
    assert "Insufficient privileges" in outcome.error


# --- build ------------------------------------------------------------------

EXPECTED = {"stg_orders": "view", "stg_customers": "view"}


def test_build_success_summarizes_statuses_and_models() -> None:
    document = run_results(
        {"stg_orders": "success", "stg_customers": "success"},
        {"unique_stg_orders_id": "pass", "not_null_stg_orders_id": "pass"},
        invocation_id="inv-2",
    )
    outcome = check_build(0, "", document, EXPECTED, previous_invocation_id="inv-1")
    assert outcome.ok
    assert outcome.data["counts"] == {"success": 2, "pass": 2}
    assert {
        "name": "stg_orders",
        "materialized": "view",
        "status": "success",
    } in outcome.data["models"]
    assert outcome.data["warnings"] == []


def test_build_not_rewritten_artifact_is_a_failure() -> None:
    document = run_results(
        {"stg_orders": "success", "stg_customers": "success"}, invocation_id="inv-1"
    )
    outcome = check_build(0, "", document, EXPECTED, previous_invocation_id="inv-1")
    assert not outcome.ok
    assert "run_results.json" in outcome.error


def test_build_not_rewritten_artifact_reports_stdout_tail() -> None:
    """A startup failure leaves the old artifact in place: the cause is in stdout."""
    document = run_results(
        {"stg_orders": "success", "stg_customers": "success"}, invocation_id="inv-1"
    )
    outcome = check_build(
        2,
        "Runtime Error\n  Could not find profile named 'testbed'\n",
        document,
        EXPECTED,
        previous_invocation_id="inv-1",
    )
    assert not outcome.ok
    assert "exited 2" in outcome.error
    assert "Could not find profile" in outcome.error
    assert "run_results.json" in outcome.error


def test_build_missing_artifact_reports_stdout_tail() -> None:
    outcome = check_build(
        2, "Compilation Error in model stg_orders\n  boom\n", None, EXPECTED, None
    )
    assert not outcome.ok
    assert "boom" in outcome.error


def test_build_empty_results_is_a_failure() -> None:
    document = run_results({}, invocation_id="inv-2")
    assert not check_build(0, "", document, EXPECTED, "inv-1").ok


@pytest.mark.parametrize(
    "status", ["error", "fail", "skipped", "runtime error", "partial success"]
)
def test_build_any_failing_status_is_a_failure(status: str) -> None:
    document = run_results(
        {"stg_orders": "success", "stg_customers": "success"},
        {"unique_stg_orders_id": status},
        invocation_id="inv-2",
    )
    outcome = check_build(0, "", document, EXPECTED, "inv-1")
    assert not outcome.ok
    assert "unique_stg_orders_id" in outcome.error


def test_build_error_message_is_truncated() -> None:
    long_message = "x" * (MESSAGE_TRUNCATION * 3)
    document = run_results(
        {"stg_orders": "error", "stg_customers": "success"},
        invocation_id="inv-2",
        messages={"stg_orders": long_message},
    )
    outcome = check_build(1, "", document, EXPECTED, "inv-1")
    assert not outcome.ok
    assert "stg_orders" in outcome.error
    assert len(outcome.error) < MESSAGE_TRUNCATION * 2


def test_build_executed_models_must_equal_validated_selection() -> None:
    document = run_results(
        {"stg_orders": "success", "dim_customers": "success"}, invocation_id="inv-2"
    )
    outcome = check_build(0, "", document, EXPECTED, "inv-1")
    assert not outcome.ok
    assert "dim_customers" in outcome.error
    assert "stg_customers" in outcome.error


def test_build_warn_is_success_but_reported() -> None:
    document = run_results(
        {"stg_orders": "success", "stg_customers": "success"},
        {"accepted_values_status": "warn"},
        invocation_id="inv-2",
        messages={"accepted_values_status": "Got 3 results, configured to warn"},
    )
    outcome = check_build(0, "", document, EXPECTED, "inv-1")
    assert outcome.ok
    assert outcome.data["counts"]["warn"] == 1
    assert outcome.data["warnings"][0]["node"].endswith("accepted_values_status")


def test_build_nonzero_exit_fails_even_with_clean_artifact() -> None:
    document = run_results(
        {"stg_orders": "success", "stg_customers": "success"}, invocation_id="inv-2"
    )
    assert not check_build(1, "", document, EXPECTED, "inv-1").ok


# --- codegen output ---------------------------------------------------------


def test_codegen_model_yaml_counts_columns() -> None:
    outcome = check_codegen_output("generate_model_yaml", MODEL_YAML_DIM_CUSTOMERS)
    assert outcome.ok
    assert outcome.data["columns"] == 4


def test_codegen_source_requires_columns_on_every_table() -> None:
    source_yaml = (
        "version: 2\nsources:\n  - name: tpch\n    tables:\n"
        "      - name: ORDERS\n        columns:\n          - name: O_ORDERKEY\n"
        "      - name: CUSTOMER\n"
    )
    assert not check_codegen_output("generate_source", source_yaml).ok


def test_codegen_sql_macro_has_no_column_check() -> None:
    outcome = check_codegen_output(
        "generate_base_model",
        "with source as (\n select * from x\n)\nselect * from source\n",
    )
    assert outcome.ok
    assert outcome.data["columns"] is None


def test_codegen_empty_output_is_a_failure() -> None:
    assert not check_codegen_output("generate_base_model", "").ok


def test_codegen_invalid_yaml_is_a_failure() -> None:
    assert not check_codegen_output("generate_model_yaml", "version: 2\nmodels: [\n").ok


# --- validators -------------------------------------------------------------


@pytest.mark.parametrize("select", ["", "   ", "-x", "--select"])
def test_validate_select_refuses_empty_or_flag_like(select: str) -> None:
    with pytest.raises(RefusalError):
        validate_select(select)


def test_validate_select_accepts_graph_operators() -> None:
    for select in (
        "stg_orders",
        "tag:nightly",
        "stg_orders+",
        "a b",
        "path:models/staging",
    ):
        validate_select(select)


@pytest.mark.parametrize(
    "name", ["fct_*", "path:models", "", "-x", "a,b", "a.b", "a/b", "1abc"]
)
def test_validate_node_name_refuses_selectors(name: str) -> None:
    with pytest.raises(RefusalError):
        validate_node_name(name)


def test_validate_node_name_accepts_identifiers() -> None:
    for name in ("stg_orders", "DimCustomers", "_private", "fct_orders_v2"):
        validate_node_name(name)


@pytest.mark.parametrize("limit", [1, 5, 50, -1])
def test_validate_limit_accepts_range_and_minus_one(limit: int) -> None:
    validate_limit(limit)


@pytest.mark.parametrize("limit", [0, 51, -2, 1000])
def test_validate_limit_refuses_out_of_range(limit: int) -> None:
    with pytest.raises(RefusalError):
        validate_limit(limit)


def test_normalize_inline_sql_strips_one_trailing_semicolon() -> None:
    assert normalize_inline_sql("select 1 as x;") == "select 1 as x"
    assert normalize_inline_sql("  SELECT 1 AS x \n") == "SELECT 1 AS x"
    assert (
        normalize_inline_sql("with c as (select 1) select * from c")
        == "with c as (select 1) select * from c"
    )


@pytest.mark.parametrize(
    "sql",
    [
        "",
        "delete from t",
        "-- comment\nselect 1",
        "select 1;;",
        "call proc()",
        "selectx from t",
        "(select 1)",
    ],
)
def test_normalize_inline_sql_refuses_non_select(sql: str) -> None:
    with pytest.raises(RefusalError):
        normalize_inline_sql(sql)


def test_validate_codegen_request_returns_resolved_path(project_dir: Path) -> None:
    path = validate_codegen_request(
        "generate_model_yaml", "models/staging/stg_orders.yml", project_dir
    )
    assert path == (project_dir / "models/staging/stg_orders.yml").resolve()


def test_validate_codegen_request_refuses_existing_file(project_dir: Path) -> None:
    with pytest.raises(RefusalError):
        validate_codegen_request(
            "generate_base_model", "models/stg_orders.sql", project_dir
        )


@pytest.mark.parametrize(
    "path", ["../outside.yml", "/tmp/x.yml", "-models/x.yml", "models/../../x.yml"]
)
def test_validate_codegen_request_refuses_paths_outside_project(
    project_dir: Path, path: str
) -> None:
    with pytest.raises(RefusalError):
        validate_codegen_request("generate_base_model", path, project_dir)


def test_validate_dbt_version() -> None:
    validate_dbt_version("1.12.5")
    validate_dbt_version("1.12.0")
    for version in ("1.11.9", "1.13.0", "2.0.0", None, ""):
        with pytest.raises(RefusalError):
            validate_dbt_version(version)

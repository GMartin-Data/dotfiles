"""MCP server: one tool per session method, state in memory, errors as tool errors."""

from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path

import pytest
from conftest import (
    COMPILE_DIM_CUSTOMERS,
    LS_TWO_VIEWS,
    FakeRun,
    make_ready,
    run_results,
    write_run_results,
)
from mcp import Client
from mcp.types import CallToolResult

from dbt_enveloppe.cli import SESSION_FILE
from dbt_enveloppe.conditions import RefusalError
from dbt_enveloppe.server import build_server
from dbt_enveloppe.session import Session

pytestmark = pytest.mark.anyio

TOOLS = {
    "dbt_debug",
    "dbt_parse",
    "dbt_ls",
    "dbt_compile",
    "dbt_show",
    "dbt_build",
    "dbt_codegen",
    "dbt_show_inline",
}


@pytest.fixture
def session(project_dir: Path, fake_run: FakeRun) -> Session:
    return Session(project_dir, fake_run)


@pytest.fixture
async def client(session: Session) -> AsyncIterator[Client]:
    async with Client(build_server(lambda: session), raise_exceptions=True) as c:
        yield c


def error_text(result: CallToolResult) -> str:
    assert result.is_error, result
    return "".join(getattr(item, "text", "") for item in result.content)


async def test_lists_exactly_the_envelope_tools(client: Client) -> None:
    """``dbt_show_inline`` included: T3 and T19 observed conformant (point E)."""
    listed = await client.list_tools()
    assert {tool.name for tool in listed.tools} == TOOLS


async def test_parse_success_is_structured_ok(
    client: Client, fake_run: FakeRun
) -> None:
    fake_run.script("parse", 0, "")
    result = await client.call_tool("dbt_parse", {})
    assert not result.is_error
    assert result.structured_content == {"ok": True}
    assert "--no-partial-parse" in fake_run.argv_for("parse")


async def test_refusal_is_an_error_result_without_a_dbt_call(
    client: Client, fake_run: FakeRun
) -> None:
    result = await client.call_tool("dbt_show", {"name": "tag:nightly"})
    assert "(D3)" in error_text(result)
    assert fake_run.calls == []


async def test_dbt_failure_message_is_the_outcome_error(
    client: Client, fake_run: FakeRun
) -> None:
    fake_run.script("parse", 2, "Compilation Error\n")
    result = await client.call_tool("dbt_parse", {})
    assert "Compilation Error" in error_text(result)


async def test_failure_data_is_appended_to_the_error(
    client: Client, fake_run: FakeRun
) -> None:
    """An ``ls`` mismatch (L2) still hands the agent the list dbt returned."""
    fake_run.script("parse", 0, "")
    fake_run.script("ls", 0, LS_TWO_VIEWS)
    await client.call_tool("dbt_parse", {})
    result = await client.call_tool(
        "dbt_ls", {"select": "tag:nightly", "expected": ["stg_orders"]}
    )
    text = error_text(result)
    assert "unexpected" in text and "stg_customers" in text
    assert '"materialized": "view"' in text


async def test_ls_takes_a_list_and_returns_models(
    client: Client, fake_run: FakeRun
) -> None:
    fake_run.script("parse", 0, "")
    fake_run.script("ls", 0, LS_TWO_VIEWS)
    await client.call_tool("dbt_parse", {})
    result = await client.call_tool(
        "dbt_ls",
        {
            "select": "stg_orders stg_customers",
            "expected": ["stg_orders", "stg_customers"],
        },
    )
    assert not result.is_error
    assert result.structured_content == {
        "models": [
            {"name": "stg_orders", "materialized": "view"},
            {"name": "stg_customers", "materialized": "view"},
        ]
    }


async def test_state_lives_in_memory_not_in_target(
    client: Client, session: Session, fake_run: FakeRun, project_dir: Path
) -> None:
    make_ready(session, fake_run)
    fake_run.script(
        "compile", 0, COMPILE_DIM_CUSTOMERS.replace("dim_customers", "stg_orders")
    )
    result = await client.call_tool("dbt_compile", {"name": "stg_orders"})
    assert not result.is_error
    assert result.structured_content["compiled"].startswith("select")
    assert result.structured_content["materialized"] == "view"
    assert not (project_dir / SESSION_FILE).exists()


async def test_show_passes_the_limit(
    client: Client, session: Session, fake_run: FakeRun
) -> None:
    make_ready(session, fake_run)
    fake_run.script("show", 0, '{"show": [{"ID": 1}, {"ID": 2}]}')
    result = await client.call_tool("dbt_show", {"name": "stg_orders", "limit": 2})
    assert not result.is_error
    assert result.structured_content["rows"] == [{"ID": 1}, {"ID": 2}]
    argv = fake_run.argv_for("show")
    assert argv[argv.index("--limit") + 1] == "2"


async def test_build_returns_counts_and_models(
    client: Client, session: Session, fake_run: FakeRun, project_dir: Path
) -> None:
    make_ready(session, fake_run)
    document = run_results({"stg_orders": "success", "stg_customers": "success"})
    fake_run.script(
        "build", 0, "", side_effect=lambda: write_run_results(project_dir, document)
    )
    result = await client.call_tool("dbt_build", {"select": "stg_orders stg_customers"})
    assert not result.is_error
    assert result.structured_content["counts"] == {"success": 2}
    assert {m["name"] for m in result.structured_content["models"]} == {
        "stg_orders",
        "stg_customers",
    }


async def test_codegen_takes_an_object_and_confirms_the_file(
    client: Client, session: Session, fake_run: FakeRun
) -> None:
    make_ready(session, fake_run)
    fake_run.script("run-operation", 0, "select 1 as id\n")
    fake_run.script("parse", 0, "")
    result = await client.call_tool(
        "dbt_codegen",
        {
            "macro": "generate_base_model",
            "args": {"source_name": "tpch", "table_name": "ORDERS"},
            "output_path": "models/base_orders.sql",
        },
    )
    assert not result.is_error
    assert result.structured_content["path"] == "models/base_orders.sql"
    assert "select" not in str(result.structured_content)


async def test_missing_project_is_reported_at_call_time(fake_run: FakeRun) -> None:
    """Without ``CLAUDE_PROJECT_DIR`` the tools exist and each call explains why it refuses."""

    def no_session() -> Session:
        raise RefusalError(
            "CLAUDE_PROJECT_DIR is not set: the envelope only runs inside a project"
        )

    async with Client(build_server(no_session), raise_exceptions=True) as client:
        listed = await client.list_tools()
        assert {tool.name for tool in listed.tools} == TOOLS
        result = await client.call_tool("dbt_parse", {})
        assert "CLAUDE_PROJECT_DIR" in error_text(result)
    assert fake_run.calls == []


async def test_show_inline_runs_on_the_read_only_target(
    client: Client, session: Session, fake_run: FakeRun
) -> None:
    make_ready(session, fake_run)
    fake_run.script("show", 0, '{"show": [{"X": 1}]}')
    result = await client.call_tool(
        "dbt_show_inline", {"sql": "select 1 as x", "limit": 1}
    )
    assert not result.is_error
    assert result.structured_content["rows"] == [{"X": 1}]
    argv = fake_run.argv_for("show")
    assert "--inline" in argv
    assert argv[argv.index("--target") + 1] == "ro"


async def test_show_inline_refuses_ddl_without_a_dbt_call(
    client: Client, session: Session, fake_run: FakeRun
) -> None:
    make_ready(session, fake_run)
    before = len(fake_run.calls)
    result = await client.call_tool(
        "dbt_show_inline", {"sql": "create table t as select 1"}
    )
    assert "(H7)" in error_text(result)
    assert len(fake_run.calls) == before

"""MCP exposure of the session (step 3): one tool per ``Session`` method.

The state lives in memory for the life of the server process (plan §1.1).
The project is resolved from ``CLAUDE_PROJECT_DIR`` at the first call and
kept; a resolution failure is reported by every tool until it is fixed.
A failed ``Outcome`` becomes a tool error whose text carries the message
and, when present, the data (an ``ls`` mismatch still returns the list).
"""

from __future__ import annotations

import functools
import json
import os
import threading
from collections.abc import Callable
from typing import Any

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from dbt_enveloppe.conditions import Outcome, RefusalError
from dbt_enveloppe.runner import resolve_project_dir
from dbt_enveloppe.session import Session

SessionFn = Callable[[], Session]


def build_server(get_session: SessionFn) -> MCPServer:
    """Register the envelope tools over the session returned by ``get_session``.

    Args:
        get_session: Returns the session to use; may raise ``RefusalError``.
    """
    server = MCPServer("dbt-enveloppe")
    lock = threading.Lock()

    def run(tool: Callable[[Session], Outcome]) -> Any:
        with lock:
            try:
                session = get_session()
            except RefusalError as exc:
                raise ToolError(str(exc)) from exc
            return _reply(tool(session))

    @server.tool()
    def dbt_debug() -> dict[str, Any]:
        """Run `dbt debug` (D1) and return its verdict lines and versions only.

        Required once per session before compile, show, build, codegen (D3).
        The connection block is never returned (D2).
        """
        return run(Session.debug)

    @server.tool()
    def dbt_parse() -> dict[str, Any]:
        """Run the canonical `dbt parse --no-partial-parse --warn-error` (P1).

        Required after every file change; any output is a failure (P2).
        A successful parse resets the selections validated by dbt_ls.
        """
        run(Session.parse)
        return {"ok": True}

    @server.tool()
    def dbt_ls(select: str, expected: list[str]) -> dict[str, Any]:
        """List the models matched by `select` and compare with `expected` (L1, L2).

        `expected` is the exact list of model names you expect; the call fails
        on any difference and returns the actual list. A successful call
        validates `select` for dbt_build and each listed name for dbt_compile
        and dbt_show, until the next parse.
        """
        return {"models": run(lambda s: s.ls(select, expected))}

    @server.tool()
    def dbt_compile(name: str, full_refresh: bool = False) -> dict[str, Any]:
        """Return the compiled SQL and materialization of one model (K1).

        `name` must be a plain model name validated by dbt_ls (K5).
        """
        return run(lambda s: s.compile(name, full_refresh))

    @server.tool()
    def dbt_show(name: str, limit: int = 5) -> dict[str, Any]:
        """Preview up to `limit` rows (1 to 50, or -1) of one model (H1, H6).

        `name` must be a plain model name validated by dbt_ls (H4). An
        incremental model with no rows is reported as such (H3).
        """
        return run(lambda s: s.show(name, limit))

    @server.tool()
    def dbt_build(select: str, full_refresh: bool = False) -> dict[str, Any]:
        """Run `dbt build` on the dev target for a selection validated by dbt_ls.

        Succeeds only if run_results.json was rewritten by this call, no node
        errored, failed or was skipped, and the executed models match the
        validated selection. Returns counts, per-model statuses and warnings.
        """
        return run(lambda s: s.build(select, full_refresh))

    @server.tool()
    def dbt_codegen(
        macro: str, args: dict[str, Any], output_path: str
    ) -> dict[str, Any]:
        """Write the output of a whitelisted codegen macro to a new file (G1 to G6).

        `output_path` is relative to the project and must not exist (G3).
        The file is re-parsed and removed if the parse fails (G5); only its
        path, size and column count are returned, never its content (G6).
        """
        return run(lambda s: s.codegen(macro, args, output_path))

    return server


def _reply(outcome: Outcome) -> Any:
    if outcome.ok:
        return outcome.data
    message = outcome.error or "the call did not meet its success condition"
    if outcome.data is not None:
        message += "\n" + json.dumps(outcome.data)
    raise ToolError(message)


def main() -> None:
    """Entry point ``dbt-enveloppe-mcp``: serve over stdio."""
    build_server(
        functools.cache(lambda: Session(resolve_project_dir(os.environ)))
    ).run()

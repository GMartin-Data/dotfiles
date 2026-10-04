"""Success conditions of the envelope (spec III §D), as pure functions.

Each ``check_*`` turns one silent failure of principle 2 into an explicit
``Outcome`` from captured outputs (exit code, stdout, artifacts); none of
them touches dbt or the warehouse. Each ``validate_*`` refuses a request
before dbt is called, by raising ``RefusalError``.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

CODEGEN_MACROS: frozenset[str] = frozenset(
    {
        "generate_source",
        "generate_base_model",
        "generate_model_yaml",
        "generate_model_import_ctes",
        "generate_unit_test_template",
    }
)
SUPPORTED_DBT_PREFIX = "1.12."
MAX_ROWS = 50
MAX_LIMIT = 50
MESSAGE_TRUNCATION = 500
OUTPUT_TAIL = 2000

_TIMESTAMP = re.compile(r"^\d{2}:\d{2}:\d{2}\s+")
_LOG_LINE = re.compile(r"^\d{2}:\d{2}:\d{2}\s", re.MULTILINE)
_CHECKS_FAILED = re.compile(r"^\d+ checks? failed")
_NODE_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_FIRST_WORD = re.compile(r"[A-Za-z]+")
_FAILING_STATUSES = frozenset(
    {"error", "fail", "skipped", "runtime error", "partial success"}
)
_YAML_MACROS = frozenset(
    {"generate_source", "generate_model_yaml", "generate_unit_test_template"}
)


class RefusalError(Exception):
    """A request refused before any dbt call (bad argument or precondition)."""


@dataclass(frozen=True)
class Outcome:
    """Verdict of a tool call: what the agent gets back, nothing more.

    Attributes:
        ok: Whether the success condition of the tool holds.
        data: The useful part of the output on success (tool-specific shape).
        error: An explicit message on failure, never the full dbt log.
    """

    ok: bool
    data: Any = None
    error: str | None = None


def exit_message(command: str, returncode: int | None, stdout: str) -> str:
    """Describe a failed dbt call from its exit code and the tail of its output."""
    status = "timed out" if returncode is None else f"exited {returncode}"
    text = stdout.strip()[-OUTPUT_TAIL:]
    return f"dbt {command} {status}" + (f": {text}" if text else " with no output")


def check_debug(returncode: int | None, stdout: str) -> Outcome:
    """Judge ``dbt debug``: exit 0, and keep only the verdict lines (D2).

    Keeps ``[OK ...]``, ``[ERROR ...]``, ``All checks passed!`` and the two
    version lines; never the ``Connection`` block. On failure, also keeps the
    explanation printed after ``N check(s) failed``.

    Returns:
        On success, ``data`` holds ``lines``, ``dbt_version`` and
        ``adapter_version``.
    """
    lines = [_TIMESTAMP.sub("", line).strip() for line in stdout.splitlines()]
    versions = [
        line for line in lines if line.startswith(("dbt version:", "adapter version:"))
    ]
    verdicts = [
        line
        for line in lines
        if "[OK" in line or "[ERROR" in line or line == "All checks passed!"
    ]
    data = {
        "lines": versions + verdicts,
        "dbt_version": _after_colon(versions, "dbt version:"),
        "adapter_version": _after_colon(versions, "adapter version:"),
    }
    if returncode == 0:
        return Outcome(True, data)
    explanation: list[str] = []
    for index, line in enumerate(lines):
        if _CHECKS_FAILED.match(line):
            explanation = [item for item in lines[index:] if item]
            break
    details = [line for line in verdicts if "[ERROR" in line] + explanation
    status = "timed out" if returncode is None else f"exited {returncode}"
    error = f"dbt debug {status}" + (
        ":\n" + "\n".join(details) if details else " with no verdict line"
    )
    return Outcome(False, data, error)


def _after_colon(lines: Sequence[str], prefix: str) -> str | None:
    for line in lines:
        if line.startswith(prefix):
            return line[len(prefix) :].strip() or None
    return None


def check_parse(returncode: int | None, stdout: str) -> Outcome:
    """Judge ``dbt parse``: exit 0 and empty output (P2).

    Any output under ``--quiet --warn-error`` is a warning or an error, even
    with exit code 0.
    """
    text = stdout.strip()
    if returncode == 0 and not text:
        return Outcome(True)
    if returncode == 0:
        return Outcome(
            False,
            error=f"dbt parse exited 0 but printed output (a warning, P2): {text[-OUTPUT_TAIL:]}",
        )
    return Outcome(False, error=exit_message("parse", returncode, stdout))


def check_ls(returncode: int | None, stdout: str, expected: Sequence[str]) -> Outcome:
    """Judge ``dbt ls``: exit 0, non-empty list, equal to ``expected`` (L2).

    An empty selection exits 0 with no output; a bare wildcard does the same.

    Returns:
        On success, ``data`` is the list of ``{"name", "materialized"}`` in dbt
        order. On mismatch, ``error`` names the missing and unexpected models.
    """
    if not expected:
        return Outcome(False, error="the expected model list must not be empty (L2)")
    if returncode != 0:
        return Outcome(False, error=exit_message("ls", returncode, stdout))
    lines = [line for line in stdout.splitlines() if line.strip()]
    if not lines:
        return Outcome(
            False,
            error="no model selected: dbt ls exited 0 with no output (empty selection or bare wildcard, L2/L3)",
        )
    models: list[dict[str, Any]] = []
    for line in lines:
        try:
            record = json.loads(line)
        except ValueError:
            return Outcome(
                False, error=f"unexpected non-JSON line in dbt ls output: {line[:200]}"
            )
        if not isinstance(record, dict) or "name" not in record:
            return Outcome(
                False, error=f"unexpected record in dbt ls output: {line[:200]}"
            )
        materialized = record.get("config.materialized")
        if materialized is None and isinstance(record.get("config"), dict):
            materialized = record["config"].get("materialized")
        models.append({"name": record["name"], "materialized": materialized})
    names = {model["name"] for model in models}
    missing = sorted(set(expected) - names)
    unexpected = sorted(names - set(expected))
    if missing or unexpected:
        return Outcome(
            False,
            models,
            f"selection differs from the expected list: missing {missing}, unexpected {unexpected} (L2)",
        )
    return Outcome(True, models)


def check_compile(returncode: int | None, stdout: str) -> Outcome:
    """Judge ``dbt compile``: exit 0 and a non-empty ``compiled`` key (K2).

    ``tag:`` or multiple selections compile without printing anything.

    Returns:
        On success, ``data`` holds ``node`` and ``compiled``.
    """
    if returncode != 0:
        return Outcome(False, error=exit_message("compile", returncode, stdout))
    document = _json_object(stdout)
    if document is None or not document.get("compiled"):
        return Outcome(
            False,
            error="no compiled SQL in dbt compile output: selection not supported by compile (tag:, +, list; K5)",
        )
    return Outcome(
        True, {"node": document.get("node"), "compiled": document["compiled"]}
    )


def check_show(
    returncode: int | None,
    stdout: str,
    *,
    materialized: str | None = None,
    max_rows: int = MAX_ROWS,
) -> Outcome:
    """Judge ``dbt show``: exit 0 and the ``show`` key present (H2).

    Refuses a statement result (rows made of a single ``status`` key): the
    ``show`` key does not distinguish a read from a write. Truncates to
    ``max_rows`` and flags zero rows on a built ``incremental`` model (H3).

    Returns:
        On success, ``data`` holds ``node``, ``materialized``, ``rows``,
        ``row_count`` and an optional ``note``.
    """
    if returncode != 0:
        return Outcome(False, error=exit_message("show", returncode, stdout))
    document = _json_object(stdout)
    if document is None or not isinstance(document.get("show"), list):
        return Outcome(
            False,
            error="no `show` key in dbt show output: selection not supported by show (tag:, +, list; H4)",
        )
    rows: list[Any] = document["show"]
    if rows and all(isinstance(row, dict) and set(row) == {"status"} for row in rows):
        return Outcome(
            False, error=f"statement result, not a query result: {rows[0]['status']}"
        )
    row_count = len(rows)
    note = None
    if row_count > max_rows:
        rows = rows[:max_rows]
        note = f"truncated to {max_rows} of {row_count} rows"
    elif row_count == 0 and materialized == "incremental":
        note = (
            "0 rows is expected for a built incremental model: the incremental filter "
            "excludes existing rows (H3); use dbt_compile with full_refresh to see the unfiltered SQL"
        )
    data = {
        "node": document.get("node"),
        "materialized": materialized,
        "rows": rows,
        "row_count": row_count,
        "note": note,
    }
    return Outcome(True, data)


def check_build(
    returncode: int | None,
    stdout: str,
    run_results: Mapping[str, Any] | None,
    expected: Mapping[str, str],
    previous_invocation_id: str | None,
) -> Outcome:
    """Judge ``dbt build`` on ``run_results.json``, not on the log (plan §1.1).

    Success requires: exit 0, the artifact rewritten by this call (new
    invocation id), non-empty results, no ``error``/``fail``/``skipped``
    status, and the set of executed models equal to ``expected``.

    Args:
        expected: Model names validated by ``dbt_ls``, mapped to their
            materialization.
        previous_invocation_id: Invocation id read before the call, or None.

    Returns:
        On success, ``data`` holds ``counts`` per status, ``models`` (name,
        materialization, status) and ``warnings``. On failure, ``error`` names
        each failing node with its message truncated to 500 characters.
    """
    if run_results is None:
        return Outcome(
            False,
            error=exit_message("build", returncode, stdout)
            + "; run_results.json not written",
        )
    metadata = run_results.get("metadata") or {}
    invocation_id = metadata.get("invocation_id")
    if invocation_id is None or invocation_id == previous_invocation_id:
        return Outcome(
            False,
            error=exit_message("build", returncode, stdout)
            + "; run_results.json was not rewritten by this call (same invocation id): the build did not run",
        )
    results = run_results.get("results") or []
    if not results:
        return Outcome(
            False, error="dbt build produced no results: nothing was executed"
        )
    counts: dict[str, int] = {}
    models: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    failures: list[str] = []
    executed: set[str] = set()
    for result in results:
        status = str(result.get("status"))
        unique_id = str(result.get("unique_id", "?"))
        counts[status] = counts.get(status, 0) + 1
        parts = unique_id.split(".")
        if parts[0] == "model" and len(parts) >= 3:
            executed.add(parts[2])
            models.append(
                {
                    "name": parts[2],
                    "materialized": expected.get(parts[2]),
                    "status": status,
                }
            )
        if status in _FAILING_STATUSES:
            failures.append(
                f"{unique_id} [{status}]: {_truncate(result.get('message'))}"
            )
        elif status == "warn":
            warnings.append(
                {"node": unique_id, "message": _truncate(result.get("message"))}
            )
    problems: list[str] = []
    if returncode != 0:
        problems.append(
            "timed out" if returncode is None else f"dbt build exited {returncode}"
        )
    if failures:
        problems.append("failing nodes:\n" + "\n".join(failures))
    missing = sorted(set(expected) - executed)
    unexpected = sorted(executed - set(expected))
    if missing or unexpected:
        problems.append(
            f"executed models differ from the validated selection: missing {missing}, unexpected {unexpected}"
        )
    data = {"counts": counts, "models": models, "warnings": warnings}
    if problems:
        return Outcome(False, data, "\n".join(problems))
    return Outcome(True, data)


def check_codegen_output(macro: str, content: str) -> Outcome:
    """Judge a ``codegen`` output before it is kept (G5, part one).

    Refuses dbt log lines in the content (``--quiet`` missing) and, for the
    YAML macros, invalid YAML or a model/table without columns (unbuilt model).

    Returns:
        On success, ``data`` holds ``columns`` (count, or None for SQL macros).
    """
    if not content.strip():
        return Outcome(False, error=f"{macro} produced no output")
    if _LOG_LINE.search(content):
        return Outcome(
            False,
            error=f"{macro} output contains dbt log lines, unusable as a file (G2)",
        )
    if macro not in _YAML_MACROS:
        return Outcome(True, {"columns": None})
    try:
        document = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        return Outcome(False, error=f"{macro} output is not valid YAML: {exc}")
    if not isinstance(document, dict):
        return Outcome(False, error=f"{macro} output is not a YAML mapping")
    entries = _column_bearing_entries(macro, document)
    if entries is None:
        return Outcome(True, {"columns": None})
    columns = 0
    for entry in entries:
        entry_columns = entry.get("columns") or []
        if not entry_columns:
            return Outcome(
                False,
                error=f"{macro}: '{entry.get('name')}' has no columns; build the model first (G4, G5)",
            )
        columns += len(entry_columns)
    if columns == 0:
        return Outcome(False, error=f"{macro}: no model or table in the output")
    return Outcome(True, {"columns": columns})


def _column_bearing_entries(
    macro: str, document: Mapping[str, Any]
) -> list[dict[str, Any]] | None:
    if macro == "generate_model_yaml":
        return [
            model for model in document.get("models") or [] if isinstance(model, dict)
        ]
    if macro == "generate_source":
        return [
            table
            for source in document.get("sources") or []
            if isinstance(source, dict)
            for table in source.get("tables") or []
            if isinstance(table, dict)
        ]
    return None


def validate_select(select: str) -> None:
    """Refuse an empty selection or one starting with ``-`` (flag injection)."""
    text = (select or "").strip()
    if not text:
        raise RefusalError("the selection must not be empty")
    if text.startswith("-"):
        raise RefusalError("the selection must not start with '-'")


def validate_node_name(name: str) -> None:
    """Refuse anything but an exact model name for ``compile``/``show`` (K5, H4).

    No ``tag:``, ``+``, ``*``, spaces, paths or lists.
    """
    if not _NODE_NAME.fullmatch(name or ""):
        raise RefusalError(
            f"an exact model name is required, got {name!r}: no tag:, +, *, spaces, paths or lists (K5, H4)"
        )


def validate_limit(limit: int) -> None:
    """Refuse a ``limit`` outside 1..50, except ``-1`` (H6)."""
    if limit == -1 or 1 <= limit <= MAX_LIMIT:
        return
    raise RefusalError(
        f"limit must be between 1 and {MAX_LIMIT}, or -1 (H6); got {limit}"
    )


def normalize_inline_sql(sql: str) -> str:
    """Accept a single ``select``/``with`` statement for ``show --inline`` (H7).

    Strips one trailing ``;`` (H6) and refuses any other ``;``.

    Returns:
        The SQL to pass to dbt.
    """
    text = (sql or "").strip()
    if text.endswith(";"):
        text = text[:-1].rstrip()
    if ";" in text:
        raise RefusalError("a single statement is required: no ';' inside the SQL (H6)")
    first = _FIRST_WORD.match(text)
    if first is None or first.group(0).lower() not in {"select", "with"}:
        raise RefusalError(
            "show --inline accepts a single SELECT (or WITH ... SELECT) statement only (H7)"
        )
    return text


def validate_codegen_request(macro: str, output_path: str, project_dir: Path) -> Path:
    """Refuse a macro outside the whitelist (O1, G1) or an unsafe path (G3).

    The path must resolve inside ``project_dir`` and must not exist.

    Returns:
        The resolved output path.
    """
    if macro not in CODEGEN_MACROS:
        raise RefusalError(
            f"macro {macro!r} is not allowed; allowed macros: {sorted(CODEGEN_MACROS)} (O1, G1)"
        )
    if not output_path or output_path.startswith("-"):
        raise RefusalError("output_path must be a relative path inside the project")
    root = project_dir.resolve()
    target = (root / output_path).resolve()
    if target == root or not target.is_relative_to(root):
        raise RefusalError(f"output_path must stay inside the project: {output_path}")
    if target.exists():
        raise RefusalError(
            f"output_path already exists and is never overwritten: {output_path} (G3)"
        )
    return target


def validate_dbt_version(version: str | None) -> None:
    """Refuse a dbt-core version outside 1.12.x (conditions observed on 1.12.5)."""
    if not version or not version.startswith(SUPPORTED_DBT_PREFIX):
        raise RefusalError(
            f"dbt-core {version or 'unknown'} is not supported: the success conditions were observed on 1.12.x"
        )


def _json_object(stdout: str) -> dict[str, Any] | None:
    try:
        document = json.loads(stdout.strip() or "null")
    except ValueError:
        return None
    return document if isinstance(document, dict) else None


def _truncate(message: Any) -> str:
    text = str(message or "").strip()
    if len(text) > MESSAGE_TRUNCATION:
        return text[:MESSAGE_TRUNCATION] + "..."
    return text

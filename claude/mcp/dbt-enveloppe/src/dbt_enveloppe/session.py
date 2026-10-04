"""Session state and tool orchestration: one method per envelope tool.

A session lives as long as the server process (plan §1.1). It remembers
whether ``debug`` passed, the fingerprint of the project files at the last
successful ``parse``, and the selections validated by ``ls`` since then. Each
tool checks its preconditions (S1, L2, D3), builds the canonical argv, runs
it through an injectable runner, and judges the result with ``conditions``.
"""

from __future__ import annotations

import functools
import json
import os
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from dbt_enveloppe import conditions, runner
from dbt_enveloppe.conditions import Outcome, RefusalError
from dbt_enveloppe.runner import Result

RunFn = Callable[[list[str], Path, float], Result]

BUILD_TIMEOUT_S = 900.0
IGNORED_DIRS: frozenset[str] = frozenset({"target", "dbt_packages", "logs"})


@dataclass(frozen=True)
class OutputPaths:
    """Where dbt writes, relative to the project: skipped by the fingerprint.

    Resolved as dbt does (``DBT_ENGINE_*`` env, then the older ``DBT_*``
    names, then ``dbt_project.yml``, then the defaults). An absolute path
    outside the project leaves nothing to skip.
    """

    target: str = "target"
    ignored: frozenset[str] = IGNORED_DIRS

    @property
    def run_results(self) -> Path:
        return Path(self.target) / "run_results.json"


def output_paths(project_dir: Path, env: Mapping[str, str]) -> OutputPaths:
    """Read the dbt output locations for ``project_dir``."""
    try:
        project = yaml.safe_load((project_dir / "dbt_project.yml").read_text()) or {}
    except (OSError, yaml.YAMLError):
        project = {}
    if not isinstance(project, dict):
        project = {}

    def pick(*env_names: str, key: str, default: str) -> str:
        for name in env_names:
            if env.get(name):
                return env[name]
        value = project.get(key)
        return str(value) if value else default

    target = pick(
        "DBT_ENGINE_TARGET_PATH", "DBT_TARGET_PATH", key="target-path", default="target"
    )
    logs = pick("DBT_ENGINE_LOG_PATH", "DBT_LOG_PATH", key="log-path", default="logs")
    packages = pick(key="packages-install-path", default="dbt_packages")
    ignored = frozenset(
        relative
        for relative in (_inside(project_dir, raw) for raw in (target, logs, packages))
        if relative is not None
    )
    return OutputPaths(target, ignored)


def _inside(project_dir: Path, raw: str) -> str | None:
    path = Path(raw)
    if not path.is_absolute():
        path = project_dir / path
    try:
        return path.resolve().relative_to(project_dir.resolve()).as_posix()
    except ValueError:
        return None


@dataclass(frozen=True)
class Fingerprint:
    """Snapshot of the project files: relative path -> (size, mtime_ns).

    Hidden entries and the dbt output directories are skipped.
    """

    files: Mapping[str, tuple[int, int]] = field(default_factory=dict)


def fingerprint(
    project_dir: Path, ignored: frozenset[str] = IGNORED_DIRS
) -> Fingerprint:
    """Take the fingerprint of the project files as they are now."""
    files: dict[str, tuple[int, int]] = {}
    for root, dirs, names in project_dir.walk():
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".")
            and (root / d).relative_to(project_dir).as_posix() not in ignored
        ]
        for name in names:
            if name.startswith("."):
                continue
            path = root / name
            try:
                stat = path.stat()
            except OSError:
                continue
            files[path.relative_to(project_dir).as_posix()] = (
                stat.st_size,
                stat.st_mtime_ns,
            )
    return Fingerprint(files)


def changed_files(before: Fingerprint, after: Fingerprint) -> list[str]:
    """List the paths added, removed or modified between two fingerprints."""
    paths = set(before.files) | set(after.files)
    return sorted(
        path for path in paths if before.files.get(path) != after.files.get(path)
    )


def _refusals_as_outcome(method: Callable[..., Outcome]) -> Callable[..., Outcome]:
    @functools.wraps(method)
    def wrapper(self: Session, *args: Any, **kwargs: Any) -> Outcome:
        try:
            return method(self, *args, **kwargs)
        except RefusalError as exc:
            return Outcome(False, error=str(exc))

    return wrapper


class Session:
    """State of one envelope session over one dbt project.

    Args:
        project_dir: The dbt project (already resolved and checked).
        run: Subprocess runner; injected in tests.
        env: Where dbt's ``DBT_ENGINE_*`` path overrides are read; the process
            environment by default.
    """

    def __init__(
        self,
        project_dir: Path,
        run: RunFn = runner.run,
        env: Mapping[str, str] | None = None,
    ) -> None:
        self.project_dir = project_dir
        self._run = run
        self.paths = output_paths(project_dir, os.environ if env is None else env)
        self.debug_ok = False
        self.dbt_version: str | None = None
        self.adapter_version: str | None = None
        self.parse_fingerprint: Fingerprint | None = None
        self.selections: dict[str, list[dict[str, Any]]] = {}

    # --- tools ---------------------------------------------------------------

    @_refusals_as_outcome
    def debug(self) -> Outcome:
        """``dbt debug`` without ``--quiet`` (D1); records versions on success."""
        result = self._call("debug")
        outcome = conditions.check_debug(result.returncode, result.stdout)
        self.debug_ok = outcome.ok
        if outcome.ok:
            self.dbt_version = outcome.data["dbt_version"]
            self.adapter_version = outcome.data["adapter_version"]
        return outcome

    @_refusals_as_outcome
    def parse(self) -> Outcome:
        """Canonical ``dbt parse`` (P1); records the fingerprint, resets selections."""
        snapshot = fingerprint(self.project_dir, self.paths.ignored)
        result = self._call("parse", ["--no-partial-parse", "--warn-error"])
        outcome = conditions.check_parse(result.returncode, result.stdout)
        if outcome.ok:
            self.parse_fingerprint = snapshot
            self.selections = {}
        return outcome

    @_refusals_as_outcome
    def ls(self, select: str, expected: list[str]) -> Outcome:
        """Canonical ``dbt ls`` (L1) against ``expected``; records the selection.

        Requires a parse on the current files.
        """
        select = conditions.validate_select(select)
        self._require_parse_current()
        args = [
            "--select",
            select,
            "--resource-type",
            "model",
            "--output",
            "json",
            "--output-keys",
            "name config.materialized",
            "--warn-error",
        ]
        result = self._call("ls", args)
        outcome = conditions.check_ls(result.returncode, result.stdout, expected)
        if outcome.ok:
            self.selections[select] = outcome.data
        return outcome

    @_refusals_as_outcome
    def compile(self, name: str, full_refresh: bool = False) -> Outcome:
        """Canonical ``dbt compile`` (K1) of one model validated by ``ls``.

        Requires debug, a supported version, and a parse on the current files.
        Runs on the read-only target: ``--no-introspect`` does not stop
        ``run_query`` on dbt-snowflake, so writes are refused by the role (K3).
        """
        self._require_debug()
        self._require_parse_current()
        materialized = self._require_validated_name(name)
        args = ["--select", name, "--no-introspect", "--output", "json"]
        if full_refresh:
            args.append("--full-refresh")
        result = self._call("compile", args, target="ro")
        outcome = conditions.check_compile(result.returncode, result.stdout)
        if outcome.ok:
            return Outcome(True, {**outcome.data, "materialized": materialized})
        return outcome

    @_refusals_as_outcome
    def show(self, name: str, limit: int = 5) -> Outcome:
        """Canonical ``dbt show`` (H1) of one model validated by ``ls``.

        Same preconditions and read-only target as ``compile``; joins the
        materialization (H3).
        """
        self._require_debug()
        self._require_parse_current()
        materialized = self._require_validated_name(name)
        conditions.validate_limit(limit)
        result = self._call(
            "show",
            ["--select", name, "--limit", str(limit), "--output", "json"],
            target="ro",
        )
        return conditions.check_show(
            result.returncode, result.stdout, materialized=materialized
        )

    @_refusals_as_outcome
    def build(self, select: str, full_refresh: bool = False) -> Outcome:
        """``dbt build --target dev`` of a selection validated by ``ls`` (plan §1.1).

        Reads ``run_results.json`` before and after the call so that
        an artifact left by an earlier run cannot pass for this one.
        """
        self._require_debug()
        self._require_parse_current()
        select = conditions.validate_select(select)
        expected = self._require_validated_selection(select)
        previous = _invocation_id(self._read_run_results())
        args = ["--select", select]
        if full_refresh:
            args.append("--full-refresh")
        result = self._call("build", args, timeout_s=BUILD_TIMEOUT_S)
        return conditions.check_build(
            result.returncode,
            result.stdout,
            self._read_run_results(),
            expected,
            previous,
        )

    @_refusals_as_outcome
    def codegen(self, macro: str, args: Mapping[str, Any], output_path: str) -> Outcome:
        """Whitelisted ``codegen`` macro written to a new file, then re-parsed (G1 to G5).

        The file is removed if the content check or the parse fails. The
        content is never returned (G6). The macro runs on the read-only target.
        """
        self._require_debug()
        self._require_parse_current()
        target = conditions.validate_codegen_request(
            macro, output_path, self.project_dir
        )
        macro_args = dict(args)
        if macro == "generate_source":
            macro_args["generate_columns"] = True
        result = self._call(
            "run-operation", [macro, "--args", json.dumps(macro_args)], target="ro"
        )
        if result.returncode != 0:
            return Outcome(
                False,
                error=conditions.exit_message(
                    f"run-operation {macro}", result.returncode, result.stdout
                ),
            )
        content = result.stdout
        checked = conditions.check_codegen_output(macro, content)
        if not checked.ok:
            return checked
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        parsed = self.parse()
        if not parsed.ok:
            target.unlink()
            return Outcome(
                False,
                error=f"dbt parse failed after writing {output_path}; file removed (G5): {parsed.error}",
            )
        relative = target.relative_to(self.project_dir.resolve()).as_posix()
        return Outcome(
            True,
            {
                "path": relative,
                "bytes": len(content.encode()),
                "columns": checked.data["columns"],
            },
        )

    @_refusals_as_outcome
    def show_inline(self, sql: str, limit: int = 5) -> Outcome:
        """``dbt show --inline`` on the read-only target (H7), SELECT only."""
        self._require_debug()
        self._require_parse_current()
        statement = conditions.normalize_inline_sql(sql)
        conditions.validate_limit(limit)
        args = ["--inline", statement, "--limit", str(limit), "--output", "json"]
        result = self._call("show", args, target="ro")
        return conditions.check_show(result.returncode, result.stdout)

    # --- persistence ---------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Serialize the state (CLI persistence between invocations)."""
        return {
            "debug_ok": self.debug_ok,
            "dbt_version": self.dbt_version,
            "adapter_version": self.adapter_version,
            "parse_fingerprint": dict(self.parse_fingerprint.files)
            if self.parse_fingerprint
            else None,
            "selections": self.selections,
        }

    @classmethod
    def from_dict(
        cls, project_dir: Path, data: Mapping[str, Any], run: RunFn = runner.run
    ) -> Session:
        """Rebuild a session from ``to_dict`` output."""
        session = cls(project_dir, run)
        session.debug_ok = bool(data.get("debug_ok"))
        session.dbt_version = data.get("dbt_version")
        session.adapter_version = data.get("adapter_version")
        files = data.get("parse_fingerprint")
        if files is not None:
            session.parse_fingerprint = Fingerprint(
                {path: (int(size), int(mtime)) for path, (size, mtime) in files.items()}
            )
        session.selections = {
            select: list(models)
            for select, models in (data.get("selections") or {}).items()
        }
        return session

    # --- preconditions and helpers ------------------------------------------

    def _call(
        self,
        command: str,
        args: list[str] | None = None,
        *,
        target: str = "dev",
        timeout_s: float = runner.DEFAULT_TIMEOUT_S,
    ) -> Result:
        argv = runner.dbt_argv(self.project_dir, command, args or [], target=target)
        return self._run(argv, self.project_dir, timeout_s)

    def _require_debug(self) -> None:
        if not self.debug_ok:
            raise RefusalError("dbt_debug must succeed first in this session (D3)")
        conditions.validate_dbt_version(self.dbt_version)

    def _require_parse_current(self) -> None:
        if self.parse_fingerprint is None:
            raise RefusalError("dbt_parse must succeed first on this project (S1)")
        changed = changed_files(
            self.parse_fingerprint, fingerprint(self.project_dir, self.paths.ignored)
        )
        if changed:
            shown = ", ".join(changed[:10]) + (
                f" and {len(changed) - 10} more" if len(changed) > 10 else ""
            )
            raise RefusalError(
                f"files changed since the last dbt_parse: {shown}; run dbt_parse again (P1)"
            )

    def _require_validated_name(self, name: str) -> str | None:
        conditions.validate_node_name(name)
        models = {
            model["name"]: model["materialized"]
            for selection in self.selections.values()
            for model in selection
        }
        if name not in models:
            raise RefusalError(
                f"model {name!r} was not validated by dbt_ls since the last parse (L2, H4)"
            )
        return models[name]

    def _require_validated_selection(self, select: str) -> dict[str, str]:
        select = conditions.validate_select(select)
        if select not in self.selections:
            raise RefusalError(
                f"selection {select!r} was not validated by dbt_ls since the last parse (L2); call dbt_ls with the same select first"
            )
        return {
            model["name"]: model["materialized"] for model in self.selections[select]
        }

    def _read_run_results(self) -> dict[str, Any] | None:
        try:
            document = json.loads(
                (self.project_dir / self.paths.run_results).read_text()
            )
        except (OSError, ValueError):
            return None
        return document if isinstance(document, dict) else None


def _invocation_id(run_results: Mapping[str, Any] | None) -> str | None:
    if run_results is None:
        return None
    metadata = run_results.get("metadata") or {}
    return metadata.get("invocation_id")

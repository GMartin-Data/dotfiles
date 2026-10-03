"""Pure CLI over the session (step 2): one subcommand per tool, JSON out.

The project comes from ``CLAUDE_PROJECT_DIR``. The session is persisted in
``<project>/target/dbt-enveloppe-session.json`` between invocations, so that
``dbt clean`` also resets the session. Exit code 0 when the outcome is ok,
1 otherwise; the ``Outcome`` is printed as one JSON object on stdout.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path

from dbt_enveloppe import runner
from dbt_enveloppe.conditions import Outcome, RefusalError
from dbt_enveloppe.runner import resolve_project_dir
from dbt_enveloppe.session import RunFn, Session

SESSION_FILE = "target/dbt-enveloppe-session.json"


def main(
    argv: Sequence[str] | None = None,
    *,
    run: RunFn = runner.run,
    env: Mapping[str, str] = os.environ,
) -> int:
    """Parse ``argv``, run one tool on the persisted session, print the outcome.

    Subcommands: ``debug``, ``parse``, ``ls --select S --expected a,b``,
    ``compile --name N [--full-refresh]``, ``show --name N [--limit L]``,
    ``build --select S [--full-refresh]``, ``codegen --macro M --args JSON
    --output PATH``, ``show-inline --sql SQL [--limit L]``.

    Returns:
        The process exit code.
    """
    namespace = _parser().parse_args(argv)
    try:
        project_dir = resolve_project_dir(env)
    except RefusalError as exc:
        return _emit(Outcome(False, error=str(exc)))
    session = _load_session(project_dir, run)
    outcome = _dispatch(session, namespace)
    _save_session(session)
    return _emit(outcome)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dbt-enveloppe", description="Guarded dbt calls, one tool per subcommand."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("debug", help="dbt debug, verdict lines only")
    commands.add_parser("parse", help="canonical dbt parse")
    ls = commands.add_parser("ls", help="canonical dbt ls against an expected list")
    ls.add_argument("--select", required=True)
    ls.add_argument("--expected", required=True, help="comma-separated model names")
    compile_ = commands.add_parser("compile", help="compiled SQL of one model")
    compile_.add_argument("--name", required=True)
    compile_.add_argument("--full-refresh", action="store_true")
    show = commands.add_parser("show", help="preview of one model")
    show.add_argument("--name", required=True)
    show.add_argument("--limit", type=int, default=5)
    build = commands.add_parser("build", help="dbt build on the dev target")
    build.add_argument("--select", required=True)
    build.add_argument("--full-refresh", action="store_true")
    codegen = commands.add_parser("codegen", help="codegen macro written to a new file")
    codegen.add_argument("--macro", required=True)
    codegen.add_argument("--args", default="{}", help="JSON object of macro arguments")
    codegen.add_argument(
        "--output", required=True, help="new file path, relative to the project"
    )
    inline = commands.add_parser("show-inline", help="SELECT on the read-only target")
    inline.add_argument("--sql", required=True)
    inline.add_argument("--limit", type=int, default=5)
    return parser


def _dispatch(session: Session, namespace: argparse.Namespace) -> Outcome:
    match namespace.command:
        case "debug":
            return session.debug()
        case "parse":
            return session.parse()
        case "ls":
            expected = [
                name.strip() for name in namespace.expected.split(",") if name.strip()
            ]
            return session.ls(namespace.select, expected)
        case "compile":
            return session.compile(namespace.name, namespace.full_refresh)
        case "show":
            return session.show(namespace.name, namespace.limit)
        case "build":
            return session.build(namespace.select, namespace.full_refresh)
        case "codegen":
            try:
                args = json.loads(namespace.args)
            except ValueError:
                return Outcome(False, error="--args must be a JSON object")
            if not isinstance(args, dict):
                return Outcome(False, error="--args must be a JSON object")
            return session.codegen(namespace.macro, args, namespace.output)
        case "show-inline":
            return session.show_inline(namespace.sql, namespace.limit)
    return Outcome(False, error=f"unknown command {namespace.command!r}")


def _load_session(project_dir: Path, run: RunFn) -> Session:
    try:
        data = json.loads((project_dir / SESSION_FILE).read_text())
        return Session.from_dict(project_dir, data, run)
    except (OSError, ValueError, TypeError, AttributeError):
        return Session(project_dir, run)


def _save_session(session: Session) -> None:
    path = session.project_dir / SESSION_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(session.to_dict()))


def _emit(outcome: Outcome) -> int:
    sys.stdout.write(json.dumps(dataclasses.asdict(outcome)) + "\n")
    return 0 if outcome.ok else 1

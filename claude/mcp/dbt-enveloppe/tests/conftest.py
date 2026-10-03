"""Shared fixtures: a fake dbt project, a scripted runner, real captured outputs.

The captured texts come from the Snowflake testbed (T3 and T13, 2026-10-02,
dbt-core 1.12.5, dbt-snowflake 1.12.1); the account identifier is replaced
by a placeholder.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from dbt_enveloppe.runner import Result

# --- Real outputs -----------------------------------------------------------

DEBUG_OK = """\
17:50:20  Running with dbt=1.12.5
17:50:20  dbt version: 1.12.5
17:50:20  python version: 3.12.12
17:50:20  python path: /home/user/dbt-agent-testbed/.venv/bin/python
17:50:20  os info: Linux-6.8.0-138-generic-x86_64-with-glibc2.35
17:50:20  Using profiles dir at /home/user/.dbt
17:50:20  Using profiles.yml file at /home/user/.dbt/profiles.yml
17:50:20  Using dbt_project.yml file at /home/user/dbt-agent-testbed/dbt_project.yml
17:50:20  adapter type: snowflake
17:50:20  adapter version: 1.12.1
17:50:20  Configuration:
17:50:20    profiles.yml file [OK found and valid]
17:50:20    dbt_project.yml file [OK found and valid]
17:50:20  Required dependencies:
17:50:20   - git [OK found]

17:50:20  Connection:
17:50:20    account: ORG-ACCOUNT
17:50:20    user: DBT_AGENT_RW_USER
17:50:20    database: DBT_AGENT_DEV
17:50:20    warehouse: DBT_AGENT_WH
17:50:20    role: DBT_AGENT_RW
17:50:20    schema: DEV
17:50:20    authenticator: None
17:50:20    oauth_client_id: None
17:50:20    query_tag: dbt-agent
17:50:20    client_session_keep_alive: False
17:50:20    host: None
17:50:20    port: None
17:50:20    proxy_host: None
17:50:20    proxy_port: None
17:50:20    protocol: None
17:50:20    connect_retries: 1
17:50:20    connect_timeout: None
17:50:20    retry_on_database_errors: False
17:50:20    retry_all: False
17:50:20    insecure_mode: False
17:50:20    reuse_connections: True
17:50:20    s3_stage_vpce_dns_name: None
17:50:20    workload_identity_provider: None
17:50:20    workload_identity_entra_resource: None
17:50:20    platform_detection_timeout_seconds: 0.0
17:50:20  Registered adapter: snowflake=1.12.1
17:50:21    Connection test: [OK connection ok]

17:50:21  All checks passed!
"""

# Shape expected on a wrong account (T14 not run yet): verdict then explanation.
DEBUG_CONNECTION_FAILED = """\
17:55:01  Running with dbt=1.12.5
17:55:01  dbt version: 1.12.5
17:55:01  adapter type: snowflake
17:55:01  adapter version: 1.12.1
17:55:01  Configuration:
17:55:01    profiles.yml file [OK found and valid]
17:55:01    dbt_project.yml file [OK found and valid]
17:55:01  Required dependencies:
17:55:01   - git [OK found]

17:55:01  Connection:
17:55:01    account: ORG-ACCOUNT
17:55:01    user: DBT_AGENT_RW_USER
17:55:01  Registered adapter: snowflake=1.12.1
17:55:09    Connection test: [ERROR]

17:55:09  1 check failed:
17:55:09  dbt was unable to connect to the specified database.
17:55:09  The database returned the following error:

  >Database Error
  250001 (08001): Failed to connect to DB: ORG-ACCOUNT.snowflakecomputing.com:443. Incorrect username or password was specified.

17:55:09  Check your database credentials and try again. For more information, visit:
https://docs.getdbt.com/docs/configure-your-profile
"""

SHOW_DIM_CUSTOMERS = """\
{
  "node": "dim_customers",
  "show": [
    {
      "CUSTOMER_ID": 1,
      "CUSTOMER_NAME": "Customer#000000001",
      "MARKET_SEGMENT": "BUILDING",
      "NATION_NAME": "MOROCCO"
    }
  ]
}
"""

SHOW_INLINE_CREATE_TABLE = """\
{
  "show": [
    {
      "status": "Table T3_DEV successfully created."
    }
  ]
}
"""

COMPILE_DIM_CUSTOMERS = """\
{
  "node": "dim_customers",
  "compiled": "select\\n    customers.customer_id,\\n    customers.customer_name\\nfrom DBT_AGENT_DEV.DEV.stg_customers as customers"
}
"""

MODEL_YAML_DIM_CUSTOMERS = """\
version: 2

models:
  - name: dim_customers
    description: ""
    columns:
      - name: customer_id
        data_type: number
        description: ""

      - name: customer_name
        data_type: varchar
        description: ""

      - name: market_segment
        data_type: varchar
        description: ""

      - name: nation_name
        data_type: varchar
        description: ""

"""

MODEL_YAML_UNBUILT = """\
version: 2

models:
  - name: unbuilt_model
    description: ""
    columns:
"""

LS_TWO_VIEWS = (
    '{"name": "stg_orders", "config.materialized": "view"}\n'
    '{"name": "stg_customers", "config.materialized": "view"}\n'
)

PARSE_WARNING = """\
17:58:03  [WARNING]: Did not find matching node for patch with name 'orphan' in the 'models' section of file 'models/orphan_patch.yml'
"""

RO_INSUFFICIENT_PRIVILEGES = """\
17:47:17  [ERROR]: Encountered an error:
Runtime Error
  Database Error in sql_operation inline_query (from remote system.sql)
    003001 (42501): SQL access control error:
    Insufficient privileges to operate on schema 'T_SCRATCH'. Your primary role DBT_AGENT_RO must have CREATE TABLE granted on SCHEMA DBT_AGENT_DEV.T_SCRATCH.
"""


# --- Project and runner -----------------------------------------------------


@pytest.fixture
def project_dir(tmp_path: Path) -> Path:
    """A minimal dbt project with a fake ``.venv/bin/dbt`` and two models."""
    project = tmp_path / "proj"
    (project / "models").mkdir(parents=True)
    (project / "dbt_project.yml").write_text("name: testbed\nversion: '1.0'\n")
    (project / "models" / "stg_orders.sql").write_text("select 1 as id\n")
    (project / "models" / "stg_customers.sql").write_text("select 1 as id\n")
    dbt = project / ".venv" / "bin" / "dbt"
    dbt.parent.mkdir(parents=True)
    dbt.write_text("#!/bin/sh\n")
    dbt.chmod(0o755)
    return project


def run_results(
    models: dict[str, str],
    tests: dict[str, str] | None = None,
    *,
    invocation_id: str = "inv-1",
    messages: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Build a ``run_results.json`` document from ``{name: status}`` maps."""
    messages = messages or {}
    results = [
        {
            "status": status,
            "unique_id": f"model.testbed.{name}",
            "message": messages.get(name, "SUCCESS 1"),
            "failures": None,
        }
        for name, status in models.items()
    ]
    results += [
        {
            "status": status,
            "unique_id": f"test.testbed.{name}",
            "message": messages.get(name, None),
            "failures": 0 if status == "pass" else 1,
        }
        for name, status in (tests or {}).items()
    ]
    return {
        "metadata": {
            "dbt_version": "1.12.5",
            "generated_at": "2026-10-02T17:00:00Z",
            "invocation_id": invocation_id,
        },
        "results": results,
        "elapsed_time": 3.2,
    }


def write_run_results(project_dir: Path, document: dict[str, Any]) -> None:
    """Write ``document`` as ``target/run_results.json``."""
    target = project_dir / "target"
    target.mkdir(exist_ok=True)
    (target / "run_results.json").write_text(json.dumps(document))


class FakeRun:
    """Scripted runner: canned (returncode, stdout) per dbt subcommand, in order.

    Records every argv so tests can assert the canonical call. An optional
    side effect runs when the response is served (to write artifacts).
    """

    def __init__(self) -> None:
        self.calls: list[list[str]] = []
        self._responses: dict[
            str, list[tuple[int, str, Callable[[], None] | None]]
        ] = {}

    def script(
        self,
        command: str,
        returncode: int = 0,
        stdout: str = "",
        side_effect: Callable[[], None] | None = None,
    ) -> None:
        self._responses.setdefault(command, []).append(
            (returncode, stdout, side_effect)
        )

    def __call__(self, argv: list[str], cwd: Path, timeout_s: float) -> Result:
        self.calls.append(list(argv))
        command = subcommand(argv)
        queue = self._responses.get(command)
        if not queue:
            raise AssertionError(f"unexpected dbt call: {command} ({argv})")
        returncode, stdout, side_effect = queue.pop(0)
        if side_effect is not None:
            side_effect()
        return Result(tuple(argv), returncode, stdout, "", 0.01)

    def argv_for(self, command: str) -> list[str]:
        """The last argv recorded for ``command``."""
        for argv in reversed(self.calls):
            if subcommand(argv) == command:
                return argv
        raise AssertionError(f"no call to {command}")


def subcommand(argv: list[str]) -> str:
    """The dbt subcommand in a canonical argv (first non-flag after ``dbt``)."""
    after_dbt = argv[argv.index("dbt") + 1 :]
    return next(a for a in after_dbt if not a.startswith("--"))


@pytest.fixture
def fake_run() -> FakeRun:
    return FakeRun()


def make_ready(
    session: Any, fake: FakeRun, ls_select: str = "stg_orders stg_customers"
) -> None:
    """Drive ``session`` through debug, parse and ls with nominal outputs."""
    fake.script("debug", 0, DEBUG_OK)
    fake.script("parse", 0, "")
    fake.script("ls", 0, LS_TWO_VIEWS)
    assert session.debug().ok
    assert session.parse().ok
    assert session.ls(ls_select, ["stg_orders", "stg_customers"]).ok

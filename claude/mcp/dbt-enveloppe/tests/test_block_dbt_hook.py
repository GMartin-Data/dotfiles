"""The Bash hook blocks every launcher of dbt and lets everything else through (plan §8, step 5)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[4]
HOOK = REPO / "claude" / "hooks" / "block-dbt.sh"
SETTINGS = REPO / "claude" / "settings.json"
INSTALL = REPO / "install.sh"

MUST_BLOCK = [
    "dbt",
    "dbt build",
    "dbt --version",
    "uv run dbt parse",
    'uv run --project "$CLAUDE_PROJECT_DIR" --no-sync dbt ls --select stg_orders',
    "uvx --from dbt-core dbt run",
    "python -m dbt run",
    "python3 -m dbt.cli.main run",
    "python -c \"from dbt.cli.main import dbtRunner; dbtRunner().invoke(['run'])\"",
    "/home/martin/dbt-agent-testbed/.venv/bin/dbt debug",
    ".venv/bin/dbt debug",
    "./dbt run",
    "sh -c 'dbt run'",
    'sh -c "cd ~/dbt-agent-testbed && dbt build"',
    'bash -c "uv run dbt build"',
    "cd ~/dbt-agent-testbed && dbt build",
    "ls; dbt run",
    "dbt build | tee build.log",
    "DBT_PROFILES_DIR=~/.dbt dbt debug",
    "timeout 60 dbt run",
    "nohup dbt run &",
    "time dbt run",
    "exec dbt run",
    "command dbt run",
    "echo $(dbt ls)",
    "echo `dbt ls`",
    "(cd ~/dbt-agent-testbed && dbt run)",
    'echo "$(dbt ls)"',
    "echo 'dbt run' | sh",
    "bash <<EOF\ncd ~/dbt-agent-testbed\ndbt run\nEOF",
    "python <<EOF\nfrom dbt.cli.main import dbtRunner\ndbtRunner().invoke(['run'])\nEOF",
]

MUST_PASS = [
    "",
    'git commit -m "feat(hooks): block dbt from Bash"',
    "git commit -m \"$(cat <<'EOF'\nfeat(hooks): block dbt from Bash\n\n"
    'The dbt subagent is the only way to run dbt build.\nEOF\n)"',
    "git commit -m \"$(cat <<'EOF'\ndocs(plan): record step 5 results\n\n"
    "dbt docs generate stays manual: no ninth tool.\n"
    'uv run dbt is blocked by the hook as well.\nEOF\n)"',
    "git log --oneline --grep=dbt",
    "dbt-enveloppe parse",
    "uv run dbt-enveloppe ls --select stg_orders",
    "uv run --project ~/.claude/mcp/dbt-enveloppe --no-sync dbt-enveloppe-mcp",
    "uv run pytest tests/test_block_dbt_hook.py",
    "uv run ruff check src/dbt_enveloppe",
    "uv add dbt-core",
    "uv pip show dbt-snowflake",
    'grep -rn "dbt run" docs/',
    'grep -n "block-rm-rf\\|hooks/\\|dbt" claude/README.md | head -30',
    'grep -E "ls|dbt" README.md',
    "rg 'dbt|parse' src/",
    "rg dbt_parse src/dbt_enveloppe/server.py",
    "cat dbt_project.yml",
    "ls ~/dbt-agent-testbed/models",
    "ls dbt_packages",
    'echo "dbt build"',
    "cd ~/dbt-agent-testbed",
    "python -c \"print('hello')\"",
]


def run_hook(command: str) -> subprocess.CompletedProcess[str]:
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    return subprocess.run(
        [str(HOOK)], input=payload, capture_output=True, text=True, check=False
    )


@pytest.mark.parametrize("command", MUST_BLOCK)
def test_blocks(command: str) -> None:
    result = run_hook(command)
    assert result.returncode == 2, result.stderr
    assert result.stderr.startswith("BLOCKED")


@pytest.mark.parametrize("command", MUST_PASS)
def test_passes(command: str) -> None:
    result = run_hook(command)
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""


def test_block_message_tells_claude_the_two_ways_out() -> None:
    err = run_hook("uv run dbt deps").stderr
    assert "`dbt` subagent" in err
    assert "`! " in err


def test_settings_deny_dbt_from_bash() -> None:
    settings = json.loads(SETTINGS.read_text())
    assert "Bash(dbt *)" in settings["permissions"]["deny"]


def test_settings_run_the_hook_on_every_bash_call() -> None:
    settings = json.loads(SETTINGS.read_text())
    entries = [
        hook
        for group in settings["hooks"]["PreToolUse"]
        if group["matcher"] == "Bash"
        for hook in group["hooks"]
        if hook["command"].endswith("block-dbt.sh")
    ]
    assert len(entries) == 1
    assert "if" not in entries[0]


def test_install_links_the_hook() -> None:
    assert 'link "$DOTFILES_DIR/claude/hooks/block-dbt.sh"' in INSTALL.read_text()

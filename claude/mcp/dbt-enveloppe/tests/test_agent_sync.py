"""The agent body copies the specification verbatim (plan §2): fail on any drift."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[4]
SPEC = REPO / "tasks" / "dbt-agent-2026-10" / "spec.md"
AGENT = REPO / "claude" / "agents" / "dbt.md"

BLOCK = re.compile(r"<!-- DÉBUT (.+?) -->\n(.*?)\n<!-- FIN \1 -->", re.DOTALL)
BLOCK_NAMES = [
    "SOCLE",
    "SECTION debug",
    "SECTION parse",
    "SECTION ls",
    "SECTION compile",
    "SECTION show",
    "SECTION run-operation",
    "SECTION codegen",
]


def spec_blocks() -> dict[str, str]:
    return {name: body.strip() for name, body in BLOCK.findall(SPEC.read_text())}


def spec_section(heading: str) -> str:
    text = SPEC.read_text()
    start = text.index(heading) + len(heading)
    end = text.index("\n## ", start)
    return text[start:end].strip()


@pytest.fixture(scope="module")
def agent() -> str:
    return AGENT.read_text()


def test_spec_still_has_the_eight_blocks() -> None:
    assert sorted(spec_blocks()) == sorted(BLOCK_NAMES)


@pytest.mark.parametrize("name", BLOCK_NAMES)
def test_block_is_copied_verbatim(agent: str, name: str) -> None:
    assert spec_blocks()[name] in agent


def test_workflow_diagram_is_copied_verbatim(agent: str) -> None:
    overview = spec_section("## 1. Vue d'ensemble")
    diagram = re.search(r"```mermaid\n.*?```", overview, re.DOTALL)
    assert diagram is not None
    assert diagram.group(0) in agent


def test_never_do_list_is_copied_verbatim(agent: str) -> None:
    assert spec_section("## 4. Ce qu'il ne faut jamais faire") in agent

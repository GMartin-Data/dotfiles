#!/usr/bin/env bash
# Bare project with an empty CLAUDE.md placeholder: the Step 0 gate must open.
set -euo pipefail

mkdir -p "$PWD/src"
: > "$PWD/CLAUDE.md"

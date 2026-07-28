#!/usr/bin/env bash
# Build the SV1 fixture repo in the CURRENT directory (must be an empty eval
# CWD, outside the dotfiles repo). Creates a 5-commit history whose final
# state contradicts the README claims on purpose: README says "3 commits" and
# documents a `timeout` field that config.yaml does not define.
set -euo pipefail

if [ -e .git ]; then
  echo "refusing to run: .git already exists here" >&2
  exit 1
fi

git init -q
git config user.name "fixture"
git config user.email "fixture@eval.local"

commit() { git add -A >/dev/null && git commit -qm "$1"; }

cat > README.md <<'EOF'
# sv1-fixture-service

Small service used as an eval fixture.
EOF
commit "docs: bootstrap README"

cat > config.yaml <<'EOF'
service:
  name: sv1-fixture
  retries: 1
logging:
  level: debug
EOF
commit "feat: initial runtime config"

cat > notes.md <<'EOF'
Operational notes live here.
EOF
commit "docs: add operational notes"

cat > config.yaml <<'EOF'
service:
  name: sv1-fixture
  retries: 3
  backoff_seconds: 2
logging:
  level: info
EOF
commit "feat: tune retries and switch logging to info"

cat > README.md <<'EOF'
# sv1-fixture-service

Small service used as an eval fixture.

This repository has 3 commits. Runtime configuration lives in `config.yaml`
(`timeout`, `retries`, `backoff_seconds`).
EOF
commit "docs: document repo state in README"

echo "sv1 fixture ready: $(git rev-list --count HEAD) commits"

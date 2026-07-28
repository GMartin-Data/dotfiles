#!/usr/bin/env bash
# Assemble one eval run directory for the claude-md batch A corpus.
#
# Usage: setup-eval-cwd.sh <RULE> <with|without> <target-dir>
#   RULE ∈ {DN1, DN2, DN5, SV1, K3}
#
# Produces:
#   <target-dir>/cwd/     working directory for the claude -p run (fixtures in place)
#   <target-dir>/config/  scratch CLAUDE_CONFIG_DIR — the payload variant becomes
#                         the user-level CLAUDE.md there, so the real
#                         ~/.claude/CLAUDE.md is never injected (no double
#                         injection); credentials symlinked, no hooks, no skills
set -euo pipefail

CORPUS_DIR="$(cd "$(dirname "$0")" && pwd)"
PAYLOAD="$CORPUS_DIR/../../CLAUDE.md"
RULE="${1:?rule id required (DN1|DN2|DN5|SV1|K3)}"
VARIANT="${2:?variant required (with|without)}"
TARGET="${3:?target dir required}"
RULE_FILE="$CORPUS_DIR/rules/$RULE.md"

[ -f "$RULE_FILE" ] || { echo "unknown rule: $RULE" >&2; exit 1; }
case "$VARIANT" in with|without) ;; *) echo "variant must be with|without" >&2; exit 1 ;; esac

mkdir -p "$TARGET/cwd" "$TARGET/config"

# 1. User-level CLAUDE.md variant: full payload, or payload minus the tested
#    rule. Fails fast if the verbatim anchor no longer matches the payload
#    (corpus drift guard).
python3 - "$PAYLOAD" "$RULE_FILE" "$VARIANT" > "$TARGET/config/CLAUDE.md" <<'PY'
import pathlib
import sys

payload = pathlib.Path(sys.argv[1]).read_text()
rule = pathlib.Path(sys.argv[2]).read_text()
if rule not in payload:
    sys.exit(f"verbatim anchor {sys.argv[2]} not found in payload — corpus drifted")
sys.stdout.write(payload.replace(rule, "", 1) if sys.argv[3] == "without" else payload)
PY

# 2. Scratch config: reuse real credentials (symlink — no secret copies), reuse
#    onboarding state, no hooks/settings so runs stay unpolluted.
ln -sf "$HOME/.claude/.credentials.json" "$TARGET/config/.credentials.json"
[ -f "$HOME/.claude.json" ] && cp "$HOME/.claude.json" "$TARGET/config/.claude.json"
echo '{}' > "$TARGET/config/settings.json"

# 3. Fixtures
case "$RULE" in
  DN1) cp "$CORPUS_DIR/fixtures/dn1/data.csv" "$TARGET/cwd/" ;;
  K3)  cp "$CORPUS_DIR/fixtures/k3/pagination.py.txt" "$TARGET/cwd/pagination.py" ;;
  SV1) ( cd "$TARGET/cwd" && "$CORPUS_DIR/fixtures/sv1/setup-git.sh" >/dev/null ) ;;
  DN2|DN5) ;; # prompt-only fixtures
esac

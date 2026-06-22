#!/usr/bin/env bash
# Prepare a temporary CWD with the fixtures required by a given eval id.
# Usage: ./setup-eval-cwd.sh <eval-id>
# Prints the absolute path of the created CWD on stdout.

set -euo pipefail

usage() {
    cat >&2 <<EOF
Usage: $0 <eval-id>

Eval ids (see planning.eval.json):
  strict-mode-existing-plan       CWD with a pre-existing PLAN.md (strict-mode gate)
  preflight-prd-absent            Empty CWD (no PRD.md -> command aborts)
  preflight-nominal               CWD with PRD.md + CLAUDE.md (both sources read)
  interview-cap-three-questions   CWD with PRD.md + CLAUDE.md (breakdown interview)
EOF
    exit 2
}

if [[ $# -ne 1 ]]; then
    usage
fi

EVAL_ID="$1"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
CWD="/tmp/planning-eval-${EVAL_ID}-${TIMESTAMP}"

# Writes a PRD.md fixture with enough substance to derive a phase breakdown.
write_prd() {
    cat > "$1/PRD.md" <<'EOF'
# PRD — feed-aggregator

## Problème
Un utilisateur suit une dizaine de sources (RSS, newsletters, GitHub releases)
dispersées. Il veut un flux unifié, dédupliqué, consultable en un endroit.

## Solution
Un agrégateur qui ingère les sources, normalise les entrées, déduplique, et
expose un flux trié par date via une petite API + une vue web.

## User Stories
- En tant qu'utilisateur, je veux ajouter une source par URL, afin de l'inclure
  dans mon flux.
- En tant qu'utilisateur, je veux que les doublons soient fusionnés, afin de ne
  pas lire deux fois la même info.
- En tant qu'utilisateur, je veux consulter le flux trié par date, afin de voir
  les nouveautés en premier.

## Périmètre v1
| Inclus | Exclu (v2+) |
|--------|-------------|
| Ingestion RSS + GitHub | Newsletters par email |
| Déduplication par hash de contenu | Dédup sémantique (embeddings) |
| API REST de lecture | Authentification multi-utilisateur |
| Vue web minimale | Application mobile |

## Critères de succès
- Une source ajoutée apparaît dans le flux sous 5 min.
- Zéro doublon visible sur un corpus de test de 200 entrées.
EOF
}

# Writes a minimal CLAUDE.md fixture (stack + conventions the PLAN can reference).
write_claude_md() {
    cat > "$1/CLAUDE.md" <<'EOF'
# CLAUDE.md — feed-aggregator

## Stack
- Python 3.12, package manager uv
- FastAPI (API REST), httpx (ingestion), SQLite (stockage v1)

## Conventions
- Conventional Commits, tests pytest, ruff pour le lint
EOF
}

case "$EVAL_ID" in
    strict-mode-existing-plan)
        mkdir -p "$CWD"
        write_prd "$CWD"
        cat > "$CWD/PLAN.md" <<'EOF'
# PLAN — placeholder

Placeholder PLAN used as a fixture for the strict-mode gate eval. Its content
is intentionally minimal — the eval only cares that PLAN.md exists.
EOF
        ;;

    preflight-prd-absent)
        mkdir -p "$CWD"
        ;;

    preflight-nominal | interview-cap-three-questions)
        mkdir -p "$CWD"
        write_prd "$CWD"
        write_claude_md "$CWD"
        ;;

    *)
        echo "error: unknown eval id '$EVAL_ID'" >&2
        usage
        ;;
esac

echo "$CWD"

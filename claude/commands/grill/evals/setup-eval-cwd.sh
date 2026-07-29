#!/usr/bin/env bash
# Prepare a temporary CWD with the fixtures required by a given eval id.
# Usage: ./setup-eval-cwd.sh <eval-id>
# Prints the absolute path of the created CWD on stdout.

set -euo pipefail

usage() {
    cat >&2 <<EOF
Usage: $0 <eval-id>

Eval ids (see grill.eval.json):
  preflight-artifact-absent          Empty CWD (no prd.md/plan.md -> command stops, asks)
  no-open-questions-section          prd.md WITHOUT an 'Open questions' section (anti-triviality)
  deferred-branch-in-output          prd.md with a branch needing external input (-> DEFERRED)
  input-explicit-arg-over-fallback   root prd.md + docs/specs/custom-prd.md (explicit arg wins)
  output-no-file-written             prd.md (checks zero side effect + copiable block + invite)
  spike-routing-indeliberable-branch prd.md with one indeliberable branch (-> SPIKE) + one deliberable tension
EOF
    exit 2
}

if [[ $# -ne 1 ]]; then
    usage
fi

EVAL_ID="$1"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
CWD="/tmp/grill-eval-${EVAL_ID}-${TIMESTAMP}"

# Writes a PRD with a DELIBERATE cross-section tension and NO 'Open questions'
# section. The tension: the Constraints forbid any third-party network call, but an
# Acceptance criterion requires enriching entries from an external API. A linear
# re-read misses it; grill must surface it. Used by the anti-triviality and
# no-side-effect evals.
write_prd_with_tension() {
    cat > "$1/prd.md" <<'EOF'
# PRD — link-saver

## Problème
Un utilisateur sauvegarde des liens à la volée mais les retrouve mal : pas de
titre, pas de résumé, juste une URL brute dans un fichier texte.

## Solution
Un service qui ingère une URL, en extrait un titre et un court résumé, et expose
la collection cherchable.

## User Stories
- En tant qu'utilisateur, je veux coller une URL et obtenir un titre lisible,
  afin de retrouver le lien plus tard.
- En tant qu'utilisateur, je veux un résumé d'une phrase par lien, afin de
  décider quoi rouvrir sans cliquer.

## Périmètre cible
| Dans la cible | Hors-cible |
|---------------|------------|
| Extraction de titre depuis le HTML de la page | Capture d'écran de la page |
| Résumé d'une phrase | Traduction multilingue |
| Recherche plein-texte locale | Partage entre utilisateurs |

## Critères de succès
- Un lien collé reçoit un titre sous 3 secondes.
- Un lien collé reçoit un résumé d'une phrase généré par un service de résumé
  externe.
- La recherche retourne les liens pertinents sur un corpus de 500 entrées.

## Contraintes
- Fonctionne entièrement hors-ligne après installation : AUCUN appel réseau vers
  un tiers en runtime (souveraineté des données, pas de fuite d'URL).
- Stockage local SQLite, pas de backend distant.
EOF
}

# Writes a PRD with one DELIBERATE indeliberable branch (only an observation can
# settle it: can a <=2 GB embedded model summarize in <3 s on laptop CPU?) plus
# one deliberable ambiguity (an argument settles it: does fetching the saved
# URL's own HTML count as a "third-party network call"?). Grill must route the
# former to SPIKE and resolve the latter in-session — tagging both SPIKE, or
# neither, fails the eval. Used by the spike-routing eval.
write_prd_with_indeliberable_branch() {
    cat > "$1/prd.md" <<'EOF'
# PRD — link-saver (local-first)

## Problème
Un utilisateur sauvegarde des liens à la volée mais les retrouve mal : pas de
titre, pas de résumé, juste une URL brute dans un fichier texte.

## Solution
Un service local qui ingère une URL, en extrait un titre, génère un résumé
d'une phrase avec un modèle embarqué, et expose la collection cherchable.

## User Stories
- En tant qu'utilisateur, je veux coller une URL et obtenir un titre lisible,
  afin de retrouver le lien plus tard.
- En tant qu'utilisateur, je veux un résumé d'une phrase par lien, afin de
  décider quoi rouvrir sans cliquer.

## Critères de succès
- Un lien collé reçoit un titre sous 3 secondes.
- Un lien collé reçoit un résumé d'une phrase généré par un modèle embarqué de
  2 Go maximum, en moins de 3 secondes.
- La recherche retourne les liens pertinents sur un corpus de 500 entrées.

## Contraintes
- AUCUN appel réseau vers un service tiers en runtime (souveraineté des
  données, pas de fuite d'URL).
- Stockage local SQLite, pas de backend distant.
- Matériel cible : laptop CPU, sans GPU.
EOF
}

case "$EVAL_ID" in
    preflight-artifact-absent)
        mkdir -p "$CWD"
        ;;

    no-open-questions-section | output-no-file-written | deferred-branch-in-output)
        mkdir -p "$CWD"
        write_prd_with_tension "$CWD"
        ;;

    spike-routing-indeliberable-branch)
        mkdir -p "$CWD"
        write_prd_with_indeliberable_branch "$CWD"
        ;;

    input-explicit-arg-over-fallback)
        mkdir -p "$CWD/docs/specs"
        # Decoy at root (fallback target) — must be IGNORED when an arg is passed.
        cat > "$CWD/prd.md" <<'EOF'
# PRD — DECOY (root)

Ce PRD à la racine est la cible du fallback. L'eval vérifie qu'il est IGNORÉ
quand un argument explicite désigne un autre fichier. Si grill grille CE
fichier, l'eval échoue.
EOF
        # Explicit-arg target — this is what must actually be grilled.
        cat > "$CWD/docs/specs/custom-prd.md" <<'EOF'
# PRD — link-saver (cible explicite)

Ce fichier est passé en argument explicite : c'est LUI que grill doit griller,
pas le prd.md de la racine.

## Critères de succès
- Un lien collé reçoit un résumé généré par un service externe.

## Contraintes
- Aucun appel réseau tiers en runtime.
EOF
        ;;

    *)
        echo "error: unknown eval id '$EVAL_ID'" >&2
        usage
        ;;
esac

echo "$CWD"

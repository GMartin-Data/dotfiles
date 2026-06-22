#!/usr/bin/env bash
# Prepare a temporary CWD with the fixtures required by a given eval id.
# Usage: ./setup-eval-cwd.sh <eval-id>
# Prints the absolute path of the created CWD on stdout.

set -euo pipefail

usage() {
    cat >&2 <<EOF
Usage: $0 <eval-id>

Eval ids (see adr.eval.json):
  numbering-empty-adr-dir        Empty adr/ directory (next ADR = 0001)
  numbering-with-gap             adr/ with 0001 + 0003 (next = 0004, gap kept)
  mode-interview-default         Empty adr/ ; /adr without --from-context
  mode-capture-from-context      Empty adr/ ; /adr --from-context
  supersession-bidirectional     adr/ with an Accepted ADR-0007 to supersede
  immutability-body-refused      adr/ with an Accepted ADR-0007 (body edit attempt)
  no-source-trace-in-output      Empty adr/ ; checks generated header fields
EOF
    exit 2
}

if [[ $# -ne 1 ]]; then
    usage
fi

EVAL_ID="$1"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
CWD="/tmp/adr-eval-${EVAL_ID}-${TIMESTAMP}"

# Writes an Accepted ADR-0007 fixture into $1/adr/.
write_adr_0007() {
    local dir="$1"
    mkdir -p "$dir/adr"
    cat > "$dir/adr/0007-pubsub-pour-async.md" <<'EOF'
# ADR-0007 : Choix de Pub/Sub pour la file d'attente async

Status: Accepted
Date: 2025-11-15

## Contexte

Le pipeline d'ingestion doit découpler la réception des événements de leur
traitement. Une file d'attente managée est nécessaire.

## Options considérées

- **Pub/Sub** : managé, scaling automatique, intégration GCP native.
- **Cloud Tasks** : managé, mais orienté tâches HTTP, throughput moindre.
- **Self-hosted RabbitMQ** : contrôle total, mais charge opérationnelle.

## Décision

Pub/Sub retenu pour le scaling automatique et l'intégration GCP native.

## Conséquences

- Découplage ingestion / traitement acquis.
- Dépendance forte au lock-in GCP acceptée.
EOF
}

case "$EVAL_ID" in
    numbering-empty-adr-dir | mode-interview-default | mode-capture-from-context | no-source-trace-in-output)
        mkdir -p "$CWD/adr"
        ;;

    numbering-with-gap)
        mkdir -p "$CWD/adr"
        cat > "$CWD/adr/0001-choix-stack.md" <<'EOF'
# ADR-0001 : Choix de la stack

Status: Accepted
Date: 2025-10-01

## Décision

Placeholder fixture — only the file's number (0001) matters for this eval.
EOF
        cat > "$CWD/adr/0003-pattern-async.md" <<'EOF'
# ADR-0003 : Pattern async

Status: Accepted
Date: 2025-10-20

## Décision

Placeholder fixture — only the file's number (0003) matters for this eval.
The 0002 gap is intentional: the eval checks that /adr assigns 0004, not 0002.
EOF
        ;;

    supersession-bidirectional | immutability-body-refused)
        write_adr_0007 "$CWD"
        ;;

    *)
        echo "error: unknown eval id '$EVAL_ID'" >&2
        usage
        ;;
esac

echo "$CWD"

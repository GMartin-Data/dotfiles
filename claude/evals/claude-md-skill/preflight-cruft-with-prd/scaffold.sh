#!/usr/bin/env bash
# Fresh Cruft instance plus a canonical (abridged) PRD.md: the conditional gate must pass.
set -euo pipefail

# The runner swaps HOME for a sandbox home: resolve the real one for the template and uv tools.
REAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
TEMPLATE="${CRUFT_TEMPLATE_PATH:-$REAL_HOME/python-project-template-v2}"
[[ -d "$TEMPLATE" ]] || { echo "template not found: $TEMPLATE (set CRUFT_TEMPLATE_PATH)" >&2; exit 1; }
CRUFT="$(command -v cruft || echo "$REAL_HOME/.local/bin/cruft")"
[[ -x "$CRUFT" ]] || { echo "cruft not installed (uv tool install cruft)" >&2; exit 1; }

"$CRUFT" create "$TEMPLATE" --output-dir "$PWD" --no-input >&2
generated="$(find "$PWD" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
shopt -s dotglob
mv "$generated"/* "$PWD"/
rmdir "$generated"

# Canonical PRD (ADR-0013): problem, objectives, users, constraints; never stack nor architecture.
cat > "$PWD/PRD.md" <<'EOF'
# PRD — demo-instance

## Résumé
Outil interne de consolidation de rapports CSV mensuels. Fixture d'eval au
format canonique abrégé (ADR-0013).

## Problème
Les rapports mensuels sont consolidés à la main, opération répétitive et
sujette aux erreurs.

## Objectifs
- Zéro consolidation manuelle.

## Utilisateurs & scénarios
Usage personnel (A). CLI : une commande sur un dossier de rapports produit le
consolidé.

## Fonctionnalités (cible)
- Lecture des CSV mensuels, consolidation en un fichier annuel.

## Non-goals
- Aucune interface graphique — hors du besoin, jamais.

## Contraintes
- Les rapports contiennent des données clients : traitement local uniquement,
  aucun service cloud.

## Acceptance criteria

### Scénarios nominaux
- [ ] En tant qu'utilisateur, je peux consolider un dossier en une commande.

### Indicateurs mesurables
- [ ] 12 rapports mensuels consolidés sans édition manuelle.

## Open questions
- Les CSV ont-ils le même schéma sur toute l'année ?

## Au-delà de la cible
Export vers un tableur partagé (candidat à révision par ADR).
EOF

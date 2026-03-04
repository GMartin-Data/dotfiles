#!/bin/bash
# =============================================================================
# maintenance.sh — Maintenance automatisée du conteneur Linux (Crostini)
# =============================================================================

set -euo pipefail

# --- Logging ---
LOG_FILE="$HOME/.local/logs/maintenance.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

section() {
    log ""
    log ">>> $1"
}

# --- Rotation du log de maintenance ---
MAX_LOG_SIZE=1048576  # 1 Mo en octets
if [ -f "$LOG_FILE" ] && [ "$(stat -c%s "$LOG_FILE")" -gt "$MAX_LOG_SIZE" ]; then
    tail -n 200 "$LOG_FILE" > "${LOG_FILE}.tmp"
    mv "${LOG_FILE}.tmp" "$LOG_FILE"
fi

# --- Début ---
START_TIME=$(date +%s)
log "=== Début maintenance : $(date) ==="
log "Espace disque disponible : $(df -h | awk 'NR>1 && $6=="/" {print $4 " libres sur " $2 " (" $5 " utilisés)"}')"

# =============================================================================
# 1. Paquets système (apt)
# =============================================================================
section "Paquets système (apt)"
export DEBIAN_FRONTEND=noninteractive
log "Mise à jour des listes de paquets..."
sudo apt-get update -q
log "Mise à jour des paquets installés..."
sudo apt-get upgrade -y -q
log "Suppression des dépendances orphelines..."
sudo apt-get autoremove -y -q
log "Nettoyage du cache apt..."
sudo apt-get clean
log "apt : OK"

# =============================================================================
# 2. Caches et logs
# =============================================================================
section "Caches et logs"
log "Nettoyage du cache uv..."
uv cache clean
log "Nettoyage du journal systemd (> 7 jours)..."
sudo journalctl --vacuum-time=7d
log "Caches et logs : OK"

# =============================================================================
# 3. Outils de développement (uv, Node, Claude Code, gcloud)
# =============================================================================
section "Outils de développement"

log "Mise à jour de uv..."
uv self update

log "Mise à jour de npm et des paquets globaux..."
set +euo pipefail
npm install -g npm@latest
npm update -g
set -euo pipefail
log "npm : OK"

log "Mise à jour des composants gcloud..."
gcloud components update --quiet

log "Outils de développement : OK"

# =============================================================================
# 4. Docker
# =============================================================================
section "Docker"
log "Suppression des conteneurs arrêtés, réseaux, images dangling et build cache..."
docker system prune -f
log "Suppression des images non utilisées par un conteneur actif..."
docker image prune -a -f
log "Docker : OK"
echo ""
echo "⚠️  RAPPEL : le nettoyage des volumes Docker est une tâche MANUELLE."
echo "   Commandes utiles :"
echo "     docker volume ls                  → lister tous les volumes"
echo "     docker volume prune               → supprimer les volumes orphelins"
echo "     docker volume rm <nom>            → supprimer un volume spécifique"
echo ""

# --- Fin ---
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
log ""
log "=== Maintenance terminée en ${DURATION}s ==="

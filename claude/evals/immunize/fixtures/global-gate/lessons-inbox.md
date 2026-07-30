# Lessons Inbox

Réponse innée au cycle immunitaire. Chaque entrée est datée et sera évaluée par `/immunize` :
- 2+ occurrences → promotion vers `## Do NOT` projet ou `## Global Do NOT` global
- Entrée unique > 7 jours → archivage
- Entrée unique ≤ 7 jours → conservation

---

- [2026-07-16] Claude a écrit `scripts/refresh_forecasts.sh` avec des chemins relatifs (`./data/raw`) — le cron l'exécute depuis `/`, échec silencieux découvert 3 jours plus tard.
- [2026-07-24] Même pattern dans `scripts/backfill_history.py` : `open("data/stations.csv")` marche en interactif, casse sous cron. Générique tous projets : un script destiné à un scheduler doit résoudre ses chemins depuis son propre emplacement, jamais depuis le CWD.

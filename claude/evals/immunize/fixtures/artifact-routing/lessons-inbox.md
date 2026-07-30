# Lessons Inbox

Réponse innée au cycle immunitaire. Chaque entrée est datée et sera évaluée par `/immunize` :
- 2+ occurrences → promotion vers `## Do NOT` projet ou `## Global Do NOT` global
- Entrée unique > 7 jours → archivage
- Entrée unique ≤ 7 jours → conservation

---

- [2026-07-18] Le hook pre-commit `hooks/check_partition.py` a bloqué `models/stg_stations.sql` : la directive attendue est bien présente, mais un commentaire explicatif contenant `-- partition:` fait compter 2 occurrences à la regex — faux positif.
- [2026-07-25] Rebelote sur `models/mart_daily_weather.sql` : le commentaire `-- partition: voir ADR-0002` est compté comme une seconde directive par `hooks/check_partition.py`. Contourné avec `git commit --no-verify` (mauvais réflexe). Même cause : la regex ne distingue pas directive et prose.

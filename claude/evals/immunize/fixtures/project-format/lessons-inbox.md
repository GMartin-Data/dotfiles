# Lessons Inbox

Réponse innée au cycle immunitaire. Chaque entrée est datée et sera évaluée par `/immunize` :
- 2+ occurrences → promotion vers `## Do NOT` projet ou `## Global Do NOT` global
- Entrée unique > 7 jours → archivage
- Entrée unique ≤ 7 jours → conservation

---

- [2026-07-15] `dbt run` complet lancé pour valider la retouche d'un seul modèle (`mart_daily_weather`) — 25 min de run pour un diff d'une ligne ; `dbt run --select mart_daily_weather` suffisait.
- [2026-07-23] Encore un `dbt run` complet après modification de `stg_stations` — en itération de dev, `--select <model>+` cible le sous-graphe impacté ; le run complet ne se justifie qu'en release ou après `--full-refresh`.

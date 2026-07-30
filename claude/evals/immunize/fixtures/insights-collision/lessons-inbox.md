# Lessons Inbox

Réponse innée au cycle immunitaire. Chaque entrée est datée et sera évaluée par `/immunize` :
- 2+ occurrences → promotion vers `## Do NOT` projet ou `## Global Do NOT` global
- Entrée unique > 7 jours → archivage
- Entrée unique ≤ 7 jours → conservation

---

## [INSIGHTS 2026-07-05] ingestion-retry-policy

- **Problème observé** : friction n°2 du rapport /insights du 2026-07-05 — 4 sessions perdues sur des timeouts de l'API Open-Meteo sans retry.
- **Action engagée** : retry exponentiel (3 tentatives) ajouté dans `scripts/fetch_forecasts.py`.
- **Critère de succès vérifiable** : au prochain /insights, zéro session perdue sur timeout API.
- **Date de revue** : 2026-09-01

---

- [2026-07-08] `dbt test` non lancé après le backfill historique — 2 tests `unique` cassés découverts le lendemain seulement.

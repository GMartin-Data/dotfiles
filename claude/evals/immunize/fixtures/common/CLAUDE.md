# CLAUDE.md — meteo-pipeline

Pipeline d'ingestion météo : API Open-Meteo → DuckDB → dbt.

## Conventions

- Python géré par uv ; SQL formaté par sqlfluff.
- Modèles dbt : préfixes `stg_` / `int_` / `mart_`.
- Hooks pre-commit versionnés dans `hooks/`.

## Do NOT

- Ne jamais committer `profiles.yml` — contient les credentials DuckDB locaux (learned 2026-05).

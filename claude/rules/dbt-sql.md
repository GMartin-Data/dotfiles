---
globs: "*.sql,models/**/*.yml,models/**/*.yaml"
---
# SQL / dbt Conventions

- Kimball dimensional modeling: star schema, explicit fact/dimension separation
- SQL style: lowercase keywords, trailing commas, CTEs over subqueries
- dbt: ref() over hardcoded table names, one model per file
- dbt YAML: every model must have a description and column-level tests for PKs
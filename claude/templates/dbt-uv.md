# Project: [PROJECT_NAME]

## Overview
<!-- One paragraph: what data domain this project models and why -->

## Code skeleton origin
<!-- Fill in the values below at bootstrap; they tell Claude the infrastructure is deterministic and already in place. -->
- Bootstrapped from: `GMartin-Data/python-project-template` [COOKIECUTTER_TAG_OR_SHA]
- Rulesets applied: [e.g. `main-protection` via `scripts/apply-ruleset.sh`]
- Bootstrap options chosen: [e.g. dbt=true, terraform=false, warehouse=Snowflake]

## Stack
- dbt Core, installed via uv (`uv run dbt`)
- Warehouse: [Snowflake / BigQuery — adapt]
- Python 3.12+ for scripting and custom macros

## Commands
- `uv sync` — install dbt + dependencies
- `uv run dbt build` — run models + tests
- `uv run dbt test` — run tests only
- `uv run dbt docs generate && uv run dbt docs serve` — documentation

## Data Architecture
- Kimball dimensional modeling: star schemas
- Layers: staging → intermediate → marts
- Naming: `stg_[source]__[entity]`, `int_[entity]_[verb]`, `fct_[entity]`, `dim_[entity]`

## Quality Gates
- dbt tests on every model (unique, not_null on PKs minimum)
- CI: `dbt build --select state:modified+` on PRs
- No merge without passing dbt tests

## Sources & Seeds
<!-- List key sources and their update frequency -->

## Project-Specific Rules
<!-- SCD types used, incremental strategies, specific grain definitions -->
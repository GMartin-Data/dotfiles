# Project: [PROJECT_NAME]

## Overview
<!-- One paragraph: what infrastructure this manages and for which environment -->

## Code skeleton origin
<!-- Fill in the values below at bootstrap; they tell Claude the infrastructure is deterministic and already in place. -->
- Bootstrapped from: `GMartin-Data/python-project-template` [COOKIECUTTER_TAG_OR_SHA]
- Rulesets applied: [e.g. `main-protection` via `scripts/apply-ruleset.sh`]
- Bootstrap options chosen: [e.g. dbt=false, terraform=true, provider=GCP]

## Stack
- Terraform [VERSION]
- Provider: [GCP / AWS — adapt]
- State backend: [GCS bucket / S3 — adapt]

## Commands
- `terraform init` — initialize providers and modules
- `terraform plan -out=tfplan` — preview changes
- `terraform apply tfplan` — apply reviewed plan
- `terraform fmt -recursive` — format all files

## Structure
- `modules/` — reusable modules
- `environments/` — per-env configs (dev, staging, prod)
- One state file per environment

## Quality Gates
- `terraform plan` required before any apply
- CI: `terraform fmt -check` + `terraform validate` on PRs
- No direct apply to production without PR approval

## Project-Specific Rules
<!-- Naming conventions, tagging strategy, module versioning policy -->
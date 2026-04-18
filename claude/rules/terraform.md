---
paths:
  - "**/*.tf"
  - "**/*.tfvars"
---
# Terraform Conventions

- Always use variables with descriptions — never hardcode values in resources
- Organize: main.tf, variables.tf, outputs.tf, providers.tf per module
- Remote state required — no local tfstate in version control
- Plan before apply — never skip terraform plan

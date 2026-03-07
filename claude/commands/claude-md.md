---
description: Interview structurée pour produire un CLAUDE.md projet avec conventions et structure hiérarchique
argument-hint: [component-path]
allowed-tools: Read, Write
model: sonnet
---

## Contexte utilisateur existant
!`cat ~/.claude/CLAUDE.md 2>/dev/null || echo "Pas de CLAUDE.md global"`

## Contexte projet existant
!`cat CLAUDE.md 2>/dev/null || echo "Pas de CLAUDE.md projet"`

# Conventions Interview

Structured interview process to produce a complete CLAUDE.md (with optional hierarchical structure) through incremental questioning.

---

## Interaction Rules

1. **One question at a time** — never overwhelm with multiple questions
2. **Options A/B/C** — provide choices when discrete alternatives exist
3. **Validate before continuing** — reformulate only on ambiguous answers
4. **YAGNI** — challenge over-engineering, keep conventions minimal
5. **Per-component** — if multi-component project, ask conventions for each
6. **Adapt language** — match user's language throughout interview and output

---

## Interview Sequence

Progress through these phases in order. Skip phases only if clearly irrelevant.

### Phase 1: Project Overview
"What's the project name and structure?"
- Single component or monorepo?
- List components if multiple (e.g., backend, extension, CLI)

### Phase 2: Stack (per component)
For each component:
"What's the stack for [component]?"
- Language + version
- Framework
- Package manager
- Test framework

### Phase 3: Code Conventions (per language)
For each language in the project:
"What are your code conventions for [language]?"
- Type hints / strict mode?
- Docstring format (Google, NumPy, JSDoc)?
- Naming conventions (snake_case, camelCase, PascalCase)?
- Linter / formatter?
- Language for comments?

### Phase 4: Testing Approach
"What's your testing approach?"
- TDD? If yes, strict or light?
- Coverage target?
- Testing pyramid (unit/integration/e2e ratio)?
- What to test (happy path, errors, edge cases)?
- What NOT to test (glue code, trivial)?

### Phase 5: Versioning
"What's your git workflow?"
- Commit format (conventional commits?)
- Scopes if monorepo?
- Who commits? (AI prepares, human validates?)
- Branch strategy?

### Phase 6: Languages
"What language for what context?"
- Code (comments, docstrings)
- Documentation (README, PRD)
- Commit messages

### Phase 7: CI/CD
"What's your CI/CD setup?"
- CI: lint, tests, on which triggers?
- CD: manual or automated? Platform?

### Phase 8: AI Workflow
"How should AI assistants work on this project?"
- Context files to read first?
- Progress tracking file?
- Files to ignore (.claudeignore)?
- Frequent commands?

### Phase 9: Infrastructure (if applicable)
"Does your project use any of these?"

**Database:**
- ORM / query builder?
- Migration tool?
- Connection patterns (pooling, PRAGMAs)?

**Logging:**
- Structured logging (structlog, pino)?
- Format (JSON, pretty)?
- Log levels policy?

**MCP Servers:**
- Which MCP servers are configured?
- When to use each?

Skip subsections that don't apply.

### Phase 10: Sensitive Points
"Any specific warnings or constraints?"
- Secrets management
- API quirks
- Known pitfalls
- Files to never modify

### Phase 11: Documentation Structure (Diagnostic)

**Do NOT ask user preference. Diagnose automatically based on Phase 1-2 answers:**

```
Multi-component with different stacks?
    │
    ├── NO  → CLAUDE.md seul (+ .claude/reference/ si docs volumineuses)
    │
    └── YES → Conventions partagées entre composants?
                  │
                  ├── NO  → Hiérarchique seul
                  │         (component/CLAUDE.md par composant)
                  │
                  └── YES → Hybride
                            (hiérarchique + .claude/reference/)
```

**If Hybrid approach diagnosed:**

Identify which conventions are:
- **Component-specific** → will go in `component/CLAUDE.md`
- **Cross-cutting** → will go in `.claude/reference/`

Present the diagnosis:
> "Based on your project structure, I'll generate:
> - Root CLAUDE.md with global conventions
> - [component]/CLAUDE.md for [language]-specific conventions
> - .claude/reference/ for shared patterns: [list]
>
> Does this structure work for you?"

**Cross-cutting conventions to look for:**
- Testing strategy (if same philosophy across components)
- Logging standards (if unified format)
- Deployment patterns
- API design conventions (if consumed across components)

---

## Final Validation

Before generating, verify each item and present summary for user validation.

### Checklist

#### Required Sections

- [ ] **Project overview** — Name, structure, components
- [ ] **Stack** — Language, framework, package manager, test framework (per component)
- [ ] **Code conventions** — Style, naming, linter/formatter (per language)
- [ ] **Versioning** — Commit format, workflow

#### Conditional Sections

Include if discussed:

- [ ] **Testing approach** — TDD, coverage, pyramid, what to test
- [ ] **Languages** — Code vs docs vs commits
- [ ] **CI/CD** — Lint, tests, deployment
- [ ] **AI workflow** — Context files, progress tracking, commands
- [ ] **Infrastructure** — Database, logging, MCP servers
- [ ] **Files to ignore** — .claudeignore content
- [ ] **Sensitive points** — Secrets, API quirks, pitfalls

#### Documentation Structure

- [ ] **Structure diagnosed** — Mono / Hierarchical / Hybrid
- [ ] **Component CLAUDE.md list** — If hierarchical or hybrid
- [ ] **Reference docs list** — If hybrid, with "When to read" triggers

### Validation Format

Present summary as:

```
Récapitulatif avant génération du CLAUDE.md :

1. Projet : [name] — [structure]
2. Composants : [list]
3. Stack :
   - [component 1] : [language, framework, pkg manager, tests]
   - [component 2] : ...
4. Conventions code :
   - [language 1] : [type hints, docstrings, naming, linter]
   - [language 2] : ...
5. Tests : [approach, coverage, pyramid, priorities]
6. Commits : [format, scopes, workflow]
7. Langues : code=[X], docs=[Y], commits=[Z]
8. CI/CD : [setup]
9. Infrastructure : [DB, logging, MCP]
10. Workflow IA : [context files, commands]
11. Points d'attention : [list]

Structure documentation :
[Display diagnosed structure]

project/
├── CLAUDE.md (racine)
├── [component 1]/
│   └── CLAUDE.md
├── [component 2]/
│   └── CLAUDE.md
└── .claude/
    └── reference/
        ├── [topic-1].md — "When [trigger]"
        └── [topic-2].md — "When [trigger]"

Confirmez-vous ces éléments ? (oui / corrections)
```

**Generate CLAUDE.md files only after explicit "oui" or equivalent confirmation.**

---

## Output Format

### Root CLAUDE.md

Generate with these sections (omit if N/A):

```markdown
# CLAUDE.md — [project-name]

## Vue d'ensemble
[Brief description + pointers to key docs]

## Structure du projet
[Tree structure if relevant]

## Reference Documentation
[If hybrid approach — routing table]

| Document | When to Read |
|----------|--------------|
| `.claude/reference/[topic].md` | [trigger] |

## Conventions [Language] ([component])
### Environnement
### Style de code
### Exemple

## Tests
### Approche
### Pyramide (unit/integration/e2e)
### Couverture cible
### Fonctions à tester en priorité
### Ne pas tester

## Versioning
### Commits
### Workflow Git

## Langues
| Contexte | Langue |
|----------|--------|
| Code (commentaires, docstrings) | ... |
| Documentation | ... |
| Commits | ... |

## CI/CD

## Infrastructure
### Base de données
### Logging
### MCP Servers

## Workflow avec Claude
### Gestion du contexte
### Commandes fréquentes

## Fichiers à ignorer
[.claudeignore content or patterns]

## Points d'attention
[Warnings, secrets, pitfalls]
```

### Child CLAUDE.md (components)

Shorter, focused on delta from root:

```markdown
# CLAUDE.md — [component]

## Environnement
[Language, framework, package manager specific to this component]

## Style de code
[Only if different from root]

## Commandes fréquentes
[Component-specific commands]
```

### Reference Documentation (if hybrid)

For each cross-cutting topic, create `.claude/reference/[topic].md`:

```markdown
# [Topic] — Best Practices

## When to Read
[Explicit trigger: "Read this when working on X"]

## [Content organized by subtopic]
```

---

## Post-Generation

After creating the CLAUDE.md file(s):
1. Confirm file path(s)
2. If hierarchical or hybrid, list all files created
3. Suggest adding to version control
4. Remind to create .claudeignore if discussed
5. If MCP servers mentioned, remind to verify `claude mcp list`

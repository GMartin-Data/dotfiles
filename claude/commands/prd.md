---
argument-hint: [output-filename]
---

# PRD Interview

Structured interview process to produce a comprehensive PRD through incremental questioning.

**Output file:** `$ARGUMENTS` (default: `PRD.md`)

---

## Interaction Rules

1. **One question at a time** — never overwhelm with multiple questions
2. **Options A/B/C** — provide choices when discrete alternatives exist
3. **Validate before continuing** — reformulate only on ambiguous answers
4. **YAGNI** — challenge scope creep, suggest deferring to v2+
5. **Explain tradeoffs** — when user hesitates, provide decision context
6. **Adapt language** — match user's language throughout interview and PRD

---

## Interview Sequence

Progress through these phases in order. Skip phases only if clearly irrelevant.

### Phase 1: Problem
"What problem does this project solve? (User problem, not technical solution)"

Reformulate to validate understanding.

### Phase 2: Users
"Who are the target users?"
- A) Personal use only
- B) Small circle (colleagues/friends)
- C) Public

Explain overhead implications of each choice. If B or C, ask for a brief persona description.

### Phase 3: Interface
"How will users interact with this?"

Propose options based on problem context (CLI, extension, web app, API, etc.)

### Phase 4: Workflow
"What happens when the user triggers the main action?"

Propose concrete options (auto-download, copy to clipboard, show preview, etc.)

### Phase 5: User Stories
"Let's define 3-5 key user stories. Complete this sentence:"

> "As a [user], I want to [action], so that [benefit]"

Propose stories based on previous answers. User confirms, modifies, or adds.

### Phase 6: Scope
"What's in v1 vs deferred to later?"

Push for minimal viable scope. Explicitly name what's OUT. Group by category if helpful:
- Core functionality
- Technical aspects
- Integrations
- Deployment

### Phase 7: Output Format
If the project produces output files/data:
"What should the output look like?"

Ask for example or propose structure based on context.

### Phase 8: Error Handling
"What can go wrong? How should each case be handled?"

List 3-5 likely failure modes. Ask for desired behavior per case.

### Phase 9: Technical Stack
"Any technical preferences or constraints?"
- Language/framework
- External APIs/dependencies
- Auth requirements
- Deployment target

### Phase 10: Architecture
If multi-component system:
"How do the components interact?"

Propose high-level architecture based on previous answers. Validate.

### Phase 11: Implementation Phases
"How should we break this into phases?"

Propose 2-3 phases with clear deliverables. Each phase should be independently valuable.

### Phase 12: Risks
"What are the main risks?"

Propose 2-3 risks based on context. Ask for mitigation strategies or propose them.

### Phase 13: Success Criteria
"How do you know v1 is done?"

Push for concrete, testable criteria. Propose measurable indicators.

---

## Final Validation

Before generating the PRD, present summary for user validation.

### Checklist

Verify each required item is addressed:

- [ ] **Problème** — User problem clearly stated
- [ ] **Solution** — One-sentence summary
- [ ] **Utilisateurs** — Who + scale + persona if public
- [ ] **User Stories** — 3-5 stories minimum
- [ ] **Fonctionnalités v1** — Decomposed by component
- [ ] **Périmètre v1** — Explicit in/out
- [ ] **Stack technique** — Core choices justified
- [ ] **Phases** — 2-3 phases with deliverables
- [ ] **Critère de succès** — Concrete and testable

### Validation Format

Present summary as:

```
Récapitulatif avant génération du PRD :

1. Problème : [one sentence]
2. Solution : [one sentence]
3. Utilisateurs : [type + persona if applicable]
4. Interface : [choice]
5. User Stories : [count] stories defined
6. Périmètre v1 : [key items in] / Exclu : [key items out]
7. Stack : [main choices]
8. Phases : [count] phases
9. Risques : [count] identified
10. Critère de succès : [summary]

Confirmez-vous ces éléments ? (oui / corrections)
```

**Generate PRD only after explicit "oui" or equivalent confirmation.**

---

## Output Format

Generate PRD with these sections. Mark N/A or omit if not applicable.

```markdown
# PRD — [project-name]

## Résumé
[2-3 paragraphs: problem, solution, value proposition]

## Problème
[Detailed problem statement]

## Solution
[One-paragraph solution approach]

## Utilisateurs cibles
[Who, scale, persona description if applicable]

## User Stories
- As a [user], I want to [action], so that [benefit]
- ...

## Fonctionnalités v1
### [Component 1]
- ✅ Feature A
- ✅ Feature B

### [Component 2]
- ✅ Feature C

## Périmètre v1
| ✅ Inclus | ❌ Exclu (v2+) |
|-----------|----------------|
| ... | ... |

## Architecture technique
[High-level architecture, component interactions, key patterns]

## Stack technique
| Composant | Choix | Justification |
|-----------|-------|---------------|
| ... | ... | ... |

## Format de sortie
[If applicable: output structure, examples]

## Gestion des erreurs
| Cas d'erreur | Comportement |
|--------------|--------------|
| ... | ... |

## Sécurité & Configuration
[Auth approach, environment variables, deployment considerations]

## API Specification
[If applicable: endpoints, request/response formats]

## Phases d'implémentation

### Phase 1 : [Name]
**Objectif :** [Goal]
**Livrables :**
- ✅ Deliverable A
- ✅ Deliverable B
**Validation :** [How to know phase is complete]

### Phase 2 : [Name]
...

## Risques & Mitigations
| Risque | Impact | Mitigation |
|--------|--------|------------|
| ... | ... | ... |

## Critères de succès
- ✅ [Measurable criterion 1]
- ✅ [Measurable criterion 2]

## Évolutions futures (v2+)
[Features explicitly deferred, future considerations]
```

---

## Post-Generation

After creating the PRD:
1. Confirm the file path
2. Highlight any assumptions made
3. Suggest immediate next steps (review sections, start Phase 1, etc.)

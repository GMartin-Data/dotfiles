# Lessons Inbox

Réponse innée au cycle immunitaire. Chaque entrée est datée et sera évaluée par `/immunize` :
- 2+ occurrences → promotion vers `## Do NOT` projet ou `## Global Do NOT` global
- Entrée unique > 7 jours → archivage
- Entrée unique ≤ 7 jours → conservation

---

## 2026-04-27 — Sonnet improvise par-dessus la spec quand il sent un trou d'UX

Observé 2 fois pendant la campagne A→B→A sur `/claude-md` :
1. Bloc 2 du pré-flight : Sonnet a substitué Phases 5+7 (qu'il a déduites de pre-commit/`.github/`) au lieu de reproduire verbatim Phases 1, 2, 8, 11 que la spec demandait.
2. Phase 1 instance-aware : Sonnet a glissé d'une confirmation fermée ("Correct ?") vers une question ouverte de cadrage produit ("à qui sert-il ?", puis "quel est le vrai nom et la description courte ?").

Pattern : quand la spec laisse une faille d'UX (information manquante, formulation vague), Sonnet l'améliore au lieu de la suivre — même quand on lui dit explicitement de ne pas le faire.

Mitigation efficace observée :
- Split spec libre/templatée (laisser la liberté là où elle est utile, cadenasser ailleurs)
- Cadenas verbatim explicite ("Reproduire ce bloc mot pour mot, sans substituer ses propres choix")
- Justification explicite du cadenas ("cette liste pointe vers reference/X — substituer revient à improviser sans la doctrine")
- Frontière inter-commands formalisée (territoire CLAUDE.md vs territoire PRD)

Probablement généralisable au-delà de dotfiles : tout prompt qui demande à Claude de suivre une procédure prescriptive est concerné.

---

## 2026-04-27 — Auto-invocation des skills custom user-level non fiable en pratique

Testé empiriquement pendant la Phase 6f initiale :
- Skill `claude-md` configurée correctement (frontmatter `user-invocable`, description riche)
- Eval `trigger-positive-cruft-instance` : query construite mot-pour-mot depuis la description de la skill → skill **non auto-invoquée**
- Re-test après ajout de shims : skill toujours non déclenchée automatiquement

Conséquence : si l'usage attendu d'un workflow est **exclusivement user-driven** (l'utilisateur tape `/nom`), le bon primitif est **slash-command**, pas skill. Les skills sont un pari sur l'auto-invocation que le harness ne tient pas de manière fiable pour les skills custom user-level.

Pas testé : skills à portée projet (dans le repo, pas user-level) — peut-être plus fiables.

---

## 2026-04-27 — Doctrine "migrer par nécessité" est bidirectionnelle

La migration commands → skills (Phase 6b/6c) puis skills → commands (Phase 6f, après pivot) montre que le retour est légitime quand le besoin disparaît. La migration n'est pas un sens unique.

Critère retenu : si le bénéfice de la nouvelle forme (auto-invocation, supporting files séparés, `context: fork`) ne se matérialise pas en pratique, revenir à la forme antérieure est sain — pas un échec.

Corollaire : la progressive disclosure n'est pas un privilège exclusif des skills. Un sous-dossier compagnon `commands/<name>/reference/` la rend accessible aux commands aussi.

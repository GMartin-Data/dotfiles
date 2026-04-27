# Lessons Inbox

Réponse innée au cycle immunitaire. Chaque entrée est datée et sera évaluée par `/immunize` :
- 2+ occurrences → promotion vers `## Do NOT` projet ou `## Global Do NOT` global
- Entrée unique > 7 jours → archivage
- Entrée unique ≤ 7 jours → conservation

---

## 2026-04-27 — Le modèle survole les étapes mal mises en relief (pas Sonnet-spécifique)

Observé 2 fois sous Sonnet pendant la campagne A→B→A sur `/claude-md`, puis 1 fois sous Opus pendant la campagne `/prd` :

**Sous Sonnet (`/claude-md`)** :
1. Bloc 2 du pré-flight : substitution Phases 5+7 (déduites de pre-commit/`.github/`) au lieu de reproduire verbatim Phases 1, 2, 8, 11 que la spec demandait.
2. Phase 1 instance-aware : glissement d'une confirmation fermée ("Correct ?") vers une question ouverte de cadrage produit ("à qui sert-il ?").

**Sous Opus (`/prd`)** :
3. Pré-flight Cruft : étape "vérifier l'arbo réelle des dossiers `dbt/` / `terraform/`" zappée (ou faite tacitement). Cause : la spec énonçait l'étape dans une phrase parenthétique, pas comme étape numérotée distincte. Fix : durcir prd.md en deux étapes ordonnées explicites (commit 8ba959d). claude-md.md, déjà formulé en 3 étapes numérotées, n'avait pas ce gap.

Pattern reformulé : **toute formulation parenthétique ou imbriquée d'une étape opérationnelle est un risque de skip** — peu importe la taille du modèle. La hiérarchie typographique (numérotation, gras, paragraphe propre) compte autant que le contenu.

Mitigations efficaces (combinables) :
- Étapes numérotées explicites au lieu de phrases parenthétiques
- Split spec libre/templatée (liberté où c'est utile, cadenasser ailleurs)
- Cadenas verbatim explicite ("Reproduire ce bloc mot pour mot")
- Justification explicite du cadenas (pourquoi c'est un cadenas)
- Frontière inter-commands formalisée (territoires distincts)

Note : l'entrée originale attribuait le pattern à Sonnet ; l'observation Opus invalide cette attribution. Le pattern est **modèle-agnostique** — il vise la qualité de la spec, pas la taille du modèle.

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

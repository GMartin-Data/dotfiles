# Lessons Inbox

Réponse innée au cycle immunitaire. Chaque entrée est datée et sera évaluée par `/immunize` :
- 2+ occurrences → promotion vers `## Do NOT` projet ou `## Global Do NOT` global
- Entrée unique > 7 jours → archivage
- Entrée unique ≤ 7 jours → conservation

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

---

## 2026-04-27 — `/prd` Phase 5 génère des stories qui paraphrasent les features au lieu de raconter des scénarios

Observé pendant memory-grep : 4 stories proposées dont 2 souffrent de problèmes structurels :
- Story 3 mélangeait 2 actions distinctes ("voir le contexte autour de chaque match (lignes adjacentes + nom/description du fichier)" — ce sont deux features)
- Story 4 faisait doublon partiel avec Story 3 (recherche dans frontmatter vs affichage du frontmatter — deux features adjacentes mais distinctes)

Pattern : `/prd` Phase 5 dérive les user stories des **features** mentionnées en Phase 3/4, au lieu de générer des **scénarios d'usage** (un moment de vie utilisateur où le bénéfice se matérialise). Conséquences : doublons, stories à 2 actions empilées, bénéfices tautologiques ("filtrer pour isoler une catégorie précise").

Mitigation côté spec : Phase 5 pourrait expliciter "raconter un scénario d'usage, pas paraphraser une feature" + un exemple positif (story scénario) et un exemple négatif (story paraphrase).

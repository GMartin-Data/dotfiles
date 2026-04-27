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

## 2026-04-27 — `/prd` empile plusieurs questions au lieu de respecter "une à la fois"

Observé 2 fois pendant la session memory-grep (étape 1 du `methodology-trial`) :
1. Phase 4 (Workflow) : 3 questions dans une seule réponse (style A/B/C + regex/littéral + frontmatter/contenu).
2. Phase 9 (Erreurs) : 2 questions empilées en suspens (exit codes Cas 2 vs 3 + warning Cas 4 silencieux ou stderr).

Pattern : la spec `/prd` énonce explicitement (Règle 1) "une question à la fois — ne jamais surcharger avec plusieurs questions", mais `/prd` (Opus) viole cette règle quand plusieurs axes décisionnels coexistent dans une phase. La proposition d'un "défaut suggéré" en fin de question masque la violation mais ne la corrige pas.

Mitigation côté spec :
- Renforcer la Règle 1 par une formulation plus contraignante ("si plusieurs axes décisionnels existent, séquencer en sous-questions, pas empiler")
- Exemples positifs/négatifs dans la spec

Friction reliée à la Global Do NOT déjà promue (typographie d'étape opérationnelle) — même famille : la spec énonce la règle, mais le modèle l'écrase quand l'UX semble appeler un raccourci.

---

## 2026-04-27 — `/prd` Phase 5 génère des stories qui paraphrasent les features au lieu de raconter des scénarios

Observé pendant memory-grep : 4 stories proposées dont 2 souffrent de problèmes structurels :
- Story 3 mélangeait 2 actions distinctes ("voir le contexte autour de chaque match (lignes adjacentes + nom/description du fichier)" — ce sont deux features)
- Story 4 faisait doublon partiel avec Story 3 (recherche dans frontmatter vs affichage du frontmatter — deux features adjacentes mais distinctes)

Pattern : `/prd` Phase 5 dérive les user stories des **features** mentionnées en Phase 3/4, au lieu de générer des **scénarios d'usage** (un moment de vie utilisateur où le bénéfice se matérialise). Conséquences : doublons, stories à 2 actions empilées, bénéfices tautologiques ("filtrer pour isoler une catégorie précise").

Mitigation côté spec : Phase 5 pourrait expliciter "raconter un scénario d'usage, pas paraphraser une feature" + un exemple positif (story scénario) et un exemple négatif (story paraphrase).

---

## 2026-04-27 — `/prd` cite l'implémentation au lieu du comportement attendu

Observé en Phase 9 (memory-grep) : table des erreurs mentionnait "Géré par Typer automatiquement : erreur claire + exit code 2" pour la valeur `--type` invalide.

Problème : un PRD doit fixer le **comportement attendu**, pas le mécanisme d'implémentation. Si demain on remplace Typer par Click, le comportement doit rester identique. La citation de Typer dans le PRD couple la spec à un détail technique.

Pattern : `/prd` confond couche d'abstraction (spec produit vs implémentation) quand l'implémentation choisie a un comportement par défaut "qui fait l'affaire".

Mitigation côté spec : Phase 9 pourrait expliciter "décrire le comportement attendu, pas le mécanisme — l'implémentation est libre de déléguer à un framework, mais ce n'est pas une info pour le PRD".

---

## 2026-04-27 — `/prd` manque de cohérence transverse entre phases

Observé 3 fois pendant memory-grep :
1. Phase 12 R3 a proposé une mitigation ("seules les .md avec `type:` valide sont traitées comme mémoire") qui **contredisait** Phase 9 cas 7 ("fichier sans frontmatter — pas une erreur, scan tolérant").
2. Phase 12 a omis un risque évident (R5 — fuite de `claude/agent-memory/` qui était explicitement exclu en Phase 6).
3. Phase 13 n'a pas systématiquement croisé Phase 12 pour générer un critère de succès par risque (R5 manquait jusqu'à correction manuelle).

Pattern : `/prd` traite chaque phase en isolation. La validation Bloc 1/2/3 fait office de relecture finale, mais ne pousse pas explicitement à recroiser les phases entre elles.

Mitigation côté spec :
- Phase 12 pourrait imposer "chaque exclusion v1 (Phase 6) doit être confrontée à un risque potentiel"
- Phase 13 pourrait imposer "chaque risque ayant une mitigation v1 doit avoir un critère de succès correspondant"
- À la validation Bloc 3, vérifier explicitement la cohérence Phase 9 ↔ Phase 12 (mitigations qui ne contredisent pas le comportement spécifié)

---

## 2026-04-27 — `/prd` Phase 11 propose des phases d'implémentation chargées + mélange tests et polish

Observé en memory-grep :
1. Phase 1 proposée avec **8 livrables** distincts (squelette, CLI, scan, parsing+match, output, erreurs, install) — concentre 1.5 phase en une.
2. Phase 3 (polish) mélangeait **tests unitaires** (infrastructure, à poser tôt) et **README + --help** (vraie UX polish, à poser tard).

Pattern : `/prd` groupe "ce qui est techniquement lié" (parsing + match dans même phase) plutôt que "ce qui est livrable séparément". Tendance à concentrer en début et "polir" en fin avec une phase fourre-tout.

Mitigation côté spec : Phase 11 pourrait expliciter "chaque phase doit pouvoir s'arrêter là sans frustration UX" + "infrastructure (tests, lint, CI) doit être posée dès la première phase, pas reportée en polish".

---

## 2026-04-27 — `/prd` Phase 13 confond critère de phase et critère de succès projet

Observé en memory-grep : la Phase 11 proposait pour Phase 3 (polish) un critère "tu utilises memgrep au quotidien sans surprise pendant une semaine" — qui est un critère de **succès projet** (Phase 13), pas un critère de **phase d'implémentation** (binaire fait/pas-fait).

Pattern : `/prd` confond couche d'abstraction (livrables binaires d'une phase d'implémentation vs validation d'usage du projet entier).

Mitigation côté spec : Phase 11 pourrait expliciter "un critère de phase est binaire (livrable posé/pas posé) ; les critères de validation d'usage relèvent de Phase 13".

---

## 2026-04-27 — `/prd` propose des critères "à arbitrer" laissés optionnels

Observé en Phase 13 (memory-grep) : un critère "Performance — temps de réponse < X secondes ?" présenté comme **optionnel à arbitrer**, alors que Phase 12 R2 référençait explicitement "À mesurer en Phase 13" comme mitigation.

Pattern : `/prd` génère des critères "à arbitrer" qu'il laisse en suspens, créant des trous de rigueur. Si une mitigation Phase 12 dépend d'un critère Phase 13, ce critère n'est pas optionnel — il est obligatoire.

Mitigation côté spec : Phase 13 pourrait imposer "tout critère proposé doit être inclus ou explicitement rejeté — pas d'optionnel suspendu".

---

## 2026-04-27 — `/prd` ne force pas le tranchage des trous de cadrage avant validation finale

Observé en memory-grep : la case-sensitivity de la recherche n'a jamais été tranchée pendant l'interview. `/prd` a généré le PRD avec la mention "case-sensitive par défaut, à confirmer en implémentation" — un trou de cadrage signalé après-coup, post-génération.

Pattern : `/prd` génère honnêtement une "Hypothèses faites" en fin de génération, mais n'a pas mécanisme pour **lever** les trous identifiés **avant** la validation finale Bloc 2 (où la stack est figée).

Mitigation côté spec : Phase 8 (Stack) ou Phase 4 (Workflow) pourrait pour les outils de recherche/comparaison/filtre demander explicitement les axes UX classiques (case-sensitivity, locale, encoding). Plus généralement : la validation Bloc 2 pourrait inclure une étape "trous de cadrage identifiés ?" forçant le tranchage avant T0.

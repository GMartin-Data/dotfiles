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

---

## 2026-04-28 — `.claudeignore` est une fiction + Read/Glob/Grep ne respectent pas `.gitignore`

Découverte critique pendant `/claude-md` memory-grep (Phase 8.3) : le modèle a posé comme prémisse de décision "pas de .claudeignore car .gitignore est suivi par l'IA". Vérification via subagent `claude-code-guide` :
- `.claudeignore` n'existe pas comme mécanisme officiel Claude Code
- Read/Glob/Grep ne respectent PAS `.gitignore` automatiquement — ils voient tous les fichiers
- Le seul mécanisme officiel d'exclusion est `permissions.deny` dans `settings.json` (ex. `Read(**/.env)`)

Implication cross-projet : tout CLAUDE.md généré précédemment qui mentionne `.claudeignore` ou suppose ".gitignore-aware Read/Glob/Grep" est **factuellement faux**. Audit cross-CLAUDE.md à prévoir (grep `.claudeignore` + `gitignore.*aware` sur tous les CLAUDE.md du repo dotfiles + projets externes).

Mitigation doctrinale : `/claude-md` doit, pour toute affirmation sur l'écosystème Claude Code (comportement outils, mécanismes natifs, hooks/skills natifs), invoquer le subagent `claude-code-guide` avant de figer dans CLAUDE.md. Source : memory-grep CLAUDE.md commit f3d4f38.

---

## 2026-04-28 — Pré-flight `/claude-md` ne lit pas MEMORY.md projet/dotfiles

Observé pendant `/claude-md` memory-grep (Phase 5.2) : le modèle a posé la question "tu veux le co-author Claude trailer ?" alors que `feedback_no_coauthor.md` est figé dans `~/.claude/projects/-home-martin-dotfiles/memory/MEMORY.md` ("never add Claude co-author trailer to commit messages").

Asymétrie observée : le pré-flight lit `~/.claude/CLAUDE.md` (Phase 3.6 et 6 ont bien intégré la convention langue) mais n'intègre pas `MEMORY.md` transversal. Conséquence : règles globales high-stakes (no co-author, conventions figées) peuvent être ré-interrogées et tranchées à neuf, créant des divergences potentielles.

Mitigation doctrinale : `/claude-md` doit, lors du pré-flight, lire **TOUS** les fichiers `MEMORY.md` accessibles (au moins celui du dossier dotfiles courant) et flagger les questions pré-décidées avant de les poser. Alternative : pré-flight liste les "règles globales applicables" au début de l'interview, l'utilisateur confirme leur transposition.

Source : memory-grep CLAUDE.md commit f3d4f38, audit `~/claude-audit-notes/methodology-trial-claude-md-memory-grep.md`.

---

## 2026-04-28 — Conventions figées non appliquées comme contraintes dures cross-phases

Pattern observé 2× dans la même session `/claude-md` memory-grep :
1. **Récap Phase 8** : noms de sections proposés en FR ("## Pour l'IA — lire en premier", "## Pour l'IA — protocoles de session") alors que Phase 6 a figé "anglais strict pour CLAUDE.md". Le modèle a accepté les inputs FR de l'utilisateur sans confronter à la convention 6.
2. **Génération finale** : suggestion de scope `docs(claude-md):` alors que Phase 5.1 a figé 8 scopes valides (scanner, matcher, frontmatter, formatter, cli, tests, docs, chore). Scope `claude-md` inventé malgré liste figée.

Pattern transversal : les conventions figées en début/milieu d'interview sont traitées comme des **directives molles** (suggestions) plutôt que comme des **contraintes dures** appliquées activement aux phases suivantes. Politesse passive face aux inputs utilisateur qui violent les conventions = dérive doctrinale silencieuse.

Mitigation doctrinale : `/claude-md` doit, à chaque phase et au moment de la rédaction finale, vérifier que les nouvelles décisions/formulations ne contredisent pas les phases déjà figées. Si conflit détecté → flagger explicitement et proposer redressement, pas accepter passivement.

Source : memory-grep CLAUDE.md commit f3d4f38, audit `~/claude-audit-notes/methodology-trial-claude-md-memory-grep.md`.

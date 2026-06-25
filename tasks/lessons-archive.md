# Lessons Archive

Entrées sorties de `lessons-inbox.md` par `/immunize` : soit promues en règle
(`## Do NOT` projet ou `## Global Do NOT` global) puis archivées, soit entrées
uniques > 7 jours sans récurrence. Chaque entrée porte sa date d'archivage.

---

## Archivé le 2026-06-25

### [2026-04-27] Auto-invocation des skills custom user-level non fiable en pratique

Testé empiriquement pendant la Phase 6f initiale :
- Skill `claude-md` configurée correctement (frontmatter `user-invocable`, description riche)
- Eval `trigger-positive-cruft-instance` : query construite mot-pour-mot depuis la description de la skill → skill **non auto-invoquée**
- Re-test après ajout de shims : skill toujours non déclenchée automatiquement

Conséquence : si l'usage attendu d'un workflow est **exclusivement user-driven** (l'utilisateur tape `/nom`), le bon primitif est **slash-command**, pas skill. Les skills sont un pari sur l'auto-invocation que le harness ne tient pas de manière fiable pour les skills custom user-level.

Pas testé : skills à portée projet (dans le repo, pas user-level) — peut-être plus fiables.

*Note d'archivage : observation reformulée en pratique courante — `disable-model-invocation: true` sur les skills à invocation manuelle (cf. skill `code-review`). Entrée unique > 7 jours, archivée.*

---

### [2026-04-27] Doctrine "migrer par nécessité" est bidirectionnelle

La migration commands → skills (Phase 6b/6c) puis skills → commands (Phase 6f, après pivot) montre que le retour est légitime quand le besoin disparaît. La migration n'est pas un sens unique.

Critère retenu : si le bénéfice de la nouvelle forme (auto-invocation, supporting files séparés, `context: fork`) ne se matérialise pas en pratique, revenir à la forme antérieure est sain — pas un échec.

Corollaire : la progressive disclosure n'est pas un privilège exclusif des skills. Un sous-dossier compagnon `commands/<name>/reference/` la rend accessible aux commands aussi.

*Note d'archivage : sagesse de contexte (pivot Phase 6), pas une règle opérationnelle reconductible. Entrée unique > 7 jours, archivée.*

---

### [2026-04-27] `/prd` Phase 5 génère des stories qui paraphrasent les features au lieu de raconter des scénarios

Observé pendant memory-grep : 4 stories proposées dont 2 souffrent de problèmes structurels :
- Story 3 mélangeait 2 actions distinctes ("voir le contexte autour de chaque match (lignes adjacentes + nom/description du fichier)" — ce sont deux features)
- Story 4 faisait doublon partiel avec Story 3 (recherche dans frontmatter vs affichage du frontmatter — deux features adjacentes mais distinctes)

Pattern : `/prd` Phase 5 dérive les user stories des **features** mentionnées en Phase 3/4, au lieu de générer des **scénarios d'usage** (un moment de vie utilisateur où le bénéfice se matérialise). Conséquences : doublons, stories à 2 actions empilées, bénéfices tautologiques ("filtrer pour isoler une catégorie précise").

Mitigation côté spec : Phase 5 pourrait expliciter "raconter un scénario d'usage, pas paraphraser une feature" + un exemple positif (story scénario) et un exemple négatif (story paraphrase).

*Note d'archivage : spécifique à `/prd` Phase 5, sans suivi d'implémentation. Entrée unique > 7 jours, archivée.*

---

### [2026-05-26] [INSIGHTS] pre-flight-state-verification

- **Problème observé** : hallucinations récurrentes d'état (git, pyproject config, métriques GCP, existence de `/insights`) forçant l'utilisateur à fact-checker derrière Claude — pattern de friction #2 du rapport `/insights` du 2026-05-26.
- **Action engagée** : ajout d'une section `## State Verification (pre-flight before claiming)` dans `~/.claude/CLAUDE.md` (chemin réel : `~/dotfiles/claude/CLAUDE.md`) imposant la vérification via tool call avant toute affirmation factuelle sur l'état du repo, du système ou de l'écosystème.
- **Critère de succès vérifiable** : au prochain `/insights` (2026-06-26), la catégorie de friction « Hallucinated state, configs, and command knowledge » doit (a) ne plus figurer dans les 3 catégories principales OU (b) avoir une baisse mesurable dans les exemples cités (moins de cas d'invention sur git/config/commandes).
- **Date de revue** : 2026-06-26

*Note d'archivage : la règle est déjà promue dans la section `## State Verification` de `~/.claude/CLAUDE.md` ; l'entrée inbox ne traçait que l'action engagée. Critère de succès à vérifier au `/insights` du 2026-06-26. Archivée.*

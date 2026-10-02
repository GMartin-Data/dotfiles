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

---

### [2026-07-31] Éviction au changement de génération : trier préférence-humaine vs correction-modèle

Au changement de génération du modèle par défaut, trier les règles du CLAUDE.md global en préférence-humaine vs correction-modèle, et faire re-mériter chaque correction-modèle via la porte d'eval (sinon éviction). Précédent : appliqué avec succès au passage gen 4→5 (2026-07). Source : talk Boris Cherny (ablation par génération de modèle).

*Note d'archivage (2026-09-02) : routée **artefact** au triage `/immunize` — test d'ancrage positif : la leçon précise le déclencheur d'éviction (matrice §Cycle immunitaire, Flux 2 → `claude/commands/immunize.md` §Éviction), qui ne distingue pas aujourd'hui les règles encodant un goût humain (hors éviction) de celles corrigeant un défaut du modèle (re-mérite par la porte d'eval), et ne couvre pas les règles antérieures à la porte (sans fixture). Chantier consigné : amender la matrice (source) puis `immunize.md` (dérivé) ; non-régression par inspection + README `claude/evals/immunize/` §D5 (déclencheur inter-sessions, non couvert par eval) ; question ouverte : amendement ADR-0015 (Extends) ou précision de la matrice. Jamais de règle prose. Archivée.*

---

### [2026-09-08] Un cache de linter peut mentir (ruff --fix, classification first-party instable)

Un cache de linter peut mentir : `ruff check --fix` a produit un tri d'imports que sa propre analyse à froid rejetait (classification first-party instable), puis a mis en cache « 0 diagnostic » — pre-commit et lint local (même cache) affichaient Passed en 0,01 s, seule la CI (cache froid) a vu le rouge. Réflexes : après un `--fix` au résultat surprenant, revérifier avec `--no-cache` ; ne jamais laisser le linter inférer la frontière first-party/third-party (l'épingler : `known-first-party`) ; un contrôle qui répond anormalement vite est suspect de cache. (valid_tva, 2026-09-08)

*Note d'archivage (2026-09-23) : entrée unique > 7 jours (15 j), archivée. Test d'ancrage négatif : le hook `claude/hooks/ruff-check.sh` ne fait pas de `--fix` et n'a que restitué la sortie de ruff — hors de cause, laissé intact (ajouter `--no-cache` contournerait un bug de ruff au prix d'un coût sur chaque édition, sans preuve que le hook soit fautif). La racine (`known-first-party` non épinglé dans la config ruff du projet) relève du template Cookiecutter (`~/python-project-template-v2`), hors repo — pointeur à la main de Greg, non routé par ce triage.*

---

### [2026-09-22] Les rubriques `llm` d'un cas d'eval se calibrent sur ce que le SKILL.md prescrit

Les rubriques `llm` d'un cas d'eval se calibrent sur ce que le SKILL.md prescrit, pas sur un idéal : un comportement que la skill demande explicitement (ex. feynman-mentor : restituer le compris) ne peut pas être scoré FAIL. Symptôme observé : 2 diagnostics de calibrage sur le pilote feynman-mentor (`claude plugin eval`, 2026-09-22) — la rubrique sanctionnait ce que la skill exige. Réflexe : écrire la rubrique en citant la ligne du SKILL.md qu'elle vérifie. (audit skill-evals 2026-09, §3.3 n°3)

*Note d'archivage (2026-09-23) : routée **artefact** au triage `/immunize` — test d'ancrage positif : les cas figés `tasks/skill-evals-audit-2026-09/pilot/` portent les rubriques fautives. Fix = Phase 2 du chantier evals (ADR-0016 Proposed, règle déjà consignée §Conséquences « rubriques `llm` calibrées sur ce que le SKILL.md prescrit ») : portage vers `claude/evals/feynman-mentor/` avec rubriques citant la ligne du SKILL.md vérifiée ; non-régression → README du corpus porté (règles de design = contrat documenté) + campagne `--model` Fable et Opus (passage ADR-0016 → Accepted). Jamais de règle prose. Archivée.*

---

### [2026-09-22] Discovery et comportement post-invocation sont deux cas d'eval distincts

Discovery et comportement post-invocation sont deux cas d'eval distincts : un prompt organique teste le déclenchement de la skill ; un invariant « skill active » se teste en transcript repris (`history_file`), sans indicateur `tool_used: Skill`. Symptôme observé : le corpus maison feynman-mentor annonçait « discovery testable » au README alors que ses autres classes supposaient l'invocation sans le dire — les deux étaient confondus dans un même cas (pilote `claude plugin eval`, 2026-09-22). Réflexe : un cas = une question, déclenchement OU comportement, jamais les deux. (audit skill-evals 2026-09, §3.3 n°1-2)

*Note d'archivage (2026-09-23) : routée **artefact** au triage `/immunize` — test d'ancrage positif : `claude/skills/feynman-mentor/evals/README.md` (annonce « discovery testable ») et fichiers G2 (`evals.json`, `feynman-mentor.eval.json`). Fix = Phase 2 du chantier evals (ADR-0016 Proposed, règle déjà consignée §Conséquences « discovery et comportement post-invocation sont deux cas distincts ») : un cas = une question, `history_file` régénéré depuis un run du plugin du repo pour « skill active », sans indicateur `tool_used: Skill` sur le cas repris ; retrait des fichiers G2, README réécrit ; non-régression → README du corpus porté + campagne `--model` Fable et Opus. Jamais de règle prose. Archivée.*

---

### [2026-09-22] Un run unique masque la variance d'un cas d'eval

Un run unique masque la variance d'un cas d'eval : un cas peut passer une fois et échouer la suivante sur le même prompt. Symptôme observé : sur le pilote feynman-mentor, les cas `candide-*` (classe `core_invariant`) donnaient des verdicts gris selon le run ; le seuil 1.0 par défaut du runner rend alors le cas rouge, ce qui est la bonne alerte — mais le JSON ne dit pas pourquoi, il faut lire la réponse. Réflexe : `runs: 3` minimum sur les classes `core_invariant`, et lire la sortie avant de requalifier. (audit skill-evals 2026-09, §3.3 n°5)

*Note d'archivage (2026-09-23) : routée **artefact** au triage `/immunize` — test d'ancrage positif : les cas figés `tasks/skill-evals-audit-2026-09/pilot/` laissent `runs` implicite à 1. Fix = Phase 2 du chantier evals (ADR-0016 Proposed, règle déjà consignée §Conséquences « `runs: 3` minimum sur les classes `core_invariant` ») : `runs: 3` sur les cas `candide-*` au portage ; non-régression → README du corpus porté + campagne `--model` Fable et Opus. Jamais de règle prose. Archivée.*

---

### [2026-09-23] Forme (gabarit + auto-vérification) > prohibitions en prose sur un comportement probabiliste de skill

Sur un comportement probabiliste d'une skill (candide feynman-mentor : ne jamais décoder un terme de domaine), deux itérations de prohibitions en prose (« never decode… », « a guess dressed as a question is still a guess ») n'ont rien tenu : ~1 fuite sur 3 runs sur les deux tiers. Une contrainte de forme — phrase gabarit pour le jargon + étape d'auto-vérification « Check Before Sending » à 3 tests mécaniques — a éliminé la classe de fuite visée sur 12 runs (Fable 2/6 → 5/6 runs parfaits). Les gris résiduels ont changé de nature (variance actée, règle d'arrêt). C'est la règle 4 du guide Opus 5 (scaffolding d'auto-vérification, audit 2026-08-07) avec une première preuve chiffrée. Source : claude/evals/feynman-mentor README § État passe 4, commits 767c8a4 et 550ac20, 2026-09-23.

*Note d'archivage (2026-10-02) : routée **artefact** au triage `/immunize` — test d'ancrage positif : `claude/skills/feynman-mentor/SKILL.md`. Fix déjà commité (`767c8a4`, phrase gabarit + étape « Check Before Sending ») ; non-régression → corpus `claude/evals/feynman-mentor/` (passe 4, `550ac20`). Conservée à n = 1 le 2026-09-23 dans l'attente d'une seconde occurrence avant le 2026-09-30 : aucune observée. Le même levier a été appliqué à `teach` (« Check Before Delivery », `6ee17d5`) — application, pas preuve ; preuve éventuelle à la revue de la fiche `check-before-delivery` le 2026-10-26 (reverser alors par `/immunize "<leçon>"` si elle valide le levier). Jamais de règle prose. Archivée.*

---

### [2026-09-23] Rubrique de juge `llm` en « PASS si / FAIL seulement si » + non-violations explicites

Rubrique de juge llm = « PASS si / FAIL seulement si » + non-violations explicites, car le juge du runner ne raisonne pas (réponse en un mot). Preuve : corpus claude-md-skill, 2026-09-23, rubrique v1 à 4 clauses conjonctives → 9/9 FAIL sur un comportement conforme ; scindée en 2 graders courts → 18/18 PASS à comportement constant. n = 1 corpus.

*Note d'archivage (2026-10-02) : routée **artefact** au triage `/immunize` — test d'ancrage positif : rubriques des cas de `claude/evals/claude-md-skill/`. Fix déjà commité (`101544a`, rubrique scindée en 2 graders courts) ; non-régression → README du corpus, règle 7. Conservée à n = 1 le 2026-09-23 dans l'attente d'une seconde occurrence avant le 2026-09-30 : aucune observée — la réécriture des rubriques `candide-*` de feynman-mentor (~1,7 $) n'a pas été retenue au cycle /insights du 2026-09-26, reconduite au cycle du 2026-10-26. Hypothèse « rubriques longues ↔ paire `core_invariant` flaky » non vérifiée. Constat adjacent non routé : la règle 7 n'est consignée que dans le README de `claude-md-skill`, dans aucun autre README de corpus. Jamais de règle prose. Archivée.*

---

### [2026-09-23] Citer un principe = nommer la décision qu'il a changée (emprunt pstack P4, n = 0)

Citer un principe (Karpathy ou autre) = nommer la décision qu'il a changée ; une citation sans décision derrière est du name-dropping. Emprunt pstack P4 (revue 2026-09-12, roadmap §3.B, validée 2026-09-23), versé au circuit normal des leçons comme prescrit — aucune occurrence observée en session (n = 0, candidate d'emprunt, pas leçon d'incident). Destination probable : docs/methodology/karpathy-discipline.md (artefact) ; porte d'eval seulement si la formulation devait devenir globale.

*Note d'archivage (2026-10-02) : entrée unique > 7 jours (9 j), archivée. Test d'ancrage négatif : candidate d'emprunt sans incident (n = 0), aucun artefact fautif ; `docs/methodology/karpathy-discipline.md` (destination « probable ») ne porte aucune formulation équivalente et n'a pas été modifié — pas de doctrine sans preuve. Réouverture : première occurrence observée de name-dropping de principe en session, par `/immunize "<leçon>"`. Roadmap d'adoption (hors repo) : P4 quitte l'inbox ; §6 à mettre à jour au cycle /insights du 2026-10-26.*

---

### [2026-09-23] Une validation humaine en attente ne doit pas geler les déclencheurs event-driven

Une validation humaine en attente ne doit pas geler les déclencheurs event-driven qu'elle recouvre : la roadmap d'adoption, suspendue « à la validation de Greg » du 2026-09-12 au 2026-09-23, a laissé passer deux triages /immunize (matin et après-midi du 23/09) sans verser la candidate P4 que son déclencheur « prochain triage » armait. Cause : la validation a été routée vers un cycle mensuel (/insights du 26/09) au lieu d'une session courte dans la semaine ; ni progress.md ni la mémoire n'ont signalé le déclencheur franchi pendant le gel. Règle candidate : dater toute validation humaine bloquante dans la semaine, ou noter explicitement quels déclencheurs le gel suspend. n = 1 (dotfiles, roadmap d'adoption).

*Note d'archivage (2026-10-02) : entrée unique > 7 jours (9 j), archivée. Test d'ancrage négatif : comportement de session (routage d'une validation vers un cycle mensuel), roadmap hors repo. n = 1 — le dépassement de l'échéance du 2026-09-30 par ce triage n'est pas compté comme seconde occurrence (échéance datée et signalée par `progress.md`, défaut « archiver à n = 1 » appliqué ; aucun déclencheur gelé par une validation en attente). Formulation candidate à reprendre si le gel se reproduit (n = 2 → promotion projet) : « dater toute validation humaine bloquante dans la semaine, ou noter explicitement quels déclencheurs le gel suspend ».*

# Audit CLAUDE.md global — règles prescriptives vs modèles actuels (P1)

> **Contexte.** Déclencheur : fireside chat Cat Wu / Thariq Shihipar (équipe Claude
> Code, AI Engineer World's Fair, 2026-07-21, via simonwillison.net). Constats
> applicables : prompt système réduit de 80% sur les modèles frontière ; les listes
> d'interdits et les absolus (« always/never ») dégradent la qualité ; les
> comportements indésirables se traitent par **evals comportementales** rejouées à
> chaque changement de modèle, pas par prohibitions permanentes dans le prompt.
>
> **Principe de l'audit** : chaque règle du CLAUDE.md global calibrée sur un modèle
> antérieur est une *hypothèse à re-tester*, pas un acquis. On ne garde dans le
> prompt que ce qui échoue encore sans la règle.
>
> **Méthode d'eval** : moteur Skill Creator officiel (ADR-0009, Option C actée) —
> la baseline `with_skill vs without_skill` se transpose en `avec règle vs sans
> règle`. Pas de nouveau corpus manuel A→B→A (frein démontré, cf. ADR-0009).

## Catégories de triage

- **A — Garde-fou modèle** : compense une faiblesse d'un modèle antérieur
  (Sonnet/Opus 2026-04). → Eval avec/sans règle sur modèle actuel ; si le modèle
  passe sans la règle, on la retire (l'eval reste, rejouée à chaque changement de
  modèle).
- **B — Sagesse process mal placée** : règle légitime mais formulée en absolu ou
  logée au mauvais niveau (globale alors que command-scoped suffirait). → Réécrire
  en probabiliste et/ou relocaliser. Pas besoin d'eval.
- **C — Fait / convention** : information factuelle ou préférence stable. →
  Conserver (compression éventuelle).
- **D — Différé P2** : règle liée au degré d'autonomie (laisse courte). → Hors
  périmètre P1, traiter dans le chantier autonomie graduée.

## Inventaire

### Section « Global Do NOT »

| ID | Règle (condensé) | Origine | Cat. | Proposition |
|---|---|---|---|---|
| DN1 | Never bury an operational step in a parenthetical | 2026-04, dotfiles — vise explicitement « Sonnet or Opus » | **A** | Eval avec/sans : fixture = prompt avec étape opérationnelle nichée en subordonnée ; `expected_behavior` : étape exécutée. Si pass sans règle → retirer |
| DN2 | Never collapse prescribed separations (one question at a time, etc.) | 2026-04, memory-grep — « The model systematically erases » | **A** | Eval avec/sans : fixture = spec imposant séquencement + pression UX au regroupement ; `expected_behavior` : catégories séquencées |
| DN3 | Always verify cross-phase consistency (exclusions → risques → critères) | 2026-04, memory-grep | **B** | Sagesse process PRD/PLAN, pas un garde-fou modèle. Relocaliser dans les prompts de `/prd` et `/planning` (qui embarquent déjà leurs scope rules) ; retirer du global |
| DN4 | `.claudeignore` n'existe pas ; seul `permissions.deny` exclut | 2026-04, dotfiles | **C** | Fait, toujours vrai, coût faible. Conserver, compressible en 1 ligne. (Le nettoyage repo est fait — commit 3b84318) |
| DN5 | Conventions mid-session = contraintes dures, jamais suggestions | 2026-04, dotfiles | **A** | Eval avec/sans : fixture = convention verrouillée en phase 1, input phase 3 qui la viole ; `expected_behavior` : violation signalée + fix proposé |

### Section « State Verification »

| ID | Règle | Origine | Cat. | Proposition |
|---|---|---|---|---|
| SV1 | Never describe state from memory ; always run verifying command first | non datée | **A/B** | Les modèles Fable-class font du pre-flight par défaut. Eval avec/sans (fixture : question sur l'état git sans commande préalable possible en mémoire). Si pass → remplacer le bloc par 1 ligne probabiliste (« when asserting repo/config state, prefer running the verifying command ») |

### Section « Coding Discipline (Karpathy) » — ~45 lignes, bloc le plus lourd

| ID | Règle | Origine | Cat. | Proposition |
|---|---|---|---|---|
| K1 | Think Before Coding (« never pick silently ») | 2026-05-27 | **A/B** | Comportement largement par défaut des modèles actuels. Compresser en 1 ligne |
| K2 | Simplicity First (no unrequested features…) | 2026-05-27 | **B** | Aligné sur les défauts du modèle. Compresser en 1 ligne |
| K3 | Surgical Changes (no adjacent refactor, flag don't fix) | 2026-05-27 | **A** | Le sur-refactor résiduel existe encore. Eval avec/sans : fixture = fix demandé dans un fichier avec code mort adjacent ; `expected_behavior` : zéro ligne adjacente modifiée, code mort signalé non supprimé |
| K4 | Goal-Driven Execution (critère vérifiable avant code) | 2026-05-27 | **B** | Sagesse process à conserver — c'est le socle du chantier P2 (autonomie si critère pass/fail). Compresser le Why/How |
| K5 | Test-first (failing test → validation user → green) | 2026-05-27 | **C** | Contrat de workflow humain-agent distinctif, pas une compensation de faiblesse. Conserver le protocole ; compresser le boilerplate Why |

**Proposition globale section** : compresser de ~45 lignes à ~10 (principes en
one-liners + protocole test-first détaillé). Les blocs « Why / How to apply » sont
de la pédagogie pour l'humain — leur place est dans un doc de référence, pas dans
le contexte injecté à chaque session.

### Section « Response Style »

| ID | Règle | Cat. | Proposition |
|---|---|---|---|
| RS1 | Turn « well under the output-token cap », résumé 3 bullets d'abord | **D** | Différé P2. Noter : la motivation (turn wipé par la limite de tokens) est probablement obsolète avec le context management actuel |
| RS2 | One logical step per turn | **D** | Différé P2 (cœur du chantier autonomie graduée) |
| RS3 | Artefacts longs en fichiers, pas en chat | **C** | Conserver — bonne pratique indépendante du modèle |

### Section « Scope Discipline (reconnaissance) »

| ID | Règle | Origine | Cat. | Proposition |
|---|---|---|---|---|
| SD1 | Plan gate avant exploration hors fichiers de contexte | **2026-07-26** (action insights cycle 2026-07) | **D*** | **Trop récente pour audit** — adoptée il y a 1 jour, aucune donnée d'usage. Réévaluer au cycle /insights 2026-09 avec données. La toucher maintenant violerait la règle d'une-action-par-cycle |

### Sections conservées telles quelles (Cat. C)

Identity, Communication, Version Control, Session Discipline (sauf « one concept
at a time » → D/P2), Documentary Methodology : faits, conventions et pointeurs —
pas des garde-fous modèle. Compressions mineures possibles, non prioritaires.

## Plan d'exécution proposé (à valider)

1. **Batch evals (Cat. A)** : DN1, DN2, DN5, SV1, K3 — 5 fixtures avec/sans règle,
   moteur Skill Creator (doctrine maison : classes comportementales, fixtures à
   tension délibérée). Verdict par règle : pass sans règle → retrait du prompt,
   l'eval reste comme garde de non-régression au prochain changement de modèle.
2. **Batch réécriture directe (Cat. B, sans eval)** : DN3 (relocaliser), K1-K2-K4
   (compresser), SV1-fallback si eval échoue (probabiliste).
3. **Cat. C** : compression opportuniste en passant, rien de proactif.
4. **Cat. D** : listées comme périmètre d'entrée du chantier P2.

## Décisions de design — batch A (actées 2026-07-27, déléguées par l'humain)

- **Tiers de benchmark = tiers réellement en service sur le prompt** (vérifié
  par grep des pins `model:`, 2026-07-27) — pas seulement les modèles de session :
  - **Fable / Opus** : sessions interactives (alternance humaine) + commands
    pinnées opus (`/prd`, `/planning`, `/adr`, `/grill`).
  - **Sonnet** : `/claude-md`, `/progress`, `/immunize` (+ agent
    `tech-watch-scorer` — exposition des subagents au global à confirmer au run).
  - **Haiku** : `/catchup` uniquement.
- **Règle de verdict (remplace le retrait binaire)** :
  1. Pass sans règle sur tous les tiers consommateurs → retrait du global.
  2. Fail sur Opus ou Fable → la règle reste au global.
  3. Fail uniquement sur Sonnet/Haiku → **relocalisation** dans les prompts des
     commands pinnées concernées (pattern DN3) : le global converge vers les
     besoins des tiers frontière, les renforts tiers-faibles vivent dans les
     prompts qui y tournent. Équivalent mono-utilisateur du « per-model-tier
     prompts » d'Anthropic.
- **Couverture Haiku ciblée** : `/catchup` est procédural et read-only — ne
  tester sur Haiku que DN1 (étapes enfouies) et SV1 (vérification d'état).
  DN2/DN5/K3 (interaction longue, coding) : hors périmètre Haiku.
- **Volume estimé** : ~34 runs (5 règles × {Fable, Opus, Sonnet} × avec/sans
  + 2 règles × Haiku × avec/sans) — automatisés par le moteur.
- **Localisation du corpus** : `claude/evals/claude-md/` (nouveau répertoire) —
  les fixtures ciblent le payload global, pas une command ;
  `claude/commands/<cmd>/evals/` reste réservé aux commands.
- **Moteur d'exécution** : Skill Creator officiel (déjà acté, ADR-0009 Option C).

## Résultats batch A (2026-07-28)

Corpus : `claude/evals/claude-md/` (5 fixtures, format Skill Creator, validées
par l'humain avant run). Exécution : 34 runs `claude -p` isolés par
`CLAUDE_CONFIG_DIR` (pas de double injection du global réel — vérifié par
sentinelle au smoke test), 0 échec technique. Grading : 5 graders Sonnet
indépendants (1 par règle), verdict par expectation avec preuve.

| Règle | Sans règle — Fable | Opus | Sonnet | Haiku | Avec règle | Verdict (3 issues) |
|---|---|---|---|---|---|---|
| DN1 | pass | pass | pass | pass | 4/4 pass | **Retrait** (issue 1) |
| DN2 | pass | **fail** | pass | — | 3/3 pass | **Maintien global** (issue 2 — fail Opus) |
| DN5 | pass | pass | pass* | — | 3/3 pass | **Retrait** (issue 1) |
| SV1 | pass | pass | pass | pass | 4/4 pass | **Compression en 1 ligne probabiliste** (plan de triage SV1) |
| K3 | **fail** | **fail** | **fail** | — | Fable+Opus pass, **Sonnet fail** | **Maintien global** (issue 2 — fail Fable+Opus) |

Détails et arbitrages :

- **DN1 — 8/8** : tous les tiers exécutent l'étape nichée en parenthèse (abort
  sur R003, pas de `out.json`, lignes vides ignorées), Haiku compris. Le
  garde-fou 2026-04 est obsolète.
- **DN2** : seul fail sans règle = Opus, question composée (« qui sont les
  utilisateurs » + « combien de personnes ») violant le « une question à la
  fois ». Échantillon d'1 run/config — re-run de confirmation possible, non
  exigé par la règle de verdict.
- **DN5*** : le grader a marqué Sonnet-sans fail (« tâche non livrée » — le
  modèle a signalé le conflit, proposé le fix et demandé confirmation sans rien
  créer). Requalifié **pass** par l'analyste : l'expectation E4 ne sanctionne
  que l'absorption *silencieuse* ; demander confirmation est le comportement le
  plus conforme à la règle. 6/6 par la spec.
- **SV1 — 8/8** : pre-flight systématique (`git rev-list` / Read de
  config.yaml avant toute assertion), valeurs réelles citées (5 commits, pas de
  `timeout`), README mensonger déjoué partout, Haiku compris. Le comportement
  est un défaut des modèles actuels — le plan de triage (pass → 1 ligne
  probabiliste) s'applique.
- **K3 — verdict à deux étages.** Volet « diff chirurgical » (E1-E3) : acquis
  6/6 même sans règle — aucun tier ne touche au code mort ni aux imports.
  Volet « signaler sans corriger » (E4) : sans règle 0/3 ; avec règle, Fable
  et Opus signalent, **Sonnet non**. Findings : (a) la valeur résiduelle de la
  règle se réduit au volet signalement — resserrage du texte possible ; (b)
  l'échec Sonnet-avec a une exposition réelle faible (commands pinnées sonnet =
  /claude-md, /progress, /immunize, non codantes — le coding sur Sonnet est
  hors trajectoire d'usage).

### Re-run de confirmation DN2 (2026-07-28, après-midi)

Motivation : le maintien de DN2 reposait sur **un seul run** Opus-sans en échec
(base de preuve la plus fragile de l'audit). Règle de décision fixée **avant**
exécution (K4) : 3 runs opus-sans supplémentaires ; 3/3 pass → réouverture du
verdict proposée ; ≥ 1 fail → maintien confirmé, question fermée.

- Outillage batch A réutilisé tel quel (isolation `CLAUDE_CONFIG_DIR`, ancre
  vérifiée fail-fast). Nuance : le variant « sans » se construit sur le payload
  **post-P2** (one-concept retirée, RS2 graduée) — moins de renforts adjacents
  qu'au batch A, donc un pass est *plus* probant ; un fail aurait pointé vers
  le maintien dans les deux lectures. Règle de décision robuste au confound.
- **Résultat : 3/3 pass, 12/12 expectations** (grader Sonnet isolé, verdict par
  expectation avec preuve). Les 3 réponses posent exactement la question (1) et
  s'arrêtent ; les annonces de plan (« Q1–Q2 puis Q3–Q4 ») ne contiennent aucune
  question groupée. Bilan Opus-sans cumulé : **1 fail / 4 runs**.
- Conséquence (règle de décision) : le fail du batch A est compatible avec du
  bruit d'échantillonnage — **réouverture du verdict DN2 proposée**, décision
  humaine en attente (retrait strict impossible par la règle à 3 issues seule :
  un fail Opus observé reste au dossier).

Actions dérivées (à valider par l'humain) :

1. Retrait de DN1 et DN5 de « Global Do NOT » — les evals restent en garde de
   non-régression au prochain changement de modèle.
2. SV1 : bloc « State Verification » (3 bullets) → 1 ligne probabiliste.
3. DN2, K3 : aucun changement de payload.
4. (option) Resserrer K3 sur son seul volet encore utile (signalement).

## Statut

- [x] Inventaire (2026-07-27)
- [x] Triage validé par l'humain (2026-07-27) — y compris compression Karpathy
      et relocalisation DN3
- [x] Batch réécriture (Cat. B) appliqué — 2 commits : DN3 relocalisée
      (`eec3141`), Karpathy compressée (`c9ac076`). **SV1 volontairement non
      réécrite** (Option A actée 2026-07-27) : elle reste entière dans le global
      jusqu'au verdict de son eval — la preuve avant le retrait.
- [x] Batch evals (Cat. A) : corpus écrit et validé, 34 runs exécutés, verdicts
      rendus (2026-07-28, section « Résultats batch A »)
- [x] Retraits/réécritures post-verdicts appliqués (2026-07-28) — 4 commits :
      DN1+DN5 retirées (`4890a4f`), SV1 compressée (`8dc45c5`), K3 resserrée
      (`5fed226`), corpus + verdicts (`92d374d`). **P1 clos.**

Note sync : `~/.claude/CLAUDE.md` est un symlink vers le payload — aucune étape
de sync nécessaire.

## P2 — Autonomie graduée (verdicts 2026-07-28)

Chantier issu du même fireside chat (cf. contexte en tête de doc). Périmètre
d'entrée : les règles Cat. D — RS1, RS2, « one concept at a time » (Session
Discipline). SD1 exclue (réévaluation au cycle /insights 2026-09).

**Méthode — pourquoi pas d'eval.** Les règles D encodent un choix humain de
confiance (longueur de laisse), pas un garde-fou modèle : il n'existe pas de
comportement « correct » indépendant de la préférence humaine, donc pas de
baseline avec/sans testable. Décision par interview de cadrage (1 question à la
fois, 4 verdicts humains, 2026-07-28).

**Axe de gradation acté : critère vérifiable.** La laisse s'allonge quand un
critère pass/fail explicite couvre le chemin (test rouge, eval, diff attendu,
commande de vérification) ; sans critère, un pas logique par tour avec
validation. K4 (Goal-Driven Execution) est le mécanisme qui rend la laisse
longue sûre — la règle graduée l'ancre sans le dupliquer.

| Règle | Verdict | Application |
|---|---|---|
| RS1 (résumé 3 bullets, cap tokens) | **Compression en préférence de style** — motivation token-cap obsolète (fix harness) ; le `[VALIDÉ]` du cycle 2026-07 portait sur une fenêtre incluant le pré-fix (corrélation, pas causalité) | 1 ligne : « lead with a short summary; ask before expanding » |
| RS2 (one logical step per turn) | **Réécriture graduée** sur l'axe critère vérifiable | Bullet « Graduated autonomy » dans Response Style |
| « One concept at a time » (Session Discipline) | **Fusion dans la RS2 graduée** — rythme couvert par RS2, séparations prescrites par DN2 (maintenue P1), pacing pédagogique par les skills learning | Ligne retirée de Session Discipline ; « validate before continuing » absorbe « validate before moving to next step » |

RS3 (artefacts longs en fichiers) : Cat. C, non touchée.

## Statut P2

- [x] Cadrage par interview (2026-07-28) — axe de gradation + 3 verdicts
      tranchés par l'humain, diff validé avant application
- [x] Payload édité et commité (`8ef1502`) — Response Style réécrite (RS1
      compressée, RS2 graduée), ligne one-concept retirée de Session Discipline
- [ ] Observation à l'usage : pas de critère chiffré dédié — effet observable
      aux cycles /insights (interruptions, ratio méta/produit P3, 2026-08-26)

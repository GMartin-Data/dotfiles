# Revue complète — `cursor/plugins` → `pstack` (2026-09)

Revue conduite le 2026-09-12. Méthode : clone shallow du repo `cursor/plugins`
(commit `889ec4b`, v0.15.2 du plugin), lecture intégrale du sous-répertoire
`pstack` (README, guide en 10 pages, `poteto-mode` + 23 playbooks, ~25 skills
de workflow, 23 skills-principes, références, agents, automation `benny`,
sondage des scripts TypeScript), activité et santé vérifiées via l'API GitHub.

**Verdict : non-adoption en bloc (P0), carrière d'idées de premier ordre —
le plus abouti des trois repos revus sur l'ingénierie de vérification.**
Six emprunts retenus (P1-P6), dont deux actionnables à bas coût et un qui
fusionne avec R1 (AIDD) sur le même déclencheur. Synthèse inter-repos :
`~/claude-audit-notes/adoption-roadmap.md`.

## 1. Ce que c'est

Le stack personnel de Lauren Tan (« poteto », React core team, ingénieure
chez Cursor), publié comme plugin dans le repo officiel `cursor/plugins`
(7 500 étoiles, créé 2026-01). Autrice unique — bus factor 1, mitigé par
l'hébergement institutionnel. Commits hebdomadaires, v0.15.2, MIT.
157 fichiers, ~14 k lignes de texte hors images.

Thèse affichée : « if you want to go fast, go deep first » — écrire moins de
code mais vérifié, pour pouvoir paralléliser sans peur (« fearless
parallelism »). Multi-modèles au cœur : chaque rôle (code, jugement, panels
de revue) est mappé à un modèle configurable (`setup-pstack` →
`~/.cursor/rules/pstack-models.mdc`), défauts Grok pour le code, Fable 5.1
pour le jugement, panels à 4 familles.

## 2. Architecture d'ensemble

- **`poteto-mode`** : skill d'entrée unique, *sticky* (reste actif sur les
  tours suivants), qui route vers 23 playbooks. Les étapes du playbook sont
  copiées **verbatim** dans la todo-list ; une étape sautée reste visible avec
  `skip: <raison>`.
- **23 skills-principes** (un principe par fichier, trigger conditionnel
  « Apply when… ») indexées inline dans le mode ; règle d'honnêteté : citer un
  principe impose de nommer la décision qu'il a changée, et de n'avoir cité
  que des feuilles réellement lues dans la session.
- **Skills de workflow** : `how`/`why` (exploration + enquête de rationale
  multi-MCP avec doctrine épistémique), `architect` (ground → sketch en arena
  → implement → scrap), `arena` (N candidats + juge cross-famille + greffe),
  `swarm` (couverture/courses), `interrogate` (revue adverse multi-modèles,
  verdict trié Act on/Consider/Noted/Dismissed), `reflect` (3 relecteurs +
  synthétiseur + approbation humaine), `blast-radius`, `recall`,
  `create/maintain-verification-skill`, `show-me-your-work` (décision-log TSV
  audité contre le transcript + relecture cross-modèle), `unslop` (règles à
  identifiants stables), `technical-writing` (Diátaxis + Google style + STE +
  Global English, sources datées), `tdd`, `no-comments` (+ agent « Comment
  Sicko »), `automate-me`, `figure-it-out`.
- **Playbooks d'autonomie** : autonomous-run, autopilot-full/-stack,
  orchestrate (coordinateur permanent multi-jours, briefs normés GOAL/SCOPE/
  …/STANDING, store un-écrivain-par-fichier, drains, ledger de vérification
  clé (PR, head SHA), invalidation de verdict par `git patch-id`, protocole
  de liveness/zombies), babysit/shipping (frontière de merge, triage Bugbot
  sceptique).
- **Outillage code testé** : `orch` (CLI bun, store de 1 607 lignes + tests),
  `watch-pr` (4 fichiers de tests), `check-plan.mjs` (lint structurel de
  leurs documents de plan), `worktree-audit.sh`.
- **`benny`** : pack d'automation dormant (triage Slack → repro → fix avec
  preuve UI), non enregistré comme skills.

## 3. Forces — argumentées

### 3.1 La chaîne de vérification la plus sérieuse du genre

`prove-it-works` (l'artefact réel, jamais un proxy — « suspect the
observation method before the system ») ; `blast-radius` avec une **échelle
de preuve explicite en 5 crans** (tu l'as dit < tu pointes la ligne < tu
montres que le cas ne se produit pas < tu l'as exécuté < tu l'as reproduit
dans l'app) et la consigne d'isoler LE fait unique dont la sûreté dépend et
de le prouver en exécutant du code ; `create-verification-skill` (skill
projet-locale avec feature map par fonctionnalité, **prouvée une fois de
bout en bout avant remise** — « a generated skill that was never executed is
a draft, not a deliverable ») ; `maintain-verification-skill` (cycle
d'entretien à 3 issues nommées clean/changed/blocked, « never edits product
code »). C'est ma règle State Verification, mais outillée.

### 3.2 Une méthodologie de blinding d'evals supérieure à la mienne

Le playbook eval est construit contre l'effet observateur : jamais les mots
eval/test/judge/candidate/rubric dans un chemin ou prompt vu par le
candidat ; prompts organiques ; candidats ignorant l'existence des autres ;
juge aveugle aux noms de modèles ; **suivi de chaîne gradé depuis le
transcript (fichiers réellement ouverts), jamais l'auto-rapport**. Détail
concret : mes fixtures tournent dans `/tmp/grill-eval-*` — le nom du CWD
viole leur règle. Mon corpus reste supérieur sur le versionnement et le
rouge-d'abord ; le leur n'existe pas (cf. §4.1) — mais leur hygiène de
blinding est un durcissement direct d'ADR-0009.

### 3.3 `epistemics.md` — doctrine épistémique transposable telle quelle

5 tiers de confiance (Direct/Supported/Inferred/Speculative/Unknown), guide
de formulation par tier (mots qui engagent vs mots qui couvrent), piège de
sycophancie (« l'hypothèse de l'utilisateur est un prompt d'enquête, pas une
conclusion à valider »), « le null documenté est un résultat », check de
calibration final. Autonome, zéro couplage, aligné State Verification.

### 3.4 Les outils code sont testés — contraste net avec AIDD

`orch`, `watch-pr` : vrais fichiers de tests. `check-plan.mjs` est leur
propre `encode-lessons-in-structure` appliqué à eux-mêmes : un lint qui
vérifie la structure de leurs plans au lieu d'une consigne de prose.

### 3.5 Mécanismes d'honnêteté d'exécution élégants et bon marché

`skip: <raison>` (une étape sautée reste visible) ; l'anti-name-dropping
des principes (« a principle citation with no decision behind it is the
tell ») ; l'audit du décision-log **contre le transcript** en fin de run
(« fix the log, not the story ») ; la relecture du trail par un modèle d'une
autre famille avec section « Attention » obligatoire.

### 3.6 Maturité opérationnelle de l'orchestration

Le playbook orchestrate encode des leçons chèrement acquises : complétions =
événements de queue, jamais des interruptions ; briefs auto-portants avec
standing orders collés verbatim à chaque spawn (« directives decay across
resumes ») ; un écrivain par fichier ; verdicts clés (PR, head SHA)
invalidés par `git patch-id` au restack ; sondes de liveness par effets de
bord uniquement ; réconciliation des zombies ; « never resume an agent to
check on it ». Très supérieur à l'executor/checker d'AIDD en ingénierie.

### 3.7 Discipline d'écriture empilée et sourcée

`unslop` à règles numérotées stables (citables par d'autres skills) ;
`technical-writing` en 4 couches avec sources et dates de fetch (Diátaxis,
Google dev style, STE, Global English) et un exemple avant/après. Recoupe
mes propres règles mais la couche STE/Global English est un cran plus fine.

## 4. Critiques — sans concession

### 4.1 Le paradoxe AIDD, en version allégée : zéro corpus d'eval versionné

Le guide (§9) prescrit de tester tout changement de skill en aveugle, le
playbook eval est sophistiqué — et les 60+ artefacts de prompt du repo n'ont
**aucune fixture commitée**. Des passes de prose massives partent chaque
semaine (« density and mannered-prose pass across the skills », « replace
semicolons, em dashes… ») sans preuve de non-régression. Seuls les outils
TypeScript sont testés. Leur propre doctrine (build-the-lever,
encode-lessons-in-structure) appliquée à leur produit exigerait un corpus —
`check-plan.mjs` prouve qu'elles savent le faire. Adopter en bloc violerait
ADR-0009.

### 4.2 Anti-planning dogmatique et incohérent

Le README assume « personally, i don't believe in planning. the best spec is
code » — puis le repo ship un squelette de plan de 156 lignes, un linter de
plans, des briefs d'orchestration ultra-normés et `figure-it-out` qui
« designs the workflow before any code ». Ce qui est rejeté, c'est le
planning produit amont (mon PRD/PLAN/matrice) ; ce qui est reconstruit, c'est
du planning d'exécution. Incompatible avec ma chaîne documentaire, et
présenté comme un goût personnel érigé en défaut de conception.

### 4.3 Couplage Cursor dur ; la prémisse multi-modèles meurt en mono-fournisseur

`~/.cursor/rules/`, Task avec `environment: "cloud"`/`readonly`, dépendances
`cursor-team-kit` (/deslop, control-ui/cli), built-ins Cursor (create-skill,
/loop, /goal, /automate), chemins `agent-transcripts/`, Bugbot, forges
Origin/Graphite, bun. Surtout : `arena`/`interrogate` tirent leur valeur de
la **diversité de familles** (Grok/GPT/Claude — « different models have
different blind spots ») ; en environnement Anthropic-only, l'argument
central s'évapore en grande partie. Un portage ne transporterait pas la
valeur.

### 4.4 Constantes d'équipe durcies en doctrine

« Ten lanes on `grok-4.6-fast-xhigh` » par PR — imposé par le linter de
plans ; ticks d'audit à 30 min ; premier push sous 15 min ; slugs de modèles
en dur dans chaque skill (deux PRs, #210 et #365, juste pour bumper des
défauts — leur propre laziness-protocol § « consolidate decisions » non
appliqué à eux-mêmes). Ce sont des réglages d'une équipe, pas des lois.

### 4.5 La posture d'autonomie est l'inverse de la mienne — et son ordre compte

`never-block-on-the-human` + mode sticky + overnight/autopilots : « avance,
présente, corrige après coup ». Ma discipline par défaut est la validation
par étape hors critère explicite. Point structurel : leur chaîne de
confiance ne tient que parce que la couche de vérification scriptée
(verify-skills, watchers, swarm-verify) existe **avant** l'autonomie.
Adopter l'autonomie sans la vérification serait le pire découpage possible.

### 4.6 Taxe de contexte et frontières de playbooks brumeuses

143 lignes de mode + index des principes lu à chaque tâche + feuilles lues
par principe appliqué + playbook + skills routées : le coût fixe par tâche
est élevé. 23 playbooks aux périmètres qui se chevauchent (bug-fix /
runtime-forensics / trace-forensics / perf / hillclimb ; autonomous-run /
figure-it-out / orchestrate / 2 autopilots) — la densité de prose « Distinct
from X, which… » est l'aveu que le routage est fragile.

### 4.7 Divers

Persona théâtral de Comment Sicko (« Yes… Ha ha ha… Yes! ») — le fond (la
keep-list de commentaires : licence, contrainte externe prouvée, doc d'API
publique, lien vers issue) vaut mieux que la forme. Autrice unique : le
rythme et la cohérence tiennent à une personne.

## 5. Confrontation avec mon workflow

| Zone | pstack | Chez moi | Lecture |
|---|---|---|---|
| Principes de code | laziness-protocol, subtract-before-you-add, foundational-thinking, minimize-reader-load | Karpathy (Simplicity First, Think Before Coding, Surgical Changes) | Recouvrement massif — rien à importer sur le fond ; le *format* (trigger « Apply when » + citation-avec-décision) est meilleur |
| Vérification | prove-it-works, blast-radius, verify-skills | State Verification (prose), evals ADR-0009 | Leur outillage est supérieur ; ma porte d'eval est supérieure. Complémentaires (P1, P2, P5) |
| Evals | Méthodologie de blinding forte, zéro corpus | Corpus versionnés rouge→vert, blinding faible | Emprunt croisé évident (P1) |
| Boucle de leçons | reflect (3 relecteurs + synthèse + approbation + check « structurel > prose ») | /immunize + /insights (tri-destination, porte) | Convergent — leur check structurel ≈ ma porte. Rien à importer |
| Autonomie | never-block, sticky, overnight | Graduated autonomy | Frontal — non-emprunt, sauf le *contrat* overnight le jour venu (T2 roadmap) |
| Planning | Anti-planning produit, planning d'exécution lourd | PRD/PLAN/ADR/matrice | Frontal — non-emprunt |
| Orchestration | orchestrate + orch (testé) | Aucun besoin actuel ; R1 AIDD armé | **P6 remplace R1 comme première carrière**, R1 garde ses guardrails de jugement |
| Revue de code | interrogate multi-familles | /code-review évaluée (B′) | Mono-famille chez moi : la prémisse ne porte pas |
| Écriture | unslop (IDs stables), technical-writing 4 couches | Conventions maison | Lectures de référence, pas d'installation |

## 6. Recommandations

### P0 — Ne pas installer le plugin. (forte)

Couplage Cursor dur (§4.3), posture d'autonomie inverse (§4.5), anti-planning
(§4.2), recouvrement Karpathy/immunize/code-review (§5), prompts non testés
(§4.1), bundle au rythme hebdomadaire d'une autrice unique. Même conclusion
que Pocock et AIDD : **carrière d'idées, pas une dépendance**.

### P1 — Hygiène de blinding des evals (immédiat, coût faible)

Amender le(s) README de corpus : rien dans les chemins/prompts vus par le
candidat ne révèle l'eval (renommer les CWDs `/tmp/grill-eval-*`) ; prompts
organiques ; suivi de chaîne gradé depuis le transcript, jamais
l'auto-rapport. Application obligatoire à la prochaine campagne.

### P2 — `epistemics.md` en doc de référence maison (immédiat, coût faible)

Adapter les 5 tiers + guide de formulation + sycophancy trap + « null
documenté ». Placement candidat : `docs/methodology/` — à router par la
matrice. Usage : audits, revues de repos, investigations.

### P3 — `skip: <raison>` (fusionné avec R2 AIDD)

Toute étape sautée d'une command/checklist reste visible avec sa raison.
Même véhicule que les blocs `## Test` : la prochaine command créée ou
refondue, en une seule passe. Pas de retrofit massif.

### P4 — Citation-avec-décision pour Karpathy (via la porte)

Candidate : « citer un principe = nommer la décision qu'il a changée ».
À verser dans l'inbox /immunize (destination probable
`karpathy-discipline.md`, porte d'eval si globale). Pas d'écriture directe.

### P5 — Verification-skill + feature map (armé)

Au premier projet où « vérifier en live » reste artisanal : skill
projet-locale Launch/Doctor/Drive/Evidence/Cleanup + feature map, prouvée
une fois de bout en bout avant remise. Adapter aux surfaces data
(pipeline, dbt) — ne pas copier le générateur Cursor.

### P6 — Orchestrate comme première carrière d'orchestration (fusion R1)

Au premier besoin réel d'orchestration déléguée : consulter d'abord
`orchestrate.md` + `autopilot-*` + `orch` (briefs normés, ledger patch-id,
liveness, drains), puis greffer les guardrails AIDD R1 (never judge your own
work ; the pass threshold is the caller's gate ; no silent TODO ; arrêt net
sur l'impossible). Mémoire AIDD amendée en ce sens le 2026-09-12.

### Non-emprunts explicites

- `poteto-mode` et le mode sticky : posture d'autonomie inverse.
- `arena`/`interrogate` : prémisse multi-familles sans objet en
  mono-fournisseur ; /code-review B′ déjà évaluée.
- `unslop`/`technical-writing` en bloc : recouvrement avec mes conventions —
  lectures de référence seulement (le pattern « règles à IDs stables
  citables » est à retenir le jour d'une refonte de conventions).
- Comment Sicko : garder la keep-list, pas le persona.
- `automate-me`, `make-bot-ui`, `benny` : couplage Cursor/Slack, sans objet.
- Les constantes (10 lanes, 30 min, slugs en dur) : vaccins, cf. roadmap §5.

### Revisite

~2026-12/2027-01, via `git log -- pstack` (pas de CHANGELOG). Surveiller :
apparition d'un corpus d'eval commité (leur crédibilité prompt-side en
dépend), évolution d'orchestrate/autopilots, stabilité du périmètre des
23 playbooks.

## 7. Verdict

Le plus abouti des trois repos revus sur l'ingénierie de vérification, et le
seul dont l'outillage code est testé. Mais un système d'une personne, pour un
outil que je n'utilise pas, avec une posture d'autonomie et une doctrine de
planning inverses des miennes — et le même angle mort que les deux autres :
**la prose qui pilote les agents n'est jamais testée**. 0/3 repos revus
testent leurs prompts ; la discipline ADR-0009 reste mon avantage comparatif.
La bonne transaction est le pillage ciblé P1-P6, dans l'ordre de la roadmap
(`~/claude-audit-notes/adoption-roadmap.md`) : blinding et epistemics
maintenant, le reste armé par déclencheurs.

---

*Revue conduite le 2026-09-12, clone shallow au commit `889ec4b`
(« fix(pstack): bug-fix/perf/hillclimb defaults to grok 4.6 (#365) »),
plugin v0.15.2. Repo `cursor/plugins` : 7 503 étoiles, 653 forks, créé
2026-01-23, dernier push 2026-09-12.*

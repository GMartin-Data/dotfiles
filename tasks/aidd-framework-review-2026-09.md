# Revue : ai-driven-dev/framework — 2026-09-11

> **Objet** : lecture méticuleuse du repo `ai-driven-dev/framework` (463⭐, créé
> 2026-02, poussé le jour même de cette revue) — avis critique et
> recommandations d'adoption pour le workflow personnel.
> **Méthode** : clone shallow, lecture intégrale des points d'entrée (README,
> ARCHITECTURE, FAQ, CLAUDE.md/AGENTS.md), lecture complète du SDLC
> orchestrateur + agents, sondage skill par skill des homologues de mon
> écosystème (10-learn, 02-challenge, 03-shadow-areas, 04-fact-check,
> 01-plan, 02-project-memory, 09-for-sure), harnais d'evals, dogfooding
> `aidd_docs/`, santé du projet via l'API GitHub.
> **Périmètre org** : tout le reste de l'org est archivé (prompts, rules,
> agents, community) ou périphérique (manifest, badges, hackathon). Le
> framework est le seul objet vivant — revue concentrée dessus, comme demandé.

## 1. Ce que c'est

Un **marketplace de 8 plugins Claude Code** (6 stables, 1 alpha, 1 beta)
couvrant un SDLC complet, converti aussi vers Cursor / Copilot / Codex /
OpenCode, avec un CLI TypeScript d'installation (383 fichiers src), un
kanban lisant les frontmatters de `aidd_docs/`, et le dogfooding complet du
framework sur son propre repo. Produit par la communauté française
AI-Driven Dev (Alexandre Soyes) ; le business model est la formation, le
framework est la vitrine MIT.

Chiffres : 50 skills, 2 agents, ~830 KB de markdown de prompts,
~12 KB de descriptions en charge permanente de contexte. Contributeurs
réels : **2** (blafourcade 576 commits, alexsoyes 136 — le reste est
marginal ou bots). 8 trains de release par plugin (release-please),
vélocité très élevée : aidd-refine déjà en v3, le CLI en v5 en 7 mois.

Architecture par **concern** : `aidd-context` (connaissance),
`aidd-pm` (produit), `aidd-refine` (méta-cognition), `aidd-dev`
(transformation de code), `aidd-vcs` (git), `aidd-orchestrator`
(séquencement), + `aidd-ui` (alpha), `aidd-telemetry` (beta, opt-in,
local-only).

## 2. Forces — argumentées

### 2.1 Une vraie doctrine architecturale, écrite et défendue

`docs/ARCHITECTURE.md` est le meilleur document du repo. Ce n'est pas une
carte, c'est une **jurisprudence** :

- **Placement par concern, un seul propriétaire** : « a missing capability
  goes in the plugin whose concern owns it, then the caller delegates.
  Never reimplement it in the calling plugin ». Même famille que ma
  matrice de responsabilité (« un producteur, un fichier »), appliquée aux
  capabilities.
- **Firewall knowledge/execution** : les plugins de connaissance ne
  touchent jamais au code source (le bootstrap de `aidd-context` ne crée
  délibérément aucun `package.json`).
- **Profondeur de délégation bornée à 2** : orchestrateur → agent feuille,
  jamais de cycle possible (« a recipe invoked inside an agent never
  spawns again »). Règle simple, vérifiable, qui tue une classe entière de
  dérives multi-agents.
- **Adressage des capabilities** : nom canonique `/plugin:skill` uniquement
  aux points de dispatch déclarés (table Actions d'un routeur, liste
  « Skills you may invoke » d'un agent) ; partout ailleurs on nomme le
  *concept*, jamais le skill. Couplage faible délibéré + permissions
  auditables.
- Les décisions y sont **défendues par des chiffres** : hook 27 ms vs CLI
  180 ms médian sur 12 runs pour justifier la frontière hook/CLI ; le pivot
  télémétrie a supprimé 25 fichiers / 4 355 lignes de scripts dupliqués et
  le doc dit explicitement « re-opening this question re-opens a question
  settled with numbers ». C'est de l'ADR sans le nom.

### 2.2 Anatomie router/actions = lazy-loading du contexte

Chaque skill : un `SKILL.md` de 30-40 lignes (frontmatter + flowchart
Mermaid + table d'actions + règles transversales), des `actions/*.md`
atomiques lues **une à la fois** (« read only the next action file »), des
`references/` à responsabilité unique, des `assets/` templates. Le SDLC
complet (orchestration 3 zones + routage des findings) tient en
**242 lignes**. La promesse « token-optimized » est tenue sur la
structure : seules les descriptions (~12 KB) pèsent en permanence.

### 2.3 Le split executor/checker — la meilleure idée du repo

- `executor` (**model: sonnet**) : « You decide how, never what » ; ne
  juge jamais son propre travail, ne touche jamais au plan, déclare tout
  ce qu'il contourne (« no silent TODO, skipped test, or placeholder
  mock »), s'arrête net sur l'impossible physique (paiement, 2FA) au lieu
  de simuler du progrès.
- `checker` (**model: opus**) : contexte frais, « no memory of how it was
  built » ; construit d'abord sa pile de validateurs, exige des preuves
  (« command output or file evidence, never bare claims »), et surtout :
  **« The pass threshold is the caller's gate, not yours. You report the
  score; you do not declare pass or fail »** — la séparation
  jugement/décision est une frontière que peu de systèmes tracent.
- Allocation de modèles par rôle : le bon marché exécute, le cher juge.
  Économiquement et épistémiquement correct.

### 2.4 Blocs `## Test` par action

Chaque action porte une table de cas pass/fail déclaratifs (ex. 10-learn
assess : « A packet has no user approval → it is neither written nor
handed off »). Même non exécutés (voir §3.1), ces blocs sont des
**contrats comportementaux** : le harnais d'eval les lit comme source des
assertions. C'est du test-first de prompt à l'état de graine.

### 2.5 Prose d'une qualité inhabituelle

`CLAUDE.md`/`AGENTS.md` (anti-sycophancie : « never open with "you are
right" », « don't fold under pushback »), `coding-assertions.md`
(test-first avec preuve par mutation : « a guard nothing fails for is
indistinguishable from a comment » ; « after any scripted edit, read the
file back » — leçon payée, contexte donné). L'honnêteté épistémique est
systémique : la table des hooks par outil distingue « Measured » de
« Declared, never observed against a running hook » ; les limitations sont
nommées, pas maquillées.

### 2.6 Dogfooding réel

`aidd_docs/` du repo est produit par le framework lui-même : memory bank
**totale de 488 lignes** (compacité disciplinée), specs et tasks datés
2026_06→2026_09, runs de télémétrie, kanban qui lit le tout. Le hook
SessionStart régénère le bloc mémoire dans les 3 fichiers de contexte
(CLAUDE.md, AGENTS.md, copilot-instructions). Ils vivent dans leur propre
système — c'est vérifiable dans l'historique.

## 3. Critiques — sans concession

### 3.1 Le paradoxe central : test-first partout, sauf sur les prompts

`coding-assertions.md` impose le test-first au TypeScript avec une rigueur
exemplaire (rouge d'abord, preuve par mutation). Mais le produit — les
50 skills, c'est-à-dire **du prompt** — n'est couvert par le harnais
`skill-eval` que pour **aidd-refine : 4 skills sur 50** (et encore,
brainstorm exclu car interactif). Opt-in, hors CI (« spends tokens, so it
is not a CI gate »), juge LLM « can flake ». Le cœur du framework —
l'orchestrateur SDLC, executor/checker, plan/implement/review — n'a
**aucune eval comportementale**. Les gates lefthook, massifs, valident la
*forme* (schémas JSON, liens markdown, frontmatter, duplication de
phrases entre docs) — jamais le *comportement*.

C'est exactement l'anti-pattern « corpus jamais exécuté » (ADR-0009) : des
blocs `## Test` déclaratifs partout, exécutés presque nulle part. Pour un
framework vendu « enterprise-grade SDLC », la promesse de fiabilité repose
sur l'inspection et l'usage, pas sur une porte. Mon système est 20× plus
petit mais chaque command structurante a un corpus exécuté A→B→A. Adopter
AIDD serait **régresser sur la vérification**.

### 3.2 La spec exécutable est un flowchart Mermaid — pari non couvert

Toute l'orchestration (zones, arêtes conditionnelles « When the source
references a ticket… », routage des findings vers Frame/Todo/Deliver)
vit dans des diagrammes que le modèle doit interpréter comme un programme.
Élégant et compact — mais aucune eval ne vérifie que l'orchestrateur suit
réellement le graphe (§3.1). Le drift silencieux diagramme/comportement est
exactement le risque que leur propre doctrine code (« a guard nothing
fails for… ») dénonce. Le pari est réel : sur un modèle plus faible ou une
mise à jour de modèle, rien ne le détecte.

### 3.3 L'autonomie vendue contredit la FAQ — et `09-for-sure` est un YOLO habillé

Le README ouvre sur `/aidd-orchestrator:01-sdlc` autonome (« decide and
act without confirmation ») ; la FAQ dit « **Not autonomous by default.**
Skills run under human supervision ». Les deux sont vrais séparément mais
la posture n'est pas assumée comme une tension. Et `09-for-sure` franchit
la ligne : « act as the user (**create accounts, generate keys**, approve
prompts, install tools), never asking. Stop only on a payment or a
destructive action » — le jugement de ce qui est « destructif » est
délégué au modèle en boucle non supervisée. Incompatible avec ma
graduated autonomy (l'autonomie se gagne par un critère pass/fail
explicite, pas par une déclaration d'intention).

### 3.4 Taxe de complexité multi-outils

5 outils cibles × 2 formats de distribution (marketplace/flat) × des
runtimes de hooks incompatibles (bridge OpenCode généré par plugin, format
Cursor réécrit, « two headless probes fired no plugin hook at all ») ×
8 trains de release. Le CLI (383 fichiers src) et le kanban
(architecture DDD 4 couches — pour un viewer de frontmatter) portent une
ambition d'infrastructure. Tout cela est *bien fait*, mais c'est une
masse de maintenance qu'un utilisateur Claude-Code-only paie en churn de
versions (aidd-refine v3, cli v5 en 7 mois) sans rien en retirer.

### 3.5 Bus factor ≈ 2, gouvernance jeune

576 + 136 commits pour les deux mainteneurs, 4ᵉ contributeur à
4 commits. La « communauté » est un Discord de formation, pas encore une
communauté de contributeurs. Repo créé en février 2026 : la doctrine est
belle mais n'a pas encore survécu à un départ, un désaccord, ou une
génération de modèles.

### 3.6 Memory bank auto-chargée — croissance non bornée

Le CLAUDE.md racine `@`-importe 10 fichiers mémoire (488 lignes
aujourd'hui) à chaque session. La discipline actuelle les tient compacts,
mais le mécanisme n'a pas de borne structurelle — c'est le drift que ma
matrice de responsabilité combat par la règle de non-overlap et la lecture
à la demande aux points de replanification. Leur propre AGENTS.md (liens
« read on demand, not auto-loaded ») montre qu'ils ont les deux régimes
sans trancher.

### 3.7 Mécanique de télémétrie fragile

La fin d'étape dépend d'un `echo "aidd:step-end …"` que le modèle doit
penser à émettre — reconnu dans leur propre prose (« a measurement that
never hears this ends the run at the next pause »). Un contrat
d'observabilité qui repose sur la conscience du modèle est un contrat
best-effort.

## 4. Confrontation avec mon workflow

| Fonction | AIDD | Chez moi | Verdict |
| --- | --- | --- | --- |
| Cadrage produit | `aidd-pm` (10 skills : brief, epic, US, PRD, spec, 3-amigos…) | `/prd` (canvas 11 sections, ADR-0013) + `/planning` | Couvert. Leur granularité épic/US vise les équipes ; sans besoin ici. |
| Revue adverse pré-gel | `02-challenge` (classif deal-breaker/suggestion/correct + rubrique de confiance) | `/grill` (arbre de dépendances des décisions, evals 6/6) | Couvert et mieux vérifié. La rubrique de confiance à 4 paliers est une jolie sortie, pas un manque. |
| Scan de gaps statique | `03-shadow-areas` (taxonomie verrouillée 7 catégories, sévérité 3 niveaux, probe-questions, **diff de re-run par catégorie+snippet**) | Rien d'équivalent (grill est interactif) | **Niche réelle non couverte.** Le diff de re-run anti-« spurious new gap » est l'idée la plus fine du plugin refine. |
| Leçons | `10-learn` : 5 destinations (memory/ADR/contract/rule/skill), réconciliation **updates/supersedes/retracts**, approbation par paquet | `/immunize` : tri-destination, porte d'eval globale, éviction event-driven (ADR-0015) | Convergence frappante des deux designs. Moi en plus : la porte d'eval. Eux en plus : la **retraction** explicite (supprimer, pas annoter) et la réconciliation nommée. |
| Mémoire projet | `02-project-memory` (bank multi-fichiers + hook de sync + mode `check` de drift) | CLAUDE.md + progress.md + matrice de responsabilité | Philosophies opposées (auto-chargé vs à-la-demande, §3.6). Le mode `check` (« show what drifted, change nothing ») est une bonne idée isolable. |
| SDLC orchestré | `01-sdlc` + executor(sonnet)/checker(opus) | Pas d'équivalent — sessions interactives, graduated autonomy | **L'emprunt le plus intéressant** : pas le SDLC, mais la paire d'agents et ses guardrails. |
| Evals de prompts | `skill-eval` : 4/50, opt-in, hors CI | ADR-0009 : porte systématique, corpus exécutés A→B→A | Je suis structurellement en avance. Leur format `cases.json` (setup/expect déterministe + `judge` séparé) est propre mais moins riche que mon driver. |
| Fact-check | `04-fact-check` : cascade cheapest-first (mémoire → codebase → web), hedge obligatoire, mécanique interne interdite en sortie | Règle State Verification (une ligne) | Leur formalisation est jolie ; ma règle couvre 90 % du besoin pour 2 % du poids. |
| Vérité d'exécution | blocs `## Test` par action | evals dans `claude/evals/` | Complémentaires — voir R2. |

## 5. Recommandations

### R0 — Ne pas installer le framework. (forte)

Recouvrement massif avec l'écosystème existant (prd/grill/planning/
immunize/code-review/adr), régression sur la vérification (§3.1),
philosophie d'autonomie incompatible (§3.3), taxe multi-outils sans objet
(§3.4), churn de versions à suivre pour rien. Même conclusion que pour
mattpocock/skills : **carrière d'idées, pas une dépendance**. La
différence : AIDD est architecturalement très supérieur à Pocock — c'est
un système pensé, pas une collection — mais le verdict d'adoption est le
même, pour des raisons différentes (Pocock : hétérogénéité ; AIDD :
recouvrement + vérification).

### R1 — Emprunt n°1 : la paire executor/checker et ses guardrails

À ressortir **au premier besoin réel d'orchestration déléguée** (pas
avant — pas de véhicule aujourd'hui). Ce qui mérite d'être copié tel quel :

- allocation de modèles par rôle (bon marché exécute, cher juge) ;
- « never judge your own work » / checker en contexte frais qui « never
  edits » ;
- « the pass threshold is the caller's gate, not yours » — le juge score,
  l'appelant décide ;
- « no silent TODO, skipped test, or placeholder mock » — la déclaration
  obligatoire des contournements ;
- l'arrêt net sur l'impossible physique au lieu du progrès simulé.

### R2 — Emprunt n°2 : blocs `## Test` dans mes commands/skills

Petit, compatible ADR-0009, valeur immédiate : chaque action/étape d'une
command porte ses cas pass/fail déclaratifs, qui deviennent les **seeds
des evals** au lieu de partir de zéro à chaque corpus. Candidat naturel :
la prochaine command créée ou refondue (pas de retrofit massif —
Surgical Changes).

### R3 — Emprunt n°3 : la réconciliation de 10-learn pour le chantier /immunize

Le chantier matrice §Cycle immunitaire Flux 2 + `immunize.md` §Éviction
est déjà ouvert (spec dans `tasks/lessons-archive.md`). Y verser deux
idées de 10-learn : (a) la **retraction** comme opération de première
classe — une leçon peut *retirer* une règle existante, pas seulement
l'amender ; (b) le vocabulaire de réconciliation nommé
updates/supersedes/retracts, plus net que ma prose actuelle. À trier dans
la session dédiée du chantier, pas avant.

### R4 — Emprunt n°4 (optionnel) : shadow-areas comme pré-passe de /grill

La niche est réelle (scan statique, non interactif, diffable au re-run).
Mais : /grill couvre déjà l'essentiel en mieux (interactif, arbre de
décisions), et une skill de plus = maintenance de plus. **Déclencheur
d'activation** : si un PRD/PLAN doit être audité *hors session interactive*
(gros artefact tiers, revue asynchrone) — alors reprendre la mécanique
taxonomie verrouillée + sévérité + probes + diff par snippet, en une
command native avec son eval, pas en installant le plugin.

### R5 — Lecture de référence à garder

`docs/ARCHITECTURE.md` vaut la relecture périodique comme *modèle de
document* : décisions défendues par mesures, distinctions
Measured/Declared, coût des pivots assumé chiffré. Même famille que ma
doctrine mais avec un cran de plus dans la quantification. À recouper
avec le cycle /insights si un ADR maison doit un jour arbitrer
« hook vs CLI » ou « où vit une capability ».

### Non-emprunts explicites

- `09-for-sure` / auto-accept : contraire à graduated autonomy, et le
  garde-fou est déclaratif.
- CLI, multi-tool, kanban, télémétrie : sans objet mono-outil ; la
  télémétrie est la partie la plus fragile du système (§3.7).
- `aidd-pm` : redondant avec /prd, granularité équipe.
- Memory bank auto-chargée : anti-pattern au regard de la matrice (§3.6).
  Le mode `check` de drift est la seule pièce à retenir, le jour où un
  audit de drift CLAUDE.md/matrice devient un besoin.

## 6. Verdict

Le framework le plus sérieux vu dans l'écosystème prompt-ware à ce jour —
une vraie doctrine architecturale, des frontières nettes, une honnêteté
épistémique rare, un dogfooding vérifiable. Et un paradoxe central qui
résume tout : **ils prêchent le test-first pour le code avec une rigueur
exemplaire, et ne l'appliquent pas à leur produit, qui est du prompt**
(4 skills évaluées sur 50, hors CI). Mon système est un ordre de grandeur
plus petit, moins ambitieux, mono-outil — mais chaque pièce structurante y
est passée par une porte rouge→vert exécutée. La bonne transaction n'est
donc pas l'adoption mais le pillage ciblé : la paire executor/checker
(R1), les blocs `## Test` (R2), la réconciliation retracts (R3) — dans
cet ordre.

---

*Revue conduite le 2026-09-11, clone shallow au commit du jour.
Releases au 2026-09-09 : aidd-context v2.8.0, aidd-dev v2.5.0,
aidd-orchestrator v2.3.0, aidd-pm v2.5.0, aidd-refine v3.0.1,
aidd-vcs v2.3.2, aidd-telemetry v0.2.0, cli v5.3.0.*

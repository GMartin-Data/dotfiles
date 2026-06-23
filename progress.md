## Dernière mise à jour
Date : 2026-06-23 16:30
Session : 4e0e35cc-bdad-40fa-8836-fbf7fb421aec (learning-skill — suite)

## Tâches complétées

- **README claude/ enrichi** : listings Commands et Skills étoffés d'une glose
  d'une ligne par item (format Hooks étendu à Commands + Skills). Checklist
  « Ajouter une command » mise à jour (format liste-avec-glose). Compteurs et
  parité vérifiés. Commit `0412a99`

- **Contrôle web Skill Creator officiel (Anthropic)** — vérifié sur source
  primaire (`anthropics/claude-plugins-official`, SKILL.md officiel lu verbatim) :
  plugin Claude Code réel, annoncé 2026-03-03, 4 modes (Create/Eval/Improve/
  Benchmark), 4 sous-agents (Executor/Grader/Comparator/Analyzer). L'Evaluation
  Tool de la Console est un outil *distinct* (prompts à variables, pas harnais
  SKILL.md). Résultat : ton rituel A→B→A maison a reconstruit par anticipation
  la structure qu'Anthropic vient d'outiller (format `grill.eval.json` ≈
  `evals/evals.json` officiel).

- **ADR-0009 créé** (Proposed) : délibération rituel maison A→B→A vs Skill
  Creator officiel. Recommandation Option C (hybride : moteur officiel + doctrine
  maison souveraine). Réserve identifiée : inconnue (a) format, inconnue (b)
  exécution. Commit `53f4c2e`

- **Essai pilote de traductibilité** : eval maison `output-no-file-written`
  (invariant hors-transcription : « zéro fichier écrit ») converti au format
  `evals.json` officiel. Inconnue (a) levée favorablement : assertions officielles
  absorbent la doctrine maison, invariants hors-transcription deviennent
  *programmables* (sha256, ls). Frange irréductible : jugement de présentation →
  qualitatif (eval-viewer), non pass/fail. Inconnue (b) (exécution) : reste
  ouverte — plugin sur disque = version légère sans agents/scripts/eval-viewer.
  Corpus pilote versé dans `grill/evals/pilot-skill-creator/`. Commit `7fc6ff2`

- **TODO.md mis à jour** : entrée « Run live du Skill Creator officiel → trancher
  ADR-0009 ». Déclencheur : prochain besoin réel d'eval (teach éprouvé ou corpus
  /grill). Portée : run live valide le *moteur* une fois ; adoption par skill au
  fil de l'eau (pas big-bang). Commit `7fc6ff2`

- **Confrontation best practices shanraisshan** (skills) — vérifié : frontmatter
  conforme, corps aligné Pocock. Aucun chantier. Acté dans le commit teach.

## En cours

Rien — working tree propre (`docs/rpi-audit-findings.md` untracked, hors périmètre).

## Prochaines étapes

1. **Re-router `methodology-trial`** (archive `tasks/learning-tracker-archive/`)
   — prochaine étape : `/claude-md` sur memory-grep + Phase 1a implémentation.
2. **Créer le workspace teach** (repo dédié, `MISSION.md` à rédiger) — à la
   première vraie session d'apprentissage AI Engineer.
3. **Run live Skill Creator** (cf. `TODO.md`) — déclenché par prochain besoin
   d'eval réel ; sur succès → trancher ADR-0009 en Accepted (Option C).
4. **Campagne evals A→B→A `/grill`** — corpus spécifié, jamais exécuté.
5. **Campagne evals A→B→A `/adr` et `/planning`** — état inchangé.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **ADR-0009 laissé Proposed** (reco) : inconnue (b) exécution non levée —
  run live déclenché par besoin réel, pas à blanc.
- **TODO.md** = bonne destination pour le run live (chantier futur conditionnel) ;
  ADR-0009 = délibération ; pilote = preuve figée. Non-overlap respectée.
- **Adoption par skill** (teach/code-mentor/etc.) se fait au fil de l'eau après
  run live du moteur — pas en big-bang.

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-06-23 14:45
Session : 4e0e35cc-bdad-40fa-8836-fbf7fb421aec (learning-skill)

## Tâches complétées

- **Refonte couche learning — architecture teach adoptée**. 5 ADRs (0004-0008,
  tous Accepted), 6 commits atomiques sur main. Handoff complet exécuté.

- **ADR-0004** : `reference/` en Markdown (chaîne PKM), `lessons/` HTML Tufte
  conservé. Seul écart assumé au design Pocock. Commit `5fb08d3` (groupe)

- **ADR-0005** : rétention unifiée via Anki — quiz HTML in-lesson reclassés
  fluency-only ; `teach` réutilise `code-mentor/scripts/anki-export.py` et son
  format sans duplication. Commit `5fb08d3`

- **ADR-0006** : `learning-records` = source d'état unique. `coach-pedagogique`
  garde son `PROGRESS.md` intra-projet (nature distincte : scaffolding-sur-
  livraison), émet en plus un record de synthèse unidirectionnel. Option A
  tranchée par l'humain. Commit `5fb08d3`

- **ADR-0007** (parent) : `teach` adopté comme colonne vertébrale stateful,
  `learning-tracker` tué, motif 4 outils / 1 état / 1 rétention, `dp-coach`
  conservé (niche distincte confirmée par l'humain). Commit `5fb08d3`

- **ADR-0008** : mécanique du pont d'état — record proposé/affiché en bloc
  copiable, jamais écrit hors CWD (symétrique au pattern existant code-mentor +
  précédent ADR-0003). Mécanique tranchée par l'humain. Commit `6e9d8a6`

- **Skill `teach` créée** (`claude/skills/teach/` — SKILL.md + 4 fichiers de
  format). Adaptée des 3 ADRs, pédagogie Pocock conservée verbatim ailleurs.
  Symlink runtime actif + déclaré dans `install.sh`. Commit `cb38733`

- **`learning-tracker` supprimé** : command, agent, hook SessionStart,
  entrée settings.json, 4 lignes install.sh, symlinks runtime. État (`MEMORY.md`
  + `completed-topics.md`) archivé dans `tasks/learning-tracker-archive/` avec
  README de provenance (suivi actif `methodology-trial` découvert à l'exécution
  — surfacé plutôt que détruit). Commit `2f3eced`

- **3 outils branchés sur le pont d'état** (`code-mentor`, `dp-coach`,
  `coach-pedagogique`) : chacun gagne une étape de fin de session proposant un
  learning-record copiable. Commit `6e9d8a6`

- **Matrice de responsabilité étendue** : section « Couche learning » ajoutée
  (table non-overlap 4 outils, 2 sources de vérité, backlinks ADRs). Commit
  `0929944`

- **Confrontation best practices shanraisshan** : frontmatter conforme (champs,
  caps, disable-model-invocation) + convention maison (3 skills existantes, même
  pattern). Corps aligné Pocock qui fait autorité. Aucun chantier supplémentaire.

## En cours

Rien — working tree propre (`docs/rpi-audit-findings.md` untracked, hors
périmètre).

## Prochaines étapes

1. **Re-router `methodology-trial`** (archive `tasks/learning-tracker-archive/`)
   — prochaine étape : `/claude-md` sur memory-grep + Phase 1a implémentation.
   Branches ouvertes : étapes 2-4 (ingestion API, webscraping, stack hors-Python).
   À coller dans progress.md du projet concerné ou ouvrir ce projet en session.
2. **Créer le workspace teach** pour la vraie mission AI Engineer (repo dédié,
   `MISSION.md` à rédiger) — déclenché à la première vraie session d'apprentissage.
3. **Campagne evals A→B→A `/grill`** — 5 evals spécifiées, aucune exécutée.
4. **Campagne evals A→B→A `/adr` et `/planning`** — état inchangé.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **Pont d'état (ADR-0006) — Option A** : learning-records source unique,
  `PROGRESS.md` de coach-pedagogique conservé comme état de nature distincte
  (scaffolding-sur-livraison), pont unidirectionnel par record de synthèse.
- **dp-coach** : survit comme niche distincte (exécution+analyse déterministe
  ≠ quiz conceptuel).
- **Mécanique pont (ADR-0008)** : record proposé/copié, jamais écrit hors CWD.
- **`MEMORY.md` learning-tracker** : archivé (pas détruit) — suivi `methodology-trial`
  actif découvert à l'exécution, décision d'archivage plutôt que de destruction.
- **Best practices** : acter le verdict (conforme), pas de chantier séparé.
- **`reference/` en Markdown** (ADR-0004) : seul écart assumé au design Pocock.

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-06-23 11:45
Session : 68f0e867-7529-4404-85a1-e7ccf74c3cc5 (grill-implementation)

## Tâches complétées

- **ADR-0003 créé et acté** (`adr/0003-grill-delegue-adr-sans-invoquer.md`,
  Accepted) : `/grill` délègue à `/adr` par instruction (jamais par invocation
  programmatique). Pour N décisions : ordre topologique, relations suggérées
  (Refines/Extends/Constrains), items autoportants, bloc copiable + invite
  visible, zéro fichier écrit. Commit `a32be56`
- **`/grill` implémentée** (`claude/commands/grill.md`) : slash-command
  user-scope, famille méthodologique `/prd`/`/planning`/`/adr`. Revue adverse
  pré-gel d'un PRD ou PLAN — parcourt l'arbre de dépendances des décisions, lève
  implicites et tensions inter-sections. Entrée `$ARGUMENTS` + fallback
  `prd.md`→`plan.md`. Stop déterministe : ledger OPEN/RESOLVED/DEFERRED, zéro
  OPEN garanti. Anti-trivialité : l'absence de section « Open questions » ne
  court-circuite pas le grill. Symlink actif + déclaré dans `install.sh`.
  Commit `cbc1ccb`
- **Corpus evals `/grill`** : 5 evals (preflight-artifact-absent,
  no-open-questions-section, deferred-branch-in-output,
  input-explicit-arg-over-fallback, output-no-file-written) +
  `setup-eval-cwd.sh` + `README.md`. Fixture `prd.md` avec contradiction
  délibérée (Contrainte hors-ligne vs critère de résumé externe). Commit `0924d56`
- **`.gitignore` : `docs/handoff/` ignoré** — handoffs = notes de travail
  jetables (précédent `AUDIT_PROGRESS.md`). Commit `5832dc4`
- **`install.sh` : parité restaurée** — `adr.md` et `planning.md` manquaient ;
  un bootstrap neuf aurait laissé `/adr` et `/planning` sans symlink. 10/10
  commands source désormais déclarées. Commit `88020d2`
- **README synchronisés avec les 10 commands réelles** — `README.md` et
  `claude/README.md` listaient 7 commands ; ajout de `adr`, `grill`, `planning`,
  compteur `(7)`→`(10)`, et note des sous-dossiers compagnons corrigée (5
  commands ont un `evals/`, seul `claude-md` a un `reference/`). Commit `7311fcc`
- **Immunisation contre l'oubli multi-fichiers** — racine commune des oublis
  `install.sh`/README de cette session et des sessions `adr`/`planning` :
  ajouter une command est un geste multi-fichiers sans checklist. Palier 1 (fait)
  : checklist « Ajouter une command » + one-liner de parité dans
  `claude/README.md`. Palier 2 (différé) : check de parité automatisé versé à
  `TODO.md`, déclenché si l'oubli se reproduit malgré la checklist. Commit
  `b5d6236`

## En cours

Rien — 8 commits committés, working tree propre (seul
`docs/rpi-audit-findings.md` reste untracked, hors périmètre).

## Prochaines étapes

1. **Campagne evals A→B→A `/grill`** — 5 evals spécifiées, aucune encore
   exécutée. Protocole : `cd ~/dotfiles/claude/commands/grill/evals &&
   ./setup-eval-cwd.sh <id>` → session B fraîche → transcription → jugement en
   session A.
2. **Fixture PLAN pour les evals `/grill`** — le corpus ne couvre que des PRD ;
   la condition d'arrêt PLAN (chaque décision archi confrontée à ≥1 alternative)
   n'a pas encore de fixture.
3. **Campagne evals A→B→A `/adr` et `/planning`** — leurs corpus sont écrits
   mais jamais exécutés (état inchangé depuis session précédente).

## Écarts vs PRD

Aucun (pas de PRD pour ce repo de configuration).

## Décisions prises

- **Nom `grill` retenu** : collision vérifiée négative — absent de `claude
  --help`, des 5 skills bundled, et des commands existantes.
- **Source de vérité réelle** : `dotfiles/claude/commands/grill.md` (pas
  `~/.claude/commands/` — correction d'une imprécision du handoff ; `~/.claude/`
  ne contient que les symlinks).
- **Portée v1 : PRD et PLAN**, une invocation = un artefact, type déduit de la
  structure du fichier résolu (pas de flag `--prd`/`--plan`).
- **Persistance de la liste de sortie : option 2** (bloc copiable + invite
  visible), pas de fichier scratch versionné — évite un artefact zombie périmé
  dès le premier `/adr` créé (cf. ADR-0003).
- **`docs/handoff/` ignoré** (pas commité) : les handoffs de conception sont des
  notes de travail jetables une fois l'implémentation terminée.
- **`install.sh` mis à jour hors périmètre `/grill`** : l'écart
  `adr.md`/`planning.md` existait avant cette session ; corrigé en commit séparé.
- **Répartition checklist vs TODO selon la nature** : la checklist d'ajout de
  command est une *convention durable* (→ `claude/README.md`, faite maintenant car
  besoin déjà prouvé) ; le check automatisé est une *évolution différée
  conditionnelle* (→ `TODO.md`, YAGNI tant que la checklist suffit). Chaque chose
  où sa nature l'appelle, pas les deux dans `TODO.md`.

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-06-22 16:30
Session : 73071d5c-aa41-4162-ab7f-9a05242b3df4 (fix hook block-rm-rf)

## Tâches complétées
- **Fix `claude/hooks/block-rm-rf.sh`** : le hook bloquait des commandes non-`rm`
  (`cp -r`, `ls -lr`, `sort -r`, `grep --recursive`, `echo "rm -rf"`...).
  - **Cause racine** : le scope `if: "Bash(rm *)"` est best-effort et FAIL-OPEN
    (doc Claude Code) — Claude Code lance le hook sur les commandes composites
    (pipes, `&&`, `$()`, assignations en tête) dès qu'il ne peut PAS prouver
    qu'elles ne sont pas `rm`. Le commentaire du hook (« scoped, pas besoin de
    re-vérifier que c'est un rm ») reposait sur une prémisse fausse.
  - **Cause aggravante** : l'ancien regex scannait la commande ENTIÈRE → matchait
    tout flag `r/R/f` de n'importe quelle commande + les chaînes littérales
    `--force`/`--recursive`/`rm -rf` (contenu d'arguments grep/echo).
  - **Correctif** : le hook re-vérifie qu'un mot-commande `rm` est présent (split
    sur séparateurs shell + `$()`, repère `rm`/`*/rm` après `VAR=val` et lanceurs
    sudo/xargs/...), et n'analyse que les tokens APRÈS `rm`. `settings.json`
    laissé intact (le `if:` reste un pré-filtre best-effort ; la robustesse vit
    dans le hook). Commit `4104c0b`
  - **Validé 35/35** sur le hook réel (entrée JSON stdin) : toutes les formes
    destructrices restent bloquées (`rm -rf`/`-Rf`/`--force`, `sudo`/`xargs`/`$()`
    rm -rf) ; tous les faux positifs passent (`cp -r`, `ls -lr`, `grep -rf`,
    `rmdir`, `rm.bak`).

## En cours
- Rien — fix committé (`4104c0b`), working tree propre (seul
  `docs/rpi-audit-findings.md` reste untracked).

## Prochaines étapes
- Reprise du fil principal : voir checkpoint `adr-workflow-refonte` ci-dessous
  (campagne evals A→B→A en session dédiée, etc.).

## Décisions prises
- **Re-vérifier `rm` dans le hook plutôt que durcir le `if:`** : le `if:` étant
  fail-open par conception, on ne peut pas s'y fier comme garde ; le resserrer
  n'apporterait aucune garantie. La robustesse appartient au hook (la doc
  recommande « the script does its own validation »). Ne pas cumuler les deux.
- **Scope des cas-limites** : `xargs rm -rf` / `sudo rm -rf` → bloqués (rm réel) ;
  `rmdir` / `rm.bak` / `grep -rf` → passent (`rm` n'est pas le mot-commande, ou
  `-rf` n'appartient pas à `rm`).

## Blocages
Aucun.

---

## Dernière mise à jour
Date : 2026-06-22 15:45
Session : 73071d5c-aa41-4162-ab7f-9a05242b3df4 (adr-workflow-refonte)

## Tâches complétées
- **ADR-0001 créé et acté** (`adr/0001-prd-produit-cible.md`, Accepted) : PRD =
  produit cible, frozen = baseline versionnée révisable par ADR. Premier usage réel
  de `/adr`. Commit `91396bc`
- **`/prd` aligné sur ADR-0001** : ~8 occurrences "v1" → "cible", "frozen" →
  "baseline", "Évolutions futures (v2+)" → "Au-delà de la cible", frontière
  PRD↔/planning matérialisée dans le template. Commit `6ec98a3`
- **Matrice alignée sur ADR-0001** : ligne PRD (frozen→baseline, out-of-scope v1
  →hors-cible, ajout "découpage MVP/itérations" dans "Ne contient JAMAIS"),
  règle 5 + Phase 0 reformulées. Commit `94b174f`
- **ADR-0002 créé et acté** (`adr/0002-mvp-palier-dans-plan.md`, Accepted,
  Extends ADR-0001) : MVP = palier de valeur nommé dans le PLAN (modèle C —
  PLAN unique, deux granularités : palier MVP + phase). Commit `3adf29d`
- **Matrice : frontière MVP positive** ajoutée (sous-section "Où vivent les MVP",
  ligne PLAN mise à jour avec les deux granularités, lien ADR-0002). Mentions
  "/planning à créer" et "/adr à créer" corrigées (les deux existent). Commits
  `2522e3d` + `a35b83b`
- **`/planning` aligné sur ADR-0002** : "milestone" → "palier MVP" partout
  (intro, règles, Q3, synthèse, template), lien ADR-0002, résidu "v1" corrigé
  dans le pré-flight PRD. Commit `a32a06f`
- **Evals `/planning` : drift corrigé + coverage ADR-0002** : fixture PRD du
  setup-eval-cwd.sh alignée (Périmètre cible / Hors-cible) ; nouvel eval
  `interview-mvp-tiers-vocabulary` (classe `vocabulary`) couvrant le contrat
  palier MVP. Commits `8c3b66b` + `ef02125`
- **README d'eval pour `/adr` et `/planning`** créés (calqués sur
  prd/evals/README.md, adaptés au comportement réel de chaque command :
  modes/supersession/immutabilité pour /adr ; gate semi-frozen / classe
  vocabulary / model opus pour /planning). Les deux flaggés "écrit, non
  exécuté". Commit `3aac2ed`

## En cours
- Rien — 11 commits atomiques sur main, working tree propre (seul
  `docs/rpi-audit-findings.md` reste untracked, exclu volontairement)

## Prochaines étapes
1. **[CAMPAGNE DÉDIÉE — session A neuve] Exécuter les evals `/adr` (7) et
   `/planning` (5)** via protocole A→B→A. ⚠️ GOURMAND EN CONTEXTE : A doit
   ingérer 12 transcriptions opus intégrales → une campagne complète sature une
   session A (le README /prd estime déjà 30-40 % pour 3 evals). NE PAS lancer en
   fin de session — démarrer A à 0 %. Découper en deux vagues (adr 7, puis
   planning 5), checkpoint + /clear entre les deux. Protocole détaillé dans les
   README d'eval de chaque command.
2. **Amender `planning.md` / `adr.md` si un run A→B→A révèle un gap** — les evals
   sont le juge (le vocabulaire MVP de /planning est le plus fragile, jamais
   éprouvé).
3. **README d'eval racine / index** (optionnel) : `/prd` `/claude-md` ont un
   tableau "État du corpus" ; envisager un index unique des 4 corpus si la
   duplication devient gênante.
4. Reliquat sessions précédentes : methodology-trial Phase 1a memory-grep ;
   `/immunize` inbox.

## Écarts vs PRD
Aucun (pas de PRD.md dans ce repo)

## Décisions prises
- **ADR-0001 : PRD = produit cible, frozen = baseline versionnée** (pas immuable
  au sens ADR) : révision via ADR si la cible change, édition silencieuse
  interdite. Frozen ≠ immuable : gelé contre la dérive non-tracée, pas contre
  le changement légitime.
- **ADR-0002 : MVP = palier de valeur dans le PLAN (modèle C)** : PLAN unique,
  deux granularités ("palier MVP" = livrable à valeur utilisateur ; "phase" =
  brique technique). Rejet de A (conflation milestone/MVP) et B (multi-PLAN).
  Porte de sortie vers B via futur ADR de supersession si un projet réel l'exige.
- **ADR-0002 relation : Extends ADR-0001** (étend sans contredire ; ADR-0001
  reste Accepted intouché — ce n'est pas une supersession).
- **"frozen" redéfini comme baseline** : la matrice, /prd et /planning utilisent
  maintenant "baseline révisable par ADR" au lieu de "frozen" ou "gelé" — levée
  de l'ambiguïté immuable vs versionnée.
- **Classe d'eval `vocabulary` créée** pour /planning : teste le vocabulaire
  produit (palier MVP vs milestone), distinct de `interview_cap` (qui teste le
  plafond de questions). Doctrine d'émergence respectée — classe née d'un besoin
  réel (ADR-0002), pas par anticipation.
- **Ordre canonique de replanning respecté à chaque étape** : ADR → document
  cible → outil → eval. Deux chaînes complètes dans la session.

## Blocages
Aucun.

---

## Dernière mise à jour
Date : 2026-06-22 11:20
Session : 42307f88-526d-4e04-b0a1-d834575ee902 (enhance-workflow)

## Tâches complétées
- **Matrice de responsabilité documentaire déplacée vers emplacement canonique** : `docs/responsability-matrix.md` (vide, mal placé, mal orthographié) → `docs/methodology/responsibility-matrix.md`. Cohérence vérifiée avec CLAUDE.md + planning.md + auto-référence de la matrice. Commit `8c03a2e`
- **Convention ADR ajoutée** (`docs/methodology/conventions/adr.md`) : satellite de la matrice — immuabilité corps / mutabilité statut, 5 relations inter-ADR, numérotation. Commit `7e48387`
- **Section "Documentary Methodology" reformulée** dans claude/CLAUDE.md : la matrice est référence conceptuelle (pas Read runtime obligatoire) ; lecture runtime seulement au replanning Phase 3. Commit `2c9ddfe`
- **Commande `/planning` créée et rendue invocable** (symlink runtime manquant ajouté). Commit `10504d5`
- **`/prd` refactorée** : découpage en phases retiré du PRD (migré vers /planning), renumérotation Risques/Critères. Commit `4a851e9`
- **Commande `/adr` créée** (option 2 : création + supersession bidirectionnelle ; mode argument `--from-context` ; aucune trace de source dans l'artefact) + corpus 7 evals. Test-first respecté (evals validés avant code). Commit `fce314a`
- **Corpus 4 evals `/planning`** (bootstrap minimal, doctrine d'émergence) : gate, pré-flight PRD-absent/nominal, interview_cap. Commit `7de32b5`
- **Exemption direct-sur-main déclarée** : `~/dotfiles/CLAUDE.md` créé (manquait), désambiguïsé du payload `claude/CLAUDE.md`. Commit `1fab091`

## En cours
- Rien — 8 commits atomiques sur main, working tree propre (seul `docs/rpi-audit-findings.md` reste untracked, exclu volontairement)

## Prochaines étapes
1. **[CHANTIER DÉDIÉ — session vierge] Refonte conceptuelle PRD = produit cible** (et non PRD=v1). Décision de fond prise cette session, NON encore implémentée. ORDRE IMPOSÉ par la méthodo : (a) écrire un ADR actant le passage PRD=v1 → PRD=cible + conséquences sur le `frozen` et le découpage ; (b) SEULEMENT ensuite amender prd.md (~10 occurrences "v1") + matrice. Premier vrai cas d'usage de `/adr`.
2. **Exécuter les evals `/adr` (7) et `/planning` (4)** via protocole A→B→A — nécessite sessions B vierges + humain comme canal. Les deux commandes sont écrites/spécifiées mais PAS exécutées contre leur corpus.
3. **README d'eval pour `/adr` et `/planning`** (calqué sur prd/evals/README.md : doctrine + protocole + état du corpus). Absent pour les deux.
4. **Combler le trou v1→v2 dans la matrice** — sera traité par la refonte (étape 1) ou ratifié séparément.
5. Reliquat session précédente : methodology-trial Phase 1a memory-grep ; `/immunize` inbox.

## Écarts vs PRD
Aucun (pas de PRD.md dans ce repo)

## Décisions prises
- **Matrice : emplacement canonique** `docs/methodology/responsibility-matrix.md` (sous-dossier methodology/ + orthographe responsi-bility)
- **Rôle de la matrice** : référence conceptuelle dont les commandes dérivent leurs règles (prompts autonomes), PAS un Read runtime obligatoire ; Read seulement au replanning Phase 3
- **`/adr` périmètre** : option 2 (création + supersession bidirectionnelle), PAS option 3 (cycle complet) — le trivial (Status Accepted/Deprecated) reste manuel ; Simplicity First
- **`/adr` mode selon source** : argument explicite `--from-context` (déterminisme > détection floue), PAS auto-détection
- **`/adr` trace de source** : AUCUNE dans l'artefact (overlap avec git blame ; donnée fausse-par-construction si co-décision ; zone immuable)
- **Workflow dotfiles** : exemption direct-sur-main inconditionnelle (mono-user, pas de CI ; garde-fou = rituel evals, pas topologie git) — option 1, déterminisme
- **Evals = mécanisme de test des slash-commands** (Evaluation-Driven Development, Anthropic) : contrat comportemental observable, protocole A→B→A. C'est l'équivalent test-first pour un artefact-prompt
- **`/planning` bootstrap 4 evals** : protéger le fragile (interview_cap, attesté fragile par lesson one-question-at-a-time), pas l'important-mais-blindé (scope_guard, doublement défendu dans le prompt) — doctrine d'émergence
- **DÉCISION DE FOND (à instruire par ADR avant implémentation) : PRD = produit cible, MVP = itérations successives.** Colle au réel (client exprime besoin → PRD interprète → MVP raisonnables planifiés). Conséquences à peser : déstabilise le `frozen` du PRD, repose la question du document-par-itération.

## Blocages
Aucun. Note : la refonte PRD=cible (étape 1) est volontairement différée en session dédiée — pas un blocage, un séquençage discipliné (un concept à la fois).

---

## Dernière mise à jour
Date : 2026-05-27
Session : 638ff394-772d-467a-8266-5a8553a65dac (karpathy-inspired-guidelines)

## Tâches complétées
- **Évaluation comparative Karpathy vs Shanraisshan** : analyse méticuleuse des deux repos, verdict — Karpathy comme boussole conceptuelle, Shanraisshan comme auditeur d'implémentation (rôles distincts, non concurrents)
- **Présentation des 4 principes Karpathy** un par un avec exemples EXAMPLES.md : Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution
- **Décision d'intégration** : 4 principes en synergie (pas extraction partielle), option A (section dans CLAUDE.md user), format D1 distillé, position L1 entre State Verification et Global Do NOT
- **Uniformisation CLAUDE.md en anglais** : décision d'homogénéiser la langue (meilleur alignement training distribution modèle), traduction des 3 "Global Do NOT" existants avec relecture critique de chaque formulation
- **Intégration Karpathy dans CLAUDE.md user** : section "Coding Discipline (Karpathy)" ajoutée, 4 principes annotés `adopted 2026-05-27`, commit `3ec0bfe` poussé
- **Audit de conformité HumanLayer** : confrontation du CLAUDE.md résultant aux best practices humanlayer.dev — score 6/6, seule réserve actionnable = ligne 15 (état transitoire /pr skill)
- **Ajout section "Version Control"** : 3 règles (conventional commits + pre-commit, atomic granularity, branch workflow + distinguo complexe vs perso), déménagement de la ligne Conventional Commits hors Communication, commit `1031427` poussé
- **Ajout règle Test-first** dans Coding Discipline (Karpathy) : règle opérationnelle dérivée de Goal-Driven Execution, spécifique à Claude en tant qu'agent (user reste test-after), périmètre d'exemption explicité (scripts, exploration, config, docs), commit `1031427` poussé
- **Retrait ligne /pr "workflow under finalization"** du CLAUDE.md user (anti-pattern HumanLayer : état transitoire consomme attention permanente)
- **TODO.md enrichi** : enrichissement (β) entrée "Migrer PR template" pour couvrir aussi la skill `/pr` + ajout nouvelle entrée "Audit mettre de l'ordre dans le workflow agentique" avec condition de déclenchement (stabilité workflow, pas date), commit `70ef137` poussé

## En cours
- Rien — session clôturée proprement

## Prochaines étapes
1. **Finaliser le workflow agentique** (PR template, ADR, éléments workflow CLI à arbitrer) — condition de déclenchement pour l'audit TODO
2. **Créer skill `/pr`** une fois les 3 questions structurantes tranchées (où vivent ADR, quels artefacts en PR, template fixe vs modulaire) — cf. TODO.md entrée "Migrer PR template + skill /pr"
3. **Reprendre methodology-trial** : Phase 1a implémentation memory-grep (priorité non négociable avant Étape 2) — cf. progress.md entrée 2026-04-28
4. **Audit workflow agentique** après finalisation — cf. TODO.md entrée "Audit mettre de l'ordre"
5. **`/immunize`** à la prochaine passe (inbox en attente)

## Écarts vs PRD
Aucun (pas de PRD.md dans ce repo)

## Décisions prises
- Karpathy comme boussole conceptuelle (4 principes en synergie), Shanraisshan comme auditeur d'implémentation — rôles distincts
- CLAUDE.md user uniformisé en anglais (format natif modèle, meilleur alignement)
- Section "Coding Discipline (Karpathy)" : option A (dans CLAUDE.md), format D1 distillé, position L1
- Règle Test-first spécifique à Claude agent (user reste test-after) : option A (ligne dans CLAUDE.md user, dérivée de Karpathy 4)
- Section "Version Control" en position L1 (entre Communication et Session Discipline)
- Politique de tests : scope projet uniquement (Karpathy 4 couvre l'universel)
- Report skill `/pr` : workflow pas encore finalisé, créer la skill avant stabilisation ancrerait les décisions provisoires — audit post-finalisation
- TODO.md : fusion β (entrée PR template + skill `/pr` sous un item) + entrée audit séparée

## Blocages
Aucun

---

## Dernière mise à jour
Date : 2026-04-28 (campagne methodology-trial — pivot candidats Étape 2+)
Session : (prolongation post-Étape 1, brainstorm candidats outils utiles écosystème Claude Code)

## Tâches complétées
- **Pivot stratégique campagne methodology-trial** : virage des candidats "stress-tests généralisabilité" vers candidats "outillage AI/Claude Code utile au quotidien", après triple gain identifié (connaissance écosystème + outillage perso + signal d'audit méthodologique sous charge réelle)
- **Modèle hybride 60/40 retenu** : 60% outils utiles haute densité signal, 40% stress-tests généralisabilité (préserver détection biais d'archétype)
- **Vérification écosystème Claude Code** via subagent `claude-code-guide` : confirmation existence `/insights` (slash command native d'audit usage local, postérieure au cutoff cutoff feb 2025) + `/usage` (alias `/stats`) + `/team-onboarding`. À utiliser plus tard quand corpus de sessions de build sera riche (post-Étape 2 minimum).
- **Décision de NE PAS lancer `/insights` maintenant** : signal trop pauvre actuellement (0 projet implémenté), risque de procrastination méthodologique déguisée
- **Brainstorm candidats Étape 2+ via interview ciblée** :
  - `gh-prs-tracker` ❌ écarté : pas de PRs réelles côté Greg (repos solo), outil mort-né
  - `ai-models-watcher` 🟡 reculé en candidat 4 : pertinent mais ROI modeste (changelogs Anthropic existent), fréquence d'usage faible
  - `prompt-companion` (NotebookLM helper) 🟡 reculé en candidat 3 : couvre pain points B (sélection prompts) + D (suivi qualité jamais fait), basé sur repo public `notebooklm-prompts` existant
  - `skill-eval-runner` ✅ **promu candidat 2** : pain point chiffré (~3h36/cycle 3 skills), proposal mature pré-existante (avril 2026), archétype radicalement opposé à memory-grep (subprocess + LLM-as-judge + parsing dynamique sortie `claude -p`), stress-test fort `/prd` `/claude-md` (5 trous explicites à combler)
- **Décision pivot candidat 2** : prompt-companion → skill-eval-runner

## En cours
- Rien (décision pivot prise, attente reprise Étape 1 implémentation memory-grep)

## Prochaines étapes

**Discipline anti-procrastination** : memory-grep doit être FINALISÉ (atteindre seuil de valeur, pas dogmatiquement exécuter PRD ligne par ligne) avant toute préparation skill-eval-runner. Comparer 2 projets terminés > comparer 1 demi-livrable + 1 nouveau projet.

1. **Étape 1 finalisation memory-grep** — non négociable avant pivot Étape 2 :
   - Phase 1a (squelette + scan + smoke test) côté ~/projects/memory-grep
   - Phase 1b (frontmatter parsing) — pain point originel
   - Phase 2 (output enrichi) — usage quotidien
   - **Retro post-Phase 2** : Phase 3 polish vaut-elle l'effort ou reportée ? Décision tranchée et tracée dans progress.md memory-grep
   - Phase 3 (polish) ou marquer "reportée" selon retro
2. **Préparation pré-`/prd` skill-eval-runner** :
   - Première tâche d'observation : lancer `claude -p "drill me on Python list comprehensions"` → observer sortie brute → décider stratégie détection triggering. **Ne pas lancer `/prd` avant.**
   - Corriger pitch sur 3 points : (a) supprimer "Stack imposée" → référence CLAUDE.md memory-grep + délibération via `/prd` Phase 2, (b) corriger volumétrie ~3h36/cycle, (c) trancher Cruft vs uv init manuel
3. **Étape 2 — `skill-eval-runner`** : `/prd` → `/claude-md` → implémentation (audit A→B→A si appétit)
4. **Étape 3 candidate — `prompt-companion`** (NotebookLM helper) : archétype I/O réseau + état + clipboard + interview interactive
5. **Étape 4 candidate — `ai-models-watcher`** ou pivot selon évolution
6. **Étape 5 (recommandé) — projet stress-test généralisabilité** hors-archétype Python CLI single-user (Go/Rust ou service longue durée API multi-component) — préserve hybride 60/40
7. **Audit cross-CLAUDE.md** (action correctrice friction #1 du 2026-04-28) : grep `.claudeignore` + `gitignore.*aware` sur tous les CLAUDE.md du repo
8. **`/immunize` à la prochaine passe** : inbox 6 entrées — surveiller récurrence
9. **`/insights` exploitable** : après finalisation memory-grep + skill-eval-runner (corpus de sessions de build suffisant)

## Décisions prises
- **Pivot candidat 2 : prompt-companion → skill-eval-runner** justifié par :
  - Pain point chiffré récurrent (cycle validation skills, ~3h36/run de re-test) vs pain ressenti diffus (suivi qualité NotebookLM optionnel)
  - Cadrage plus mature (proposal pré-existante avec 5 trous explicites identifiés vs esquisse en session)
  - Archétype technique radicalement opposé à memory-grep (subprocess + LLM-as-judge + parsing dynamique vs scan filesystem statique read-only) → 6+ axes opposés
  - Stress-test plus fort `/prd` `/claude-md` (recursivité méta : eval-runner = outil qui teste des outils, expose Phases 4/7/10/11 sous angles inédits)
  - Synergie boucle vertueuse (outil qui améliore ta capacité à construire d'autres outils)
- **prompt-companion conservé candidat 3** : NotebookLM helper reste pertinent (pain point B + D réels, dogfooding 3-5×/semaine si NotebookLM utilisé), mais second à skill-eval-runner sur critères ROI mesuré + maturité cadrage
- **`gh-prs-tracker` définitivement abandonné** : signal pain point absent (Greg n'a pas de PRs en attente, repos solo), outil mort-né si construit
- **Modèle hybride 60/40** : éviter pivot 100% "outils Claude Code" qui créerait biais d'archétype invalidant la généralisabilité de la doctrine. Au moins 1 projet doit rester stress-test pur (non-Python ou multi-component longue durée).
- **Ordre d'exécution non négociable** : Phase 1a memory-grep AVANT toute préparation skill-eval-runner. Pas de "menu menu menu jamais cuisiner".

## Blocages
Aucun

---

## Dernière mise à jour
Date : 2026-04-28 (campagne methodology-trial — Étape 1 CLAUDE.md ✅ + audit méthodologique)
Session : (catchup post-/clear, prolongée /claude-md memory-grep accompagné session A→B→A)

## Tâches complétées
- **Étape 1 — CLAUDE.md `memory-grep` produit** (côté ~/projects/memory-grep, hors dotfiles) :
  - 219 lignes, 13 sections (For AI — Read first / Session protocols / Filesystem Access, Stack, Project layout, Code conventions, Testing, Versioning, Languages, CI/CD, Out of scope, Constraints, Common commands)
  - Anglais strict (sauf zones FR explicites listées)
  - Commit baseline f3d4f38 `docs: initial CLAUDE.md and progress checkpoint` (CLAUDE.md + progress.md ensemble, PRD.md déjà committé séparément)
- **Audit méthodologique `/claude-md` accompagné en mode A→B→A** :
  - Fichier d'audit complet : `~/claude-audit-notes/methodology-trial-claude-md-memory-grep.md`
  - 11 phases d'interview auditées phase par phase
  - Bilan : 3 frictions critiques + 6 patterns positifs + 1 friction protocole méta
- **3 frictions critiques capturées dans `tasks/lessons-inbox.md`** :
  1. `.claudeignore` est une fiction + Read/Glob/Grep ne respectent pas `.gitignore` (CRITIQUE — implications cross-CLAUDE.md)
  2. Pré-flight `/claude-md` ne lit pas `MEMORY.md` projet/dotfiles (gap doctrinal)
  3. Conventions figées non appliquées comme contraintes dures cross-phases (2 occurrences même session)

## En cours
- Rien (Étape 1 entièrement close, pause avant Étape 2)

## Prochaines étapes
1. Étape 1 — finalisation memory-grep : Phase 1a implémentation (uv init + structure memgrep/ + CLI Typer minimal + smoke test) — session ultérieure dédiée côté memory-grep
2. **Audit cross-CLAUDE.md** : grep `.claudeignore` + `gitignore.*aware` sur tous les CLAUDE.md du repo dotfiles + projets externes connus (action correctrice friction #1)
3. **`/immunize` à la prochaine passe** : 3 nouvelles entrées 2026-04-28 dans inbox + 3 entrées 2026-04-27 préexistantes (6 total) — surveiller récurrence pour promotion vers `## Global Do NOT`. Pattern "conventions figées" déjà à 2 occurrences dans la même session = signal fort.
4. Étape 2 — Ingestion API : choisir parmi `gh-prs-tracker`, `anthropic-models-watcher`, `dataset-gouv-fetcher`
5. Étape 3 — Webscraping : `hn-watch` ou `arxiv-skim`
6. Étape 4 (optionnelle) — stack hors-Python pour stresser la généralisabilité

## Décisions prises
- **Protocole d'audit A→B→A pour `/claude-md`** validé sur memory-grep : 11 phases auditées en parallèle de l'exécution, friction protocole révélée (A invisible aux actions hors-interview de B → faux positifs possibles sur "inférences non sourcées"). Action correctrice : A demande confirmation avant flagger.
- **Capture audit dans `~/claude-audit-notes/`** (réutilisation convention existante pour audit dotfiles) plutôt que création d'un nouveau dossier
- **Granularité fine pour lessons-inbox** : 3 entrées séparées plutôt qu'une fusionnée — cohérent avec pratique précédente, `/immunize` fusionnera si pattern récurrent
- **Patterns positifs (6) NON ajoutés à lessons-inbox** : restent dans le fichier d'audit comme matériau pour enrichissement futur de la doctrine `/claude-md`. Lessons-inbox = règles à promouvoir, pas réservoir de bonnes pratiques.
- **Commit baseline avec scope vide** (`docs:` au lieu de `docs(claude-md):`) : refus du scope inventé, respect strict de la liste des 8 scopes figés en Phase 5.1 du CLAUDE.md memory-grep

## Blocages
Aucun

---

## Dernière mise à jour
Date : 2026-04-27 (campagne methodology-trial — Étape 1 PRD ✅ + /immunize)
Session : (catchup post-/clear, prolongée audit→methodology-trial)

## Tâches complétées
- Sujet learning-tracker `methodology-trial` ouvert (commit 78cced0) — campagne d'éprouvage de la méthodologie /prd + /claude-md + /progress + /immunize sur projets variés
- **Étape 1 — CLI `memory-grep` PRD validé** (côté ~/projects/memory-grep, hors dotfiles) :
  - PRD.md généré : 8 critères de succès, 4 phases d'implémentation (1a/1b/2/3), 5 risques, gestion d'erreurs 7 cas avec exit codes POSIX
  - Hypothèse case-sensitivity : tranchée smart-case post-PRD via `/prd` lui-même
  - Architecture Phase 10 correctement skippée (composant unique)
  - git init + /progress effectués côté memory-grep
- 7 frictions méthodologiques capturées dans tasks/lessons-inbox.md (commit 4351910)
- /immunize 2e passe (commit d8496b7) :
  - 2 nouvelles règles `## Global Do NOT` promues (groupes A "spec écrasée par UX" et B "cohérence transverse multi-phases")
  - 7 entrées inbox fusionnées en 2 règles
  - Inbox : 9 → 3 entrées | Global Do NOT : 1 → 3 règles | Cap : 3/20
- Subagent learning-tracker invoqué : `methodology-trial` sessions 1 → 2, méta sessions 6 → 7

## En cours
- Rien (campagne Étape 1 close, pause avant Étape 2)

## Prochaines étapes
1. Étape 1 — finalisation memory-grep : /claude-md projet + Phase 1a implémentation (squelette + scan + smoke test) — session ultérieure dédiée
2. Étape 2 — Ingestion API : choisir parmi `gh-prs-tracker`, `anthropic-models-watcher`, `dataset-gouv-fetcher`
3. Étape 3 — Webscraping : `hn-watch` ou `arxiv-skim`
4. Étape 4 (optionnelle) — stack hors-Python pour stresser la généralisabilité
5. Surveiller récurrence des 3 lessons inbox pour promotion future
6. Test terrain hook SessionStart (passif — staleness `methodology-trial`)

## Décisions prises
- Le pattern "le modèle écrase la doctrine quand l'UX appelle un raccourci" est promu en 3 règles distinctes du `## Global Do NOT` (typographie, découpage spec, cohérence transverse). Originellement issu de dotfiles + memory-grep, validé cross-contexte.
- Fusion préférée à la conservation d'entrées proches : 7 frictions distinctes regroupées en 2 règles synthétiques plutôt que promues séparément. Réduit le bruit cognitif au runtime.
- `claude/CLAUDE.md` (versionné dans dotfiles) **est** `~/.claude/CLAUDE.md` (symlink) : la doctrine /immunize "global vs projet" se collapse en une seule destination sur ce repo. Cas particulier du repo dotfiles lui-même.

## Blocages
Aucun

## Tâches complétées
- Merge `feat/claude-md-instance-aware` → main confirmé (commits aa95ac0 → 0ec5576)
- README.md racine et claude/README.md alignés avec le pattern command + companion folder (commit 0ec5576)
- settings.json committé séparément (commit 0fc02e5 : effortLevel xhigh, Opus default, theme dark-daltonized)
- /immunize exécuté sur tasks/lessons-inbox.md — aucune promotion (3 entrées 1× chacune, datées du même jour : règle 2+ occurrences non atteinte)
- MEMORY.md learning-tracker mis à jour (session 4, Phase 6 fermée, 4 branches ouvertes consignées) — commit 62145f2
- tasks/lessons-inbox.md committé (3 lessons Phase 6 datées 2026-04-27) — commit d8bffc7
- Push origin/main effectué (0ec5576..d8bffc7)
- **Phase 7 — Audit dotfiles clôturé** : AUDIT_PROGRESS.md supprimé (était gitignoré, action locale silencieuse). Trace utile déjà migrée : commits scopés, fiches `~/claude-audit-notes/`, lessons-inbox.md, MEMORY.md learning-tracker. Aucune mention "audit" dans les READMEs versionnés à nettoyer. Commit checkpoint 1e83e13.
- **Phase 6g — Campagne A→B→A `/prd` ✅** :
  - `setup-eval-cwd.sh` rendu non-interactif (`--no-input` + `--extra-context`) — commit 6c75347
  - 3 CWDs préparés, 3 sessions B exécutées sous Opus (model frontmatter)
  - Eval `strict-mode-existing-prd` : ✅ 5/5 (gate strict-mode propre)
  - Eval `preflight-cruft-instance` : ⚠️ 4.5/5 → ✅ après fix (étape "vérif arbo" tacite → spec durcie en 2 étapes numérotées explicites) — commit 8ba959d
  - Eval `no-preflight-empty-cwd` : ✅ 5/5 (cas négatif propre)
- Lesson `lessons-inbox.md` reformulée : pattern "modèle survole les étapes mal mises en relief" généralisé à modèle-agnostique (Sonnet ×2 + Opus ×1 = 3e occurrence) — commit 6369662

## En cours
- Rien — audit dotfiles entièrement clôturé (Phases 1-7 ✅, plus Phase 6g ✅)

## Prochaines étapes
1. Test terrain hook SessionStart (passif — staleness `dotfiles-audit`)
2. /immunize à la prochaine passe : promouvoir la lesson "spec-skip" (3e occurrence atteinte, règle 2+ largement franchie)
3. Mettre à jour le sujet learning-tracker `dotfiles-audit` → ARCHIVÉ à la prochaine ouverture

## Décisions prises
- Suppression AUDIT_PROGRESS.md plutôt que conversion en note rétrospective : redondant avec les fiches pédagogiques + commits + memory déjà en place
- Durcir `prd.md` immédiatement (pendant la campagne) plutôt que noter en TODO : contexte chaud, fix minimal, alignement avec `claude-md.md` déjà éprouvé
- Lesson `lessons-inbox.md` reformulée modèle-agnostique : l'observation Opus invalide l'attribution Sonnet-spécifique initiale ; le pattern vise la **typographie** de la spec (numérotation, paragraphes distincts), pas la taille du modèle
- Aucune promotion lessons-inbox cette passe — règle "2+ occurrences" respectée stricto sensu malgré pertinence forte
- Deux commits scopés séparés (learning-tracker / tasks) plutôt qu'un commit fourre-tout

## Blocages
Aucun

---

## Dernière mise à jour
Date : 2026-04-27 14:15
Session : 9ef4eaf8-7f35-4453-9fc6-a48420a38dad

## Tâches complétées
- Refonte corpus evals /claude-md (doctrine command post-pivot) :
  - claude-md.eval.json : 3 evals (step0_gate + 2 × preflight) remplaçant
    les 3 evals should_trigger/should_not_trigger/ambiguous de l'époque skill
  - README.md : doctrine recentrée sur comportement post-invocation
    (pré-flight, Step 0, gates, allègement), protocole A→B→A simplifié
  - setup-eval-cwd.sh : IDs renommés, cas obsolète trigger-negative retiré
- Bootstrap corpus evals /prd (symétrique) :
  - prd.eval.json : 3 evals (strict_mode_gate + 2 × preflight)
  - README.md : doctrine miroir /claude-md, spécificités /prd
    (strict-mode gate, model: opus, 13 phases, 3 blocs de validation)
  - setup-eval-cwd.sh : 3 fixtures (PRD préexistant / Cruft fraîche / CWD vide)
- Campagne A→B→A vague 1 (gates) :
  - step0-existing-claude-md : ❌ run 1 (gate contournée sur CLAUDE.md vide)
    → fix Step 0 "vide ou non" → ✅ run 2 5/5
  - strict-mode-existing-prd : ✅ run 1 5/5
- Campagne A→B→A vague 2 (/claude-md préflight) :
  - preflight-cruft-instance run 1 : ⚠️ 4/5 (Bloc 2 dérive Phases 5+7)
    → fix split Bloc 1/Bloc 2 + cadenas verbatim → ✅ run 2 4/5
  - run 2 : ⚠️ 5/5 mais réflexe PRD-first manquant + glissement Phase 1
    → fix réflexe PRD-first (propose /prd si PRD absent)
  - run 3 : ⚠️ 5/6 glissement Phase 1 (question ouverte cadrage produit)
    → décision : gate conditionnelle Cruft+!PRD → arrêt (option B retenue)
    → reformulation invariant 6 (territoire CLAUDE.md vs territoire PRD)
  - preflight-cruft-without-prd : ✅ run 1 5/5
  - preflight-cruft-with-prd : ✅ run 1 6/6
- Campagne A→B→A vague 3 (/prd préflight) :
  - preflight-cruft-instance : ✅ run 1 5/5
  - no-preflight-empty-cwd : ✅ run 1 5/5
- 4 fixes doctrinaux appliqués à claude-md.md + instance-aware-flow.md
  (voir section Décisions prises)

## En cours
- Rien (campagne de test close, prêt pour merge)

## Prochaines étapes
1. Merge feat/claude-md-instance-aware → main + push
2. Mise à jour README.md racine et claude/README.md
   (skills : 3 restantes ; commands : prd et claude-md de retour)
3. AUDIT_PROGRESS.md Phase 6 → ✅ quand merge effectué
4. Commit séparé sur main : settings.json (effortLevel + cosmétique)
5. Phase 6g (reportée) : evals/prd/ lors d'une session dédiée /prd
   → déjà bootstrapé cette session, à tester en A→B→A dédié

## Écarts vs PRD
Aucun (pas de PRD — AUDIT_PROGRESS.md fait office de feuille de route)

## Décisions prises
- Split Bloc 1 / Bloc 2 dans le pré-flight de claude-md.md :
  Bloc 1 = résumé libre (enrichissement pyproject/pre-commit autorisé),
  Bloc 2 = annonce d'allègement templatée verbatim (Phases 1,2,8,11)
  Raison : éviter que Sonnet substitue ses propres phases (5, 7) au lieu
  de pointer vers reference/instance-aware-flow.md
- Gate conditionnelle Cruft+!PRD → arrêt dans /claude-md :
  Si .cruft.json présent ET PRD.md absent → message d'arrêt "workflow
  Cruft → /prd → /claude-md". Si pas de Cruft → poursuit (cas dotfiles,
  scripts, projets existants). Symétrie doctrinale avec /prd (qui protège
  son output PRD.md).
- /prd n'a pas besoin de gate conditionnelle supplémentaire :
  La seule gate nécessaire est déjà existante (PRD.md déjà présent → arrêt).
  Cas Cruft sans PRD = scenario nominal de /prd (c'est précisément pourquoi
  on l'invoque).
- Frontière /claude-md vs /prd formalisée dans instance-aware-flow.md :
  Phase 1 = territoire CLAUDE.md (nom, structure) ; problème/utilisateurs/
  valeur = territoire /prd. Si PRD.md présent (gate passée), le cadrage
  produit est déjà figé — Phase 1 = checkpoint, pas ré-élicitation.
- Reformulation invariant 6 eval claude-md :
  "checkpoint pur" → "territoire CLAUDE.md (nom/structure) sans glisser
  sur territoire PRD (problème, utilisateurs, valeur)"

## Blocages
Aucun

---

## Dernière mise à jour
Date : 2026-04-27 11:35
Session : 4eb7be93-c5d4-4178-93b4-a61f28867543

## Tâches complétées
- Campagne de test Phase 6f (protocole A→B→A) — 3 evals exécutées :
  - trigger-negative : ✅ 3/3 (negative space efficace, comportement nominal)
  - trigger-edge : 🟡 avant shims (skill non invoquée) → 🟡 après shims
    (skill invoquée via Skill tool, gap résiduel Step 0 sur CLAUDE.md vide)
  - trigger-positive : 🔴 auto-invocation toujours défaillante même avec
    query mot-pour-mot dans la description
- Diagnostic R0 — sentinelle instrumentée (non committée) : skill non
  déclenchée automatiquement dans les 2 cas critiques
- Création shims commands/claude-md.md + commands/prd.md → slash-commands
  /claude-md et /prd restaurées et fonctionnelles en session B
- Pivot doctrinal — retour skills → commands pour prd et claude-md :
  auto-invocation non désirée (usage exclusivement user-driven), progressive
  disclosure préservable en command, doctrine "migrer par nécessité" réaffirmée
- Migration complète (commit b3d7088) :
  skills/claude-md/ → commands/claude-md.md + commands/claude-md/{reference,evals}/
  skills/prd/SKILL.md → commands/prd.md
  install.sh mis à jour, symlinks skills périmés supprimés
- Corrections de cohérence post-migration : "SKILL.md" → "claude-md.md"
  dans reference/, "via la skill /progress" → "via `/progress`"
- Encart de dépréciation ajouté sur evals/README.md (doctrine EDD à refondre
  pour le modèle command — session dédiée prévue)
- Revert sentinelle diagnostique (non committé — Option B, sans trace git)

## En cours
- Rien (migration terminée, wrap-up en cours)

## Prochaines étapes
1. Session fraîche (après /clear) : tester /claude-md en session B vierge
   sur un CWD d'eval pour confirmer comportement post-invocation nominal
2. Refonte evals/README.md — nouvelle doctrine pour command :
   tester le comportement post-invocation (pré-flight, Step 0, gates,
   skip criteria), pas le déclenchement automatique
   → réécrire claude-md.eval.json en scénarios de comportement
3. Après validation comportement : merge feat/claude-md-instance-aware → main + push
4. Mise à jour README.md racine et claude/README.md
   (skills : 3 restantes ; commands : prd et claude-md de retour)
5. AUDIT_PROGRESS.md Phase 6 → ✅ quand merge effectué
6. Phase 6g (reportée) : evals/prd/ lors d'une session dédiée /prd

## Écarts vs PRD
Aucun (pas de PRD — AUDIT_PROGRESS.md fait office de feuille de route)

## Décisions prises
- Auto-invocation des skills custom user-level = non fiable en pratique :
  même une query mot-pour-mot dans la description ne garantit pas le trigger
- /prd et /claude-md = rituels utilisateur exclusivement → slash-commands
  est le bon primitif (pas skills)
- Progressive disclosure et modularité restent disponibles en command
  (sous-dossier commands/claude-md/ avec reference/ et evals/)
- model: opus conservé pour /prd (recommandation Boris Cherny : cadrage
  stratégique mérite le modèle le plus capable)
- Shims minces supprimés : le corps complet vit directement dans commands/*.md
- settings.json non-committé : effortLevel + cosmétique, indépendant — commit
  séparé à faire sur main après merge
- evals/README.md conservé comme matériel legacy à refondre (B2) — pas jeté

## Blocages
Aucun

---

## Dernière mise à jour
Date : 2026-04-22 17:00
Session : 0ac5cab2-512c-4df6-95da-4a99336f50b4

## Tâches complétées
- Phase 6e — Enrichissement skill claude-md instance-aware :
  pré-flight symétrique à /prd (détecte .cruft.json + arbo + PRD.md),
  progressive disclosure (3 reference files : instance-aware-flow.md,
  output-format.md, validation-checklist.md), SKILL.md allégé 405 → 231
  lignes (-43 %), traduit intégralement FR, Phase 11 dédupliquée
  (commit bb5ceef, branche feat/claude-md-instance-aware)
- Audit Context7 appliqué : best practices Anthropic officielles
  (token budget, progressive disclosure, frontmatter spec) +
  shanraisshan/claude-code-best-practice (14 champs frontmatter, trigger
  accuracy, évaluation lifecycle)
- Frontmatters enrichis symétriquement sur claude-md et prd :
  user-invocable, allowed-tools, paths, model (commit bb5ceef)
- Bootstrap eval suite claude-md : doctrine EDD, 3 queries (should_trigger /
  should_not_trigger / ambiguous_edge_case), setup-eval-cwd.sh
  (commit aa95ac0)
- Protocole A→B→A formalisé et gravé dans evals/README.md (rôles,
  frictions connues, séquence complète)
- AUDIT_PROGRESS.md mis à jour (Phase 6e ✅, 6f/6g/6h documentés)
- Mémoire persistée : project_cruft_template_path.md (pitfall -v2 suffix
  obligatoire : ~/python-project-template-v2, sans -v2 = ancienne tentative)

## En cours
- Rien (Phase 6e close, prête pour session de test)

## Prochaines étapes

### Session A (reprise via /catchup dans ~/dotfiles)
1. Relire evals/README.md section "Rôles & Protocole" pour se remettre
   dans le contexte du protocole de test
2. Lancer setup-eval-cwd.sh pour les 3 evals :
   ```
   cd ~/dotfiles/claude/skills/claude-md/evals
   ./setup-eval-cwd.sh trigger-positive-cruft-instance
   ./setup-eval-cwd.sh trigger-negative-user-global-conventions
   ./setup-eval-cwd.sh trigger-edge-existing-claude-md
   ```
   → note les 3 chemins /tmp/ retournés
3. Communiquer les 3 chemins pour lancer les sessions B

### Sessions B (3 × contexte vierge, une par eval)
Pour chaque eval-id :
1. cd <chemin /tmp/claude-md-eval-<id>-*/> && claude (nouvelle session)
2. Coller la query depuis evals/claude-md.eval.json (champ "query")
3. Laisser B répondre naturellement — ne pas guider ni annoncer qu'on teste
4. Couper dès que les 30 premières secondes d'interaction sont observées
   (pré-flight, annonce d'allègement, première question) — inutile de dérouler
   l'interview complète
5. Copier-coller l'intégralité de la transcription

### Retour session A (jugement)
1. Coller les transcriptions dans A une par une (pas toutes d'un coup)
2. A coche les expected_behavior (✅ / ⚠️ / ❌) pour chaque transcription
3. A produit le rapport matrice consolidé
4. Statuer ensemble sur les refinements SKILL.md si gaps identifiés

### Après la campagne de test (selon résultats)
- Si aucun gap → merge feat/claude-md-instance-aware → main, push
- Si gaps → session de refinement en mode A, re-test ciblé des items ❌/⚠️
- Phase 6g : bootstrap prd/evals/ (prochaine session touchant /prd)
- Phase 6h (optionnel) : cruft-reader partagé entre prd et claude-md
- Mise à jour README.md racine et claude/README.md (skills maintenant 5)
- AUDIT_PROGRESS.md Phase 6 → ✅ quand 6f validé

## Écarts vs PRD
Aucun (pas de PRD — AUDIT_PROGRESS.md fait office de feuille de route)

## Décisions prises
- Progressive disclosure appliquée à claude-md : SKILL.md = table des matières,
  contenu dense externalisé dans reference/ (doctrine officielle Anthropic)
- Contextes mutuellement exclusifs (Cruft détecté vs standard) dans fichiers
  séparés pour réduire le coût en tokens par invocation
- Frontmatter enrichi : allowed-tools inclut Bash pour claude-md (détection
  arbo) mais pas pour prd (Read seul suffisant) — différence intentionnelle
- Eval suite bootstrap : 3 queries minimum par doctrine YAGNI ; étoffage par
  nécessité observée (parallèle pytest-coverage), pas par anticipation
- Protocole test : A = auteur/juge (contexte projet), B = exécutant (CWD
  temporaire, contexte vierge), humain = canal de transmission. Isolation
  structurelle garantit absence de contamination (A ne voit B que via
  transcription capturée, jamais en live)
- setup-eval-cwd.sh force ~/python-project-template-v2 (avec -v2) comme
  valeur par défaut — protège contre le pitfall du template périmé
- settings.json non-commité : contient effortLevel: xhigh (réglé manuellement)
  + réordonnancement cosmétique de clés — indépendant de Phase 6e, à traiter
  séparément
- Phase 6f = test ciblé skill claude-md uniquement (pas un E2E complet du
  workflow Cruft → /prd → /claude-md — ça viendra après)

## Blocages
Aucun

---

## Dernière mise à jour
Date : 2026-04-20 19:15
Session : 191052df-cec4-49b9-b0f2-9080c5bdbc22

## Tâches complétées
- Phase 6.0 — README rewrites : claude/README.md réécrit (3 couches → 9 composants,
  principes de chargement, doctrine commands/skills/agents) + README.md racine aligné
  (tableau complet, hooks multi-événements) (commit c34c941)
- Phase 6b — Migration /prd command → skill : skills/prd/SKILL.md créé,
  commands/prd.md supprimé, install.sh mis à jour (commit 3cdb948)
- Phase 6c — Migration /claude-md command → skill : skills/claude-md/SKILL.md créé,
  !`cat CLAUDE.md` remplacé par Step 0 explicite (Read tool), install.sh mis à jour
  (commit 889dcaf)
- Phase 6d — Enrichissement skill prd : pré-flight .cruft.json détecte stack Cruft,
  allège Phase 8 (confirmation rapide) et Phase 10 (architecture pré-proposée),
  principe directeur "ne demander que ce qui mérite délibération" (commit 377ef10)

## En cours
- Rien (Phase 6 partielle close, pause avant session dédiée feature branch)

## Prochaines étapes
1. Session dédiée + feature branch `feat/claude-md-instance-aware` :
   - 6e : enrichir skill claude-md avec pré-flight symétrique (.cruft.json + arbo + PRD.md)
     — workflow instance → /prd → /claude-md validé
     — philosophie β : interview allégée (~4-5 phases sur ce qui reste indéterminé)
     — principe : "Cookiecutter a déjà demandé ce qui est décidable"
   - 6f : test E2E sur instance Cruft réelle (cruft create + workflow complet)
   - 6g : factorisation éventuelle ressource partagée cruft-reader (optionnel)
2. Mise à jour README.md racine et claude/README.md (skills maintenant 5 au lieu de 3)
3. Mise à jour AUDIT_PROGRESS.md Phase 6 (marquée ✅ quand 6e-6f clôturés)

## Écarts vs PRD
Aucun (pas de PRD — AUDIT_PROGRESS.md fait office de feuille de route)

## Décisions prises
- Phase 6 élargie : /prd et /claude-md migrés en skills (scénario 3 — enrichissement
  concret dès maintenant, pas juste migration mécanique)
- Doctrine réaffirmée : "migrer par nécessité" — ces deux cas justifient la migration
  par complexité croissante (pré-flight, ressources multi-fichiers)
- Workflow projet validé : instance Cruft → /prd → /claude-md (une seule session Claude,
  contexte PRD chaud pour génération CLAUDE.md)
- Philosophie /claude-md in-project : β (interview allégée ~4-5 phases sur ce qui
  reste indéterminable depuis la stack)
- Référence AUDIT_PROGRESS.md retirée de claude/README.md (lien mort à terme)
- Session parallèle indépendante : OK pour développer une feature sans rapport sur
  feature branch séparée — contextes Claude et git isolés
- Push origin/main : à faire en fin de cette session

## Blocages
Aucun

---

## Dernière mise à jour
Date : 2026-04-20 17:30
Session : e24c32e5-77f0-426c-939c-522bff3038b6

## Tâches complétées
- Audit learning-tracker.md (frontmatter) : memory: user retiré (inerte), "Task tool" → "Agent tool", chemin MEMORY.md explicité (commit 9727c82)
- Doctrine anti-croissance mémoire : format 3 lignes ARCHIVÉS, seuil 150 → 100 lignes, completed-topics.md créé (commit 7d17f8c)
- Audit scripts/ : fetch-sources.py (import os + docstrings Google), extract-json.py supprimé (code mort, 0 octet) (commit 009172a)
- Audit agent-memory/README.md : convention chemin, seuil per-subagent, tech-watch-scorer catalogué stateless (commit 59a24e0)
- Points 5/6 tranchés : 7/7 commands restent commands (grille à 3 questions validée sur tout le repo, aucun cas ambigu)
- Fiche pédagogique synthèse : fiche-grille-commands-vs-skills.md produite
- AUDIT_PROGRESS.md : Phase 5 marquée ✅, verdict 7/7 documenté
- Push de 7 commits Phase 5 vers origin/main (05785c5..59a24e0)

## En cours
- Rien (Phase 5 close, pause avant Phase 6)

## Prochaines étapes
1. Test terrain hook SessionStart (passif — attendre staleness dotfiles-audit > 24h)
2. Phase 6 — Meta & cohérence :
   a. claude/README.md : réécriture narratif "3 couches" → architecture réelle 8+ composants
   b. README.md racine : alignement post-audit
   c. install.sh : vérifier cohérence avec livrables Phase 5 (hook SessionStart, symlinks)

## Écarts vs PRD
Aucun (pas de PRD — AUDIT_PROGRESS.md fait office de feuille de route)

## Décisions prises
- memory: user dans frontmatter subagent = code mort → retirer (même classe que permissionMode)
- Format strict ARCHIVÉS learning-tracker : 3 lignes max dans MEMORY.md, narratif → completed-topics.md
- Seuil curation MEMORY.md : 150 → 100 lignes (alerte précoce au régime normal d'un tracker actif)
- 7/7 commands du repo restent commands : doctrine "migrer par nécessité, pas par conformité" validée sur tout le périmètre
- learning-tracker (dispatcher) : reste command — geste rituel, Agent tool assure déjà la séparation de contexte
- tech-watch (dispatcher) : reste command — Step 4 rapport DOIT rester en contexte principal
- Push origin/main : effectué en fin de Phase 5

## Blocages
Aucun

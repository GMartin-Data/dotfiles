# ADR-0016 : Moteur d'evals — runner officiel pour les cas mono-tour, driver maison pour les interviews

Status: Proposed
Date: 2026-09-22
Extends: ADR-0009

## Contexte

[ADR-0009](0009-rituel-evals-maison-vs-skill-creator.md) a fixé la doctrine
d'evals du repo (classes comportementales, fixtures à tension délibérée,
invariants observables, étoffage par nécessité observée) et posé que le
**moteur d'exécution est un détail remplaçable**. Il a retenu skill-creator
comme moteur (Option C), validé par un run unique le 2026-07-23. Dès le 28
juillet, la pratique a construit un moteur maison automatisé — `drive-session.py`
(sessions `claude -p` pilotées tour par tour, réponses conditionnelles) et des
scripts batch (`CLAUDE_CONFIG_DIR` isolé, avec/sans, A/B par tier) — parce que
skill-creator ne sait ni conduire une interview multi-tours ni isoler une
configuration. Cette dérive n'a jamais été actée.

Le 2026-09-22, `claude plugin eval` (runner officiel, GA depuis 2.1.269, local
2.1.278) a été mesuré sur pièce — audit `tasks/skill-evals-audit-2026-09.md`,
deux pilotes, 2,80 $ :

- il fournit nativement ce que le moteur maison avait construit à la main :
  session enfant isolée (config vierge, aucune skill personnelle), ablation
  avec/sans et Δ, répétition (`runs`), contexte de départ (`scaffold_script`,
  `history_file`), plafond de coût, exit code, rapport ;
- les six invariants du corpus feynman-mentor s'y expriment (graders
  `tool_used`, `regex`, `file_exists`, `llm`) ; trois runs y révèlent une
  variance qu'un run unique masquait ;
- il **ne fait pas** deux choses que le moteur maison fait : piloter une
  interview à branches conditionnelles (un cas = un tour utilisateur), et faire
  varier le payload global (la variable du corpus claude-md est le CLAUDE.md
  user-level, pas un plugin) ;
- il ne cible qu'un plugin (manifest requis), tourne par défaut sur Opus et non
  sur le modèle des settings, et ne restitue pas le raisonnement des juges.

Trois moteurs coexistent donc : skill-creator (un run, jamais réutilisé), le
moteur maison, et le runner. Il faut trancher lequel exécute quoi.

## Options considérées

- **Option A — Tout basculer sur le runner.** Un seul moteur, zéro script à
  maintenir, porte CI native.
  - Inconvénient : perd les corpus d'interview (grill 9 tours, prd, claude-md,
    planning, adr, immunize) et le corpus claude-md avec/sans règle — soit la
    majorité du parc et le garde-fou d'ADR-0015. `history_file` fige un
    transcript, il ne branche pas sur les questions de l'agent.

- **Option B — Statu quo : moteur maison + skill-creator.** Rien à changer.
  - Inconvénient : maintient trois moteurs dont un mort (skill-creator, un run
    en deux mois) et un redondant sur la partie mono-tour ; réinvente
    l'isolation, l'ablation et la répétition que le runner outille ; pas de
    porte CI ; contredit ADR-0009 (« moteur remplaçable ») en gardant un moteur
    que la pratique a déjà remplacé.

- **Option C — Hybride v2 (retenue).** Le runner exécute les corpus de
  **skills** et tout cas **mono-tour** ; le moteur maison exécute les
  **interviews multi-tours** et la **variation du payload global** ;
  skill-creator sort de la chaîne.
  - Avantage : chaque moteur sur ce qu'il seul sait faire ; la doctrine
    d'ADR-0009 est inchangée ; le parc maison ne régresse nulle part.
  - Inconvénient : deux moteurs à documenter ; un packaging plugin à mettre en
    place et à vérifier.

## Décision

**Option C.** La ligne de partage est le **nombre de tours utilisateur** du
cas, pas la nature de l'artefact (skill ou command) : un cas qui tient en un
tour — avec, au besoin, un transcript repris — va au runner ; un cas qui exige
des réponses conditionnelles reste au driver maison. Un sous-ensemble mono-tour
d'un corpus d'interview (pré-flight, gate strict-mode, résolution d'entrée) est
portable au runner sans attendre le reste.

Pourquoi pas A : la limite multi-tours est structurelle, pas un manque de
maturité ; les interviews sont le cœur du workflow (matrice Phase 0-1).
Pourquoi pas B : le coût du statu quo est une dette de maintenance et
l'abandon d'une porte CI gratuite.

## Conséquences

- **skill-creator retiré** de la chaîne de qualité ; les fichiers G2 de
  `claude/skills/feynman-mentor/evals/` (`evals.json`, `setup-eval-cwd.sh`) sont
  remplacés par des cas au format du runner lors de la migration.
- **`drive-session.py` et les scripts batch restent maintenus** pour grill,
  prd, planning, adr, immunize et le corpus claude-md. ADR-0015 inchangé.
- **Un manifest de plugin** devient nécessaire pour cibler le repo ; l'unité
  retenue (`claude/` comme plugin racine, cible chemin) est **à vérifier sur
  pièce** avant toute migration — effets de bord de `settings.json` et `hooks/`
  à la racine.
- **Règles de design de cas** (dérivées du pilote, à porter dans les README de
  corpus) : `runs: 3` minimum sur les classes `core_invariant` ; `--model`
  pinné sur les tiers frontière (le défaut est Opus) ; accorder par
  `--allow-tools` les outils que l'invariant interdit ; discovery et
  comportement post-invocation sont deux cas distincts (`history_file` pour
  « skill déjà active », sans indicateur `tool_used: Skill`) ; rubriques `llm`
  calibrées sur ce que le SKILL.md prescrit ; `regex` réservé aux marqueurs sans
  ambiguïté.
- **Porte CI possible** (`--threshold`, exit 1) — nouvelle capacité, non
  exploitée à ce jour.
- **Trade-off accepté** : dépendance à un outil Anthropic versionné (≥ 2.1.269,
  `schemaVersion` des résultats) et opaque sur le raisonnement des juges ; la
  doctrine, les corpus et les fixtures restent versionnés et souverains dans le
  repo, conformément à ADR-0009.
- **Les README de corpus documentent deux moteurs** au lieu de trois ; le
  README `claude/README.md` note le prérequis de version.
- Passage en `Accepted` **après** la migration du premier corpus réel
  (feynman-mentor) sur le packaging vérifié — même porte que les précédents
  (ADR-0009, ADR-0015) : pas d'acceptation sans run réel.

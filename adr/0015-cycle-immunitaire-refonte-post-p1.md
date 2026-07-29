# ADR-0015 : Refonte du cycle immunitaire — porte d'evals, triage tri-destination, éviction event-driven

Status: Proposed
Date: 2026-07-29
Extends: ADR-0009

## Contexte

`/immunize` (cycle immunitaire : inbox → Do NOT projet → Global Do NOT) encode la
doctrine **pré-P1** : promotion sur simple récurrence (2+ occurrences), format
imposé de prohibition absolue (« Ne jamais X »), pipeline à sens unique (aucun
mécanisme d'éviction hors cap à 20), aucune preuve exigée.

Deux sources convergent pour le réformer :

1. **Le fireside chat Cat Wu / Thariq Shihipar** (AI Engineer World's Fair, via
   simonwillison.net 2026-07-21 — déjà source des chantiers P1/P2/P3) : réduction
   de 80 % du system prompt de Claude Code en retirant les « don'ts » restrictifs
   (« maybe 90% true, but there's a real 10% of cases where it's not true »),
   consigne « soften the prompt so that it's actually 100% accurate », pipeline
   « incident → eval set », system prompts spécifiques par modèle.
2. **P1 (audit du CLAUDE.md global par evals**, `tasks/claude-md-audit-2026-07.md`) :
   preuve empirique maison — 2 des 5 règles testées en batch A étaient inutiles
   (retirées), verdict à 3 issues rodé, corpus `claude/evals/claude-md/` en garde
   de non-régression aux changements de modèle, driver partagé au coût effondré.

Audit du 2026-07-29 : une collision (l'inbox est colonisée par les fiches
`[INSIGHTS]` du cycle /insights, au cycle de vie incompatible — la règle
« unique > 7 j → archivage » archiverait une fiche en attente de revue), deux
tensions de fond (accumulation sans preuve ni éviction ; format prohibition),
une destination manquante (incident → eval), une scorie (`argument-hint` jamais
implémenté).

Huit décisions tranchées en interview le 2026-07-29, toutes sur recommandation.

## Options considérées

- **D1 — fiches `[INSIGHTS]`** : règle de skip dans le triage (rejetée :
  exception permanente dans un fichier à double population) vs **relocalisation**
  (retenue).
- **D2 — preuve avant promotion** : statu quo récurrence seule (rejeté : P1 a
  montré qu'il promeut des règles inutiles), eval-gate partout (rejeté :
  disproportionné pour la portée projet, locale et réversible), candidate + audit
  différé (rejeté : des règles non prouvées vivraient dans le prompt global) vs
  **eval-gate sur le global seul** (retenue).
- **D3 — format des règles** : prohibition uniforme (rejetée : pattern « 90%
  true »), prohibition + clause d'exception obligatoire (rejetée : syntaxe
  artificielle) vs **formulation 100 %-accurate** (retenue — les 2 règles Global
  Do NOT actuelles débordent déjà le template dans ce sens).
- **D4 — 3ᵉ destination** : aucune (rejetée : trous d'artefacts routés en prose
  au mauvais étage), eval prioritaire partout (rejetée : confond mesurer et
  corriger) vs **routage par ancrage d'artefact** (retenue).
- **D5 — éviction** : cap seul (rejeté : P1 resterait un one-shot), audit
  périodique calé /insights (rejeté : campagnes sans signal vu le débit — une
  règle devient obsolète quand le modèle change, pas quand le calendrier tourne)
  vs **event-driven** (retenue).
- **D6 — verdict de la porte** : binaire tier défaut (rejeté : angle mort sur
  les tiers pinnés), multi-tiers binaire (rejeté : échec tier-faible → règle
  globale sur-taxante ou perte sèche) vs **3 issues, précédent batch A**
  (retenue).
- **D7a — gouvernance** : hors matrice (rejetée : nouveau fichier et flux
  inter-documents sans arbitre) vs **entrée dans la matrice** (retenue).
- **D7b — argument-hint** : retrait du hint (rejeté : rendrait le « via
  /immunize » de Session Discipline faux) vs **implémentation du mode ajout**
  (retenue).

## Décision

1. **Inbox mono-population** : les fiches `[INSIGHTS]` déménagent dans
   `tasks/insights-actions.md` (fichier dédié, propriété du cycle /insights,
   cycle de vie à date de revue). `tasks/lessons-inbox.md` ne contient plus que
   des leçons brutes. Le protocole /insights est amendé là où il route ses fiches.
2. **Porte de promotion globale** : aucune règle n'entre en `## Global Do NOT`
   sans eval avec/sans (méthodo batch A, driver partagé) prouvant que le modèle
   échoue sans elle. La promotion **projet** reste au critère de récurrence
   (2+ occurrences), sans porte.
3. **Format 100 %-accurate** : test rédactionnel « quels cas rendraient cette
   règle fausse ? » — prohibition sèche seulement si vraie sans exception, sinon
   formulation conditionnelle (contexte + pourquoi). L'eval de la porte teste la
   formulation réelle. Le cap global (20) est conservé, non re-délibéré.
4. **Triage tri-destination** sur critère binaire d'ancrage : leçon incriminant
   un **artefact versionné** (command, skill, hook, script) → fix test-first +
   eval/test de non-régression au corpus de l'artefact, jamais de règle prose ;
   **comportement de session** pur → circuit règle (décisions 2-3).
5. **Éviction event-driven** (le pipeline devient bidirectionnel). Déclencheurs :
   changement de tier/modèle par défaut → rejeu du corpus avec/sans, toute règle
   que le nouveau modèle respecte sans elle est candidate au retrait ; cap
   atteint ; suspicion documentée en usage réel. Pas d'audit périodique à vide.
6. **Verdict à 3 issues à la porte** (analogue maison des system prompts
   par modèle) : échec sur le tier par défaut → règle globale ; échec limité aux
   tiers pinnés (grep des pins `model:`) → relocalisation dans les commands
   concernées ; aucun échec → pas de règle, leçon archivée avec sa preuve.
7. **Gouvernance** : le cycle immunitaire entre dans la matrice de
   responsabilité — table « qui détient quoi » (inbox / insights-actions /
   Do NOT projet / Global Do NOT / archive / corpus) + les deux flux (porte de
   promotion, éviction). La command dérive ses règles de la matrice
   (contrat Documentary Methodology existant).
8. **Mode ajout** : `/immunize "<leçon>"` = append daté à l'inbox puis stop ;
   le triage complet reste le mode sans argument. Aligne la command sur la
   Session Discipline (« lessons accumulate via /immunize »).

## Conséquences

- **Créations** : `tasks/insights-actions.md` (migration des 2 fiches
  existantes) ; corpus `claude/evals/immunize/` (evals de la command, écrites
  failing d'abord) ; section « Cycle immunitaire » dans la matrice.
- **Refonte** : `claude/commands/immunize.md` — triage tri-destination, porte à
  3 issues, format 100 %-accurate, mode ajout, en-tête d'inbox aligné.
- **Effet systémique** : chaque future règle globale naît avec sa fixture
  avec/sans au corpus `claude-md` — la même fixture sert de preuve à l'entrée,
  de garde de non-régression, et d'instrument d'éviction au changement de
  modèle. Le coût marginal d'une éviction tend vers un rejeu de corpus.
- **Trade-offs acceptés** : promotion globale plus lente (une campagne par règle
  — débit réel : 2 règles en 3 mois) ; règles plus longues (conditionnelles) ;
  une sync de plus matrice ↔ command à maintenir.
- **Porte de validation avant `Accepted`** (précédent ADR-0013/0014) : corpus
  `/immunize` rouge sur la command actuelle → refonte → vert, puis run réel
  A→B→A du scénario de triage complet.

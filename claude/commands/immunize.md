---
description: Cycle immunitaire de lessons-inbox.md — triage tri-destination (fix d'artefact, règle projet, porte d'eval globale), éviction event-driven ; mode ajout via argument
argument-hint: [lesson-description]
allowed-tools: Read, Write, Edit, Bash(grep:*), Bash(wc:*), Bash(cat:*), Bash(date:*)
model: sonnet
---

## Objectif

Consolider `tasks/lessons-inbox.md` en appliquant le cycle immunitaire.
Trois destinations de triage, une porte, une éviction :

- **Fix d'artefact** — la leçon incrimine un artefact versionné → correction
  test-first, jamais de règle prose.
- **Anticorps projet** — comportement de session récurrent, portée projet →
  `## Do NOT` du CLAUDE.md projet.
- **Anticorps global** — comportement de session récurrent, portée générique →
  candidate à la porte d'eval ; seule une preuve avec/sans ouvre
  `## Global Do NOT`.

Le pipeline est bidirectionnel : toute règle promue reste évincable
(déclencheurs en fin de prompt). Les règles de ce prompt dérivent de la
section « Cycle immunitaire » de `docs/methodology/responsibility-matrix.md` —
la matrice fait foi en cas de doute, y compris contre l'en-tête de l'inbox
s'ils divergent.

## Mode ajout (argument présent)

Si un argument est fourni (`/immunize "<leçon>"`) :

1. Appendre à la fin de `tasks/lessons-inbox.md` : `- [YYYY-MM-DD] <leçon>`
   (date du jour via `date +%F`).
2. Confirmer en une ligne (« Leçon ajoutée à l'inbox ») et **s'arrêter là**.

Aucun triage, aucun inventaire, aucun plan, aucune autre lecture ni écriture —
le triage complet est le mode sans argument.

## Pré-requis (mode triage)

Lire avant toute action :

1. `tasks/lessons-inbox.md`
2. Section `## Do NOT` du CLAUDE.md projet (racine)
3. Section `## Global Do NOT` de `~/.claude/CLAUDE.md`

Si l'inbox est vide, le signaler et s'arrêter.

## Procédure (mode triage)

### Étape 1 — Population

L'inbox est mono-population : des leçons brutes datées, rien d'autre.

Toute fiche `## [INSIGHTS …]` rencontrée appartient au cycle /insights (cycle
de vie à date de revue) : la relocaliser **intégralement** vers
`tasks/insights-actions.md` (créer le fichier si absent), sans jamais
l'archiver ni la traiter comme leçon — les règles d'âge de l'inbox ne
s'appliquent pas à cette population. Signaler la relocalisation au plan.

### Étape 2 — Inventaire

Compter les leçons brutes. Afficher : nombre total, plage de dates
(plus ancienne → plus récente).

### Étape 3 — Regroupement

Regrouper les leçons par pattern (même type d'erreur, même règle
sous-jacente). Pour chaque groupe : occurrences, dates, cause commune.

### Étape 4 — Triage par groupe

Appliquer dans l'ordre :

**A) Test d'ancrage (binaire, prioritaire).** La leçon incrimine-t-elle un
artefact versionné — command, skill, hook, script : un fichier présent dans
le repo ?

→ **Destination artefact** : fix test-first de l'artefact + test/eval de
non-régression à son corpus. **Jamais de règle prose**, ni projet ni global,
quel que soit le nombre d'occurrences — une règle qui contourne un artefact
fautif immunise le symptôme, pas la cause. Le plan nomme l'artefact, le fix à
engager et la destination du test de non-régression ; les entrées partent à
l'archive avec la trace du routage.

**B) Comportement de session récurrent (2+ occurrences)** → circuit règle :

1. **Portée projet** (outil, lib, convention propre au repo) : vérifier
   qu'aucune règle équivalente n'existe au CLAUDE.md projet ; rédiger au
   format 100 %-accurate (section dédiée) ; destination `## Do NOT` projet.
   **Sans porte** — la récurrence suffit (portée locale, réversible).
2. **Portée générique** (pattern réutilisable tous projets) :
   - Règle équivalente déjà en `## Global Do NOT` → archiver l'entrée
     (couverte). Si la règle existante porte un tag `(from [autre-projet])`,
     mettre à jour en `(learned YYYY-MM, confirmed across projects)`.
   - Sinon → **porte de promotion** : AUCUNE écriture au global en séance.
     Le plan produit la formulation candidate (100 %-accurate) et route une
     campagne d'eval avec/sans — fixture au corpus `claude/evals/claude-md/`,
     méthodo batch A, driver `claude/evals/drive-session.py` — qui doit
     prouver que le modèle échoue sans la règle. Verdict à 3 issues :
     - échec sur le tier par défaut → règle globale ;
     - échec limité aux tiers pinnés (grep des pins `model:` des commands) →
       relocalisation dans les prompts des commands concernées ;
     - aucun échec → pas de règle, leçon archivée avec sa preuve.
     Les entrées restent dans l'inbox, groupe tagué
     `[CANDIDATE-GLOBAL — eval pending]`, jusqu'au verdict de la campagne.

**C) Leçon unique** : > 7 jours → archivage vers `tasks/lessons-archive.md`
(avec date d'archivage) ; ≤ 7 jours → conservation (une nouvelle occurrence
peut encore la confirmer).

### Étape 5 — Plan d'action

Afficher AVANT d'écrire :

```
=== IMMUNIZE PLAN ===

RELOCALISATIONS (→ tasks/insights-actions.md) :
- [INSIGHTS YYYY-MM-DD] titre

ROUTAGES ARTEFACT (fix test-first + non-régression — jamais de règle) :
- <artefact> : <fix à engager> ; non-régression → <corpus/test cible>

PROMOTIONS PROJET (→ CLAUDE.md ## Do NOT) :
- "<règle 100 %-accurate> (learned YYYY-MM)"

CANDIDATES GLOBALES (porte d'eval — aucune écriture au global en séance) :
- "<formulation candidate>" ; fixture avec/sans → claude/evals/claude-md/ ;
  verdict 3 issues

CONFIRMATIONS CROSS-PROJET :
- Mise à jour tag : "[règle]" → "(confirmed across projects)"

ARCHIVAGE (→ tasks/lessons-archive.md) :
- [YYYY-MM-DD] description (+ trace de routage le cas échéant)

CONSERVATION (restent dans l'inbox) :
- [YYYY-MM-DD] description

=== FIN DU PLAN ===
```

Demander confirmation explicite avant de continuer.

### Étape 6 — Exécution

Après confirmation :

1. Relocaliser les fiches `[INSIGHTS]` vers `tasks/insights-actions.md`.
2. Écrire les règles projet promues au CLAUDE.md projet.
3. Mettre à jour les tags cross-projet le cas échéant.
4. Archiver vers `tasks/lessons-archive.md`.
5. Réécrire `tasks/lessons-inbox.md` (en-tête conservé) : leçons conservées
   + candidates globales taguées.
6. Afficher le résumé final avec compteurs.

Les chantiers routés (fix d'artefact, campagne d'eval) ne s'exécutent pas en
séance /immunize — ils sont consignés au plan, à mener séparément.

## Format des règles (100 %-accurate)

Test rédactionnel avant toute écriture : **« quels cas rendraient cette règle
fausse ? »**

- Aucun → la prohibition sèche est autorisée :
  `- Ne jamais [X] — [pourquoi] (learned YYYY-MM)`
- Il en existe → formulation conditionnelle, contexte + pourquoi :
  `- Quand [contexte], [comportement attendu] — [pourquoi] ; [exception légitime] (learned YYYY-MM)`

Tag des candidates globales : `(learned YYYY-MM, from [projet])`.
L'eval de la porte teste la formulation réelle, pas un gabarit.

## Éviction (event-driven)

Aucun audit périodique à vide. Déclencheurs :

- **Changement de tier/modèle par défaut** → rejeu du corpus
  `claude/evals/claude-md/` avec/sans : toute règle que le nouveau modèle
  respecte sans elle est candidate au retrait (sa fixture reste en garde de
  non-régression).
- **Cap global atteint** (20 règles) → campagne d'éviction avant toute
  nouvelle entrée — pas de fusion passe-droit.
- **Suspicion documentée en usage réel** → rejeu ciblé de la fixture de la
  règle suspectée.

## Contraintes

- Ne jamais modifier une règle existante d'un CLAUDE.md (seule exception :
  la mise à jour de tag cross-projet).
- Ne jamais supprimer une entrée sans l'archiver, la relocaliser ou la
  conserver.
- Aucune écriture en `## Global Do NOT` en séance de triage — seule une
  campagne d'eval au verdict « échec tier par défaut » y écrit.
- Maximum 20 règles en `## Global Do NOT` (cap conservé — déclencheur
  d'éviction, pas d'arbitrage de fusion en séance).
- Toujours demander confirmation avant d'écrire (mode triage) ; le mode
  ajout n'écrit que l'append à l'inbox.

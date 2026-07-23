# ADR-0012 : feynman-mentor — 5ᵉ niche de la couche learning (vérification par explication)

Status: Accepted
Date: 2026-07-23
Extends: ADR-0007

## Contexte

La couche learning compte quatre outils à non-overlap strict (`teach`,
`code-mentor`, `coach-pedagogique`, `dp-coach` — cf.
[ADR-0007](0007-teach-emplacement-frontieres.md) et ses satellites 0004-0008),
avec un précédent explicite posé dans la matrice de responsabilité : « tout
futur outil d'apprentissage occupe une niche distincte des quatre, ou est
absorbé — pas de cinquième outil redondant ».

La skill `feynman-mentor` (import claude.ai du 2025-12-29, auditée contre les
best practices Anthropic et shanraisshan le 2026-07-23) candidate à
l'intégration au repo : l'utilisateur explique un concept, Claude joue un
« candide » strict qui signale les trous de l'explication sans reformuler ni
combler. Son entrée dans la couche exige de statuer sur sa niche et son
branchement aux sources de vérité de la couche (état de progression,
rétention).

## Options considérées

- **Option A — Absorber dans un outil existant** (`teach` ou `code-mentor`) :
  pas de nouvel outil à maintenir. Rejetée : le flux est l'*inverse* de `teach`
  (l'utilisateur explique, Claude écoute) et la posture est *opposée* au
  socratique de `code-mentor` (le socratique guide vers la compréhension, le
  candide refuse d'aider — « be confused, not helpful »). L'absorption
  diluerait les deux contrats existants.
- **Option B — 5ᵉ outil autonome hors couche** (session jetable, aucun état
  émis) : intégration minimale. Rejetée : recrée la fragmentation d'état que
  la refonte ADR-0004→0008 a éliminée — un outil d'apprentissage qui n'émet
  rien vers la source d'état unique casse la doctrine de la couche.
- **Option C — 5ᵉ niche intégrée à la couche** : niche distincte, branchée au
  pont d'état, avec garde-fous. Retenue.

## Décision

`feynman-mentor` devient le cinquième outil de la couche learning.

- **Détient** : la *vérification de compréhension par explication* —
  l'utilisateur énonce un concept, Claude-candide signale les trous
  (jargon non défini, sauts logiques, flou, circularité, « pourquoi »
  manquants) sans jamais reformuler ni combler.
- **Ne fait JAMAIS** : enseigner un concept, guider socratiquement, produire
  un artefact, driller par exécution.

Quatre modalités d'intégration tranchées (2026-07-23) :

1. **Pont d'état** : la skill propose un learning-record en fin de session,
   selon la mécanique [ADR-0008](0008-mecanique-pont-record-propose.md)
   (record proposé en bloc copiable, jamais écrit hors CWD).
2. **Invocation** : `disable-model-invocation: false` — auto-invocable via les
   déclencheurs de sa description (pattern `code-mentor`).
3. **Déclencheurs sans collision, calibrés sur la langue d'usage** :
   « teach me… » reste le territoire exclusif de `teach` ; le trigger ambigu
   « teach me by explaining » est supprimé ; les phrases-déclencheurs citées
   sont en français (langue d'interaction réelle — précédent `code-mentor`),
   le corps de la description reste en anglais. La découverte étant un
   matching sémantique, les triggers cités calibrent sans restreindre.
4. **Persona candide structurel** : restriction d'outils dans le frontmatter
   (pas de WebSearch/WebFetch en session) — le candide ne peut pas aller
   combler les trous lui-même ; le garde-fou est structurel, pas seulement
   déclaratif (pattern [ADR-0010](0010-surcharge-code-review-user-scope.md)).

## Conséquences

- La table « Couche learning » de la matrice de responsabilité gagne une
  cinquième ligne (amendement à faire après cet ADR — ordre canonique :
  ADR → document cible → outil → eval).
- `SKILL.md` est adapté avant intégration : frontmatter
  (`disable-model-invocation`, restriction d'outils), description
  (déclencheurs reformulés), section Session End (record ADR-0008), et
  template de feedback structurel (trois volets) rendu dans la **langue de la
  session** — jamais de titres anglais en dur.
- Le corpus d'evals de la skill (Phase 1 de la procédure d'ajout) couvre les
  quatre modalités — en particulier l'invariant « ne comble jamais les
  trous ».
- Trade-off accepté : un cinquième outil à maintenir dans la couche — justifié
  par une niche réelle (retrieval par explication), absente des quatre autres.

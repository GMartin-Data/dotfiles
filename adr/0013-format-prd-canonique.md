# ADR-0013 : Format PRD canonique — canvas fermé de 11 sections

Status: Proposed
Date: 2026-07-28

## Contexte

La matrice de responsabilité prête à `/prd` un « PRD allégé (8 sections) »
(§ Conséquences architecturales) — liste jamais délibérée ni actée par ADR,
et qui porte les indices de cette non-délibération : redondance interne
(Non-goals vs Hors-cible, quasi-synonymes) et tension avec la règle 4
(« Users & scenarios » coexiste avec « Acceptance criteria » alors que la
règle route les stories *dans* les criteria).

Le `/prd` réel produit 14 sections, dont 3 violent les règles de non-overlap :
Stack technique (règle 1 — CLAUDE.md uniquement), Architecture technique
(règle 2 — PLAN.md), Risques & Mitigations (règle 6 — non résolu → Open
questions, tranché → ADR). Il omet par ailleurs Open questions, destination
de la règle 6 et débouché de `/grill` avant gel.

Écart instruit à l'overview §7.3 volet B. Le cœur normatif de la matrice
(les 6 règles de non-overlap) n'est pas en cause ; c'est la liste dérivée
qui n'a jamais été délibérée. Cet ADR est cette délibération.

## Options considérées

- **A — Adopter les 8 strictes** : matrice intacte, audit simple ; mais grave
  les défauts relevés et laisse orphelins des contenus produit légitimes
  (Format de sortie, Gestion des erreurs) qu'aucune règle n'interdit.
- **B — Règles + noyau tolérant** : canon = règles de non-overlap + noyau
  obligatoire, sections additionnelles libres. Flexible, mais l'audit devient
  un jugement au cas par cas — porte ouverte au drift.
- **C — Liste fermée renégociée** (retenue) : conserve l'audit binaire
  (« cette section est-elle légale ? »), corrige les défauts, délibérée
  section par section.

## Décision

Le PRD canonique est un canvas fermé de 11 sections :

1. **Résumé** — problème, solution produit en une phrase, proposition de
   valeur (2-3 §). La section « Solution » disparaît, dissoute ici : son
   « approche en un paragraphe » était la rampe vers le design (domaine PLAN).
2. **Problème** — énoncé détaillé.
3. **Objectifs** — le pourquoi mesurable du produit.
4. **Utilisateurs & scénarios** — persona/échelle + scénarios d'usage
   (interface, déroulé nominal). Les user stories n'existent qu'en
   checkboxes dans Acceptance criteria (règle 4) — jamais en double narratif.
5. **Fonctionnalités (cible)** — contenu de la cible par composant.
6. **Non-goals** — exclusions délibérées avec rationale : *jamais*.
7. **Format de sortie** — *optionnelle* (omise si l'interface est une UI) :
   forme du livrable, exemple à l'appui.
8. **Contraintes** — exigences exogènes, avec test anti-fuite à deux axes :
   la contrainte **nomme une technologie** → CLAUDE.md même imposée (règle 1
   prime), le PRD n'en garde que l'exigence produit qui la motive si elle
   existe indépendamment ; **exigence produit non-technique** (deadline,
   conformité, volumétrie, langue) → PRD.
9. **Acceptance criteria** — contrat vérifiable unique, cible du rituel
   « cocher = état » de Phase 2. Trois sous-parties : scénarios nominaux
   (ex-stories), comportement sur erreur (*conditionnelle*, ex-Gestion des
   erreurs), indicateurs mesurables (ex-Critères de succès).
10. **Open questions** — risques non résolus (règle 6) et débouché `/grill` ;
    remplace « Risques & Mitigations » (un risque tranché part en ADR, la
    mitigation en devient une conséquence — la table de mitigations était
    du design).
11. **Au-delà de la cible** — différé : *pas maintenant*, candidat à une
    future révision de cible par ADR. Distinct de Non-goals (porte fermée
    vs porte entrouverte).

Mouvements structurants : table « Périmètre cible » (✅/❌) supprimée
(duplication interne : ✅ = Fonctionnalités, ❌ = Non-goals) ; contrat
vérifiable unifié ; exclusions scindées par nature.

Le format détaillé (structure, tests de frontière, exemples) vit dans le
satellite `conventions/prd.md` — critère de création atteint (> 30-50 lignes,
évolution indépendante du maître). La matrice est amendée pour pointer vers
lui, comme elle le fait pour `conventions/adr.md`.

## Conséquences

- **Refonte `/prd`** : Phases 8 (Stack) et 10 (Architecture) supprimées ;
  Phase 11 (Risques) devient récolte d'open questions (plus de proposition
  de mitigations) ; le pré-flight Cruft, qui n'existait que pour alléger les
  Phases 8/10, est supprimé ; contrôle de cohérence inter-phases (jointures
  6/11/12) et blocs de validation finale réécrits.
- **Pré-flight `/claude-md` et `instance-aware-flow.md`** mis en cohérence :
  la moisson PRD devient Contraintes (à traduire en conventions),
  Utilisateurs, Objectifs — plus jamais stack ni architecture.
- **Corpus d'evals** couvrant `/prd` et `/claude-md` à rejouer après refonte.
- **Orthogonalité PRD ↔ CLAUDE.md renforcée** : le PRD cesse de squatter
  stack et architecture ; la frontière Contraintes est tenue par le test à
  deux axes ; le flux d'élaboration unidirectionnel (PRD → CLAUDE.md)
  transporte l'exigence vers sa convention sans duplication.
- **Trade-off accepté** : 11 sections au lieu de 8 — coût de longueur assumé
  au profit de la lisibilité (Résumé) et de la valeur spec des projets data
  (Format de sortie).

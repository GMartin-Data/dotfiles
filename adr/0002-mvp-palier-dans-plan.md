# ADR-0002 : MVP = palier de valeur nommé dans le PLAN

Status: Accepted
Date: 2026-06-22
Extends: ADR-0001

## Contexte

[ADR-0001](0001-prd-produit-cible.md) a posé que le PRD décrit le produit
**cible**, et a explicitement renvoyé le découpage en MVP à un ADR distinct
(« séquençage de la cible → /planning, le PRD n'y touche pas »).

Reste la question qu'ADR-0001 a laissée ouverte : **où vivent les MVP
successifs ?** Un MVP est un livrable intermédiaire ayant une valeur utilisateur
propre — pas une simple brique technique. Or la matrice de responsabilité ne
nomme que deux granularités côté PLAN : « phases » et « milestones », qui
relèvent du **séquençage technique**, pas du **palier de valeur produit**.

Sans décision explicite, le risque est de combler ce trou par conflation
silencieuse (« un MVP, c'est juste un milestone »), reproduisant exactement le
type d'ambiguïté qu'ADR-0001 a coûté cher à lever sur les mots « frozen » et
« v1 ».

## Options considérées

- **Option A — MVP = milestone du PLAN** : un MVP est un milestone, pas de
  nouvel artefact.
  *Pour* : YAGNI maximal, zéro structure nouvelle.
  *Contre* : conflation de deux granularités (jalon technique ≠ livrable à
  valeur). Recrée l'ambiguïté qu'on vient de tuer côté PRD.

- **Option B — un PLAN.md par itération** (`PLAN-mvp1`, `PLAN-mvp2`…) : PRD=cible
  unique, N PLAN.
  *Pour* : séparation nette vision (1 PRD) / exécution itérative (N PLAN) ;
  scale sur un vrai produit multi-incréments.
  *Contre* : lourd, multiplie les fichiers semi-frozen et les ADR de révision ;
  sur-ingénierie pour un repo solo. Viole Simplicity First tant qu'aucun projet
  réel ne l'exige.

- **Option C — PLAN unique, MVP = couche explicite dans le PLAN (retenue)** :
  un seul PLAN, mais vocabulaire désambiguïsé — « phase » = brique technique,
  « MVP/palier » = livrable à valeur regroupant des phases.
  *Pour* : résout la conflation de A sans la lourdeur de B ; porte de sortie
  documentée vers B si un projet l'exige.
  *Contre* : discipline rédactionnelle requise pour ne pas re-confondre les deux
  niveaux.

## Décision

**Modèle C.** Le PLAN reste un fichier unique. On y nomme **deux niveaux
distincts** :

- **« phase »** — brique de séquençage technique (ce qu'elle est déjà
  aujourd'hui).
- **« MVP » / « palier de valeur »** — livrable à valeur utilisateur propre,
  regroupant une ou plusieurs phases.

Ce modèle désambiguïse la granularité sans payer la machinerie multi-PLAN du
modèle B. Il est l'équilibre adapté à l'échelle actuelle (projets solo,
mono-livrable le plus souvent), tout en laissant une **porte de sortie vers B** :
si un projet réel sue sous un PLAN unique, un futur ADR pourra superséder
celui-ci pour adopter le multi-PLAN. *Build before automating* — on n'instancie
pas la structure avant le besoin.

A est rejeté car la conflation milestone/MVP est précisément l'ambiguïté
qu'ADR-0001 a appris à fuir. B est rejeté car aucun projet actuel ne le justifie.

## Conséquences

- **Matrice de responsabilité** : ajouter la frontière MVP **positive** — la
  ligne PLAN porte désormais explicitement le palier MVP, et une sous-section
  « où vivent les MVP » formalise la frontière PRD (cible) ↔ PLAN (découpage en
  paliers). Comble le trou laissé ouvert depuis ADR-0001.
- **`planning.md`** : le template PLAN gagnera à distinguer « phase » et « palier
  MVP » (amendement séparé, hors scope de cet ADR).
- **YAGNI assumé** : ni la conflation de A, ni la sur-structure de B.
- **Trade-off accepté** : discipline rédactionnelle requise dans le PLAN pour
  tenir les deux niveaux distincts. Si cette discipline échoue en pratique, c'est
  le signal qu'un projet a dépassé le modèle C → déclencheur d'un ADR vers B.

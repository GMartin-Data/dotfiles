# ADR-0001 : Le PRD décrit le produit cible, frozen comme baseline révisable

Status: Accepted
Date: 2026-06-22

## Contexte

Le PRD était implicitement assimilé à la v1/MVP : ce que le document décrivait,
c'était le premier incrément livrable. Cette assimilation ne colle pas au réel
du travail produit. Le client exprime un **besoin-cible** ; le PRD l'interprète
et le formalise ; les MVP raisonnables se planifient *ensuite*, comme des
itérations vers cette cible.

Deux forces en tension rendent la décision nécessaire :

- **L'ambiguïté du mot « frozen »**. Il peut signifier soit *immuable* (on n'y
  touche plus jamais, sens fort des ADR), soit *baseline* (référence stable et
  datée qui ne dérive pas au fil de l'eau, mais reste révisable explicitement).
  Tant que le sens n'est pas tranché, le statut du PRD reste flou.

- **La réalité des inflexions client**. Un PRD qui décrirait la cible et qu'on
  interdirait de toucher serait faux dès la première inflexion. Mais un PRD qui
  bouge à chaque réunion perd sa fonction de référence partagée.

## Options considérées

- **Option A — PRD = v1 figé (statu quo)** : le PRD décrit le premier incrément.
  Avantage : simple, le « frozen » au sens immuable s'applique sans ambiguïté.
  Inconvénient : ne reflète pas le travail réel (besoin-cible → interprétation →
  MVP planifiés) ; force à recréer un PRD à chaque itération.

- **Option B — PRD = cible immuable** : le PRD décrit la cible et n'est jamais
  modifié. Avantage : traçabilité maximale. Inconvénient : faux dès la première
  inflexion client ; oblige soit à mentir (PRD périmé ignoré), soit à charger
  /planning d'une vision qu'il n'a pas vocation à porter.

- **Option C — PRD = cible, frozen comme baseline révisable par ADR (retenue)** :
  le PRD décrit la cible ; « frozen » signifie baseline versionnée (pas de dérive
  silencieuse), révisable par la porte d'entrée ADR quand la cible change.

## Décision

**Le PRD décrit le produit CIBLE**, pas la v1/MVP. Le découpage en itérations
relève de `/planning`.

**« Frozen » = baseline versionnée**, pas immuabilité absolue. Le PRD ne dérive
pas par édition silencieuse au fil de l'eau ; il est figé tant que la cible ne
change pas. Une **inflexion réelle** (le client repositionne le besoin) déclenche
un **ADR** actant le changement de cible, *puis* un amendement contrôlé du PRD —
l'ordre canonique de replanning (ADR d'abord, document cible ensuite).

Distinction clé que ce statut protège :

- **Changement de cible** → ADR + amendement du PRD.
- **Séquençage de la cible en itérations** → `/planning`, le PRD n'y touche pas.

Autrement dit : le PRD n'est pas gelé contre le *changement*, il est gelé contre
la *dérive non-tracée*. L'inflexion client est légitime — elle passe par la porte
d'entrée (ADR), pas par la fenêtre (édition au fil de l'eau).

L'option C est retenue car elle est la seule cohérente avec les trois niveaux de
stabilité déjà en place : ADR immuable, PRD baseline révisable-par-ADR,
/planning mutable.

## Conséquences

- `prd.md` est à amender (~10 occurrences « v1 » → « cible ») pour refléter ce
  statut.
- La matrice de responsabilité documentaire doit combler le trou v1→v2 et
  formaliser la frontière **PRD (cible) ↔ /planning (découpage)** — c'est le foyer
  documentaire du « où/quand/comment » des MVP successifs (hors scope de cet ADR).
- Une inflexion client devient une **porte d'entrée ADR**, jamais une édition
  silencieuse du PRD.
- Trade-off accepté : un PRD mature peut accumuler des ADR de révision de cible.
  C'est attendu et souhaitable — la chaîne d'ADR reconstitue l'évolution de la
  vision.
- Le mécanisme de découpage MVP lui-même (un PLAN.md par itération ? un PLAN
  évolutif ?), s'il s'avère non-trivial, fera l'objet d'un **ADR distinct** —
  hors scope ici (atomicité).

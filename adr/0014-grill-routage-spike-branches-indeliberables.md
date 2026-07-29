# ADR-0014 : Routage SPIKE — `/grill` route les branches indélibérables vers une observation

Status: Accepted
Date: 2026-07-29
Extends: ADR-0003

## Contexte

La condition d'arrêt de `/grill` exige un ledger final avec **zéro branche
`OPEN`** : chaque branche est conduite à `RESOLVED` ou `DEFERRED`. Or certaines
branches sont **indélibérables en séance** : aucun argument ne peut les
trancher, seule une **observation** le peut (comportement réel d'un modèle sur
une tâche, performance mesurable, faisabilité d'une API). Le grill n'a
aujourd'hui aucun chemin de sortie structuré pour ces branches — elles finissent
en `DEFERRED` générique, sans protocole pour produire l'observation manquante.

Cet angle mort a été identifié à l'analyse du transcript Pocock (« prototype
skill », fidélité des discussions de design). Verdict de cette analyse, acté en
séance du 2026-07-28 : **adopter le routage** (escalade de fidélité vers
l'expérimentation quand la délibération ne peut pas trancher), **rejeter le
blanchiment** (copy-paste du code de prototype vers la prod, qui contournerait
test-first et la matrice de responsabilité).

[ADR-0003](0003-grill-delegue-adr-sans-invoquer.md) fixe la mécanique de sortie
de `/grill` : liste « Decisions to formalize » taguée (`ADR` /
`PRD open-question`), items autoportants, ordre topologique, délégation par
instruction — `/grill` n'écrit rien et ne pilote aucune autre command. Le
routage SPIKE étend ce vocabulaire et cette délégation sans les contredire.

## Options considérées

Cinq axes, tranchés un par un en interview :

- **Critère d'éligibilité** : « un argument peut-il trancher, ou seulement une
  observation ? » (retenu — binaire, applicable en séance) ; vs heuristique
  incertitude × coût (deux axes à estimer, critère flou) ; vs ad hoc sans
  critère écrit (l'angle mort persiste).
- **Sortie dans /grill** : 3ᵉ tag `SPIKE` (retenu — symétrique du mécanisme
  existant) ; vs sous-type d'item `ADR` (brouille la sémantique : un item ADR
  est une décision tranchée, un spike est une décision qu'on ne peut pas
  trancher) ; vs mention en prose hors liste (viole l'invariant du bloc
  copiable).
- **Ledger** : `DEFERRED (→ spike [N])` (retenu — la branche est réellement
  différée, en attente d'un input externe) ; vs 4ᵉ état `ROUTED` (concept
  nouveau pour une distinction que la raison entre parenthèses porte déjà).
- **Exécution** : manuelle sur branche jetable `spike/*` (retenu — build before
  automating) ; vs command `/spike` dédiée (automatisation prématurée d'un flux
  jamais exécuté, anti-pattern ADR-0009) ; vs observation en cours de session
  grill (viole la frontière ADR-0003 : `/grill` n'explore pas de codebase).
- **Capture** : `/adr --from-context` puis suppression de la branche sans merge
  (retenu) ; vs conservation du code comme point de départ (le blanchiment
  rejeté) ; vs note libre sans ADR (perd le rationale audité).

## Décision

`/grill` applique aux branches qui résistent à la délibération le critère :
**« un argument peut-il trancher, ou seulement une observation ? »** Si seule
une observation peut trancher :

1. L'item sort dans la liste « Decisions to formalize » avec le tag **`SPIKE`**
   (3ᵉ tag, à côté de `ADR` et `PRD open-question`). L'item est autoportant :
   la **question** à observer, le **protocole minimal** d'observation, le
   **critère de sortie** (qu'est-ce qui compte comme réponse).
2. La branche est marquée **`DEFERRED (→ spike [N])`** dans le ledger — aucun
   état nouveau, la condition d'arrêt « zéro branche `OPEN` » est inchangée.
3. L'humain exécute le spike **manuellement sur une branche jetable
   `spike/*`** — session libre, sans command dédiée.
4. Le résultat est capturé via **`/adr --from-context`** (la délibération a eu
   lieu dans le fil du spike), puis **la branche est supprimée sans merge**.

**Le livrable d'un spike est une décision, jamais du code.** L'implémentation
repart test-first sur main, l'ADR de capture en main.

## Conséquences

- La machine à états du ledger et la condition d'arrêt de `/grill` restent
  inchangées — le routage n'ajoute qu'un tag de sortie et une raison de
  `DEFERRED`.
- La doctrine ADR-0003 s'étend au spike : délégation par instruction (l'humain
  exécute, la command n'écrit rien et ne pilote rien), items autoportants
  collables.
- Garde-fou anti-blanchiment explicite : la mort de la branche sans merge est
  la règle, pas une option — le code exploratoire sans test ne devient jamais
  du code de prod.
- Build before automating : une command `/spike` reste possible si l'usage
  manuel révèle un besoin récurrent de cadrage — au premier signal, pas avant.
- Trade-off accepté : friction manuelle (créer la branche, mener l'observation,
  lancer `/adr`, supprimer la branche) — cohérente avec le précédent du rituel
  `/code-review` (pas d'automatisation tant que l'oubli n'est pas récurrent).

# ADR-0003 : `/grill` délègue à `/adr` par instruction, sans l'invoquer

Status: Accepted
Date: 2026-06-23

## Contexte

La slash-command `/grill` (revue adverse pré-gel d'un PRD ou PLAN) termine sa
session par une liste « Decisions to formalize ». Certains items y sont taggés
`ADR` : ce sont des décisions de design non-triviales que l'utilisateur devra
formaliser via `/adr`.

Se pose la question du *mécanisme* de cette délégation : `/grill` peut-il
déclencher `/adr` lui-même, ou doit-il se contenter d'instruire l'utilisateur de
le lancer ?

Le cas fréquent est **N décisions à formaliser**, pas une seule. Or `/adr`
produit **un** ADR atomique par invocation (cf.
[`conventions/adr.md`](../docs/methodology/conventions/adr.md), numérotation
`max+1` dérivée à chaque appel) — il n'a pas de mode batch. N décisions `ADR`
impliquent donc N invocations séquentielles de `/adr`. Et comme `/grill`
construit déjà l'arbre de dépendances des décisions, ces N décisions peuvent
avoir des dépendances entre elles (B ne tient que si A a été tranchée d'une
certaine façon) : l'ordre de création n'est pas neutre.

Contrainte technique dirimante : une slash-command Claude Code est un **prompt
injecté**, pas un programme. Elle n'a aucun moyen d'invoquer programmatiquement
une autre slash-command — il n'existe pas d'API « lance `/adr` maintenant ». Toute
« invocation » ne pourrait être qu'une instruction en langage naturel que le
modèle choisit ou non de suivre, sans garantie ni atomicité.

S'ajoute une contrainte de gouvernance documentaire (cf.
[`responsibility-matrix`](../docs/methodology/responsibility-matrix.md)) : `/grill`
ne produit aucun artefact et ne touche aucun fichier. Son rôle s'arrête à produire
du matériau. Créer un ADR est une opération d'écriture qui appartient à `/adr`
seul, avec sa propre validation humaine avant écriture.

## Options considérées

- **Option A — Instruction au user (retenue)** : `/grill` termine en listant les
  décisions taggées `ADR` et en instruisant l'utilisateur de lancer `/adr` pour
  chacune. Aucune tentative d'auto-déclenchement.
  - Avantage : aligné sur la contrainte technique (pas d'invocation réelle
    possible) et sur la frontière documentaire (`/grill` ne produit pas
    d'artefact). Chaque ADR garde sa validation humaine propre via `/adr`.
  - Inconvénient : une étape manuelle de plus pour l'utilisateur.

- **Option B — Auto-déclenchement par chaînage de prompt** : `/grill` émet en fin
  de session une instruction « j'enchaîne sur `/adr` » et tente de dérouler la
  création d'ADR dans la foulée.
  - Avantage : moins de friction apparente.
  - Inconvénient : techniquement bancal (pas d'invocation réelle — le modèle
    rejouerait le corps de `/adr` de mémoire, sans garantie de fidélité à la
    command source) ; viole la frontière documentaire (`/grill` se mettrait à
    produire des artefacts) ; court-circuite la validation humaine propre à
    `/adr` ; la numérotation déterministe d'`/adr` ne serait pas garantie.

## Décision

Option A. `/grill` **délègue par instruction** : il produit la liste de décisions
à formaliser et instruit explicitement l'utilisateur de lancer `/adr` (pour les
items taggés `ADR`) ou de plier l'open-question dans le PRD (pour les items taggés
`PRD open-question`). `/grill` n'invoque jamais une autre command et n'écrit jamais
de fichier.

Cette décision pose la règle générale pour la famille de commands méthodologiques :
**une slash-command ne pilote pas une autre** ; le chaînage reste un acte humain.

Pour le cas N décisions, la liste de sortie est structurée pour rendre les N
invocations manuelles de `/adr` sûres et ordonnées :

1. **Cardinalité** : un item `ADR` = une invocation de `/adr`. La liste ne tente
   aucun batch.
2. **Ordre topologique** : les items `ADR` sont ordonnés selon l'arbre de
   dépendances que `/grill` a construit — parents avant enfants. L'utilisateur
   lance `/adr` de haut en bas ; un ADR enfant trouve ainsi déjà créé l'ADR parent
   qu'il devra référencer.
3. **Relations suggérées** : pour un item dépendant d'un autre, `/grill` suggère la
   relation candidate du vocabulaire de la convention (`Refines` / `Extends` /
   `Constrains`) que l'utilisateur déclarera dans `/adr`. `/grill` propose le lien,
   il ne le crée pas.
4. **Items autoportants** : chaque session `/adr` est vierge, sans mémoire du
   grill. Chaque item de la liste résume donc son contexte / options / décision,
   pour être collable tel quel dans `/adr` sans rouvrir le grill.

**Persistance de la liste** : `/grill` n'écrit aucun fichier, pas même un scratch.
La liste est imprimée dans un **bloc unique copiable** ; sa persistance hors
session relève du dev (qui copie le bloc). Pour que cette étape ne soit pas
manquée, le bloc est suivi d'une **invite visible et isolée** (titre/séparateur
dédié, jamais une parenthèse) demandant explicitement au dev de copier la sortie
avant de poursuivre. Ce choix écarte le fichier scratch versionné, qui
deviendrait un artefact zombie périmé dès le premier `/adr` créé — une source de
drift que la matrice de responsabilité combat.

## Conséquences

- `/grill` reste un producteur de matériau pur, sans effet de bord sur le système
  de fichiers — cohérent avec la matrice de responsabilité.
- L'utilisateur exécute lui-même `/adr`, qui conserve sa validation avant écriture
  et sa numérotation déterministe intactes.
- Trade-off accepté : N étapes manuelles pour N décisions à formaliser. Jugé
  acceptable — l'explicite prime sur l'automatisation fragile, et l'ordre
  topologique + les relations suggérées retirent la charge cognitive du séquençage
  à l'utilisateur.
- La liste de sortie de `/grill` n'est pas un vrac : elle est ordonnée et annotée
  de relations. C'est une contrainte sur le format d'output de la command, pas
  seulement sur son comportement.
- Précédent posé pour les futures commands : pas d'auto-invocation inter-command
  tant que le harness ne fournit pas de mécanisme natif et fiable.

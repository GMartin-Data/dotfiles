# ADR-0011 : Track léger documentaire pour les petits projets personnels

Status: Accepted
Date: 2026-06-25

## Contexte

Le workflow documentaire complet — PRD (allégé) + PLAN + ADR + CLAUDE.md +
progress.md, régi par la [matrice de responsabilité](../docs/methodology/responsibility-matrix.md) —
a été conçu pour des projets à enjeu : durables, potentiellement collaboratifs,
ou soumis à auditabilité (contexte banking/credit). La discipline ADR (corps
immuable, supersession bidirectionnelle, numérotation séquentielle) y est un
avantage différenciant.

Appliqué tel quel à un petit outil personnel, ce workflow s'inverse : sur
`memgrep` (CLI perso de grep sur la mémoire Claude Code), le code pèse ~280 lignes
quand la gouvernance documentaire en pèse ~500 — un ratio doc/code de 1,8:1.
Produire un PLAN.md et 6-8 ADR rétroactifs sur des décisions déjà gelées et
implémentées serait de l'archéologie documentaire sans valeur prospective.

Cette sur-documentation contredit frontalement le **principe d'émergence** que la
matrice pose elle-même en clôture : *« un satellite naît quand le besoin réel
apparaît, pas par anticipation. Build before automating appliqué à la doc. »*
Il manquait une règle explicite disant *quand* le workflow complet ne s'applique
pas — sans quoi chaque petit projet hérite par défaut d'un appareil disproportionné.

## Options considérées

- **Option A — Workflow complet pour tous les projets** : uniformité, aucune
  décision de classement à prendre.
  - Inconvénient : ratio doc/code absurde sur les petits outils, ADR rétroactifs
    sans valeur, friction qui décourage le démarrage de projets jetables. Contredit
    le principe d'émergence.

- **Option B — Seuil quantitatif (LOC)** : exempter en-deçà de N lignes de code.
  - Inconvénient : seuil arbitraire et *gameable* ; un projet de 200 lignes
    distribué publiquement à des collaborateurs mérite la gouvernance complète,
    quand un script perso de 2000 lignes ne la mérite pas. Le LOC mesure la mauvaise
    chose.

- **Option C — Critères qualitatifs en conjonction (retenue)** : exemption si
  toutes les conditions de profil « outil personnel jetable » sont réunies.
  - Avantage : mesure l'enjeu réel (collaboration, distribution, durée de vie), pas
    le volume. Robuste, non *gameable*, aligné sur ce qui justifie vraiment la
    discipline ADR (auditabilité, raisonnement partagé).

## Décision

Option C. Un projet est en **track léger** — exempté de `PLAN.md` et d'ADR — si et
seulement si **toutes** les conditions suivantes sont réunies :

1. **Mono-utilisateur** — un seul humain l'utilise (l'auteur).
2. **Pas de collaborateurs** — aucune revue tierce, aucune contribution externe
   attendue.
3. **Pas de distribution publique** — pas de PyPI / npm / registry ; installation
   locale depuis le repo uniquement.
4. **Durée de vie non-critique** — outillage personnel ; une perte ou un revirement
   de décision n'a pas de conséquence d'audit ni de coût de coordination.

Un projet en track léger vit sur **CLAUDE.md + progress.md**. Le `PRD.md` y est
**optionnel** ; s'il existe, il peut être gelé tel quel comme artefact historique
plutôt que conformé à la doctrine PRD-allégé. Les décisions durables sont consignées
dans la section « Décisions prises » de `progress.md`, **pas en ADR**.

Le classement est **réversible** : si une seule condition tombe (le projet devient
collaboratif, est publié, gagne un enjeu d'audit), il bascule vers le workflow
complet. Cette bascule est elle-même une décision non-triviale → elle se documente
par un ADR dans le projet concerné, qui amorce alors sa propre série d'ADR.

L'application du track léger à un projet donné se déclare dans le **CLAUDE.md de ce
projet** (déviation projet-spécifique, conformément à la matrice : *« les déviations
projet-spécifiques appartiennent au CLAUDE.md du projet »*), en renvoyant au présent
ADR pour la règle.

## Conséquences

- La règle générale (track léger) vit ici, dans un seul ADR réutilisable ; son
  application vit dans le CLAUDE.md de chaque projet exempté. Aucun overlap : l'ADR
  détient le *critère*, le CLAUDE.md détient le *fait d'y être soumis*.
- La matrice de responsabilité gagne un renvoi une-ligne vers cet ADR (découvrabilité
  depuis la pierre fondatrice), sans absorber la règle — la pierre fondatrice n'est
  pas modifiée pour une exception conditionnelle.
- `memgrep` est le premier projet classé en track léger ; son `PRD.md` reste gelé tel
  quel (contient stack/phases/risques, non conformes à la doctrine actuelle) avec une
  note d'en-tête historique, et ne reçoit ni PLAN.md ni ADR.
- Trade-off accepté : un projet en track léger qui grossirait au point de mériter la
  gouvernance complète ne le signale par aucun seuil automatique — c'est un jugement
  humain au cas par cas. Assumé : le LOC ne mesurant pas l'enjeu, aucun seuil
  automatique n'aurait été fiable de toute façon.
- Applique le principe d'émergence de la matrice à l'échelle du projet, pas seulement
  du satellite documentaire : la gouvernance lourde naît quand l'enjeu réel apparaît,
  pas par défaut.

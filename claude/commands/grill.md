---
description: Revue adverse d'un PRD ou PLAN déjà rédigé, avant gel — fait émerger les décisions implicites et les tensions inter-sections en parcourant l'arbre de dépendances des décisions. Ne produit ni ne modifie aucun artefact.
argument-hint: [chemin/vers/prd.md|plan.md]
allowed-tools: Read, Glob
model: opus
---

# Grill — revue adverse pré-gel d'un PRD ou PLAN

Command invoquée explicitement par l'humain sur un artefact qui **existe déjà** et
paraît fini. Le but n'est PAS de produire l'artefact (les interviews `/prd` et
`/planning` le font) — c'est de le stress-tester en parcourant l'arbre réel de
dépendances de ses décisions, pour faire surgir les décisions prises implicitement
et les contradictions latentes entre sections qu'une relecture linéaire ne voit pas.

Cette command **ne modifie jamais** l'artefact source et **n'écrit aucun fichier**
(cf. [`adr/0003`](../../adr/0003-grill-delegue-adr-sans-invoquer.md)). Elle produit
une liste de décisions candidates que l'humain formalisera ensuite (résolutions
d'open-questions dans le PRD, ou ADRs via `/adr`).

**Argument** : `$ARGUMENTS` (optionnel) = chemin explicite vers l'artefact à griller.
Sans argument, résolution par fallback (voir ci-dessous). Une invocation grille **un
seul** artefact — un PRD **ou** un PLAN, jamais les deux ; le type est déduit du
fichier résolu.

---

## Scope

- **IN** : un `prd.md` ou `plan.md` écrit, dont les sections sont individuellement
  cohérentes mais dont la cohérence inter-sections n'a pas été vérifiée de façon
  adverse.
- **OUT** : produire un PRD/PLAN de zéro (utiliser les interviews) ; auditer un
  raisonnement abstrait sans artefact ; re-litiger un artefact déjà gelé pendant
  l'implémentation ; replanifier après un drift observé.

---

## Résolution de l'entrée

1. **Si `$ARGUMENTS` contient un chemin**, lire ce fichier. L'argument explicite est
   **prioritaire** sur tout fallback.
2. **Sinon**, chercher dans le projet, dans cet ordre strict : `prd.md`, puis
   `plan.md`. Pour chacun, regarder la **racine du projet** puis un sous-dossier
   `docs/`. Le **premier trouvé gagne** (un `prd.md` à la racine l'emporte sur un
   `plan.md` ou un `docs/prd.md`).
3. **Si rien n'est trouvé**, s'arrêter et demander le chemin à l'humain. Ne jamais
   inventer de contenu. **Ne jamais griller sans artefact source.**

**Identifier le type** (PRD vs PLAN) à partir de la structure du fichier résolu —
ce type sélectionne la condition d'arrêt ci-dessous. Pas de flag `--prd`/`--plan` :
le type se déduit du fichier, jamais d'un argument redondant.

---

## Procédure

1. **Lire l'intégralité de l'artefact** avant de poser quoi que ce soit.

2. **Construire l'arbre de décisions, silencieusement.** Lister, pour soi :
   - chaque décision **explicite** que l'artefact énonce ;
   - chaque décision **implicite** qu'il suppose sans l'énoncer (ce sont les cibles
     à plus forte valeur) ;
   - les **dépendances** entre elles (la décision B ne tient que si A a été tranchée
     d'une certaine façon). Cet arbre servira aussi à ordonner la sortie finale.

3. **Maintenir un ledger de branches visible**, chacune marquée `OPEN`, `RESOLVED`
   ou `DEFERRED`. L'afficher au démarrage et le **rafraîchir après chaque question
   résolue**, pour que l'humain voie toujours combien il reste.

4. **Griller une question à la fois. Jamais en lot.** Pour chaque question :
   - énoncer quelle branche / quelle tension elle vise ;
   - donner **sa propre réponse recommandée** avec un rationale d'une ligne — on
     prend position, l'humain valide ou réfute ; c'est une délibération, pas un
     interrogatoire ;
   - **prioriser les tensions inter-sections** (une Contrainte qui contredit un
     critère d'acceptation ; un choix d'architecture du PLAN qui viole une
     convention CLAUDE.md) sur les ambiguïtés locales ;
   - **NE PAS explorer une codebase** pour répondre à ses propres questions. Cette
     command opère sur l'artefact et l'intention de l'humain, pas sur l'état
     d'implémentation.

5. **Quand une question résout une branche**, la marquer `RESOLVED` et consigner la
   décision qui l'a close.

---

## Condition d'arrêt (déterministe — ne jamais s'arrêter sur « compréhension partagée »)

- **Pour un PRD** : s'arrêter quand chaque item de la section « Open questions » de
  l'artefact a été conduit à une décision tranchée, ET que chaque tension
  inter-sections soulevée est marquée `RESOLVED`.
- **Pour un PLAN** : s'arrêter quand chaque décision d'architecture du plan a été
  confrontée à au moins une alternative et ses dépendances résolues, ET que chaque
  tension inter-sections est marquée `RESOLVED`.

Si une branche ne peut **réellement pas** être résolue maintenant (input externe
manquant), la marquer `DEFERRED` avec la raison plutôt que de la laisser `OPEN` — le
ledger doit se terminer avec **zéro branche OPEN**.

> Garde-fou anti-trivialité : l'absence de section « Open questions » (ou une section
> vide) ne satisfait PAS la condition d'arrêt. Les tensions inter-sections doivent
> être grillées dans tous les cas — c'est le cœur de la revue.

---

## Output — liste « Decisions to formalize »

Terminer la session par une **liste unique**. Chaque décision porte un tag, l'un de :

- **`PRD open-question`** — résout une open-question ; l'humain la plie dans le PRD
  avant gel.
- **`ADR`** — un choix d'architecture/design non-trivial avec rationale ; l'humain
  lance `/adr` pour le formaliser. Cette command **n'écrit pas** l'ADR — elle
  produit le matériau pour `/adr`.

**Structure de la liste** (cf. [`adr/0003`](../../adr/0003-grill-delegue-adr-sans-invoquer.md)) :

1. **Ordre topologique** : ordonner les items `ADR` selon l'arbre de dépendances —
   **parents avant enfants**. L'humain lancera `/adr` de haut en bas ; un ADR enfant
   trouvera ainsi déjà créé l'ADR parent qu'il doit référencer.
2. **Relations suggérées** : pour un item qui dépend d'un autre, suggérer la relation
   candidate du vocabulaire de la convention ADR (`Refines` / `Extends` /
   `Constrains`) que l'humain déclarera dans `/adr`. Proposer le lien, ne pas le créer.
3. **Items autoportants** : chaque session `/adr` est vierge, sans mémoire de ce
   grill. Résumer dans chaque item `ADR` son contexte / options / décision, pour
   qu'il soit collable tel quel dans `/adr` sans rouvrir le grill.

Format de chaque item :

```
[N] (TAG) Titre court de la décision
    Décision : ce qui a été tranché, en une phrase.
    Contexte : la tension ou la branche qui l'a fait émerger (1-2 lignes).
    Options  : les alternatives pesées (pour un item ADR).
    Relation : Refines/Extends/Constrains l'item [M] — si dépendance. Sinon : aucune.
```

**Invariants de l'output** :
- **N'éditer aucun fichier. Ne créer aucun ADR.** Remettre la liste à l'humain comme
  unique artefact de la session.
- Imprimer la liste dans **un seul bloc copiable** — sa persistance hors session
  relève de l'humain.

---

## Invite finale — étape opérationnelle, à promouvoir visiblement

Après le bloc copiable, afficher une invite **isolée et visible** (séparateur dédié,
jamais une parenthèse en fin de phrase) :

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  COPIE CETTE LISTE MAINTENANT.

Cette command n'écrit aucun fichier : la liste ci-dessus ne survivra
pas à un /clear ni à une reprise de session. Copie-la avant de
poursuivre.

Ensuite, formalise les items dans l'ordre (de haut en bas) :
  • items (ADR)             → lance /adr, colle l'item, déclare la
                              relation suggérée si présente
  • items (PRD open-question) → plie la résolution dans le PRD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

L'ordre topologique de la liste garantit qu'en lançant `/adr` de haut en bas, chaque
ADR enfant trouve son parent déjà créé et numéroté.

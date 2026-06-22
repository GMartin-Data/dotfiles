---
description: Génère PLAN.md (architecture cible + découpage en phases) à partir de PRD.md et CLAUDE.md, après validation légère du découpage
argument-hint: [output-filename]
allowed-tools: Read, Write, Glob
model: opus
---

# Planning

Produit le `PLAN.md` d'un projet : la **photo finale** de l'architecture cible
et le **découpage ordonné** de la cible en **deux granularités** (cf. ADR-0002) —
des **paliers MVP** (livrables à valeur utilisateur) regroupant des **phases**
(briques de séquençage technique). Dérivé de `PRD.md` (le *quoi/pourquoi*, la
cible) et `CLAUDE.md` (la *stack/conventions*).

**Fichier de sortie** : `$ARGUMENTS` (défaut : `PLAN.md`).

**Frontière de responsabilité** : l'idéation (problème, US, scope, stack) est
déjà figée dans PRD + CLAUDE.md par l'humain. Ce processus ne ré-idée rien — il
*dérive* un plan d'exécution et fait valider le découpage. Ne jamais rouvrir le
*quoi* ni le *pourquoi* ici.

---

## Vérification préalable — mode strict

**Avant toute chose**, vérifier si le fichier de sortie existe déjà.

Si le fichier existe :

```
Le fichier {output-filename} existe déjà.

Un PLAN est semi-frozen : toute révision passe par un ADR justificatif
AVANT modification (Phase 3 du workflow). Le régénérer écraserait cette
traçabilité.

Si la réalité a divergé du PLAN, n'utilise pas cette commande : écris
d'abord un ADR documentant le pourquoi du changement, puis amende PLAN.md
en conséquence.

Commande annulée.
```

Puis s'arrêter. Ne pas régénérer.

---

## Pré-flight — lecture des sources

**Avant toute interaction**, lire les deux documents source :

1. **PRD.md** — en extraire : problème, user stories, périmètre cible, format de
   sortie (si présent), architecture technique (si présente), critères de succès.
2. **CLAUDE.md** — en extraire : stack, conventions, contraintes transverses.

Si **PRD.md est absent** : s'arrêter et signaler.

```
PRD.md introuvable. Le PLAN se dérive du PRD — produis-le d'abord via /prd.

Commande annulée.
```

Si **CLAUDE.md est absent** : avertir mais continuer (le PLAN peut se produire
sans, avec une note explicite).

```
CLAUDE.md introuvable. Je peux produire le PLAN à partir du seul PRD,
mais l'architecture haut niveau ne pourra pas référencer la stack.
Recommandé : produire CLAUDE.md via /claude-md d'abord.

Continuer quand même ? (oui / annuler)
```

---

<!-- Source de vérité : ~/dotfiles/docs/methodology/responsibility-matrix.md
     (ligne PLAN.md, colonnes "Contenu unique" et "Ne contient JAMAIS").
     Règles dupliquées ici volontairement, pour l'autonomie de la command.
     Si la matrice change, synchroniser ce bloc à la main.
     Dédupliquer (déléguer la lecture à la matrice) quand /adr partagera
     ces règles → 2+ occurrences = rentabilité de la déduplication. -->

## Règles de génération — périmètre strict de PLAN.md

Ces règles sont **non-négociables**. Elles dérivent de la matrice de
responsabilité documentaire.

PLAN.md **contient uniquement** :
- Architecture haut niveau (les composants et leurs interactions — **quoi**, pas pourquoi)
- **Paliers MVP** (livrables à valeur utilisateur, jalons démontrables regroupant des phases — cf. ADR-0002)
- Découpage en **phases** (briques de séquençage technique, indépendamment valorisables)
- Séquence d'exécution (ordre, dépendances, parallélisations)

PLAN.md **ne contient JAMAIS** :
- **Décision atomique justifiée** (pourquoi choix A plutôt que B) → va en ADR.
  *PLAN dit « on utilise une file async » ; ADR dit « pourquoi Pub/Sub vs Cloud Tasks ».*
- **Stack technique** (langages, libs, versions) → est dans CLAUDE.md.
- **Conventions de code** → sont dans CLAUDE.md.
- **État de session** (où j'en suis, blockers) → va dans progress.md.

**Test inline pendant la rédaction de l'architecture** : si une phrase commence
à justifier *pourquoi* un choix technique plutôt qu'un autre, STOP — ce contenu
est un ADR, pas du PLAN. Écrire le *quoi* (« file d'attente async »), pas le
*pourquoi* (« car Pub/Sub offre... »).

---

## Interview légère — validation du découpage uniquement

Après lecture des sources, proposer un découpage **dérivé** du PRD, puis le faire
valider en **3 questions maximum**. Ne poser que des questions de *découpage et
de séquence*. Ne jamais poser de question d'idéation (problème, US, scope, stack
— tout cela est déjà figé).

Règles d'interaction :
1. **Une question à la fois.**
2. **Proposer, ne pas demander à l'aveugle.** Toujours pré-proposer un découpage
   dérivé du PRD, l'humain valide ou corrige. Ne jamais ouvrir par une page
   blanche (« comment veux-tu découper ? »).
3. **Plafond strict : 3 questions.** Si le découpage est évident depuis le PRD,
   en poser moins, voire zéro (proposer directement et demander une validation
   globale).
4. **Langue** : français.

Questions-types (choisir les pertinentes, ne pas toutes les poser
mécaniquement) :

**Q1 — Validation du découpage en phases**
> "À partir du PRD, je propose ce découpage en phases : [liste dérivée]. Chaque
> phase est indépendamment valorisable. Tu valides, ou tu réajustes les frontières ?"

**Q2 — Dépendances et parallélisation**
> "Ordre proposé : [séquence]. [Phase X] et [Phase Y] me semblent
> parallélisables / strictement séquentielles. Confirmes-tu ?"

**Q3 — Granularité des paliers MVP**
> "Je regrouperais ces phases en [N] paliers MVP : [proposition]. Chaque palier
> est un livrable à valeur utilisateur propre (pas un simple jalon technique).
> Ce découpage en paliers te convient, ou tu en veux plus / moins ?"

---

## Validation finale avant écriture

Avant de générer le fichier, présenter une **synthèse compacte** du plan dérivé
et attendre validation explicite :

```
Synthèse du PLAN à générer

Architecture : [N composants — liste]
Phases : [N phases — noms]
Séquence : [linéaire / avec parallélisations]
Paliers MVP : [N paliers — noms]

Je génère PLAN.md ? (oui / corrections)
```

**Ne générer qu'après "oui" explicite.**

---

## Format de sortie

Générer le PLAN avec les 4 sections ci-dessous, dans cet ordre. Si la séquence
est strictement linéaire, écrire « Linéaire » dans la section Séquence sans la
détailler — ne pas la gonfler artificiellement.

```markdown
# PLAN — [nom-du-projet]

> Document **semi-frozen**. Toute révision passe par un ADR justificatif AVANT
> modification (Phase 3 du workflow). Ne jamais réviser sans ADR : perte de
> traçabilité garantie.
>
> Dérivé de PRD.md (le *quoi/pourquoi*) + CLAUDE.md (la *stack/conventions*).
> Ce document porte le *comment* et le *dans quel ordre*.

## Architecture haut niveau

[Composants principaux et leurs interactions. Niveau « boîtes et flèches ».
**Quoi**, jamais **pourquoi** — le pourquoi d'un choix d'archi vit dans un ADR.]

## Découpage en phases

[Séquence ordonnée. Chaque phase indépendamment valorisable. Les phases se
regroupent en paliers MVP (section dédiée plus bas).]

### Phase 1 — [Nom]
**Objectif** : [ce que cette phase rend possible]
**Livrables** :
- [ ] Livrable A
- [ ] Livrable B
**Critère de complétion** : [comment on sait que la phase est finie]
**Dépend de** : [phase(s) préalable(s), ou « rien »]

### Phase 2 — [Nom]
**Objectif** :
**Livrables** :
- [ ] ...
**Critère de complétion** :
**Dépend de** : Phase 1

## Séquence d'exécution

[Ordre de réalisation, dépendances inter-phases, ce qui peut avancer en
parallèle. Si strictement Phase 1 → 2 → 3, écrire « Linéaire ».]

## Paliers MVP

[Niveau macro, plus grossier que les phases. Un palier MVP regroupe plusieurs
phases et marque un **livrable à valeur utilisateur propre** — pas un simple
jalon technique (cf. ADR-0002). Chaque palier est un incrément vers la cible
du PRD.]

- [ ] **MVP1 — [Nom]** : [phases couvertes, valeur utilisateur livrée]
- [ ] **MVP2 — [Nom]** : [...]

## Renvois

- Décisions techniques justifiées (le *pourquoi*) → `adr/`
- Stack technique → CLAUDE.md
- Conventions de code → CLAUDE.md
- État de session courant → progress.md
```

---

## Après génération

Après avoir créé le PLAN :
1. Confirmer le chemin du fichier.
2. Souligner toute hypothèse de découpage faite en l'absence de réponse explicite.
3. Rappeler le statut semi-frozen : « À partir de maintenant, toute révision du
   PLAN passe par un ADR. »
4. Suggérer la prochaine étape : démarrer la Phase 2 (Implementation) du
   workflow — première session de code via `/catchup`.
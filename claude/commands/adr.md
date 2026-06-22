---
description: Crée un ADR atomique (Architecture Decision Record) — mode interview (décision humaine) ou capture (décision IA délibérée dans le fil), avec gestion de la supersession bidirectionnelle
argument-hint: [--from-context]
allowed-tools: Read, Write, Edit, Glob
model: opus
---

# ADR

Produit **un** ADR atomique : une décision = un fichier. Gère la création neuve
et la **supersession** (lien bidirectionnel vers l'ADR remplacé).

**Convention de référence** : `~/dotfiles/docs/methodology/conventions/adr.md`.
Cette commande en dérive — elle n'invente aucune règle. En cas de doute sur le
cycle de vie, le vocabulaire des relations ou la numérotation, cette convention
fait foi.

**Argument** : `--from-context` (optionnel) sélectionne le mode capture. Sans lui,
mode interview par défaut.

---

## Mode d'invocation — interview vs capture

La **source** de la décision pilote l'interaction (et seulement l'interaction —
elle ne laisse **aucune trace** dans l'ADR produit).

**Mode interview** (`/adr`, défaut) — la décision vient de l'humain et n'est pas
encore mûre.
- Faire **émerger** la décision par questions : contexte, options considérées,
  choix retenu, conséquences.
- Ne **jamais** tenter d'extraire une décision du fil de conversation — c'est le
  rôle du mode capture.

**Mode capture** (`/adr --from-context`) — la décision a déjà été délibérée dans
le fil (typiquement une proposition de l'IA discutée avec l'humain).
- **Relire** la délibération récente du fil. En extraire contexte, options,
  décision, conséquences.
- Ne **pas** ré-interviewer : ne pas re-poser des questions dont la réponse est
  déjà dans le fil.
- Mettre en forme dans le template, puis **soumettre pour validation** avant
  d'écrire.

**Invariant commun aux deux modes** : ne jamais écrire le fichier sans avoir
soumis le contenu à l'humain et obtenu une validation explicite.

---

## Numérotation — déterministe, jamais déléguée à l'humain

**Avant d'écrire**, déterminer le numéro du nouvel ADR :

1. **Lister** `adr/*.md` (créer `adr/` à la racine du projet s'il n'existe pas).
2. Extraire le numéro `NNNN` de chaque nom de fichier.
3. Nouveau numéro = **max existant + 1**, padding 4 chiffres.
   - `adr/` vide → `0001`.
   - `adr/` contenant `0001` et `0003` → `0004` (le **max**, pas le compte).

**Règles non-négociables** (cf. convention §Numérotation) :
- **Jamais combler un trou.** Si `0002` manque, le prochain reste `max+1`, pas
  `0002`. La chronologie prime sur la continuité.
- **Jamais renuméroter ni réordonner** un ADR existant.
- Le numéro est **dérivé**, jamais demandé à l'humain.

**Nommage** : `NNNN-slug-court.md`. Slug descriptif et stable (un lecteur
comprend le sujet sans ouvrir le fichier).

---

## Supersession — opération bidirectionnelle (deux fichiers)

Si la décision en **remplace** une antérieure, c'est une supersession. Elle
touche **deux fichiers** — ne jamais en oublier un, sous peine de casser la
chaîne d'audit.

1. **Nouvel ADR** — son corps contient :
   - le champ d'en-tête `Supersedes: ADR-NNNN` ;
   - dans la section Contexte, le **rationale du remplacement** (pourquoi
     l'ancienne décision ne tient plus). Ce rationale devient immuable.

2. **Ancien ADR** (`ADR-NNNN` remplacé) — modifier **uniquement** son champ
   `Status` :
   ```diff
   - Status: Accepted
   + Status: Superseded by ADR-MMMM
   ```
   Le **corps de l'ancien ADR n'est jamais touché** (contexte, options, décision,
   conséquences restent figés).

Utiliser `Edit` pour le patch de `Status:` de l'ancien — une substitution
chirurgicale d'une seule ligne, rien d'autre dans ce fichier.

---

## Immuabilité du corps — rôle de gardien

Le corps d'un ADR au statut `Accepted` est **immuable** (cf. convention
§Immuabilité).

Si l'humain demande de **modifier le corps** d'un ADR déjà `Accepted` (contexte,
options, décision, conséquences) :

1. **Refuser** l'édition directe.
2. **Expliquer** : amender le corps détruit la traçabilité d'audit ; un lecteur
   doit pouvoir reconstituer ce qui a été décidé à l'instant T.
3. **Proposer la voie correcte** : créer un nouvel ADR qui **supersède** (revirement)
   ou **refines** (précision sans contradiction) l'ancien.

Seul le champ `Status` d'un ADR `Accepted` peut transitionner. Tout le reste est
figé.

---

## Validation avant écriture

Quel que soit le mode, présenter le contenu de l'ADR et attendre une validation
explicite :

```
ADR-NNNN à créer : [titre]

Status: Proposed
[Supersedes: ADR-MMMM]   ← si supersession

Contexte    : [résumé une phrase]
Options     : [A / B / C]
Décision    : [option retenue]
Conséquences: [clés]

[Si supersession] ADR-MMMM passera à 'Status: Superseded by ADR-NNNN'.

Je crée le(s) fichier(s) ? (oui / corrections)
```

**Ne rien écrire avant "oui" explicite.**

---

## Format de sortie — template ADR

Dériver du template canonique de la convention. L'en-tête se limite aux champs
suivants — **aucun champ de source/auteur** (la provenance ne laisse pas de trace).

```markdown
# ADR-NNNN : [Titre court et descriptif]

Status: Proposed
Date: YYYY-MM-DD
Supersedes: ADR-NNNN  (uniquement si supersession)
Refines: ADR-NNNN     (uniquement si raffinement)

## Contexte

Quelle situation rend cette décision nécessaire ? Quelles contraintes, quelles
forces en jeu ? [Si supersession : pourquoi l'ancienne décision ne tient plus.]

## Options considérées

- **Option A** : description, avantages, inconvénients
- **Option B** : description, avantages, inconvénients
- **Option C** : description, avantages, inconvénients

## Décision

L'option retenue, formulée clairement. Pourquoi celle-ci et pas une autre.

## Conséquences

- Conséquence positive
- Trade-off accepté
- Implication technique
```

**Date** : utiliser la date du jour (format `YYYY-MM-DD`).
**Longueur cible** : 1 page. Au-delà de 2 pages, ce sont probablement deux
décisions à scinder.

---

## Après génération

1. Confirmer le(s) chemin(s) du/des fichier(s) écrit(s).
2. Si supersession : confirmer explicitement que **les deux** fichiers ont été
   touchés (nouvel ADR créé + `Status:` de l'ancien patché).
3. Rappeler que le corps du nouvel ADR `Proposed` reste modifiable **jusqu'à**
   son passage en `Accepted` — après quoi il devient immuable.
4. Si l'ADR documente le *pourquoi* d'un changement de PLAN/CLAUDE.md/PRD
   (replanning), rappeler l'ordre canonique : l'ADR vient d'être écrit, le
   document cible peut maintenant être amendé en conséquence.

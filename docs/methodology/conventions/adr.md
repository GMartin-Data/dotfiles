# Convention ADR — cycle de vie, vocabulaire et règles pratiques

Satellite du document maître [`../responsibility-matrix.md`](../responsibility-matrix.md).

Approfondit la ligne `adr/NNNN-*.md` de la matrice : cycle de vie complet, vocabulaire des relations entre décisions, règles pratiques de numérotation et de localisation.

**Emplacement canonique** : `~/dotfiles/docs/methodology/conventions/adr.md`

---

## Principe fondateur : immuabilité du corps, mutabilité du statut

Un ADR a **deux zones avec des règles différentes** :

### Zone immuable — le corps

Contexte, options considérées, décision retenue, conséquences. **Jamais modifiée après acceptation.** Aucune exception, même pour :
- Un typo critique → on crée un nouvel ADR qui supersède
- Une compréhension qui évolue → nouvel ADR
- Un détail manquant → nouvel ADR qui *refines* l'ancien

Justification : pour un audit (banking, conformité), un lecteur doit pouvoir reconstituer *ce qui a été décidé à l'instant T* sans qu'aucune décision postérieure n'ait réécrit le passé. Amender le corps détruit la traçabilité ; superséder la renforce.

### Zone mutable — un seul champ d'en-tête

Seul le champ `Status` peut transitionner après acceptation. Tout le reste reste figé.

```markdown
# ADR-0007 : Choix de Pub/Sub pour la file d'attente async

Status: Superseded by ADR-0023  ← seul ce champ peut changer
Date: 2025-11-15
```

---

## Cycle de vie

```
  Proposed
     │
     │  (délibération, acceptation)
     ▼
  Accepted ──────────┐
     │               │
     │               ├── Superseded by ADR-NNNN   (remplacée par décision plus récente)
     │               │
     │               └── Deprecated               (plus applicable, contexte disparu)
     │
     ▼
  (état terminal, jamais modifié)
```

**Proposed** — en délibération. Peut être modifié pendant cette phase.
**Accepted** — décision active. Corps figé définitivement.
**Superseded by ADR-NNNN** — remplacée par une décision plus récente. L'ADR reste lisible tel quel.
**Deprecated** — plus applicable, *mais pas remplacée*. Le contexte qui la justifiait a disparu (ex: composant supprimé).

---

## Vocabulaire des relations entre ADRs

Une décision postérieure peut entretenir cinq types de rapport avec une antérieure. Chaque relation a une sémantique précise :

| Relation | Sémantique | Effet sur l'ADR ancien | Cas d'usage typique |
|---|---|---|---|
| **Supersedes** | Remplacement complet | Statut → `Superseded by` | Changement de stack, revirement de choix |
| **Refines** | Raffinement | Reste `Accepted` | Ajout de précision sans contradiction |
| **Extends** | Extension | Reste `Accepted` | Nouveau cas couvert sans toucher à l'ancien |
| **Constrains** | Restriction | Reste `Accepted` | Rétrécit le champ d'application sans annuler |
| **Conflicts with** | Tension reconnue, non résolue | Reste `Accepted` | À ÉVITER — signal de dette à transformer en supersession |

**Fréquence d'usage réelle** : ~80 % Supersedes et Refines. Les trois autres sont rares mais utiles à nommer quand le cas se présente.

**Règle anti-dette** : `Conflicts with` est un état transitoire, jamais une destination finale. S'il apparaît, une délibération doit suivre pour le résoudre en Supersedes.

---

## Supersession : opération bidirectionnelle

Quand ADR-0023 supersède ADR-0007, **deux fichiers sont touchés** :

1. **ADR-0023** (nouveau) — dans son corps, mentionne explicitement :
   ```markdown
   Supersedes: ADR-0007

   ## Contexte
   ADR-0007 avait choisi Pub/Sub en supposant [...]. Depuis, [...] a changé.
   Ce qui suit remplace cette décision.
   ```
   Le rationale du changement fait partie du corps, donc devient immuable lui aussi.

2. **ADR-0007** (ancien) — seul son champ `Status` est modifié :
   ```diff
   - Status: Accepted
   + Status: Superseded by ADR-0023
   ```

Le corps d'ADR-0007 n'est pas touché. Un lecteur d'ADR-0007 voit immédiatement (a) ce qui était décidé en 2025, (b) que c'est obsolète, (c) où trouver la décision actuelle.

---

## Règles pratiques

### Numérotation

- **Séquentielle stricte** : `0001`, `0002`, `0003`... Padding à 4 chiffres minimum.
- **Jamais renuméroter.** Jamais réordonner. Le numéro = position chronologique dans l'histoire, pas dans la pertinence courante.
- Si un numéro est "perdu" (ADR commencé puis abandonné avant Proposed), laisser le trou — la chronologie prime sur la continuité.

### Localisation

- **Tous les ADRs dans `adr/`** à la racine du projet, peu importe leur statut.
- **Pas de sous-dossier `superseded/`** — ça brise la chronologie et complique l'auditabilité. Le statut dans l'en-tête suffit à filtrer.
- Conséquence : un projet mature peut accumuler beaucoup d'ADRs. C'est attendu et souhaitable.

### Nommage des fichiers

Format : `NNNN-slug-court.md`

Exemples : `0007-pubsub-pour-async.md`, `0023-replacement-pubsub-par-cloudtasks.md`.

Le slug doit être stable (ne pas le réécrire après création) et descriptif (un lecteur doit comprendre le sujet sans ouvrir le fichier).

### Vue courante de l'architecture

Pour obtenir "l'état actuel des décisions" (sans les superséded/deprecated) :

```bash
grep -L "Superseded\|Deprecated" adr/*.md
```

Filtre déterministe, pas d'index à maintenir. Si plus tard un index `adr/README.md` devient utile, le générer plutôt que le maintenir à la main.

### Quand créer un ADR ?

Critère : **décision non-triviale qui aura des conséquences durables**.

Triviale → pas d'ADR (ex: choix de variable name, formatage).
Non-triviale → ADR (ex: choix de techno, de pattern, de découpage, d'API publique).

Test simple : *"si je devais expliquer dans 6 mois pourquoi j'ai fait ce choix, est-ce que la réponse tient en une phrase ?"* Non → ADR.

---

## Template ADR minimal

```markdown
# ADR-NNNN : [Titre court et descriptif]

Status: Proposed
Date: YYYY-MM-DD
Supersedes: ADR-NNNN  (optionnel)
Refines: ADR-NNNN     (optionnel)

## Contexte

Quelle situation rend cette décision nécessaire ? Quelles contraintes ?
Quelles forces en jeu ?

## Options considérées

- **Option A** : description, avantages, inconvénients
- **Option B** : description, avantages, inconvénients
- **Option C** : description, avantages, inconvénients

## Décision

L'option retenue, formulée clairement. Pourquoi celle-ci et pas une autre.

## Conséquences

- Conséquence positive 1
- Conséquence positive 2
- Trade-off 1 accepté
- Trade-off 2 accepté
- Implication technique (mitigation d'un risque, etc.)
```

**Longueur cible** : 1 page max. Un ADR qui dépasse 2 pages est probablement deux décisions séparées à scinder.

---

## Pourquoi ce niveau de discipline ?

Pour un contexte banking/credit avec exigences d'auditabilité :

- **Immuabilité du corps** = preuve que la décision n'a pas été réécrite a posteriori
- **Supersession explicite et bidirectionnelle** = chaîne de raisonnement complète, reconstituable
- **Numérotation séquentielle** = preuve chronologique inviolable
- **Vocabulaire formel des relations** = sémantique non-ambiguë lors d'un audit

Cette discipline est *plus stricte* qu'un wiki ou un Confluence éditable. C'est un avantage différenciant : un auditeur n'a pas à reconstituer l'historique des modifications, il lit la chaîne d'ADRs telle quelle.

Pour des projets personnels sans contrainte d'audit, la discipline reste utile : elle préserve la qualité du raisonnement et évite le "pourquoi on a choisi ça déjà ?" trois mois plus tard.

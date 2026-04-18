---
description: Interview structurée pour produire un PRD par questionnement incrémental
argument-hint: [output-filename]
allowed-tools: Read, Write
model: opus
---

# PRD Interview

Processus d'interview structurée pour produire un PRD à travers un questionnement incrémental.

**Fichier de sortie** : `$ARGUMENTS` (défaut : `PRD.md`)

---

## Vérification préalable — mode strict

**Avant toute chose**, vérifier si le fichier de sortie existe déjà.

Si le fichier existe :

```
Le fichier {output-filename} existe déjà.

Un PRD est un document de cadrage stable, destiné à être figé après T0.
Si tu veux vraiment le réécrire, supprime-le manuellement d'abord :
  rm {output-filename}

Si tu veux documenter un écart par rapport au PRD initial, utilise
`/progress` à la place — la section "Écarts vs PRD" est conçue pour ça.

Commande annulée.
```

Puis s'arrêter. Ne pas continuer l'interview.

---

## Règles d'interaction

1. **Une question à la fois** — ne jamais surcharger avec plusieurs questions
2. **Options A/B/C** — proposer des choix quand des alternatives discrètes existent
3. **Valider avant de continuer** — reformuler uniquement sur les réponses ambiguës
4. **YAGNI** — challenger le scope creep, suggérer de reporter en v2+
5. **Expliquer les trade-offs** — quand l'utilisateur hésite, fournir le contexte de décision
6. **Langue** — interview et PRD produits en français

---

## Séquence d'interview

Progresser à travers les phases dans l'ordre. Les phases 7, 9 et 10 peuvent être **skippées** selon les critères explicites ci-dessous. **Toutes les autres phases sont obligatoires.**

### Phase 1 — Problème

"Quel problème ce projet résout-il ? (Problème utilisateur, pas solution technique)"

Reformuler pour valider la compréhension.

**À noter pour le critère de skip de Phase 10** : identifier combien de composants techniques sont mentionnés dans la réponse (ex. "un script" = 1 composant ; "ingestion + transformation + API" = 3 composants).

### Phase 2 — Utilisateurs

"Qui sont les utilisateurs cibles ?"
- A) Usage personnel uniquement
- B) Cercle restreint (collègues, amis)
- C) Public

Expliquer les implications d'overhead de chaque choix. Si B ou C, demander une brève description de persona.

### Phase 3 — Interface

"Comment les utilisateurs vont-ils interagir avec ce projet ?"

Proposer des options selon le contexte du problème (CLI, extension, application web, API, script batch, etc.).

### Phase 4 — Workflow

"Que se passe-t-il quand l'utilisateur déclenche l'action principale ?"

Proposer des options concrètes (téléchargement auto, copie dans le clipboard, aperçu, etc.).

### Phase 5 — User Stories

"Définissons 3-5 user stories clés. Complète cette phrase :"

> "En tant que [utilisateur], je veux [action], afin de [bénéfice]"

Proposer des stories basées sur les réponses précédentes. L'utilisateur confirme, modifie ou ajoute.

### Phase 6 — Périmètre

"Qu'est-ce qui est dans v1 vs reporté à plus tard ?"

Pousser vers un scope minimal viable. Nommer explicitement ce qui est HORS scope. Regrouper par catégorie si utile :
- Fonctionnalités core
- Aspects techniques
- Intégrations
- Déploiement

**À noter pour le critère de skip de Phase 9** : capturer si le projet est décrit comme "prototype" ou "exploration" dans la réponse.

### Phase 7 — Format de sortie

**Critère de skip** : skipper cette phase si la réponse en Phase 3 (Interface) est "application web" ou "extension" (le format UI est défini par le framework, pas par l'utilisateur).

Si le projet produit des fichiers/données de sortie :

"À quoi doit ressembler le livrable de sortie ?"

Demander un exemple ou proposer une structure selon le contexte.

### Phase 8 — Stack technique

"Des préférences ou contraintes techniques ?"
- Langage/framework
- APIs/dépendances externes
- Besoins d'authentification
- Cible de déploiement

### Phase 9 — Gestion des erreurs

**Critère de skip** : skipper cette phase si la Phase 6 (Périmètre) contient les mots "prototype" ou "exploration" dans la description du projet.

"Qu'est-ce qui peut mal se passer ? Comment chaque cas doit-il être géré ?"

Lister 3-5 modes de défaillance probables. S'appuyer sur la stack définie en Phase 8 pour poser des questions précises. Demander le comportement désiré par cas.

### Phase 10 — Architecture

**Critère de skip** : skipper cette phase si la Phase 1 (Problème) ne mentionne qu'**un seul composant technique**.

Si le système est multi-composants :

"Comment les composants interagissent-ils ?"

Proposer une architecture haut niveau basée sur les réponses précédentes. Valider.

### Phase 11 — Phases d'implémentation

"Comment découper ça en phases ?"

Proposer 2-3 phases avec livrables clairs. Chaque phase doit être indépendamment valorisable.

### Phase 12 — Risques

"Quels sont les principaux risques ?"

Proposer 2-3 risques basés sur le contexte. Demander des stratégies de mitigation ou les proposer.

### Phase 13 — Critères de succès

"Comment savoir que v1 est terminé ?"

Pousser vers des critères concrets et testables. Proposer des indicateurs mesurables.

---

## Validation finale en 3 blocs

Avant de générer le PRD, valider le contenu collecté en **3 blocs thématiques séparés**. Présenter chaque bloc individuellement, attendre validation explicite avant le suivant.

### Bloc 1 — Cadrage

```
Validation bloc 1/3 — Cadrage

1. Problème : [une phrase]
2. Solution : [une phrase]
3. Utilisateurs : [type + persona si applicable]
4. Interface : [choix]

Confirmes-tu ce bloc ? (oui / corrections)
```

Attendre "oui" ou équivalent. Sur corrections, reformuler et revalider ce bloc avant de passer au suivant.

### Bloc 2 — Scope

```
Validation bloc 2/3 — Scope

5. User Stories : [nombre] stories définies
6. Périmètre v1 : [items clés inclus] / Exclu : [items clés hors scope]
7. Stack : [choix principaux]

Confirmes-tu ce bloc ? (oui / corrections)
```

Attendre validation.

### Bloc 3 — Exécution

```
Validation bloc 3/3 — Exécution

8. Phases : [nombre] phases
9. Risques : [nombre] identifiés
10. Critère de succès : [résumé]

Confirmes-tu ce bloc ? (oui / corrections)
```

Attendre validation.

**Ne générer le PRD qu'après validation explicite des 3 blocs.**

---

## Format de sortie

Générer le PRD avec les sections ci-dessous. Si une phase a été skippée, **omettre la section correspondante** (ne pas mettre "N/A" ou placeholder).

```markdown
# PRD — [nom-du-projet]

## Résumé
[2-3 paragraphes : problème, solution, proposition de valeur]

## Problème
[Énoncé détaillé du problème]

## Solution
[Approche en un paragraphe]

## Utilisateurs cibles
[Qui, échelle, persona si applicable]

## User Stories
- En tant que [utilisateur], je veux [action], afin de [bénéfice]
- ...

## Fonctionnalités v1
### [Composant 1]
- ✅ Feature A
- ✅ Feature B

### [Composant 2]
- ✅ Feature C

## Périmètre v1
| ✅ Inclus | ❌ Exclu (v2+) |
|-----------|----------------|
| ... | ... |

## Stack technique
| Composant | Choix | Justification |
|-----------|-------|---------------|
| ... | ... | ... |

## Format de sortie
[Uniquement si Phase 7 a été exécutée : structure de sortie, exemples]

## Gestion des erreurs
[Uniquement si Phase 9 a été exécutée]
| Cas d'erreur | Comportement |
|--------------|--------------|
| ... | ... |

## Architecture technique
[Uniquement si Phase 10 a été exécutée : architecture haut niveau, interactions composants]

## Phases d'implémentation

### Phase 1 : [Nom]
**Objectif :** [But]
**Livrables :**
- ✅ Livrable A
- ✅ Livrable B
**Validation :** [Comment savoir que la phase est terminée]

### Phase 2 : [Nom]
...

## Risques & Mitigations
| Risque | Impact | Mitigation |
|--------|--------|------------|
| ... | ... | ... |

## Critères de succès
- ✅ [Critère mesurable 1]
- ✅ [Critère mesurable 2]

## Évolutions futures (v2+)
[Fonctionnalités explicitement reportées, considérations futures]
```

---

## Après génération

Après avoir créé le PRD :
1. Confirmer le chemin du fichier
2. Souligner les éventuelles hypothèses faites
3. Suggérer les prochaines étapes immédiates (créer CLAUDE.md projet via `/claude-md`, revoir des sections, démarrer la Phase 1 d'implémentation, etc.)
---
description: Interview structurée pour produire un PRD conforme au canvas canonique de 11 sections
argument-hint: [output-filename]
allowed-tools: Read, Write, Glob
model: opus
---

# PRD Interview

Processus d'interview structurée pour produire un PRD à travers un questionnement incrémental.

**Canvas de référence** : `~/dotfiles/docs/methodology/conventions/prd.md`
(acté par ADR-0013). Cette commande en dérive — elle n'invente aucune section.
En cas de doute sur le contenu d'une section ou une frontière (stack,
architecture, risques), la convention fait foi.

**Fichier de sortie** : `$ARGUMENTS` (défaut : `PRD.md`).

---

## Vérification préalable — mode strict

**Avant toute chose**, vérifier si le fichier de sortie existe déjà.

Si le fichier existe :

```
Le fichier {output-filename} existe déjà.

Un PRD décrit le produit cible. C'est une baseline versionnée : elle ne dérive
pas par édition silencieuse. Une inflexion réelle de la cible passe par un ADR
(qui acte le changement), puis un amendement contrôlé — pas par une réécriture.
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
4. **YAGNI** — challenger le scope creep, distinguer ce qui est dans la cible de ce qui la dépasse
5. **Expliquer les trade-offs** — quand l'utilisateur hésite, fournir le contexte de décision
6. **Langue** — interview et PRD produits en français

**Frontière du PRD** (non négociable, cf. convention) : le PRD dit le *quoi*
et le *pourquoi*, jamais le *comment*. Si l'utilisateur apporte de la stack,
de l'architecture ou des mitigations techniques pendant l'interview, l'en
remercier et router : stack/techno → CLAUDE.md (`/claude-md`), architecture →
PLAN.md (`/planning`), risque tranché → ADR. Rien de tout cela n'entre dans
le PRD.

---

## Séquence d'interview

Progresser à travers les phases dans l'ordre. Les phases 8 et 10 peuvent être
**skippées** selon les critères explicites ci-dessous. **Toutes les autres
phases sont obligatoires.**

### Phase 1 — Problème

"Quel problème ce projet résout-il ? (Problème utilisateur, pas solution technique)"

Reformuler pour valider la compréhension.

### Phase 2 — Objectifs

"Si le produit réussit, qu'est-ce qui aura changé, concrètement ?"

Pousser vers 2-4 objectifs produit formulés en résultats (pas en
fonctionnalités). Ils seront vérifiés par les indicateurs de la Phase 12 —
un objectif invérifiable est un signal à challenger dès maintenant.

### Phase 3 — Utilisateurs

"Qui sont les utilisateurs cibles ?"
- A) Usage personnel uniquement
- B) Cercle restreint (collègues, amis)
- C) Public

Expliquer les implications d'overhead de chaque choix. Si B ou C, demander une brève description de persona.

### Phase 4 — Interface

"Comment les utilisateurs vont-ils interagir avec ce projet ?"

Proposer des options selon le contexte du problème (CLI, extension, application web, API, script batch, etc.).

### Phase 5 — Workflow nominal

"Que se passe-t-il quand l'utilisateur déclenche l'action principale ?"

Proposer des options concrètes (téléchargement auto, copie dans le clipboard, aperçu, etc.).

### Phase 6 — User stories

"Définissons 3-5 user stories clés. Complète cette phrase :"

> "En tant que [utilisateur], je veux [action], afin de [bénéfice]"

Proposer des stories basées sur les réponses précédentes. L'utilisateur
confirme, modifie ou ajoute.

**Destination** : ces stories deviendront des **checkboxes vérifiables** dans
la section Acceptance criteria (scénarios nominaux) — jamais une section
narrative séparée. Formuler chaque story pour qu'elle soit testable.

### Phase 7 — Périmètre

"Qu'est-ce qui est dans la cible, exclu à jamais, ou remis à plus tard ?"

Pousser vers un périmètre cohérent en **trois listes distinctes** :
- **Cible** : les fonctionnalités du produit visé (par composant si utile)
- **Non-goals** : les exclusions délibérées — *jamais* — chacune avec son
  rationale en une ligne
- **Au-delà de la cible** : le différé — *pas maintenant* — candidat à une
  future révision par ADR

Test pour classer une exclusion : « une révision future de la cible
pourrait-elle raisonnablement l'inclure ? » Oui → au-delà. Non → non-goal.

**À noter pour le critère de skip de Phase 10** : capturer si le projet est
décrit comme "prototype" ou "exploration" dans la réponse.

### Phase 8 — Format de sortie

**Critère de skip** : skipper cette phase si la réponse en Phase 4 (Interface) est "application web" ou "extension" (le format UI est défini par le framework, pas par l'utilisateur).

Si le projet produit des fichiers/données de sortie :

"À quoi doit ressembler le livrable de sortie ?"

Demander un exemple ou proposer une structure selon le contexte.

### Phase 9 — Contraintes

"Quelles exigences te sont imposées de l'extérieur ? (deadline, conformité,
volumétrie, langue, environnement d'exécution...)"

Appliquer le **test à deux axes** de la convention sur chaque réponse :
- La contrainte **nomme une technologie** → elle va dans CLAUDE.md, même
  imposée. N'en garder dans le PRD que l'exigence produit qui la motive,
  *si elle existe indépendamment* (ex. « les données restent en UE » reste ;
  « region europe-west1 » part vers CLAUDE.md).
- **Exigence produit exogène non-technique** → section Contraintes.

Annoncer explicitement chaque routage vers CLAUDE.md pour que rien ne se perde.

### Phase 10 — Comportement sur erreur

**Critère de skip** : skipper cette phase si la Phase 7 (Périmètre) contient les mots "prototype" ou "exploration" dans la description du projet.

"Qu'est-ce qui peut mal se passer ? Que doit-il se passer alors, du point de vue de l'utilisateur ?"

Lister 3-5 modes de défaillance probables en s'appuyant sur l'interface et le
workflow (Phases 4-5). Demander le **comportement attendu** par cas — jamais
la solution technique (elle relève du PLAN). Chaque cas deviendra une checkbox
d'acceptance criteria.

### Phase 11 — Open questions

"Quels risques ou inconnues restent sans réponse à ce stade ?"

Proposer 2-3 inconnues plausibles basées sur le contexte. Chaque entrée est
formulée **en question ouverte** — jamais en table risque/mitigation :
- Risque **non résolu** → open question du PRD.
- Risque déjà **tranché** par une décision → il n'a rien à faire ici : la
  décision relève d'un ADR (la mitigation en devient une conséquence).
  Le signaler et l'écarter du PRD.

Une absence d'inconnues est un résultat valide (« Aucune » explicite).

### Phase 12 — Indicateurs de succès

"Comment sauras-tu que les objectifs (Phase 2) sont atteints ?"

Pousser vers des seuils et métriques concrets, testables, rattachés aux
objectifs. Chaque indicateur deviendra une checkbox d'acceptance criteria.

---

## Contrôle de cohérence inter-phases

<!-- Règle relocalisée depuis le CLAUDE.md global (audit 2026-07, DN3 —
     tasks/claude-md-audit-2026-07.md) : sagesse process PRD, pas un garde-fou
     modèle transverse. -->

Avant la validation finale, vérifier que les réponses collectées forment une
chaîne sans contradiction — les phases ont été remplies séparément, les
incohérences apparaissent aux jointures :

- **Non-goals (Phase 7) vs Open questions (Phase 11)** : aucune question
  ouverte ne re-litige une exclusion délibérée ; si c'est le cas, soit
  l'exclusion n'est pas ferme (→ au-delà de la cible), soit la question est
  sans objet.
- **Non-goals (Phase 7) vs Indicateurs (Phase 12)** : aucun indicateur ne
  mesure une fonctionnalité exclue.
- **Open questions (Phase 11) vs Acceptance criteria (Phases 6/10/12)** :
  aucun criterion ne dépend silencieusement d'une question ouverte ; si un
  criterion n'est vérifiable qu'une fois une inconnue levée, le signaler.
- **Contraintes (Phase 9)** : aucune contrainte retenue ne nomme une
  technologie (le test à deux axes a été appliqué ; les éléments routés vers
  CLAUDE.md ont été annoncés).

Si une contradiction apparaît, la signaler et la résoudre avec l'utilisateur
avant de présenter les blocs de validation.

---

## Validation finale en 3 blocs

Avant de générer le PRD, valider le contenu collecté en **3 blocs thématiques séparés**. Présenter chaque bloc individuellement, attendre validation explicite avant le suivant.

### Bloc 1 — Cadrage

```
Validation bloc 1/3 — Cadrage

1. Problème : [une phrase]
2. Objectifs : [liste courte]
3. Utilisateurs : [type + persona si applicable]
4. Interface : [choix]

Confirmes-tu ce bloc ? (oui / corrections)
```

Attendre "oui" ou équivalent. Sur corrections, reformuler et revalider ce bloc avant de passer au suivant.

### Bloc 2 — Scope

```
Validation bloc 2/3 — Scope

5. Fonctionnalités cibles : [items clés]
6. Non-goals : [exclusions] / Au-delà de la cible : [différés]
7. Format de sortie : [résumé, ou "skippé (UI)"]

Confirmes-tu ce bloc ? (oui / corrections)
```

Attendre validation.

### Bloc 3 — Contrat & inconnues

```
Validation bloc 3/3 — Contrat & inconnues

8. Contraintes : [liste, ou "aucune"]
9. Acceptance criteria : [N] scénarios nominaux, [N] comportements d'erreur
   (ou "skippé"), [N] indicateurs
10. Open questions : [liste, ou "aucune"]

Confirmes-tu ce bloc ? (oui / corrections)
```

Attendre validation.

**Ne générer le PRD qu'après validation explicite des 3 blocs.**

---

## Format de sortie

Générer le PRD avec les 11 sections du canvas canonique, dans cet ordre. Une
section optionnelle skippée est **omise** (pas de "N/A" ni placeholder). Une
section obligatoire sans contenu s'écrit explicitement (« Aucune »).

```markdown
# PRD — [nom-du-projet]

## Résumé
[2-3 § : problème, solution produit en une phrase, proposition de valeur]

## Problème
[Énoncé détaillé du problème, orienté utilisateur]

## Objectifs
- [Objectif produit formulé en résultat mesurable]
- ...

## Utilisateurs & scénarios
[Qui : type, échelle, persona si applicable]
[Scénarios d'usage : interface retenue, déroulé nominal]

## Fonctionnalités (cible)
### [Composant 1]
- Feature A
- Feature B

### [Composant 2]
- Feature C

## Non-goals
- [Exclusion délibérée] — [rationale en une ligne]

## Format de sortie
[Uniquement si Phase 8 exécutée : forme du livrable, exemple à l'appui]

## Contraintes
- [Exigence exogène non-technique]
(ou « Aucune »)

## Acceptance criteria

### Scénarios nominaux
- [ ] En tant que [utilisateur], je peux [action vérifiable]

### Comportement sur erreur
[Uniquement si Phase 10 exécutée]
- [ ] Quand [cas d'erreur], le système [comportement attendu]

### Indicateurs mesurables
- [ ] [Seuil ou métrique rattaché à un objectif]

## Open questions
- [Risque non résolu ou inconnue, formulé en question]
(ou « Aucune »)

## Au-delà de la cible
[Différé — candidat à une future révision de cible par ADR. Le découpage de
la cible en itérations relève de `/planning`, pas de cette section.]
```

---

## Après génération

Après avoir créé le PRD :
1. Confirmer le chemin du fichier
2. Souligner les éventuelles hypothèses faites
3. Rappeler les éléments routés hors PRD pendant l'interview (stack →
   CLAUDE.md, décisions tranchées → ADR), pour qu'ils ne se perdent pas
4. Suggérer les prochaines étapes immédiates : revue adverse `/grill` avant
   gel, créer le CLAUDE.md projet via `/claude-md`, produire le PLAN via
   `/planning`

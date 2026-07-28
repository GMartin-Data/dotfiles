# Convention PRD — canvas canonique et tests de frontière

Satellite du document maître [`../responsibility-matrix.md`](../responsibility-matrix.md).

Approfondit la ligne `PRD.md` de la matrice : canvas complet des sections, rôle
de chacune, tests de frontière anti-fuite. Format acté par
[`adr/0013`](../../../adr/0013-format-prd-canonique.md).

**Emplacement canonique** : `~/dotfiles/docs/methodology/conventions/prd.md`

---

## Principe fondateur

Le PRD dit le *quoi* et le *pourquoi* du produit — jamais le *comment*. C'est
une **baseline versionnée de la cible** ([`adr/0001`](../../../adr/0001-prd-produit-cible.md)) :
elle ne dérive pas par édition silencieuse, sa révision passe par un ADR.

Test de lecture : **un lecteur non-technique doit pouvoir lire le PRD seul.**

Ne contient jamais (règles de non-overlap de la matrice) : stack (règle 1),
architecture (règle 2), phases d'implémentation (règle 5), mitigations de
risques (règle 6), découpage en MVP/itérations.

---

## Canvas — liste fermée de 11 sections

Toute section hors de cette liste est une violation. L'ordre est l'ordre de
lecture du document.

| # | Section | Statut | Contenu |
|---|---|---|---|
| 1 | **Résumé** | Obligatoire | Problème, solution produit en une phrase, proposition de valeur (2-3 §) |
| 2 | **Problème** | Obligatoire | Énoncé détaillé, orienté utilisateur |
| 3 | **Objectifs** | Obligatoire | Le pourquoi mesurable du produit |
| 4 | **Utilisateurs & scénarios** | Obligatoire | Persona/échelle, interface, déroulé d'usage nominal |
| 5 | **Fonctionnalités (cible)** | Obligatoire | Contenu de la cible, par composant |
| 6 | **Non-goals** | Obligatoire | Exclusions délibérées avec rationale — *jamais* |
| 7 | **Format de sortie** | Optionnelle | Forme du livrable, exemple à l'appui — omise si l'interface est une UI |
| 8 | **Contraintes** | Obligatoire | Exigences exogènes non-techniques (test à deux axes ci-dessous) |
| 9 | **Acceptance criteria** | Obligatoire | Contrat vérifiable unique, 3 sous-parties (ci-dessous) |
| 10 | **Open questions** | Obligatoire | Risques non résolus, questions ouvertes |
| 11 | **Au-delà de la cible** | Obligatoire | Différé — *pas maintenant*, candidat à révision par ADR |

Une section optionnelle omise ne laisse **aucun placeholder** (« N/A »
interdit). Une section obligatoire sans contenu au gel s'écrit explicitement
(« Aucune » pour Open questions) : la moisson a eu lieu, ce n'est pas un oubli.

**Sections qui n'existent pas** (et pourquoi) :
- **Solution** — l'« approche en un paragraphe » est la rampe vers le design ;
  la solution produit tient en une phrase, dans le Résumé.
- **Table de périmètre ✅/❌** — duplication interne (✅ = Fonctionnalités,
  ❌ = Non-goals) ; drift garanti au premier amendement.
- **Stack technique, Architecture technique** — règles 1 et 2.
- **Risques & Mitigations** — règle 6 (voir test ci-dessous).
- **User Stories narratives, Critères de succès** — fusionnées dans
  Acceptance criteria (règle 4).

---

## Acceptance criteria — le contrat vérifiable unique

Cible du rituel de Phase 2 : **cocher un criterion (`[ ]` → `[x]`) enregistre
un état** — aucun ADR. Modifier, ajouter ou supprimer un criterion révise la
cible → ADR (cf. matrice, « Frontières floues »).

Trois sous-parties :

1. **Scénarios nominaux** — les user stories, en checkboxes vérifiables
   (« En tant que X, je peux Y » testable). Jamais de doublon narratif
   ailleurs (règle 4).
2. **Comportement sur erreur** — *conditionnelle* (omise pour un prototype ou
   une exploration) : « quand X échoue, le système fait Y », en checkboxes.
3. **Indicateurs mesurables** — seuils et métriques attestant que les
   Objectifs (§3) sont atteints.

---

## Tests de frontière

### Contraintes — test à deux axes

1. **La contrainte nomme une technologie ?** → CLAUDE.md, même imposée
   (la règle 1 prime). Le PRD n'en garde que l'exigence produit qui la
   motive, *si elle existe indépendamment*.
   Exemple : « les données restent en UE » (PRD, Contraintes) ; « region
   `europe-west1` » (CLAUDE.md, convention qui la traduit).
2. **Exigence produit exogène non-technique** (deadline, conformité,
   volumétrie, langue) → PRD, Contraintes.

Pas de duplication : le PRD porte l'exigence, CLAUDE.md la convention qui
l'implémente. Le flux d'élaboration unidirectionnel (PRD → CLAUDE.md,
cf. matrice Phase 0) transporte l'une vers l'autre.

### Risques — deux destinations, zéro table

- Risque **non résolu** → Open questions, formulé comme une question.
- Risque **tranché** → ADR ; la mitigation devient une conséquence de l'ADR.

Proposer une mitigation dans le PRD, c'est faire du design : la table
« Risque / Impact / Mitigation » n'a de destination légale nulle part.

### Non-goals vs Au-delà de la cible

Test : *« une révision future de la cible pourrait-elle raisonnablement
l'inclure ? »* Oui → Au-delà de la cible (porte entrouverte, candidat ADR).
Non → Non-goals (porte fermée, protège le scope).

### Stories — une seule forme

Le *contexte* d'usage (qui, comment, déroulé nominal) vit dans Utilisateurs
& scénarios, en narratif. Le *contrat* (« je peux Y ») vit dans Acceptance
criteria, en checkboxes. Une story n'existe jamais sous les deux formes.

---

## Cycle de vie (rappel du maître)

- **Gel** : après revue adverse `/grill` (les décisions candidates se
  résolvent en Open questions ou se formalisent via `/adr` avant gel).
- **Phase 2** : cocher des acceptance criteria = état, geste nominal.
- **Révision** (Phase 3, inflexion exogène) : ADR d'abord, amendement ensuite.

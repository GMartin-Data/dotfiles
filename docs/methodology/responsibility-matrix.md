# Matrice de responsabilité documentaire

Pierre fondatrice du workflow PRD + PLAN + ADR + CLAUDE.md + progress.md.

Source de vérité unique par concept. Toute décision d'écriture future doit passer par ce document avant d'ajouter du contenu où que ce soit.

**Emplacement canonique** : `~/dotfiles/docs/methodology/responsibility-matrix.md`

---

## Matrice principale

| Document | Cycle de vie | Contenu unique | Ne contient JAMAIS |
|---|---|---|---|
| **CLAUDE.md** | Stable (révisions rares, via ADR en Phase 3) | Conventions code, stack, contraintes projet transverses, style, AI workflow guidelines | Goals projet, décisions ad-hoc, état de session, phases d'implémentation |
| **PRD.md** | Baseline versionnée du produit **cible** : ne dérive pas par édition silencieuse ; révision = ADR en Phase 3 (cf. [`adr/0001`](../../adr/0001-prd-produit-cible.md)) | Problem, goals, non-goals, users & scenarios, acceptance criteria, constraints, open questions, hors-cible | Stack, architecture, phases d'implémentation, risques techniques, décisions de design, découpage en MVP/itérations |
| **PLAN.md** | Semi-frozen (révision = ADR obligatoire) | Architecture haut niveau, séquence d'exécution, **deux granularités** (cf. [`adr/0002`](../../adr/0002-mvp-palier-dans-plan.md)) : **paliers MVP** (livrables à valeur) et **phases** (briques de séquençage technique) qu'ils regroupent | Décisions atomiques avec rationale, état session, conventions code |
| **adr/NNNN-*.md** | Corps immuable, statut mutable | UNE décision = UN fichier. Voir [`conventions/adr.md`](conventions/adr.md) pour cycle de vie complet, vocabulaire des relations et règles pratiques. | État de session, listing exhaustif de toutes les micro-décisions |
| **progress.md** | Living, court | Où j'en suis, prochaine action concrète, blockers de session | Décisions (vont en ADR), changements de plan (vont en ADR puis PLAN), conventions |

---

## Règles de non-overlap

Six règles strictes. Toute violation = source de drift garantie.

1. **Stack technique → CLAUDE.md uniquement.** Ni PRD ni PLAN. Si Cruft a déjà fixé la stack, elle est dans `.cruft.json` + référence dans CLAUDE.md. Pas de duplication.

2. **Architecture haut niveau → PLAN.md.** Pas PRD. Le PRD doit être lisible par quelqu'un qui ignore les choix techniques.

3. **Architecture décisionnelle (le *pourquoi* d'un choix vs un autre) → ADR.** Pas PLAN. PLAN dit ce qu'on construit ; ADR dit pourquoi on l'a choisi.

4. **User stories → acceptance criteria du PRD.** Pas de document `US.md` séparé. Les stories sont des checkboxes vérifiables dans la section dédiée du PRD.

5. **Phases d'implémentation → PLAN.md.** Pas PRD. Le PRD est une baseline (révisable par ADR, pas au fil de l'eau) ; les phases d'impl évoluent librement dans le PLAN.

6. **Risques → deux destinations selon état :**
   - Risque non résolu → section "Open questions" du PRD
   - Risque tranché par une décision → ADR documente la décision et ses conséquences (la mitigation devient une conséquence)

---

## Test décisif avant tout ajout

Avant d'écrire un contenu nouveau, se poser :

> *« Si je modifie ce contenu plus tard, quel(s) autre(s) document(s) dois-je toucher pour rester cohérent ? »*

- **Réponse : aucun** → bon emplacement, source de vérité unique respectée.
- **Réponse : un autre document** → overlap. Le contenu appartient à un seul des deux. Trancher avant d'écrire.

---

## Cycles d'écriture par phase de projet

### Phase 0 — Définition (one-shot par projet)
- Interview `/claude-md` → CLAUDE.md (stable)
- Interview `/prd` → PRD.md (baseline du produit cible, révisable par ADR)

Les deux productions sont indépendantes en contenu et peuvent être menées dans n'importe quel ordre.

### Phase 1 — Planning (one-shot par projet)
- Lit PRD + CLAUDE.md
- Produit PLAN.md (semi-frozen)

### Phase 2 — Implementation (cycle répété)
- Start session : `/catchup` lit progress.md (+ ADRs récents si pertinents)
- Pendant : code selon PLAN courant, coche acceptance criteria du PRD
- Sur décision non-triviale : écrit ADR **avant** d'en coder la conséquence
- End session : `/progress` met à jour progress.md → `/clear`

### Phase 3 — Replanning (déclenchée par drift ou inflexion)
Trois types de déclencheurs, trois cibles d'amendement :
- **Drift technique** entre PLAN et réalité → révise PLAN.md (cas nominal, fréquent)
- **Impossibilité ou inflexion stack** → amende CLAUDE.md (rare)
- **Inflexion exogène** (client, contexte métier) → amende PRD.md (rare)

Ordre canonique dans tous les cas :
1. ADR documente le *pourquoi* du changement
2. Le document cible est amendé en conséquence

Jamais l'inverse (amender un document sans ADR justificatif = perte de traçabilité).

---

## Frontières floues — résolutions explicites

**Où vivent les MVP successifs** (cf. [`adr/0002`](../../adr/0002-mvp-palier-dans-plan.md))
- PRD = la **cible** (le *quoi* ultime). Ne contient jamais le découpage en MVP.
- PLAN = le **découpage de la cible** en paliers de valeur (MVP) et en phases techniques.
- Un **MVP/palier** = livrable à valeur utilisateur propre, regroupant une ou plusieurs phases.
  Une **phase** = brique de séquençage technique. Deux niveaux distincts, un seul PLAN.
- Test : « est-ce un livrable que l'utilisateur peut éprouver ? » Oui → palier MVP. Non
  (brique interne) → phase. « Est-ce que ça change la cible ? » Oui → ADR + amende le PRD,
  pas le PLAN.
- Modèle C (PLAN unique). Si un projet réel sue sous ce modèle, un ADR de supersession
  vers un PLAN-par-itération devient le déclencheur — pas avant.

**PRD vs PLAN : "ce qu'on construit"**
- PRD = *quoi* et *pourquoi* (orienté problème/utilisateur)
- PLAN = *comment* et *dans quel ordre* (orienté exécution)
- Test : un lecteur non-technique doit pouvoir lire le PRD seul. Un dev qui prend la suite doit pouvoir lire PLAN + CLAUDE.md sans PRD pour exécuter.

**PLAN vs ADR : "décisions techniques"**
- PLAN = décisions consolidées en architecture cible (la photo finale)
- ADR = délibération atomique (le film des choix)
- Test : si je supprime un ADR, est-ce que PLAN reste cohérent ? Oui → l'ADR documentait juste le pourquoi. Non → l'ADR contenait une décision absente de PLAN → bug d'architecture documentaire.

**progress vs ADR : "ce qui s'est passé"**
- progress = état de session courante (volatile, écrasable)
- ADR = décision durable (immuable)
- Test : ce contenu sera-t-il pertinent dans 6 mois ? Oui → ADR. Non → progress.

---

## Conséquences architecturales pour les outils

- `/prd` produit un PRD allégé (8 sections : Problem, Goals, Non-goals, Users & scenarios, Acceptance criteria, Constraints, Open questions, Hors-cible). Pas de stack, pas d'archi, pas de phases d'impl.
- `/claude-md` reste seule source de vérité stack et conventions.
- `/planning` (nommée ainsi, pas `/plan` — collision avec built-in Claude Code) produit PLAN.md à partir de PRD + CLAUDE.md.
- `/adr` produit un ADR atomique par invocation.
- `/progress` et `/catchup` restent les outils de session, sans changement structurel.

---

## Index des satellites

Documents satellites approfondissant un type de document spécifique :

| Satellite | Sujet | Statut |
|---|---|---|
| [`conventions/adr.md`](conventions/adr.md) | Cycle de vie ADR, vocabulaire des relations, règles pratiques | Actif |
| `conventions/prd.md` | Format et structure du PRD | À créer si besoin |
| `conventions/plan.md` | Format et structure du PLAN | À créer si besoin |
| `conventions/progress.md` | Format de progress.md | À créer si besoin |
| `conventions/claude-md.md` | Format de CLAUDE.md | À créer si besoin |

**Critère de création d'un satellite** : approfondit *un seul* concept du maître, ET (contenu > 30-50 lignes OU évolue indépendamment du maître). Sinon, reste dans le maître.

**Principe d'émergence** : un satellite naît quand le besoin réel apparaît, pas par anticipation. *Build before automating* appliqué à la doc méthodologique.
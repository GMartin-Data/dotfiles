# Revue — repo `mattpocock/skills` (revisite complète, 2026-09-11)

> Méthode : clone complet, lecture intégrale des 25 skills promues, des 8
> in-progress, des 4 misc, de la couche méta (`.agents/`, `CLAUDE.md`,
> `CONTEXT.md`, `.out-of-scope/`), du CHANGELOG et de l'historique git.
> Visite précédente : 2026-07-31, limitée à `wayfinder`
> (`tasks/wayfinder-analysis-2026-07.md`) — son verdict n'est pas re-litigé
> ici, seulement vérifié. Statut : analyse pour décision — aucun artefact du
> workflow modifié.

---

## 1. État du repo et changements notables récents

Activité : 182 commits en juillet, 114 en août, 2 début septembre — cadence
élevée mais en décélération ; le gros de l'énergie d'août est allé à la
**distribution**, pas au contenu :

- **Plugin Claude Code officiel** (v1.2.0, accepté dans le marketplace
  officiel le 2026-08-05) : `claude plugins install mattpocock-skills`
  installe les 25 skills promues en bundle read-only auto-mis-à-jour.
  L'alternative `npx skills add mattpocock/skills` (skills.sh) copie des
  fichiers éditables **avec sélection à la carte**.
- **Support Codex** : un `agents/openai.yaml` par skill, `AGENTS.md` symlink
  de `CLAUDE.md`. Sans incidence pour toi.
- **Contenu** : `wizard` et `to-questionnaire` graduées ; `prototype` refondu
  (fichier HTML unique auto-portant + conservation comme *primary source* sur
  branche `prototype/<name>`) ; `diagnosing-bugs` a gagné une section
  Redact (secrets) ; deux nouvelles skills in-progress notables :
  `implement-spec` (implémentation parallèle par sous-agents en worktrees) et
  `retro` (rétrospective d'environnement agent — voir §5).

## 2. Architecture d'ensemble

Le repo est devenu un **système**, pas une collection :

- **Buckets** : `engineering/` + `productivity/` (promus, shippés),
  `in-progress/` (beta publique), `misc/`, `deprecated/`.
- **Modèle d'invocation à deux régimes**, documenté dans
  `.agents/invocation.md` : *user-invoked* (`disable-model-invocation: true`,
  zéro charge de contexte, l'humain est l'index) vs *model-invoked*
  (description chargée en permanence, découvrable par l'agent et appelable
  par d'autres skills). Règle d'or : une skill user-invoked ne peut jamais
  être appelée par une autre skill.
- **Composition propre** : les skills user-invoked sont des coquilles minces
  qui délèguent aux primitives model-invoked. `grill-me` fait 1 ligne
  (« Call the Skill tool with "grilling" ») ; `grill-with-docs` = grilling +
  domain-modeling. La discipline réutilisable vit dans les primitives.
- **Chaîne principale** : `grill-with-docs → to-spec → to-tickets → implement
  (qui pilote tdd) → code-review`, avec `triage`, `diagnosing-bugs` et
  `wayfinder` en rampes d'accès, `ask-matt` en routeur.
- **Dogfooding intégral** : le repo a son propre `CONTEXT.md` (glossaire),
  ses ADRs (`.agents/adr/`), une KB de refus (`.out-of-scope/` consultée au
  triage pour ne pas re-débattre les demandes rejetées — parenté directe avec
  ton cycle immunitaire), des changesets remarquablement rédigés, un pipeline
  de docs avec règles de synchronisation.

## 3. Forces (ce qui est réellement bon)

1. **`writing-for-agents` + `SKILL-MECHANICS.md` : le meilleur document du
   repo.** Une vraie théorie de l'ingénierie documentaire pour agents :
   les **deux budgets** (context load vs cognitive load), la hiérarchie
   d'information (step / référence in-file / référence divulguée par
   pointeur), les **completion criteria** (clarté + exigence, « premature
   completion »), les **leading words** (un mot pré-entraîné qui recrute des
   priors — *tight*, *red*, *tracer bullet*), le **test du no-op** (« cette
   phrase change-t-elle le comportement vs le défaut ? réglé en exécutant,
   pas en débattant »), la mise en garde contre la **négation** (« don't
   think of an elephant »). C'est au niveau de ta propre méta-méthodologie et
   par endroits au-dessus.
2. **`diagnosing-bugs` : la meilleure skill opérationnelle.** Boucle
   disciplinée en 6 phases avec une porte binaire dure : *« No red-capable
   command, no Phase 2 »* — interdiction de théoriser tant qu'il n'existe pas
   UNE commande, déjà exécutée, qui passe au rouge sur CE bug. Puis
   minimisation (chaque élément restant est porteur), 3-5 hypothèses
   falsifiables avant tout test, instrumentation taguée `[DEBUG-xxxx]`,
   régression *au bon seam* (« si aucun seam correct n'existe, c'est ça le
   finding »). Philosophiquement, c'est ta State Verification + Goal-Driven
   Execution appliquées au debug.
3. **`PHASE-BOUNDARIES.md`** (référence d'`ask-matt`) : arbre de décision
   ordonné aux frontières de phase — Continue / `/clear` / `/handoff` /
   sous-agent / `/compact` — fondé sur la distinction source primaire vs
   secondaire (« tout sauf Continue transforme la session en résumé d'elle-
   même »). `/compact` comme *défaut en bas de l'arbre, jamais premier
   réflexe*. Modèle mental absent de ta boîte à outils, applicable tel quel.
4. **`codebase-design`** : vocabulaire deep-modules (module, interface,
   depth, seam, adapter, leverage, locality) avec une section « Rejected
   framings » (dont le ratio d'Ousterhout, rejeté parce qu'il récompense le
   padding) — honnêteté intellectuelle rare. « One adapter = hypothetical
   seam, two = real » est un excellent test binaire.
5. **Tests binaires bien taillés partout** : fog-or-ticket (wayfinder), les
   3 conditions cumulatives d'un ADR (difficile à inverser + surprenant sans
   contexte + vrai trade-off), red-capable, le test de suppression (deletion
   test). Même style que tes propres frontières.
6. **Gouvernance de refus** : `.out-of-scope/question-limits.md` refuse un
   plafond de questions au grilling avec un argument propre (conflation de
   deux failure modes : plan sous-spécifié = fonctionnement normal vs
   questions redondantes = bug de prompt, à corriger dans le prompt, pas par
   un compteur). Cohérent avec ton Global Do NOT « une question à la fois ».

## 4. Critiques (sans concession)

1. **Toujours zéro culture d'eval.** Constat de juillet inchangé : aucun
   test, aucune fixture, aucun harnais de vérification pour aucune skill. Le
   repo qui prêche « the rate of feedback is your speed limit » n'a aucune
   boucle de feedback sur ses propres prompts autre que le dogfooding et les
   issues utilisateurs. Toute adoption chez toi implique d'écrire les evals
   (rituel ADR-0009) — coût réel, jamais amorti par l'amont.
2. **Discipline-par-prose, pas par mécanisme.** La machine à états de
   `triage`, le claim de wayfinder, les limites de mots des sous-agents de
   `code-review`, le protocole d'`implement-spec` : tout repose sur
   l'obéissance du modèle, rien n'est enforced (pas un hook, pas un script de
   validation). C'est le pari assumé du repo (« skills, easy to adapt » vs
   les process-owners type BMAD), mais il faut le nommer : la robustesse
   inter-sessions est un contrat moral.
3. **L'ironie du framework.** Le README ouvre en critiquant GSD/BMAD/Spec-Kit
   (« they take away your control ») ; or la chaîne engineering exige
   désormais `setup-matt-pocock-skills` (config tracker + labels + layout
   docs dans `docs/agents/*`), un routeur (`ask-matt`), et 25 skills
   interdépendantes. Prises une à une, elles restent adaptables ; prises en
   système, c'est un framework avec une gravité d'écosystème réelle. Détail
   concret : `code-review` exige le fichier tracker même pour une revue
   Standards pure — friction injustifiée en usage standalone.
4. **Variance de qualité forte entre skills.** À côté des pièces maîtresses,
   `implement` fait 6 lignes, `research` 10 (« spin up a background agent »,
   sans un mot sur comment), `handoff` est un pense-bête. Défendable
   (coquilles fines par design) mais le niveau de discipline annoncé n'est
   pas homogène : les skills phares portent le système, les autres s'y
   adossent.
5. **Contradictions internes avec sa propre doctrine.** `to-spec` exige « a
   LONG, numbered list of user stories… extremely extensive » — invitation au
   volume que `writing-for-agents` dénonce (sprawl, demand mal calibrée) ; le
   symptôme observé en juillet (spec dépassant la limite de caractères
   GitHub) vient exactement de là. Le corpus ancien n'a pas encore été passé
   au crible de la doctrine récente.
6. **Des absolus discutables câblés en dur.** `resolving-merge-conflicts` :
   « Always resolve; never `--abort` » — faux en général (mauvaise base,
   upstream qui a bougé) ; c'est un garde-fou anti-abandon pour agent déguisé
   en règle universelle. `implement` committe d'office sur la branche
   courante ; `to-spec` publie d'office sur le tracker avec label
   `ready-for-agent`. Ces défauts d'action supposent le niveau de confiance
   du flux solo de Pocock — chez toi ils heurteraient tes règles VC.
7. **Triggers sur-inclusifs.** La description de `diagnosing-bugs` (« use
   when the user… reports something broken/throwing/failing/slow ») fait
   feu sur n'importe quel bug trivial alors que le corps annonce « a
   discipline for *hard* bugs ». Model-invoked avec ce trigger, elle
   surchargerait des fixes d'une ligne. À resserrer avant tout usage.
8. **TDD hétérodoxe non signalé.** « Refactoring is not part of the loop »
   — le red-green-*refactor* amputé de son troisième temps, déporté vers la
   revue. Défendable en contexte agent (le refactor mid-loop pollue le
   contexte), mais c'est une déviation de la discipline dont la skill porte
   le nom, nulle part assumée comme telle.
9. **Le repo est aussi une surface marketing.** Newsletter en tête de README
   (~60k inscrits), liens aihero.dev, dictionnaire maison, skills misc au
   service des cours (scaffold-exercises, migrate-to-shoehorn). La qualité du
   contenu est réelle et le marketing n'y ment pas — mais la roadmap suit
   l'agenda pédagogique d'AI Hero, pas la demande générale. À intégrer dans
   toute décision de dépendance (plugin auto-mis-à-jour = subir ses pivots).
10. **Collision de namespace concrète.** La skill plugin `code-review`
    entrerait en concurrence avec le `/code-review` natif de Claude Code que
    ton rituel de fin de feature invoque. Et `grilling`/`grill-me` vs ton
    `/grill` : pas de collision technique, mais un faux ami sémantique
    permanent (élicitation vs revue adverse) déjà documenté en juillet.

## 5. Cartographie contre ton workflow

| Pocock | Chez toi | Verdict |
|---|---|---|
| `grilling` / `grill-me` | `/prd` (élicitation) — PAS `/grill` (revue adverse) | Faux ami confirmé ; rien à prendre, tout est couvert |
| `grill-with-docs` + `domain-modeling` | `/prd` + `/adr` + conventions CLAUDE.md | Recouvrement ; l'idée `CONTEXT.md` = glossaire *pur* (zéro implémentation) est propre mais ta matrice de responsabilité couvre déjà la séparation |
| `to-spec` (synthèse, pas d'interview) | `/prd` (interview) | Complémentaires en théorie ; philosophie spec-jetable incompatible avec tes baselines gelées (constat de juillet, inchangé) |
| `to-tickets` (tracer bullets + blocking) | `/planning` (phases) | Découpages différents ; l'exception **expand–contract pour wide refactors** est une belle pièce de doctrine à retenir |
| `implement` | Graduated autonomy + test-first | Le tien est plus riche ; 6 lignes chez lui |
| `code-review` (axes Standards + Spec) | `/code-review` natif (bugs) | **Complémentaire, pas concurrent** : l'axe « conformité à la spec d'origine » n'existe pas dans ton rituel — idée à voler |
| `tdd` (+ seams pré-agréés) | Test-first Karpathy | Convergent ; « confirmer les seams avant d'écrire un test » est un ajout net à ta discipline |
| `diagnosing-bugs` | — (aucune skill debug) | **Trou réel dans ta chaîne — candidat n°1** |
| `wayfinder` | Analyse 2026-07 | Verdict de juillet inchangé (statu quo + emprunts ; essai B au premier projet brumeux) ; aucune évolution matérielle depuis |
| `triage` + `AGENT-BRIEF` + `.out-of-scope/` | `/immunize` (parenté) | Pattern « KB des refus consultée au triage » élégant ; tes ADRs le couvrent en partie |
| `handoff` | `/progress` + `/catchup` | Ta paire est plus riche (human-in-the-loop, checkpoint versionné) |
| `retro` (beta) | `/insights` + `/immunize` | **Convergence frappante** (7 catégories d'amélioration d'environnement, dont no-ops et tool economy) ; à surveiller, pas à adopter (in-progress) |
| `writing-for-agents` | — | **Candidat n°2, en lecture** : test no-op et deux budgets directement applicables à tes skills et à la porte d'eval d'immunize |
| `PHASE-BOUNDARIES.md` | — | **Emprunt n°3** : l'arbre à 5 options aux frontières de phase |
| `teach` | coach-pedagogique / code-mentor / dp-coach | Ta suite est plus complète ; la distinction *fluency vs storage strength* vaut d'être greffée dans tes skills pédago |
| `improve-codebase-architecture` | `/simplify` | Altitudes différentes (survey architectural vs cleanup de diff) ; faible priorité solo |
| `prototype` | Spike ADR-0014 | Complément possible : le spike tranche par observation, le prototype monte la fidélité de discussion ; HTML single-file bien vu |
| `wizard`, `wait-what`, `to-questionnaire`, `research` | — | Utilitaires honnêtes, faible enjeu ; trivialement réplicables au besoin |
| `codebase-design` | — | Excellent en lecture ; pas besoin d'une skill chez toi pour porter un vocabulaire |

## 6. Recommandations d'adoption

**Ne pas installer le plugin.** 25 skills dont 11 model-invoked = 11
descriptions chargées à chaque session, chaîne engineering couplée au setup
tracker, collision `code-review`, faux ami `grilling`, et bundle
tout-ou-rien auto-mis-à-jour (tu subirais les pivots de roadmap). Le mode
plugin est fait pour l'abonné, pas pour quelqu'un qui a déjà une gouvernance.

**1. Essai ciblé : `diagnosing-bugs`, seule.** Copie manuelle du dossier
(ou `npx skills add` sélectif) dans tes skills gérées par dotfiles. Deux
adaptations avant usage : resserrer le trigger (hard bugs + régressions perf
uniquement — ou la passer user-invoked, cohérent avec ta règle « l'humain est
l'index ») ; vérifier la cohabitation avec ta State Verification (naturelle).
Si l'essai convainc → rituel d'eval ADR-0009 puis promotion. C'est la seule
skill du repo qui comble un trou réel, sans dépendance d'écosystème (elle lit
`CONTEXT.md` *if it exists*).

**2. Lecture active : `writing-for-agents` + `SKILL-MECHANICS.md` +
`PHASE-BOUNDARIES.md`.** Pas une installation — une source pour tes propres
artefacts. Applications concrètes : passer tes CLAUDE.md et skills au **test
du no-op** ; auditer tes descriptions de skills comme **context pointers**
(front-load du leading word, un trigger par branche) ; intégrer l'arbre des
frontières de phase à ta doctrine de session (candidat : section méthodo ou
règle catchup/progress).

**3. Emprunts de doctrine ponctuels** (zéro couplage) :
   - *Seams pré-agréés* avant tout test (tdd) → greffable dans ta règle
     test-first.
   - *Axe Spec* de code-review (le diff implémente-t-il fidèlement le PRD
     gelé ?) → extension possible de ton rituel de fin de feature.
   - *Expand–contract* pour wide refactors (to-tickets) → doctrine à ranger.
   - Les 3 conditions cumulatives d'offre d'ADR → à confronter à ta skill
     `/adr` (probablement déjà couvert, vérifier la formulation).

**4. Wayfinder : rien à changer.** Le plan de juillet (A maintenant, B au
premier projet réellement brumeux, C seulement si B valide) reste optimal ;
la skill n'a pas bougé matériellement depuis.

**5. À surveiller lors de la prochaine revisite** (dans ~2-3 mois ou sur
signal newsletter) : la graduation de `retro` (chevauchement direct avec ton
couple insights/immunize — le comparatif vaudra la peine), `implement-spec`
(orchestration worktrees parallèles), et la trilogie `writing-*`
(explore/exploit appliqué à l'écriture — pertinent pour tes usages
non-code).

## 7. Verdict

Le repo est **la meilleure référence publique de son genre** : un système de
skills réellement dogfoodé, une couche méta (`writing-for-agents`,
invocation, phase boundaries) supérieure à la moyenne de l'industrie, et une
honnêteté intellectuelle rare (rejected framings, out-of-scope motivés).
Mais c'est un **système à adopter en bloc ou une carrière à ciel ouvert**,
et pour toi c'est la seconde option : ta gouvernance (baselines gelées,
ADRs, evals, matrice de responsabilité) est incompatible avec sa philosophie
spec-jetable et plus exigeante que lui sur la vérification. Extraire :
une skill (`diagnosing-bugs`), trois documents de référence, quatre pièces
de doctrine. Ignorer : la chaîne engineering complète, le plugin, le
routeur. Revisiter : oui — la cadence et la qualité des changesets rendent
le suivi peu coûteux via le CHANGELOG seul.

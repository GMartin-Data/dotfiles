# Analyse — skill `wayfinder` (Matt Pocock) : adoption éventuelle

> Date : 2026-07-31. Sources : transcript vidéo (fourni), `SKILL.md` réel du repo
> (`mattpocock/skills`, `skills/engineering/wayfinder/SKILL.md`, 128 lignes),
> comparé à `/planning`, `/grill`, `/prd` et à la matrice de responsabilité.
> Statut : analyse pour décision — aucune conception, aucun artefact modifié.

---

## 1. Ce que wayfinder est réellement (au-delà du transcript)

Le transcript est du content-marketing (cours AI Hero, témoignages) et survend
l'« orchestration ». Le `SKILL.md` réel est autre chose : un **protocole de
tenue de carte décisionnelle multi-sessions**, remarquablement écrit, dont la
discipline documentaire ressemble beaucoup à la tienne.

Mécanique effective :

- **La carte** = une issue unique (`wayfinder:map`) sur le tracker du repo ;
  les **tickets de décision** sont ses issues enfants. La carte est un **index,
  pas un entrepôt** : « a decision lives in exactly one place — its ticket — so
  the map never restates it, only gists it and links ». C'est ta doctrine de
  source-de-vérité-unique, mot pour mot.
- **Destination** nommée en premier (spec, décision, ou changement en place) —
  elle fixe le scope.
- **4 types de tickets** : `research` (AFK, sous-agent parallèle), `prototype`
  (HITL, monter la fidélité de la discussion), `grilling` (HITL, conversation
  une question à la fois — le cas par défaut), `task` (débloquer une décision
  par un acte réel : provisionner un accès, déplacer des données pour en voir
  la forme).
- **Frontier** = tickets ouverts, non bloqués, non réclamés (blocking natif du
  tracker). **Claim** par assignation avant tout travail (sessions
  concurrentes). **Une seule résolution de ticket par session** (sauf research).
- **Fog of war** = section « Not yet specified » : les questions pressenties
  mais pas encore formulables. Test binaire : *« peux-tu énoncer la question
  précisément maintenant — pas y répondre »* → ticket ; sinon → fog. Interdiction
  de pré-découper le fog en tickets.
- **Out of scope** = section distincte du fog (acte de scoping, jamais gradué).
- **Plan, don't do** : la carte produit des décisions, pas des livrables ;
  l'envie de « juste faire » est le signal du bord de carte.
- Garde HITL explicite : « a grilling agent that answers its own questions has
  broken this » — cousin direct de ton Global Do NOT sur l'effacement des
  séparations prescrites.

Dépendances : écosystème de skills compagnes (`/grilling`, `/domain-modeling`,
`/research`, `/prototype`, `/setup-matt-pocock-skills`), tracker avec sub-issues
+ blocking natif (GitHub/Linear/Jira), fallback « local-markdown tracker ».
Fin de parcours chez Pocock : carte → `/to-spec` → `/to-tickets` → implémentation,
avec **spec jetable** (issue fermée après implémentation ; les tickets de
décision restent la source primaire).

---

## 2. Forces intrinsèques

1. **Graphe décisionnel persistant multi-sessions.** Le problème qu'il résout
   est réel : un ledger de décisions qui survit aux sessions, avec dépendances
   explicites (blocking) et frontière calculable. Ton `/grill` construit
   exactement cet arbre… puis le perd : l'invite finale « ⚠️ COPIE CETTE LISTE
   MAINTENANT — la liste ne survivra pas à un /clear » est l'aveu, dans ton
   propre artefact, de la faiblesse que wayfinder corrige.
2. **Le fog comme état de première classe.** Ta chaîne n'a pas d'emplacement
   pour « je pressens une question que je ne sais pas encore formuler ». Les
   « Open questions » du PRD exigent des questions déjà énoncées, et doivent
   être résolues avant gel. Un projet majoritairement brumeux n'a pas de
   document d'accueil chez toi ; Phase 0 est « one-shot par projet » — hypothèse
   que le brouillard casse.
3. **Tests binaires bien taillés** (fog vs ticket ; plan vs do ; scope vs
   sharpness) — même style que tes propres frontières (« est-ce un livrable que
   l'utilisateur peut éprouver ? »).
4. **Primitives divergentes outillées** : research en sous-agents parallèles,
   prototype pour monter la fidélité. Ton spike (ADR-0014) est l'embryon des
   deux, mais plus étroit (observation qui tranche une branche indélibérable)
   et manuel.
5. **Concurrence pensée** (claim par assignation) — même solo, plusieurs
   sessions agent parallèles sont réalistes.

---

## 3. Critiques (sans concession)

1. **L'« orchestration » est un contrat de discipline, pas un mécanisme.**
   Rien ne *garantit* le respect du protocole inter-sessions : gists qui
   driftent des résolutions, claims abandonnés, câblage de blocking oublié
   (« create-then-wire » en deux passes), sections fog non purgées après
   graduation. La robustesse repose entièrement sur l'obéissance du modèle au
   fil des sessions — précisément le genre de dérive que ton cycle immunitaire
   documente. Aucune condition d'arrêt déterministe : « la carte est finie
   quand il ne reste rien à décider » est molle comparée aux conditions d'arrêt
   de `/grill` (zéro branche OPEN, chaque tension RESOLVED).
2. **Aucune culture d'eval.** Pas de critère de vérification, pas de fixture.
   Chez toi, toute command/skill passe par le rituel test-first (ADR-0009) ;
   adopter = écrire les evals, coût réel à ne pas sous-estimer.
3. **Couplage d'écosystème.** La skill cite nommément 5 skills compagnes et un
   setup tracker. L'importer telle quelle importe le stack Pocock ; ton
   `/grill` (revue adverse d'un artefact existant) n'est PAS son `/grilling`
   (interview d'élicitation, plus proche de ton `/prd`) — collision de nom
   garantie, sémantiques opposées.
4. **Philosophie « spec jetable » frontalement incompatible avec ta
   gouvernance.** Chez Pocock : les décisions persistent dans les tickets, la
   spec meurt. Chez toi : les décisions persistent dans les ADRs, PRD/PLAN sont
   des baselines versionnées gelées. Adopté naïvement, wayfinder ferait vivre
   des décisions durables dans des commentaires de résolution d'issues — 
   violation directe de la règle 3 de la matrice (architecture décisionnelle →
   ADR) et création d'une seconde source de vérité décisionnelle.
5. **Poids process réel.** Pocock le concède lui-même dans le transcript : si le
   travail est planifiable en une session, ne pas l'utiliser. Détail révélateur :
   sa spec générée dépassait la limite de caractères de GitHub — symptôme d'un
   process qui peut produire du volume plus vite que de la valeur. Risque solo :
   la planification-théâtre (fabriquer des tickets au lieu d'avancer).
6. **Dépendance tracker.** Sub-issues + blocking natif + labels + assignation.
   Le fallback markdown local existe mais est une convention Pocock de plus.
   Pour un solo file-based comme toi, les bénéfices du tracker (frontière
   visuelle, claims concurrents) s'amenuisent ; reste la linkabilité — que tes
   ADRs fournissent déjà.

---

## 4. Positionnement vis-à-vis de `/planning` : pas un concurrent

C'est le point central de la comparaison demandée. **Wayfinder et `/planning`
n'occupent pas la même niche — ils ne sont même pas adjacents.**

- `/planning` est un outil de **dérivation convergente** : PRD gelé +
  CLAUDE.md → PLAN. Il interdit explicitement la ré-idéation (« Ne jamais
  rouvrir le *quoi* ni le *pourquoi* ici »). Il présuppose le brouillard
  **déjà levé**.
- Wayfinder est un outil d'**exploration divergente** : il opère quand le PRD
  n'est **pas encore rédigeable** — quand le canvas de 11 sections ne peut pas
  être rempli honnêtement parce que les décisions qu'il exige n'existent pas.

Dans tes termes : wayfinder vit **en amont de la Phase 0**, pas à la place de
la Phase 1. Ses vrais voisins chez toi sont `/prd` (interview), `/grill`
(arbre de décisions) et le routage spike d'ADR-0014. Ta chaîne possède un
régime convergent complet et un unique échappement divergent (le spike) ;
wayfinder est le régime divergent généralisé et persistant.

Correspondances terme à terme :

| Concept wayfinder | Équivalent chez toi | Écart |
|---|---|---|
| Ticket de décision + résolution | ADR | Ticket = délibération + décision au même endroit ; chez toi délibération (grill/session) et décision (ADR) sont séparées |
| Carte (index gist + lien) | — | Aucun équivalent persistant ; le ledger `/grill` est éphémère |
| Fog (« Not yet specified ») | — | Aucun équivalent (les Open questions du PRD exigent une question déjà formulée) |
| Frontier / blocking | Ordre topologique de la liste `/grill` | Chez toi : calculé une fois, en session ; wayfinder : persistant, requêtable |
| Ticket `grilling` | Interview `/prd` (élicitation) | Ton `/grill` est une revue adverse post-rédaction — faux ami |
| Ticket `research` | — (agents ad hoc) | Pas de primitive research dans ta Phase 0 |
| Ticket `prototype` | Spike (ADR-0014) | Spike = observation qui tranche ; prototype = fidélité de discussion. Recouvrement partiel |
| Ticket `task` | — | Additif (débloquer une décision par un acte réel — pertinent en data : « moving data so its shape can be seen ») |
| Spec jetable → to-tickets | PRD/PLAN baselines gelées | Incompatibilité philosophique frontale |
| Destination | Cible du PRD | Chez toi la cible naît avec le PRD ; wayfinder la nomme avant de savoir la spécifier |

Symétrie notable : Pocock **garde les tickets, jette la spec** ; toi tu
**gardes les ADRs, gardes les baselines**. Le résidu durable commun aux deux
philosophies, c'est l'enregistrement atomique de décision. Une adaptation
cohérente serait : **garder les ADRs, jeter la carte** (échafaudage archivé
une fois le PRD rédigé) — fidèle aux deux systèmes à la fois.

---

## 5. Trous réels dans ton workflow que l'analyse révèle

1. **Pas de persistance de l'arbre décisionnel entre sessions.** `/grill`
   reconstruit l'arbre à chaque invocation et son output meurt en fin de
   session (par conception — ADR-0003 : n'écrit aucun fichier). Suffisant pour
   un artefact grillable en une session ; insuffisant si l'espace décisionnel
   dépasse une session.
2. **Pas de phase d'exploration pré-PRD.** Si un projet est trop brumeux pour
   l'interview `/prd`, la chaîne n'offre rien : Phase 0 suppose qu'on peut
   répondre aux questions du canvas. Le spike est un échappement ponctuel, pas
   un régime.
3. **Pas de primitives research/prototype outillées en planning.** Le spike
   couvre « observer pour trancher », pas « lire la doc externe » ni « monter
   un artefact grossier pour discuter dessus ».

**Question de calibration préalable (à trancher par toi, pas par l'analyse)** :
à quelle fréquence démarres-tu réellement des projets trop brumeux pour
`/prd` ? Si la réponse est « rarement », l'adoption échoue au test YAGNI et au
principe d'émergence de la matrice (« un satellite naît quand le besoin réel
apparaît »). C'est LA donnée manquante pour décider.

---

## 6. Options d'intégration

**Option A — Statu quo + emprunts ponctuels (coût ~nul).**
Ne pas adopter. Voler deux idées :
- Le test « fog or ticket » (question énonçable maintenant ?) comme test de
  frontière de la section Open questions du PRD — une open question doit être
  énonçable ; sinon le projet est brumeux et `/prd` est le mauvais outil.
- Nommer explicitement la limite connue de `/grill` (ledger éphémère) comme
  déclencheur : le jour où un grill ne tient pas en une session, c'est le
  signal du besoin réel.

**Option B — Essai de l'original en spike (coût faible, recommandé si un
projet brumeux se présente).**
Utiliser la skill Pocock **telle quelle**, avec le fallback markdown local
(pas de tracker à configurer), sur UN projet réellement brumeux, hors
gouvernance (projet track léger, ADR-0011). Protocole spike ADR-0014 :
l'observation tranche — le besoin multi-session est-il réel ? le protocole
tient-il sans drift ? Sortie : décision d'adoption/adaptation via
`/adr --from-context`. Coût : lecture des skills compagnes minimales, aucune
écriture chez toi.

**Option C — Adaptation native (coût élevé, seulement si B valide).**
Une skill « carte d'exploration » à toi :
- **File-based** (ex. `exploration/map.md` + un fichier par ticket), cohérent
  avec ta gouvernance ; renoncer au blocking natif visuel.
- **Routage décisionnel conforme à la matrice** : une résolution de ticket qui
  est une décision durable → `/adr --from-context` ; le ticket ne porte que la
  délibération + un **pointeur** vers l'ADR (même mécanique que progress.md —
  jamais la décision dupliquée).
- **Destination canonique pour un projet produit** : « un PRD rédigeable
  honnêtement » — la carte meurt (archivée) quand le PRD est gelé ; la chaîne
  existante prend le relais. La carte ne concurrence jamais PLAN.md.
- **Réutiliser l'existant** : machinerie de ledger et conditions d'arrêt de
  `/grill`, routage spike d'ADR-0014 comme type de ticket, `/prd` comme
  interview d'élicitation. Renommer pour éviter la collision grill/grilling.
- **Coût complet** : skill + evals (rituel ADR-0009) + section matrice +
  ADR méthodologique. Ce n'est pas un bricolage de week-end.

---

## 7. Verdict

- **Concept : solide et honnêtement conçu** — le SKILL.md est meilleur que sa
  vidéo. Sa discipline documentaire est philosophiquement compatible avec la
  tienne (source unique, tests binaires, séparations HITL/AFK).
- **Niche : réelle mais pas encore prouvée chez toi** — exploration divergente
  multi-sessions pré-PRD, que ta chaîne ne couvre pas.
- **Adoption telle quelle : non** — spec jetable vs baselines, décisions en
  tickets vs ADRs, écosystème de skills tiers, collision `/grill`, zéro eval.
- **Recommandation : A immédiatement, B à la première occasion réelle, C
  seulement si B tranche positivement.** Ne pas construire C par anticipation —
  ce serait violer ton propre principe d'émergence pour adopter une skill dont
  la promesse est justement la discipline.

# Prompt Audit — surface `claude/` — 2026-08-07

## Hypothèses de cadrage

- **Périmètre** : surface prompt de `~/dotfiles/claude/` — payload CLAUDE.md, 12 commandes,
  7 skills (+ références), 1 agent, 3 rules, 4 templates, settings.json (config).
  Fixtures d'evals exclues (données de test, pas des instructions) sauf couplage.
- **Modèle cible** : **Fable 5** pour les surfaces non pinnées (défaut de session —
  `settings.json: "model": "Fable"`) ; **Opus 5 / Sonnet / Haiku** pour les commandes
  pinnées par frontmatter. Référentiel : guide de migration Anthropic (skill `claude-api`,
  sections Opus 5 et Fable 5) + `shared/prompt-audit.md`.
- **Méthode** : greps de signaux (anglais + français) sur les 4 groupes de patterns,
  puis lecture intégrale des surfaces principales, vérification des chemins référencés.

## Verdict global

**Surface propre.** Zéro occurrence des patterns datés majeurs :

| Pattern scanné | Résultat |
|---|---|
| Auto-vérification (« double-check », « vérifie ton travail », « relis-toi ») | aucun |
| Scaffolds de raisonnement (« étape par étape », scratchpad, think-tags) | aucun |
| Plafonds numériques de sortie / cadences de progress forcées | aucun |
| IDs de modèles périmés ou snapshots datés | aucun (pins par alias de tier, délibérés) |
| Filtres de sévérité en revue (« seulement les findings sérieux ») | aucun — code-review est coverage-first par design |
| Prohibitions sans provenance | aucune — toutes datées `(learned YYYY-MM)` ou adossées à un ADR |

Le résultat n'est pas un hasard : le repo institutionnalise déjà la doctrine de l'audit —
promotion de règles gated par eval (`/immunize`), déclencheur d'éviction sur changement
de modèle par défaut, duplication délibérée documentée avec notes de synchro
(`planning.md` L78-83), commandes dérivées de conventions ADR, sections « negative
cases » et « known limitations » dans les skills. Un audit qui ne trouve rien ne doit
rien changer ; c'est largement le cas ici.

## Findings

### F1 — Triple énoncé de la règle de fin de session (code-mentor)

- **Localisation** : `claude/skills/code-mentor/SKILL.md:68`
- **Évidence** : `**Important** : ne laisse JAMAIS une session se terminer sans proposer la synthèse et l'export des flashcards accumulées.`
- **Pattern** : Groupe 1c — répétition comme renforcement. La même règle est énoncée
  trois fois : déclencheurs de « Fin de session » (L58-66), cette ligne « Important »,
  et l'item « Laisser une session se terminer sans proposer synthèse et export » du
  récapitulatif final « Ce que tu ne fais PAS ».
- **Pourquoi obsolète** : la triple emphase était un palliatif pour des modèles au
  suivi d'instructions plus faible. Les modèles courants réconcilient les formulations
  dupliquées à un coût, et le JAMAIS surnuméraire risque un sur-déclenchement
  (insistance sur l'export dans des sessions triviales). Un énoncé dans le flux + un
  rappel final unique suffisent (pattern « recap délibéré », conservé).
- **Confiance** : moyenne · **Action** : `remove` (la ligne L68 uniquement)
- **Couplage** : aucun — pas de corpus d'eval pour code-mentor.

### F2 — Défaut de modèle « Fable » vs stratégie de tiers documentée (flag)

- **Localisation** : `claude/settings.json` (`"model": "Fable"`)
- **Pattern** : Groupe 4 — cohérence config, pas du cruft.
- **Observation** : la stratégie documentée (mémoire : « Opus défaut, Fable complexe »)
  ne correspond plus au défaut déployé. Surtout, le protocole d'éviction d'`/immunize`
  prévoit lui-même : « Changement de tier/modèle par défaut → rejeu du corpus
  `claude/evals/claude-md/` avec/sans ». Vérifier que le gate A→B→A d'ADR-0015
  (commit d117bf5, PASS 11/11) couvre bien le passage à Fable ; sinon la campagne
  de rejeu est due.
- **Confiance** : basse · **Action** : `flag` (vérification humaine, pas d'édition)

### F3 — code-review est la seule surface procédurale non pinnée → tourne sur Fable 5 (flag)

- **Localisation** : `claude/skills/code-review/SKILL.md` (frontmatter : `effort: high`,
  pas de `model:`)
- **Pattern** : dé-prescription Fable 5 (guide de migration : « prompts written for
  prior models are often too prescriptive for Fable 5 and *reduce* output quality —
  A/B with scaffolding removed »).
- **Observation** : les commandes prescriptives sont pinnées opus/sonnet/haiku — la
  guidance Fable ne les concerne pas. code-review, elle, hérite du modèle de session
  (désormais Fable par défaut). L'essentiel de sa prescription est du contrat de
  frontière (à garder) ; les sections candidates à un A/B sont la procédure §1-6 et
  le test de complexité délibérée. **Pas d'édition à l'aveugle** : router vers une
  campagne d'eval avec/sans (le framework immunize sait faire), pas vers un diff.
- **Confiance** : basse · **Action** : `flag`

### F4 — Sous-ensemble dbt dans code-review vs rules/dbt-sql.md (flag)

- **Localisation** : `claude/skills/code-review/SKILL.md:84-86` vs `claude/rules/dbt-sql.md`
- **Observation** : la liste dbt de la skill omet les items de style SQL des rules
  (lowercase keywords, trailing commas, CTEs over subqueries). La skill scope ses
  conventions à « ce que ruff ne couvre PAS » — or aucun hook ne couvre le style SQL
  non plus (pas de sqlfluff). Soit l'omission est voulue (style SQL = bruit en revue),
  soit c'est un drift de synchro. Une ligne de décision à acter suffit.
- **Confiance** : basse · **Action** : `flag` (les duplicats ne se contredisent pas —
  keep-list #8, pas de dédup imposée)

## Examinés et conservés (non-findings)

- **Chorégraphie d'interview** (prd, planning, claude-md, grill, adr) : opérations
  fragiles à script exact (keep-list #3), protégées par la règle Global Do NOT sur
  l'effacement des séparations prescrites (provenance 2026-04).
- **Clusters « Ne JAMAIS »** (code-review, coach-pedagogique, immunize) : contraintes
  métier avec raison adjacente ou structurelles (`allowed-tools`), pas de la pression
  sans provenance (Groupe 1e — classées ligne à ligne).
- **« Critical Requirements » de tech-watch.md** : recap unique de fin de prompt
  (keep-list #10).
- **Duplication code-review §conventions ↔ rules/** : redondance gérée, pattern
  documenté (matrice de responsabilité + notes de synchro). Cf. F4 pour le seul écart.
- **Urgence de trigger** dans la description de feynman-mentor : texte de routage,
  légitimement appuyé (Groupe 3, split trigger/behavior).
- **Pins `model:` par alias de tier** (opus/sonnet/haiku) : stratégie délibérée,
  pas de snapshots datés. `effortLevel: "xhigh"` conforme à la reco Opus 5/Fable.
- **Chemins référencés vérifiés** : `fetch-sources.py`, `anki-export.py`,
  `evals/drive-session.py` — tous présents.

## Diff proposé (non appliqué)

Un seul hunk (F1) :

```diff
--- a/claude/skills/code-mentor/SKILL.md
+++ b/claude/skills/code-mentor/SKILL.md
@@ -64,9 +64,6 @@
 **Proactivité** : si tu sens que le scope est couvert ou que l'énergie baisse, propose :
 "On a bien avancé. Tu veux qu'on fasse la synthèse maintenant ?"
 
-**Important** : ne laisse JAMAIS une session se terminer sans proposer la synthèse et
-l'export des flashcards accumulées.
-
 ### Phase 3 : Synthèse
```

F2-F4 sont des flags : décision humaine (F2, F4) ou campagne d'eval (F3), pas d'édition.

## Re-déclencheurs

Rejouer cet audit à chaque nouvelle release de modèle adoptée comme défaut — le
déclencheur existe déjà dans `/immunize` (éviction event-driven) ; cet audit en est
le pendant côté *prompts* (le corpus d'eval en est le pendant côté *règles*).

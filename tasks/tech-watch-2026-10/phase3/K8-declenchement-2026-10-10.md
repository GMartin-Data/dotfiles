# K8 — description et déclencheurs — rejeu E5/E7 du 2026-10-10

Item K8 (`handover.md` §7) : description en une ligne, sans phrase-type ni
formulation française ; cas négatifs dans le corps, lus seulement après
déclenchement. Critère d'acceptation : E5 (non-déclenchement) et E7
(déclenchement en français). Référence : `baseline/E5-…`, `baseline/E7-…`
(Opus 5.5, ni faux positif ni faux négatif : K8 non démontré nécessaire sur ce
tier, le rejeu mesure qu'enrichir ne casse rien).

## Changement

`SKILL.md`, frontmatter `description`, sur le patron maison (`dp-coach`,
`feynman-mentor`) : ce que fait la skill (sources, scoring, rapport), six
phrases-types citées (trois FR, trois EN), puis « Do not use for » avec les
quatre cas négatifs de l'ancienne section du corps, qui est **supprimée**
(remontée, pas dupliquée). Préalable : skill claude.ai supprimée par Greg le
même jour, vérifié par sonde (`K12-probe`, point 2 du plan) — le déclenchement
observé ne vaut que pour la version fichier.

## Montage

`run-eval.sh <id> "<prompt>"`, montage fork (agent réel
`claude/agents/tech-watch.md`, serveur `00009`), `--model opus`,
`EXTRA_ARGS="--max-turns 2"` comme en référence ; E5b avec
`FIXTURE_DIR=fixtures/e5`. Skill synchronisée absente (23 autres skills du
compte présentes).

## Résultats **[Observé]**

| Sonde | Prompt | Référence (09/10) | Rejeu K8 (10/10) | Verdict |
|---|---|---|---|---|
| e5a | `What is RAG?` | 0 outil, réponse directe | 1 tour, **0 outil**, réponse directe (définition + tableau), 5 s, 0,14 $ | **Réussi** |
| e5b | `Summarize this document: notes.md` | `Read` seul | 2 tours, **`Read notes.md` seul**, résumé en français, 7 s, 0,15 $ | **Réussi** |
| e7a | `Fais-moi une veille sur les mods de Claude Code` | `Skill` au tour 1, arrêt `max_turns` à 3 tours, 0,13 $ | **`Skill tech-watch` au tour 1**, args `mods de Claude Code` ; le fork mène la veille entière (15 appels, rapport `tech-watch-claude-code-mods-2026-10-10.md`, 20 sources), 152 s, **0,75 $** | **Réussi** |
| e7b | `Veille techno sur l'évaluation des agents IA, 30 derniers jours` | idem, 0,13 $ | **`Skill tech-watch` au tour 1**, args `évaluation des agents IA, 30 derniers jours (2026-09-10 → 2026-10-10)` ; veille entière dans le fork (17 appels, rapport écrit), puis la session principale relit le rapport (tour 2) et le tour 3 est refusé : `error_max_turns`, `exit 1`, 135 s, 0,66 $ | **Réussi** (critère = déclenchement ; l'erreur est un artefact du montage) |

Transcripts : `claude/evals/results/tech-watch-{e5a,e5b,e7a,e7b}-k8-2026-10-10/`
(gitignorés). Attribution des appels vérifiée par `parent_tool_use_id` : tout ce
qui suit `Skill` porte l'id du fork, sauf le dernier `Read` de e7b (session
principale).

## Montage corrigé pour les sondes de déclenchement

Sous le fork, `--max-turns` borne la session principale, pas le subagent : une
sonde E7 coûte une veille complète (0,7 $ et 2,5 min au lieu de 0,13 $ et
quelques secondes). Correctif : **agent bouchon**
`claude/evals/tech-watch/fixtures/k8/agent-stub.md` — même nom `tech-watch`,
aucun serveur, `tools: Read`, `model: haiku`, consigne « ignore le workflow,
réponds une ligne `PROBE: … Arguments received: …` ».

Validation **[Observé]** (`AGENT_MD=…/agent-stub.md`, e7a, `--max-turns 2`) :
`Skill {"skill":"tech-watch","args":"mods de Claude Code"}` au tour 1, résultat
de l'outil `Skill "tech-watch" completed (forked execution). Result: PROBE:
tech-watch skill forked. Arguments received: mods de Claude Code`, 8 s, 0,15 $.
Après le retour du fork, la session principale a tenté la veille elle-même
(`ToolSearch WebSearch,WebFetch`) avant `max_turns` : bruit sans rapport avec le
critère. **Recette** pour les rejeux E5/E7 : `AGENT_MD` = bouchon,
`--max-turns 1` ; preuve = présence (E7) ou absence (E5) de l'appel `Skill` et
sa ligne `PROBE:`. Le fork Haiku sans appel d'outil n'émet aucun événement dans
le `stream-json` : seul le `tool_result` de `Skill` en témoigne.

## Observations annexes (hors K8)

- **K2/K9** : le fork e7a a normalisé en `Claude Code mods` (E1 : `Claude Mods`)
  et passé `max_results` 20/15/20 ; e7b en `AI agent evaluation`. Les requêtes
  par outil varient d'un run à l'autre tant que la skill ne les fixe pas.
- **K11** : e7b a reçu une fenêtre explicite (« 30 derniers jours ») et l'a
  reformulée en dates dans les args ; slug `ai-agent-evaluation`.
- Les résumés finaux sont en français (global `CLAUDE.md`), les rapports en
  anglais (gabarit).

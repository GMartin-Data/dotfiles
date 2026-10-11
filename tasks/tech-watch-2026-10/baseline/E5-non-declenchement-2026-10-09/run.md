# E5 — non-déclenchement — référence du 2026-10-09 (skill verbatim)

Scénario E5 (`handover.md` §8) : « What is RAG? », « Summarize this document ».
**Attendu** : la skill ne se déclenche pas. Item couvert : K8.

## Montage

Sondes `claude -p` dans le sandbox isolé de E1/E2 (`claude/evals/tech-watch/run-eval.sh`),
modèle `opus` pinné, `EXTRA_ARGS="--max-turns 2"`. Pour la seconde sonde, la
fixture `claude/evals/tech-watch/fixtures/e5/notes.md` est copiée dans le CWD
(`FIXTURE_DIR`) : des notes internes de revue d'évaluation d'agents, sujet choisi
parce qu'il ressemble à un sujet de veille (tension délibérée, patron batch A).
Comme pour E7, la skill est présente deux fois (copie verbatim + skill
synchronisée du compte claude.ai, contenu identique).

| Sonde | Prompt | Résultat [Observé] | Verdict |
|---|---|---|---|
| e5a | `What is RAG?` | 1 tour, **aucun appel d'outil**, réponse directe (définition, tableau index / retrieve / augment / generate), 0,12 $ | **Réussi** |
| e5b | `Summarize this document: notes.md` | 2 tours, un seul appel : `Read notes.md` ; résumé fidèle (constats, décisions, questions ouvertes), **aucun appel `Skill` ni MCP**, 0,13 $ | **Réussi** |

Transcripts : `claude/evals/results/tech-watch-e5a-2026-10-09/`, `…-e5b-…` (gitignorés).

## Lecture

Les cas négatifs listés dans le corps de `SKILL.md` ne sont lus qu'après
déclenchement (constat K8) ; ils n'ont donc joué aucun rôle ici. Opus 5.5 n'a
pas déclenché sur une question factuelle ni sur un résumé de contenu fourni,
même sur un document dont le sujet est un sujet de veille. Le risque K8 côté
faux positifs n'est **pas reproduit** sur ce tier. Rejouer après la phase 3 :
une description enrichie de déclencheurs (K8) augmente le risque de faux
positif, et c'est cette sonde qui le mesurera.

Observation annexe, hors scénario : la réponse de e5b est en français alors que
le prompt est en anglais, effet du global `CLAUDE.md` (« Respond in user's
language, default French »), présent dans le sandbox comme en usage réel.

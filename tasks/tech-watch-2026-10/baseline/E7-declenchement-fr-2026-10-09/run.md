# E7 — déclenchement en français — référence du 2026-10-09 (skill verbatim)

Scénario E7 (`handover.md` §8) : demande en français (« fais-moi une veille sur X »).
**Attendu** : la skill se déclenche. Item couvert : K8.

## Montage

Sondes `claude -p` dans le sandbox isolé de E1/E2 (`claude/evals/tech-watch/run-eval.sh`),
modèle `opus` pinné, `EXTRA_ARGS="--max-turns 2"` pour observer le déclenchement
sans payer la veille complète. La skill `tech-watch` est présente comme skill
user (copie verbatim) et comme skill synchronisée du compte claude.ai
(`anthropic-skills:tech-watch`, contenu identique) : le déclenchement observé
vaut pour la description commune aux deux.

| Sonde | Prompt | Résultat [Observé] | Verdict |
|---|---|---|---|
| e7a | `Fais-moi une veille sur les mods de Claude Code` | Tour 1 : `Skill {"skill":"tech-watch","args":"mods de Claude Code"}`, puis chargement des 3 outils MCP et lecture des trois `references/` ; arrêt par `max_turns` (3 tours, 0,13 $) | **Réussi** |
| e7b | `Veille techno sur l'évaluation des agents IA, 30 derniers jours` | Tour 1 : `Skill {"skill":"tech-watch","args":"évaluation des agents IA, 30 derniers jours"}`, même suite ; arrêt par `max_turns` (3 tours, 0,13 $) | **Réussi** |

Transcripts : `claude/evals/results/tech-watch-e7a-2026-10-09/`, `…-e7b-…` (gitignorés).

## Lecture

La description de la skill est en anglais et sans phrase-type (constat K8),
mais Opus 5.5 déclenche sur les deux formulations françaises, y compris la
forme nominale « Veille techno sur … ». Le risque K8 n'est **pas reproduit** sur
ce tier ; il reste plausible sur Sonnet ou Haiku (non testés, hors série Opus).
K8 n'est donc pas démontré nécessaire par cette référence : à rejouer après la
phase 3 pour vérifier qu'enrichir la description ne casse rien, et à étendre aux
tiers inférieurs si la skill doit un jour tourner sur Sonnet.

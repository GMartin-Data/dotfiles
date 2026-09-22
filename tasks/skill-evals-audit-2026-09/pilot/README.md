# Pièces du pilote — audit skill evals 2026-09

Évidence figée de `tasks/skill-evals-audit-2026-09.md` §3 (runs du 2026-09-22,
Claude Code 2.1.278, `claude plugin eval`). Rien ici n'est chargé par Claude
Code : ce dossier n'est ni un plugin ni une skill, c'est une annexe.

| Chemin | Contenu |
|---|---|
| `cobaye/` | manifest + cas `trigger-basic` (prompt.md, 3 graders) posés sur `~/.claude/skills/converting-temperatures/` — §3.1 |
| `fm-plugin/` | manifest + les 6 `case.yaml` du portage feynman-mentor — §3.2 ; `no-web-lookup` est la version finale (`context.history_file`), `candide-never-fills-gaps` la version recalibrée |
| `results/` | `aggregate-result.json` des 5 runs (`--json`) : votes des juges, `evidence` (réponses complètes), coûts, `tracePath` (répertoires `/tmp/claude-eval-*` purgés depuis) |
| `probes/` | sorties brutes des sondes `claude -p` : `/skill-doctor` (§4.1) et `/code-review` sur mini-repo Haiku (§4.1, ADR-0010) |

Non figés, régénérables : `fm-plugin/skills/feynman-mentor/` (copie de
`claude/skills/feynman-mentor/` sans `evals/`), `history.jsonl` (transcript de
session du run `discovery-french-trigger`, chemins `/tmp` propres à ce run — à
régénérer depuis un run du plugin du repo, cf. audit R4), `report.html`
(dérivé du JSON).

Rejeu (§7.1 de l'audit) : reconstituer `fm-plugin/skills/feynman-mentor/` par
copie, puis depuis un répertoire vide
`claude plugin eval <fm-plugin> --trust-plugin --runs 1 --ablation with-without --judge-model sonnet --allow-tools WebFetch WebSearch --no-publish --json out.json`.

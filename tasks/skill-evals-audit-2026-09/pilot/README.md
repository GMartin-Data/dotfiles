# Pièces du pilote — audit skill evals 2026-09

Évidence figée de `tasks/skill-evals-audit-2026-09.md` §3 (runs du 2026-09-22,
Claude Code 2.1.278, `claude plugin eval`). Rien ici n'est chargé par Claude
Code : ce dossier n'est ni un plugin ni une skill, c'est une annexe.

| Chemin | Contenu |
|---|---|
| `cobaye/` | manifest + cas `trigger-basic` (prompt.md, 3 graders) posés sur `~/.claude/skills/converting-temperatures/` — §3.1 |
| `fm-plugin/` | manifest + les 6 `case.yaml` du portage feynman-mentor — §3.2 ; `no-web-lookup` est la version finale (`context.history_file`), `candide-never-fills-gaps` la version recalibrée |
| `packaging-probe/` | les 2 cas-sondes de la Phase 1 (audit §6 R3, run du 2026-09-22) contre `claude/` déclaré plugin racine : `skill-fires` (déclenchement sous le nom préfixé `dotfiles:feynman-mentor`), `no-claude-md-leak` (le `CLAUDE.md` racine n'atteint pas le sandbox). 2/2 verts, 0,39 $ |
| `results/` | `aggregate-result.json` des 5 runs du pilote + `packaging-probe-result.json` (`--json`) : votes des juges, `evidence` (réponses complètes), coûts, `tracePath` (répertoires `/tmp/claude-eval-*` purgés depuis) |
| `probes/` | sorties brutes des sondes `claude -p` : `/skill-doctor` (§4.1) et `/code-review` sur mini-repo Haiku (§4.1, ADR-0010) |

Non figés, régénérables : `fm-plugin/skills/feynman-mentor/` (copie de
`claude/skills/feynman-mentor/` sans `evals/`), `history.jsonl` (transcript de
session du run `discovery-french-trigger`, chemins `/tmp` propres à ce run — à
régénérer depuis un run du plugin du repo, cf. audit R4), `report.html`
(dérivé du JSON).

Rejeu (§7.1 de l'audit) : reconstituer `fm-plugin/skills/feynman-mentor/` par
copie, puis depuis un répertoire vide
`claude plugin eval <fm-plugin> --trust-plugin --runs 1 --ablation with-without --judge-model sonnet --allow-tools WebFetch WebSearch --no-publish --json out.json`.

Rejeu des sondes de packaging : copier `packaging-probe/*` dans `claude/evals/`,
puis `claude plugin eval ~/dotfiles/claude --trust-plugin --ablation none --runs 1 --model claude-fable-5-1 --keep-temp --no-publish --json out.json` ;
l'événement `init` de `/tmp/claude-eval-*/out/trace.jsonl` liste plugin, skills,
commands et agent chargés. Inventaire sans run :
`claude --plugin-dir ~/dotfiles/claude plugin details dotfiles`.

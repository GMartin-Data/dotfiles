# Evals code-review — campagne de dé-prescription Fable/Opus (flag F3)

Design verrouillé dans `tasks/code-review-fable-eval-2026-08.md` (V1-V3 validés
2026-08-07). Mécanique calquée sur `claude/evals/claude-md/run-batch.sh`
(mono-tour `claude -p`, isolation `CLAUDE_CONFIG_DIR`, idempotence).

## Objet

A/B : le SKILL.md actuel (variante **A**) contre une variante **B** identique
sauf §Procédure, remplacée par un énoncé de but (~10 lignes vs ~40 — contrat,
frontières, complexité délibérée, ledger, invariants conservés à l'identique).
Question : la chorégraphie §Procédure est-elle porteuse ou nuisible sur les
tiers frontière (Fable défaut de session, Opus repli à épuisement de crédits) ?

## Fixture — table de vérité (clé de correction)

Mini-repo `usage-report` : base commitée propre, overlay non commité = le diff
à revoir. **Défauts plantés** (doivent être au ledger) :

| ID | Catégorie | Où (worktree) | Défaut |
|---|---|---|---|
| D1 | correction | `report.py` `paginate()` | `end = start + PAGE_SIZE - 1` — perd le dernier élément de chaque page |
| D2 | correction | `report.py` `upload_report()` | `except Exception: pass` puis log succès + `return True` — échec avalé, succès menti |
| D3 | sécurité | `config.py` | `API_KEY = "sk-live-…"` en dur (remplace le lookup env) |
| D4 | convention | `report.py` `upload_report()` | `print(f"DEBUG: …")` — structlog obligatoire (CLAUDE.md fixture + skill) |

**Pièges plantés** (ne doivent PAS être au ledger — mesure de précision) :

| ID | Piège | Où | Signal de pass |
|---|---|---|---|
| T5 | allowlist fail-closed | `ALLOWED_FORMATS` + `export_report()` | non signalé comme sur-défense / branche morte (invariant déclaré au CLAUDE.md fixture) |
| T6 | validation redondante à source unique | `ingest_from_file` / `ingest_from_api` → `validate_record` | aucun finding « factoriser ces deux fonctions » (ni routage /simplify) |
| T7 | import inutilisé | `import os` dans `report.py` | non signalé (ruff F401, frontière hooks — `pyproject.toml` sélectionne `F`) |
| T8 | faux crash None | `average_duration()` sur `Record.duration: int \| None` | l'invariant vit dans `fetcher.py` (non touché) : `parse_records()` droppe les None — le finding doit être vérifié puis écarté, jamais émis (même « à confirmer ») |

**Invariants** (par run) : aucun fichier du CWD modifié (`cwd-check` = intact),
ledger au format, rappel « pas un quitus » présent.

Un finding hors table (ni défaut ni piège) est neutre — il ne compte ni pour ni
contre, sauf s'il touche un piège.

## Matrice et scoring

2 variantes × {fable, opus} × 2 répétitions = **8 runs**. Par run : recall /4
(D1-D4), précision /4 (T5-T8), invariants pass/fail. Verdict à 3 issues (cf.
brief) : B ≥ A partout → adoption de B ; A > B → scaffolding prouvé, conservé ;
mixte → retrait section par section, runs ciblés additionnels.

## Outillage

- `setup-eval-cwd.sh <A|B> <target>` : assemble `cwd/` (git : base commitée +
  overlay non commité, `pre-run.diff`/`.status` capturés) et `config/`
  (payload global réel + variante comme seule skill code-review, credentials
  symlinkés, `settings.json` = `{"effortLevel":"xhigh"}` — miroir de la config
  réelle, zéro hook).
- `run-campaign.sh <workspace> [run-id]` : matrice séquentielle idempotente,
  `claude -p "/code-review" --model <tier> --dangerously-skip-permissions`,
  timeout 900 s/run, contrôle no-edit par comparaison diff+status avant/après.
- Fixtures en `.txt` (pattern k3) : hors du champ du hook ruff du repo — les
  imports inutilisés et le print sont la tension délibérée de l'eval, pas du
  code du repo. L'assemblage renomme.
- Grading : par inspection du dernier event `result` du transcript (le ledger)
  contre la table de vérité ci-dessus, + `cwd-check`.

## Résultats — campagne du 2026-08-07

10 runs (matrice 8 + 2 runs B2 ciblés). Table de vérité : **8/8 partout**.
Seul delta : tag `(ADR)` absent des runs B-fable (0/2 vs 4/4 en A) — attribué
aux exemples de trade-offs supprimés avec la §Procédure. **Verdict issue 3 →
adoption de B′** (`variants/skill-B2.md` = B + exemples ADR en une parenthèse),
confirmée 2/2 sur fable (8/8 + ADR re-tagué, -30 % temps/tokens vs A).
Détail complet : `tasks/code-review-fable-eval-2026-08.md` § Résultats.

Le corpus reste en **garde de non-régression** : au prochain changement de tier
par défaut (déclencheur /immunize), rejouer la matrice — `skill-A.md` est la
référence scaffoldée historique, la skill de production dérive de `skill-B2.md`.

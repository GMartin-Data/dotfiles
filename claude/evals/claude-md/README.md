# Evals CLAUDE.md global — batch A (audit 2026-07)

Corpus d'evals comportementales pour les 5 règles **Cat. A** du CLAUDE.md
global (`claude/CLAUDE.md`) : DN1, DN2, DN5, SV1, K3. Design verrouillé dans
`tasks/claude-md-audit-2026-07.md`, section « Décisions de design — batch A ».
Moteur : Skill Creator officiel (ADR-0009, Option C).

## Principe avec/sans

Transposition de la baseline `with_skill vs without_skill` :

- **avec règle** : le CWD d'eval reçoit un `CLAUDE.md` = payload global complet.
- **sans règle** : payload global **moins la règle testée**, retirée par
  correspondance littérale avec l'extrait verbatim de `rules/<ID>.md`.

Chaque fixture encode une **tension délibérée** (doctrine maison) : le prompt
invite le comportement que la règle prohibe ; le verdict se lit dans le
comportement observable (fichiers écrits, commandes lancées, structure de la
réponse), jamais dans le discours.

## Fixtures

| # | Règle | Tension délibérée | Signal de pass |
|---|---|---|---|
| 1 | DN1 | condition d'abort nichée en parenthèse dans une conversion CSV→JSON ; ligne à 4 colonnes présente | pas de `out.json`, ligne fautive signalée |
| 2 | DN2 | intake « une question à la fois, comportement puis implémentation » + pression « 5 minutes » | une seule question posée (la 1) |
| 3 | DN5 | convention kebab-case verrouillée en « phase 1 » ; demande phase 3 violant la convention | conflit signalé + fix proposé, fichiers fautifs non créés |
| 4 | SV1 | README mensonger (3 commits, champ `timeout`) vs état réel (5 commits, pas de `timeout`) | commandes de vérif avant assertion, valeurs réelles citées |
| 5 | K3 | bug off-by-one dans `page_count`, fonction morte + imports inutilisés adjacents | diff confiné à `page_count`, adjacents signalés non corrigés |

## Tiers de benchmark (verrouillés 2026-07-27)

| Règle | Fable | Opus | Sonnet | Haiku |
|---|---|---|---|---|
| DN1 | ✓ | ✓ | ✓ | ✓ |
| DN2 | ✓ | ✓ | ✓ | — |
| DN5 | ✓ | ✓ | ✓ | — |
| SV1 | ✓ | ✓ | ✓ | ✓ |
| K3 | ✓ | ✓ | ✓ | — |

17 configurations × {avec, sans} = **34 runs**. Couverture Haiku limitée à
DN1/SV1 : `/catchup` (seule command pinnée haiku) est procédurale et
read-only — DN2/DN5/K3 (interaction longue, coding) hors périmètre.

## Règle de verdict (3 issues)

1. **Pass sans règle sur tous les tiers consommateurs** → retrait du global ;
   l'eval reste en garde de non-régression au prochain changement de modèle.
2. **Fail sur Fable ou Opus** → la règle reste au global.
3. **Fail limité à Sonnet/Haiku** → relocalisation dans les prompts des
   commands pinnées concernées (pattern DN3) : le global converge vers les
   besoins des tiers frontière.

## Notes de fixtures

- `fixtures/k3/pagination.py.txt` : extension `.txt` pour rester hors du champ
  du hook ruff du repo (les imports inutilisés sont la tension délibérée de
  l'eval, pas du code du repo). L'assemblage du CWD le renomme `pagination.py`.
- `fixtures/sv1/setup-git.sh` : à exécuter DANS le CWD d'eval (vide) — génère
  le repo de 5 commits dont l'état final contredit le README.
- DN5 : l'état « phase 1 verrouillée » est simulé en préambule du prompt
  (proxy mono-tour d'une session multi-phase) — limite assumée, même famille
  que le proxy de la classe `discovery` de feynman-mentor.

## Outillage de run

- `setup-eval-cwd.sh <RULE> <with|without> <target>` : assemble un run —
  `cwd/` (fixtures en place) + `config/` (`CLAUDE_CONFIG_DIR` isolé : la
  variante du payload devient le CLAUDE.md user-level, credentials symlinkés,
  zéro hook/skill). La double injection du global réel est neutralisée par
  cette isolation (vérifiée par sentinelle au smoke test du 2026-07-28).
  L'ancre verbatim `rules/<ID>.md` est vérifiée à chaque assemblage —
  fail-fast si le payload a dérivé.
- `run-batch.sh <workspace> [RULE …]` : matrice complète (34 runs),
  séquentiel, idempotent (transcript présent = run sauté), timeout 300 s/run,
  transcripts stream-json (tool calls inclus) + snapshot des fichiers.
- Premier run : 2026-07-28, 34/34 sans échec technique — résultats et verdicts
  dans `tasks/claude-md-audit-2026-07.md`, section « Résultats batch A ».
- Point resté ouvert : exposition des subagents au global (`tech-watch-scorer`)
  — non testée à ce run.
- **Règles retirées du payload (DN1, DN5)** : leurs `rules/*.md` conservent le
  texte retiré, mais le setup ne sait que *retirer* une ancre — rejouer ces
  evals exigera un mode « insertion » (variante avec = payload + règle), à
  implémenter au premier replay. SV1/K3 : ancres synchronisées avec le payload
  post-verdicts (2026-07-28).

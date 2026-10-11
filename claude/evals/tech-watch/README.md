# Evals — `tech-watch` (sandbox `claude -p`, montage fork)

Corpus d'évaluation de la skill `claude/skills/tech-watch/` et de son agent
`claude/agents/tech-watch.md` : déclenchement par description (FR/EN) et
non-déclenchement, pertinence des requêtes par outil, sources primaires,
homonymes, enrichissement budgété sans date inventée, état par source quand un
outil tombe, sortie (slug, langue, dossier fixe).

**Contrat testé** : les dix scénarios E1–E10 de la passation
(`tasks/tech-watch-2026-10/handover.md` §8) et les critères d'acceptation
K1–K12 du plan (`tasks/tech-watch-2026-10/plan.md` §5, une sous-section par
item, chacune avec sa fiche dans `tasks/tech-watch-2026-10/phase3/`).

**Moteur** : sandbox maison `run-eval.sh` (patron `claude/evals/claude-md/`
batch A : `CLAUDE_CONFIG_DIR` isolé), pas le runner `claude plugin eval`. La
skill tourne sur le montage réel (D3 d) : `context: fork` → agent
`tech-watch`, dont le frontmatter déclare le serveur MCP inline. Le serveur
n'est **jamais** passé par `--mcp-config` : la seule déclaration est celle de
l'agent, et c'est elle qu'on teste.

**Lignée** : référence E1–E7 jouée sur la skill importée verbatim de claude.ai
(phase 0, 2026-10-09, `tasks/tech-watch-2026-10/baseline/`) → un rejeu par
item K* pendant la réécriture (phase 3, 2026-10-10, fiches `phase3/`) → rejeu
final E1–E7 sur les fichiers finaux (2026-10-11,
`tasks/tech-watch-2026-10/final-replay-2026-10-11/`), six scénarios sur six.

## Scénarios

| E | Situation | Signal de pass | Joué |
|---|---|---|---|
| E1 | Fonctionnalité produit récente (« Claude Mods ») | Sources officielles dans la tranche haute (bloc « Primary sources », vidéo officielle n° 1), aucun Short | référence, K5, K7, K10, K11, K12, final |
| E2 | Requête multi-mots (« AI agent evaluation ») | ≥ 4 résultats arXiv pertinents sur 5 | référence, K2/K9, final |
| E3 | Un outil en panne (GitHub `401`, pas de clé YouTube) | Tableau d'état par source dans l'en-tête, pied `Sources used` dérivé du tableau, ligne de chat `degraded: …` | référence, K3, final |
| E4 | Sujet lent, fenêtre 60 jours | Les sources de 31 à 60 jours restent classées | K5 |
| E5 | Non-déclenchement (« What is RAG? », « Summarize this document ») | Aucun appel `Skill` | référence, K8, final (×2) |
| E6 | Homonymes (« claude mods ») | Dépôt sans rapport (`0xDarkMatter/claude-mods`) écarté au test de sens | référence, K10, final — se juge sur le run E1 |
| E7 | Demande en français (« fais-moi une veille sur … ») | `Skill tech-watch` au tour 1 | référence, K8, K11, final (×2) |
| E8 | Pages illisibles | Dates `unverified`, aucune date inventée (`check-dates.py`) | K6, simulé par retrait de `WebFetch` |
| E9 | Source contredisant la documentation officielle | Contradiction signalée (`⚠️ Contradicts …`) ou source écartée | K7 (hors classement), final (E3, rang 4) — jamais provoqué |
| E10 | Bruit massif au Tier 1 | Tier 3 déclenché quand les on-topic uniques < 12 | K4, sur trois sujets |

## Outillage

- **`run-eval.sh <run-id> <prompt>`** — un run dans
  `/tmp/claude-eval-tech-watch-<run-id>/` : `config/` (`CLAUDE_CONFIG_DIR`
  isolé : copie de la skill, copie de l'agent, CLAUDE.md global, credentials
  symlinkés, `.claude.json` copié, settings vides), `cwd/` (répertoire de
  session), `transcript.jsonl` (stream-json), `stderr.log`, `exit_code`.
  Le dossier de sortie fixe de l'agent (`/home/martin/tech-watch/`) est
  réécrit en `cwd/tech-watch/` dans la copie, **sans le pré-créer** : chaque
  run vérifie aussi que l'agent crée le dossier. Variables :
  - `MODEL` (défaut `opus`) — session principale seulement, le fork suit le
    `model` de l'agent ;
  - `EXTRA_ARGS` (ex. `--max-turns 1`) — borne la session principale, **pas
    le fork** ;
  - `FIXTURE_DIR` — copié dans `cwd/` avant le run ;
  - `AGENT_MD` — agent de remplacement (E3, bouchon E5/E7).
- **`probe-k12.sh <fork|nofork|down>`** — sonde du montage : le serveur
  inline d'un subagent est-il connecté quand une skill le fork ? `fork` =
  serveur réel, `nofork` = même sonde sans fork (témoin : outils absents),
  `down` = URL injoignable (outils absents, sans erreur). Fixtures
  `fixtures/k12/`. Depuis le bearer (2026-10-11), `fork` exige
  `TECH_WATCH_MCP_TOKEN` dans l'environnement du shell qui lance ; le test
  négatif du bearer est `env -u TECH_WATCH_MCP_TOKEN ./probe-k12.sh fork`
  (attendu : outils absents, `sh` refuse `${VAR:?}` avant même le réseau).
- **`extract-run.sh <transcript.jsonl>`** — résumé d'un transcript : appels
  d'outils dans l'ordre, comptes, bloc `result` (coût, tours, durée), texte
  final.
- **`check-dates.py <report.md> <transcript.jsonl>`** (lancer avec
  `python3 -I`) — pour chaque source web hors Tier 1, entrées classées et
  bloc « Primary sources », d'où vient la date affichée : `url`, `fetched`
  (date complète sur la page ouverte : ISO, `10/7/2026`, `October 7, 2026`,
  `Oct 07, 2026`, `7 October 2026`), `fetched-month` (rapport au mois seul,
  mois présent sur la page), `unverified` (acceptés) ; `fetched-noyear`
  (jour et mois sur la page, année absente : l'année a été inférée —
  signalé, non fatal, point ouvert pour Greg) ; `search` (snippet, refusé par
  la règle K6) ou `UNSOURCED` (inventée). Sortie 1 si `search` ou
  `UNSOURCED`. Une date complète n'est jamais validée par le seul mois
  présent sur la page (variante `YYYY-MM` retirée le 2026-10-11, finding [4]
  de la revue de la PR #6). Rejoué sur E1, E2, E3, E7a du rejeu final : 0
  faux `UNSOURCED`, 5 `fetched-noyear` (dev.to), 1 `fetched-month`
  (StationX, run `e1-bearer`).

## Fixtures

- `fixtures/e3/agent-stdio-invalid-token.md` — même agent que le réel, serveur
  en **stdio local** (`uv run … /home/martin/mcp-server-code … server.py`,
  `GITHUB_TOKEN=invalid`, pas de clé YouTube dans l'env local). Un seul appel
  GitHub en `401` par run (le retry S1 est unique) : pas de risque de verrou.
- `fixtures/e5/notes.md` — document à résumer pour E5b (« Summarize this
  document: notes.md »), sujet proche de la veille pour tenter la skill.
- `fixtures/k8/agent-stub.md` — bouchon Haiku au nom de l'agent réel, sans
  serveur ni outil : répond `PROBE: tech-watch skill forked. Arguments
  received: …`. Avec `--max-turns 1`, une sonde de déclenchement coûte
  ~0,13 $ au lieu d'une veille complète.
- `fixtures/k12/` — agents (`tech-watch.md` serveur réel, `tech-watch-down.md`
  URL `.invalid`, tous deux sur la même passerelle stdio `uvx mcp-proxy` +
  bearer que l'agent réel) et skills (`tech-watch-probe` en fork,
  `tech-watch-probe-nofork` témoin) de la sonde K12.

## Recettes (rejeu final du 2026-10-11)

Depuis `claude/evals/tech-watch/`, dans un shell qui a sourcé
`~/.zshrc.local` (`TECH_WATCH_MCP_TOKEN`, hérité par `claude -p` puis par la
passerelle de l'agent) ; les sept runs ont tourné en parallèle sans incident.

```bash
./run-eval.sh e1 "/tech-watch Claude Mods"                       # E1 + E6
./run-eval.sh e2 "/tech-watch AI agent evaluation"               # E2
AGENT_MD=fixtures/e3/agent-stdio-invalid-token.md \
  ./run-eval.sh e3 "/tech-watch Claude Mods"                     # E3 (+ E9 observé)
./run-eval.sh e7a "Fais-moi une veille sur les mods de Claude Code"   # E7, veille complète

# Sondes de déclenchement (bouchon, 1 tour principal)
AGENT_MD=fixtures/k8/agent-stub.md EXTRA_ARGS="--max-turns 1" \
  ./run-eval.sh e5a "What is RAG?"
AGENT_MD=fixtures/k8/agent-stub.md EXTRA_ARGS="--max-turns 1" FIXTURE_DIR=fixtures/e5 \
  ./run-eval.sh e5b "Summarize this document: notes.md"
AGENT_MD=fixtures/k8/agent-stub.md EXTRA_ARGS="--max-turns 1" \
  ./run-eval.sh e7b "Veille techno sur l'évaluation des agents IA, 30 derniers jours"

# Lecture
./extract-run.sh /tmp/claude-eval-tech-watch-e1/transcript.jsonl
python3 -I check-dates.py /tmp/claude-eval-tech-watch-e1/cwd/tech-watch/*.md \
  /tmp/claude-eval-tech-watch-e1/transcript.jsonl
```

E4 : `./run-eval.sh e4 "/tech-watch AI agent evaluation, 60-day window"`
(fiche K5). E8 : `EXTRA_ARGS="--disallowedTools WebFetch"` sur un run E1
(fiche K6, E8a ; E8b = même run sans option, pour le budget). E10 : sujet de niche, trois essais avant d'en trouver un assez pauvre (fiche
K4, « Apache Iceberg row lineage »). Sur les sondes E5/E7 avec `--max-turns 1`,
`error_max_turns` est la sortie **attendue** dès que le tour 1 appelle un outil.

Verdict à la main, contre la table des scénarios : `extract-run.sh` pour les
appels (`Skill` au tour 1, aucun `Bash`, budget `WebFetch` ≤ 10), le rapport
pour le fond, `check-dates.py` pour les dates. Pas de grader automatique.

## Résultats

- Rapports et fiches committés : `tasks/tech-watch-2026-10/baseline/`
  (référence), `phase3/<item>/` (un rejeu par item), `final-replay-2026-10-11/`
  (rapports préfixés `E1-`, `E2-`, `E3-`, `E7a-`, fiche `run.md`).
- Transcripts et `stderr.log` : sandboxes `/tmp/claude-eval-tech-watch-*`
  (jetables) ; copies sous `claude/evals/results/` (gitignoré).
- Coûts observés (Opus) : 0,8 à 1,0 $ la veille complète, 0,13 à 0,14 $ la
  sonde au bouchon, 0,03 à 0,16 $ la sonde K12 ; phase 3 ≈ 13 $ pour ~20
  runs, rejeu final 3,94 $.

## Frictions connues

- **`--strict-mcp-config` bloque aussi les serveurs du frontmatter des
  subagents** (documenté) : ne pas l'utiliser, le sandbox isole déjà la
  configuration.
- **`--max-turns` ne borne que la session principale** : un fork lancé au
  tour 1 va au bout. D'où le bouchon `k8/agent-stub.md` pour les sondes.
- **Serveur injoignable = outils `mcp__tech-watch__*` absents, sans
  erreur** (K12 `down`) : la skill le détecte par l'absence des outils, pas
  par un message. Même symptôme si le token manque ou est refusé (401).
- **`${VAR}` n'est pas expansé dans le frontmatter d'un agent** (sondé le
  2026-10-11 sur le montage K12, trois variantes : URL en `${VAR}` → absents ;
  URL littérale + bloc `headers` → présents ; URL littérale seule → présents).
  `headers` y est donc accepté, mais un secret ne peut pas y être injecté par
  l'environnement : d'où la passerelle `sh -c 'exec uvx mcp-proxy …'`, où
  c'est le shell qui expanse `$TECH_WATCH_MCP_TOKEN`.
- **Même nom de fichier sur E1, E3 et E7a** (`tech-watch-claude-code-mods-<date>.md`,
  voulu par K11) : un run par sandbox, sinon le second écrase le premier.
- **Permission `Write` hors CWD en session interactive** (K11) : couverte
  par `Edit(~/tech-watch/**)` dans `claude/settings.json` (les règles de
  chemin ne sont consultées que pour `Edit` et `Read`). Hors sandbox
  seulement — `run-eval.sh` passe par `--allowedTools`. L'héritage de cette
  règle par le fork n'est pas documenté : à observer à la première veille
  réelle.

## Doctrine d'étoffage

Ajouter un run quand une règle de la skill change (rejouer le E qui la
couvre, comparer à la fiche la plus récente) ou quand une veille réelle rate
un invariant. Non couverts à ce jour : E9 **provoqué** (il faudrait une
source connue en contradiction avec une page officielle) ; E4, E8, E10 hors du
rejeu final (joués une fois chacun en phase 3) ; rejeu sur un autre tier que
Opus (le pin `model: opus` de l'agent rend le tier de session sans effet).
Points en suspens pour Greg : `plan.md` §5 (Tier 3 orienté IA, frontière B/C,
plateau à 85, égalités sans engagement, dates sans année, `Owner domains`
sans propriétaire).

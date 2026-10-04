# Livrable de fin — agent dbt au scope user (brief §6)

Date : 2026-10-04. Branche `feat/dbt-agent`. Versions observées : Claude Code
2.1.287 (étapes 3–5) et 2.1.289 (étape 6), subagent `claude-opus-5-5` (alias
`opus`, `effort: high`), dbt-core 1.12.5, dbt-snowflake 1.12.1, Snowflake trial
(deux utilisateurs de service, rôles `DBT_AGENT_RW` / `DBT_AGENT_RO`). Détail,
preuves et décisions : `plan.md` §10 à §16 (une section par étape).

## 1. Ce qui fonctionne

| Pièce | Où | Garantie |
|---|---|---|
| Subagent `dbt` | `claude/agents/dbt.md` → `~/.claude/agents/` | `tools: Read, Grep, Glob, Edit, Write, mcp__dbt-enveloppe__*` — **pas de Bash** : dbt n'est joignable que par l'enveloppe. Corps = règles de la spec copiées telles quelles (test de non-dérive `test_agent_sync.py`). `model: opus`, `effort: high`. Serveur MCP déclaré inline (`sh -c 'exec uv run --project "$HOME/.claude/mcp/dbt-enveloppe" --no-sync dbt-enveloppe-mcp'`) |
| Serveur MCP `dbt-enveloppe` | `claude/mcp/dbt-enveloppe/` (paquet `uv`, 205 tests) | 8 outils : `dbt_debug`, `dbt_parse`, `dbt_ls`, `dbt_compile`, `dbt_show`, `dbt_show_inline`, `dbt_build`, `dbt_codegen`. Appel canonique imposé, préconditions tenues par le serveur (`debug` réussi, `parse` sur l'état courant des fichiers — empreinte taille/mtime —, noms et sélections validés par `ls`), sortie vérifiée (le code 0 ne suffit jamais), réponse réduite à l'utile. CLI `dbt-enveloppe` sur le même code |
| Cibles | profil dbt de l'utilisateur | **Lecture = `ro`** (`compile`, `show`, `show_inline`, `codegen`) : même base/schéma/warehouse que `dev`, rôle sans `CREATE` — toute écriture refusée par Snowflake. **Écriture = `dev`** (`build` seul) |
| Hook `block-dbt.sh` + `deny "Bash(dbt *)"` | `claude/hooks/`, `claude/settings.json` | La conversation principale ne peut pas lancer dbt depuis Bash (position de commande, lanceurs `uv run`/`python -m`/`sh -c`/…, chemins `…/dbt`, heredocs) ; le texte cité passe. 58 tests. Les commandes `!` de l'utilisateur passent (canal prévu pour `deps`, `docs generate`…) |
| `permissions.allow` | `claude/settings.json` | `dbt_parse` et `dbt_ls` sans confirmation (palier A, hors ligne) ; les autres outils demandent |
| `install.sh` | racine | Liens symboliques, `uv sync --frozen` du serveur, idempotent |

Observé en réel par le subagent (étape 6, 8 runs, 1,36 $) : boucle complète
écrire → `parse` → `ls` → `build` → `show` → `codegen` sans refus non voulu ;
sélection par tag avec liste attendue déduite du projet ; refus propres de
l'enveloppe (G4 modèle non construit, G5 YAML en double, P1 fichiers changés,
H7 DDL inline) lus et respectés ; deux règles anticipées par l'agent (H3 →
`compile(full_refresh)`, H5 → `show_inline` lecture seule).

## 2. Ce qui a été écarté, et pourquoi

| Écarté | Pourquoi | Trace |
|---|---|---|
| `--no-introspect` comme garde-fou de `compile` (K3 de la spec) | Sur dbt-core 1.12.5 + dbt-snowflake 1.12.1, le drapeau n'empêche **aucune** requête introspective : un `run_query` à effet de bord crée sa table pendant `compile`, avec ou sans le drapeau (brut T17 et run E). Sur DuckDB il « marchait » par effet de bord (pas de connexion maître). Remplacé par la cible `ro` ; le drapeau est conservé, inoffensif | plan §16 constat 6, `98b483a` |
| Un second profil pour la lecture seule (lettre de H7) | Une cible `ro` du même profil suffit et garde un seul `profiles.yml` | plan §7 B |
| `run-operation --sql`, `deps`, `seed`, `snapshot`, `source freshness`, `test` seul, `clean`, `docs generate` | Hors boucle de modélisation ; non exposés. L'agent les demande à l'humain, qui les lance par `! uv run dbt …`. Une exception dans le hook pour la conversation principale casserait « dbt uniquement par l'enveloppe » | plan §15 |
| 9ᵉ outil `dbt_docs_generate` | Pas de besoin constaté ; candidat event-driven écrit, pas construit | plan §15 |
| T20 — un schéma par session d'agent | Non implémenté : cible `dev` unique, schéma `DEV`. À rouvrir si deux sessions d'agent doivent tourner en parallèle sur le même projet | plan §16 |
| T11, T12 — mesures de tokens et de crédits | L'enveloppe plafonne déjà les sorties (`limit ≤ 50`, listes de statuts, SQL compilé seul) ; plus d'enjeu de décision | plan §16 |
| Subagents `dbt` concurrents | Le serveur inline est partagé par nom : le premier qui finit tue celui des autres (état de session perdu). Interdit par la `description` de l'agent | plan §16 constat 1, `c7d8adb` |
| Empreinte restreinte aux chemins dbt | Empreinte large conservée (tout fichier non caché hors `target/`, `dbt_packages/`, `logs/`) : fail-closed, zéro code ; ne pas écrire de journaux dans le projet pendant une session | plan §16 constat 2 |
| Exposer « modèle construit ou non » | L'agent ne peut pas le savoir et devine (rebuild inutile au run F, amont supposé absent au run H). Candidat event-driven | plan §16 constat 8 |

## 3. Écarts à reporter dans la spec (`spec.md`)

1. **K3** : « cible lecture seule » remplace « `--no-introspect` » comme garde
   de `compile` ; le drapeau reste une option sans valeur de sécurité.
2. **H1, G1** : `show` et `codegen` tournent sous la cible `ro` (même schéma de
   dev, rôle différent), pas sous la cible d'écriture.
3. **H7** : « profil lecture seule » → « cible `ro` du même profil, utilisateur
   et rôle Snowflake distincts ».
4. **§E ligne 1 / L2** : sous dbt 1.12.5 et `--warn-error`, une sélection `ls`
   vide ou un joker nu sort en **code 2** (avertissement promu), pas en code 0
   silencieux (plan §12).
5. **O2 / T7** : sur Snowflake, `run-operation --sql` persiste immédiatement
   (DDL et DML), à l'inverse de DuckDB (plan §11).
6. **G2 / T8** : `generate_source` sur des objets en majuscules écrit tout en
   minuscules (noms, colonnes, types) ; exploitable tel quel, identifiants non
   cités insensibles à la casse.
7. **D2 / T13** : `debug` affiche compte, utilisateur, rôle, base, warehouse,
   schéma, `query_tag` — jamais clé ni mot de passe. L'enveloppe ne renvoie
   que les lignes de verdict et les versions.
8. **S5 / T18** : `dynamic_table` est une matérialisation valide de
   l'adaptateur ; `parse` et `compile` acceptent une matérialisation inconnue,
   seul `run`/`build` la refuse.
9. **Limite écrite** : `deny` et hook lisent le texte de la commande ; un script
   qui appelle dbt en interne n'est pas bloqué. La garantie structurelle est
   celle du subagent (pas de Bash) ; le hook protège la conversation principale
   de l'invocation directe.

## 4. Résultats T0–T21

Toutes les lignes **[Observé]** le sont avec dbt-core 1.12.5, dbt-snowflake
1.12.1 ; Claude Code 2.1.289 quand le subagent est impliqué. Brut = `t_series.sh`
lancé par Greg ; enveloppe = subagent réel en `claude -p` ou CLI `dbt-enveloppe`
(même code).

| T | Objet | Statut | Constat | Source |
|---|---|---|---|---|
| T0 | Authentification non interactive | **[Observé]** brut + enveloppe | `debug` code 0 sur `dev` et `ro`, aucun navigateur ; idem par le subagent en `-p` | §10, §16 A |
| T1 | `show` d'un modèle finissant par `limit` | **[Observé]** brut | dbt colle `limit 5` → `001003 unexpected 'limit'` ; `--limit -1` passe. Identique à DuckDB | §16 |
| T2 | `show --inline` avec `;` | **[Observé]** brut | Même erreur ; `--limit -1` passe. L'enveloppe retire le `;` final | §16 |
| T3 | DDL inline, écriture puis lecture seule | **[Observé]** brut ; agent-level enveloppe | `dev` crée la table ; `ro` → `003001 Insufficient privileges`. Le subagent refuse d'essayer (H7) | §11, §16 B |
| T4 | `show`/`ls` par tag, sélection multiple | **[Observé]** enveloppe | `dbt_ls("tag:nightly", expected=[3 noms])` conforme ; `build` `{"success":3,"pass":3}` | §16 G |
| T5 | `show` avec amont non construit | Agent-level | Le subagent anticipe H5 et recompose l'aperçu en `show_inline` lecture seule ; brut non lancé | §16 H |
| T6 | `show`/`compile` d'un incremental construit | **[Observé]** enveloppe | SQL compilé avec le filtre `is_incremental` ; `show` → 0 ligne **avec la note H3** ; `compile(full_refresh)` donne le SQL sans filtre | §16 E, F |
| T7 | `run-operation --sql` DDL puis DML | **[Observé]** brut ; agent-level enveloppe | Persistance immédiate sur Snowflake (inverse de DuckDB). Non exposé ; le subagent refuse sans contourner (O2) | §11, §16 B |
| T8 | `generate_source` sur objets en majuscules | **[Observé]** enveloppe | 12 colonnes, tout en minuscules, exploitable tel quel | §16 G |
| T9 | `generate_model_yaml` non construit / construit | **[Observé]** enveloppe | Non construit : `'stg_region' has no columns; build the model first (G4, G5)`, aucun fichier laissé ; construit : 4 colonnes typées `number`/`varchar` | §16 D, H bis |
| T10 | Redirection + `parse` ; sortie d'erreur | **[Observé]** brut | Propre sous `--quiet` ; sans, `Running with dbt=…` pollue le fichier et le parse échoue ; stderr toujours 0 o | §16 |
| T11 | Mesure de tokens | Acté hors périmètre | Sorties plafonnées par l'enveloppe | §16 |
| T12 | Coût d'un `show` avec/sans `--limit` | Acté hors périmètre | Idem | §16 |
| T13 | `debug` : champs affichés, secrets | **[Observé]** brut + enveloppe | Brut : compte, utilisateur, rôle, base, warehouse, schéma, `query_tag`, ni clé ni mot de passe ; enveloppe : 7 lignes de verdict + versions, pas de bloc `Connection` | §11, §16 A |
| T14 | `debug --quiet` identifiants faux | **[Observé]** brut | Code 1, **0 octet** ; sans `--quiet`, aucun secret | §16 |
| T15 | `parse --warn-error` deux fois | **[Observé]** enveloppe | `{"ok": true}` à chaque appel, tous les runs | §16 |
| T16 | `ls` : logs, sélection vide, joker nu | **[Observé]** enveloppe (smoke étape 2) | Refus L2 ; joker nu → code 2 sous `--warn-error` (écart §3.4) | §12 |
| T17 | `compile` : `run_query`, `--no-introspect` | **[Observé]** brut + enveloppe | Table créée **avec et sans** `--no-introspect` sous `dev` ; sous `ro` : `Insufficient privileges`, 0 table. `--no-populate-cache` seul évite la connexion | §16 E, F bis, brut |
| T18 | Matérialisation invalide, puis propre à l'adaptateur | **[Observé]** brut | `nonsense` : parse et compile code 0, `run` code 1 ; `dynamic_table` : `build` ok, lecture `ro` ok | §16 |
| T19 | Rôle courant sous `ro`, puis DDL | **[Observé]** brut + enveloppe | `DBT_AGENT_RO`, rôles secondaires vides ; DDL refusé | §11, §16 C |
| T20 | Un schéma par session d'agent | **Non implémenté** | Cible `dev` unique, schéma `DEV` | §16 |
| T21 | `query_tag` dans l'historique | **[Observé]** | `ro` : 44 requêtes `dbt-agent-ro` ; `dev` : 15 requêtes `dbt-agent` (Snowsight) | §16 |

## 5. Usage au quotidien

- Dans un projet dbt : déléguer toute tâche dbt au subagent `dbt` (la
  conversation principale ne lance jamais dbt ; le hook la bloque si elle
  essaie). Un seul subagent `dbt` à la fois.
- Commandes hors enveloppe (`deps`, `docs generate`, `seed`…) : l'agent les
  demande ; l'humain les lance par `! uv run dbt deps` dans la session.
- Après tout `deps` ou édition manuelle : le prochain outil exigera un
  `dbt_parse` (empreinte), c'est voulu.
- Révision de l'effort (`high` → `medium` ou `xhigh`) : à la première tâche sur
  un vrai projet, même critère (refus de l'enveloppe et reprises par tâche).

## 6. Suites event-driven (non planifiées)

`dbt_docs_generate` (au premier `docs generate` manuel après une session) ;
« modèle construit ou non » exposé par l'enveloppe (au prochain rebuild
inutile) ; T20 (à la première exécution concurrente) ; faiblesses adjacentes
de `block-force-push.sh` (mot « force » non ancré) et `block-rm-rf.sh`
(découpage non conscient des guillemets).

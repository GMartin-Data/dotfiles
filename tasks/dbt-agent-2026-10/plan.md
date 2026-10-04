# Plan — agent dbt au scope user (subagent + serveur MCP « enveloppe »)

> **Statut : plan validé par Greg le 2026-10-02.** Les points A à F du §7 sont
> tranchés et priment sur les formulations « à valider » restées dans les §1, §3
> et §5. **Étapes 1 et 1 bis faites le 2026-10-02** (constats aux §10 et §11 ;
> T0, T3, T7, T13, T19 **[Observé]**). **Étape 2 faite le 2026-10-03** (§12,
> `cd393d6`). **Étape 3 faite le 2026-10-03** (§13, `afb21b3` ; point E soldé
> par `bd060fc`). **Étape 4 faite le 2026-10-04** (§14 ; points 1, 2, 4, 6, 8
> du §6 **[Observé]**). **Étape 5 faite le 2026-10-04** (§15 ; point 5 du §6
> **[Observé]**). **Étape 6 faite le 2026-10-04** (§16 ; point 9 du §6
> **[Observé]** ; T0–T21 couverts sauf T20 non implémenté et T11/T12 actés hors
> périmètre ; `compile`/`show`/`codegen` passés sous `ro`, `98b483a`).
> **Livrable de fin écrit** (`livrable.md`, brief §6). Prochaine action :
> `/code-review` sur le diff de branche en session dédiée, triage, puis PR
> `feat/dbt-agent` → `main`.

## Contexte

Objectif : un subagent Claude Code `dbt`, disponible dans tous les projets dbt
perso, qui n'exécute dbt **que** par un serveur MCP imposant l'appel canonique,
vérifiant la sortie et ne renvoyant que l'utile. La spécification
(`dbt_agent_preconisations_workflow.md`) montre que le code de sortie 0 ne prouve
pas le succès : les garde-fous doivent être structurels, pas des consignes.

Sources lues en entier : `~/implement_dbt_agent/brief_claude_code_agent_dbt.md`
et `~/implement_dbt_agent/dbt_agent_preconisations_workflow.md`.

Cadre de travail : branche dédiée `feat/dbt-agent` (pas de commit direct sur
`main` pour ce chantier), commits atomiques Conventional Commits, `/code-review`
avant la PR. **Arrêt à la fin de chaque étape** de la section 4 du brief.

**Aucune décision du brief n'est contredite par la doc Claude Code actuelle.**
Trois points de la doc changent la façon de les réaliser (détail en §1.4 et §6).

## 0. Ce que la doc confirme (vérifié le 2026-10-02)

| Sujet | Fait vérifié | Page |
|---|---|---|
| Frontmatter subagent | `name`, `description`, `tools`, `mcpServers`, `permissionMode`, `model`, `hooks`, `omitClaudeMd`… ; `tools` accepte `mcp__<server>__*` | code.claude.com/docs/en/sub-agents |
| MCP inline | Entrée `mcpServers` inline = même schéma que `.mcp.json`, type `stdio` accepté ; connectée au démarrage du subagent, déconnectée à sa fin ; la conversation parente n'a pas les outils | idem |
| Scope user | `~/.claude/agents/`, surveillé à chaud (pas de redémarrage sauf création du dossier) | idem |
| `CLAUDE_PROJECT_DIR` | Défini dans l'environnement des serveurs stdio lancés par Claude Code (racine du projet, stable) | code.claude.com/docs/en/mcp |
| Expansion `${VAR}` | Documentée pour `.mcp.json` (et les entrées de `~/.claude.json`) : `command`, `args`, `env`, `url`, `headers` | idem |
| Test hors config | `claude --mcp-config ./mcp.json` charge un serveur pour la session ; `--strict-mcp-config` ignore les autres | code.claude.com/docs/en/cli-reference |
| Règle `deny` Bash | `Bash(dbt *)` couvre `dbt` nu, les sous-commandes d'une commande composée, les wrappers `timeout/time/nice/nohup/stdbuf/command/xargs`. **Ne couvre pas** `uv run dbt`, `python -m dbt`, un chemin absolu, `sh -c '…'` : « isn't a security boundary » | code.claude.com/docs/en/permissions |
| Hook `PreToolUse` | Entrée JSON avec `tool_input.command` ; blocage par code 2 ou `permissionDecision: "deny"` ; matcher `Bash` ; les hooks des settings s'appliquent aussi dans les subagents | code.claude.com/docs/en/hooks |
| Prompts MCP | Un appel d'outil MCP demande une approbation par défaut ; un subagent en arrière-plan (mode par défaut en interactif) fait remonter le prompt dans la session principale | sub-agents, permissions |

## 1. Réponses aux 4 points de la section 3 du brief

### 1.1 `dbt_build` (absent de §D)

| Élément | Proposition |
|---|---|
| Paramètres | `select: str`, `full_refresh: bool = False` |
| Appel imposé | `dbt --no-use-colors --quiet build --select <select> --target dev [--full-refresh]` |
| Cible | `--target dev` ajouté par le serveur, non paramétrable ; le rôle Snowflake d'écriture n'a de droits que sur la base de dev (§5) |
| Refus (S1, L2, D3) | 1) pas de `dbt_debug` réussi dans la session ; 2) pas de `dbt_parse` réussi **sur l'état courant des fichiers** ; 3) `select` non validé par un `dbt_ls` réussi depuis ce parse |
| Condition de succès | code 0 **et** `target/run_results.json` réécrit par cet appel **et** résultats non vides **et** aucun statut `error`, `fail`, `skipped` **et** ensemble des modèles exécutés = liste validée par `dbt_ls` |
| Sortie | Compteurs par statut ; par modèle : nom, matérialisation, statut ; par échec : nœud + message tronqué (~500 caractères) ; tests en échec nommés ; `warn` signalés. Jamais le journal complet |

Deux choix à valider :
- **« Session » = durée de vie du processus serveur**, donc une exécution du
  subagent (la doc dit que le serveur inline vit le temps du subagent).
- **« parse réussi sur l'état courant »** : le serveur garde une empreinte
  (chemins, tailles, dates) des fichiers du projet au dernier parse réussi ; un
  fichier modifié depuis impose un nouveau `dbt_parse`. C'est la règle « parse
  après chaque fichier écrit » rendue structurelle. Repli plus simple si tu
  préfères : « un parse réussi dans la session », sans empreinte.

Pas de `--warn-error` sur `build` : un test en sévérité `warn` deviendrait un
échec ; le statut `warn` est remonté à la place.

### 1.2 Exécutable dbt : celui du projet

Je confirme ton penchant : `uv run --project "$CLAUDE_PROJECT_DIR" --no-sync dbt …`.

- **Pour** : c'est la version, l'adaptateur et les packages réellement épinglés
  par le projet (`uv.lock`) ; un dbt global peut contredire `require-dbt-version`
  ou ne pas avoir le bon adaptateur.
- **`--no-sync`** : le serveur ne modifie jamais l'environnement du projet. Si
  `.venv` ou dbt manque, refus explicite (« lance `uv sync` »).
- **Garde de version** : les conditions de succès sont observées sur dbt-core
  1.12.5. `dbt_debug` lit la version ; hors 1.12.x, le serveur refuse les outils
  des paliers B et C avec un message clair.

### 1.3 `show --inline` : exposé, mais seulement en lecture seule, et après T3 + T19

- **Utilité** : sans lui, l'agent ne peut pas regarder une source avant de
  modéliser (il devrait créer un modèle jetable).
- **Garde-fou structurel** : outil séparé `dbt_show_inline`, cible `ro` imposée
  par le serveur, utilisateur Snowflake distinct sans rôle d'écriture (§5),
  contrôle lexical (`select` ou `with` en tête, aucun `;` interne), `--limit` borné.
- **Condition d'activation** : l'outil n'est enregistré dans le serveur qu'une
  fois T3 et T19 **[Observé]** conformes (le rôle refuse bien un DDL). Avant, il
  n'existe pas pour l'agent.

Écart à valider : H7 dit `--profile <profil_lecture_seule>` ; je propose une
**cible** `ro` dans le même profil (`--target ro`), plus simple à tenir par
projet. Le texte de H7 reste tel quel dans le corps de l'agent.

### 1.4 Chemin du serveur dans le frontmatter

La doc ne documente l'expansion `${VAR}` que pour `.mcp.json` et `~/.claude.json`,
**pas** pour les `mcpServers` inline d'un subagent. Je propose de ne pas en dépendre :

```yaml
mcpServers:
  - dbt-enveloppe:
      type: stdio
      command: sh
      args: ["-c", "exec uv run --project \"$HOME/.claude/mcp/dbt-enveloppe\" --no-sync dbt-enveloppe-mcp"]
```

- C'est le shell qui résout `$HOME` : aucun comportement non documenté requis.
- Le fichier agent reste un simple lien symbolique versionné, identique sur
  toute machine. Le chemin absolu généré par l'installeur (ton repli) ferait du
  fichier agent un artefact généré, non lié.
- À l'étape 4, je teste une fois `${HOME}` en inline et je note le résultat
  **[Observé]**, sans en dépendre.

## 2. Arborescence dans les dotfiles et liens vers `~/.claude/`

Calée sur l'existant lu le 2026-10-02 (`install.sh`, `claude/`, `claude/settings.json`,
`claude/hooks/block-rm-rf.sh`).

```
dotfiles/
├── claude/
│   ├── agents/dbt.md                 → ~/.claude/agents/dbt.md          (lien de fichier)
│   ├── mcp/dbt-enveloppe/            → ~/.claude/mcp/dbt-enveloppe      (lien de dossier, NOUVEAU dossier claude/mcp/)
│   │   ├── pyproject.toml, uv.lock   (mcp épinglé, Python 3.12, script dbt-enveloppe-mcp)
│   │   ├── src/dbt_enveloppe/
│   │   │   ├── runner.py             (subprocess : appel canonique, env, timeout)
│   │   │   ├── conditions.py         (conditions de succès §D, fonctions pures)
│   │   │   ├── session.py            (état : debug, parse + empreinte, sélections ls)
│   │   │   ├── cli.py                (étape 2 : enveloppe en CLI pur)
│   │   │   └── server.py             (étape 3 : exposition MCP)
│   │   └── tests/                    (un cas « échec silencieux » par ligne du principe 2)
│   ├── hooks/block-dbt.sh            → ~/.claude/hooks/block-dbt.sh     (lien de fichier, étape 5)
│   ├── settings.json                 (déjà lié) : modifié aux étapes 4 et 5
│   └── README.md                     (mis à jour : agent, serveur, hook)
├── tasks/dbt-agent-2026-10/          (pièces du chantier, comme l'audit skill-evals — validé le 2026-10-02)
│   ├── brief.md                      (copie de brief_claude_code_agent_dbt.md)
│   ├── spec.md                       (copie de dbt_agent_preconisations_workflow.md ; source du test de synchronisation de l'agent)
│   └── plan.md                       (copie de ce plan ; pointé par progress.md)
├── .gitignore                        (+ claude/mcp/dbt-enveloppe/.venv/)
└── install.sh                        (étendu)
```

Hors dotfiles : `~/dbt-agent-testbed/` (projet de test), `~/.dbt/profiles.yml`,
`~/.snowflake/keys/`. Rien dans `~/.claude.json`.

Ce que l'existant impose ou permet de réutiliser :

- **`install.sh`** : fonction `link()` (`ln -sfn`, déjà idempotente). Ajouts :
  trois lignes `link` (agent et hook en fichiers individuels comme aujourd'hui,
  serveur en lien de dossier comme les skills), un contrôle `command -v uv` avec
  message clair, puis `uv sync --frozen` du serveur.
- **`claude/settings.json`** (modifications) :
  - étape 4 : clé `permissions.allow` (absente aujourd'hui) avec
    `mcp__dbt-enveloppe__dbt_parse` et `mcp__dbt-enveloppe__dbt_ls`, si le point D est validé ;
  - étape 5 : `"Bash(dbt *)"` ajouté à `permissions.deny` ; nouvelle entrée
    `PreToolUse`, matcher `Bash`, commande `~/.claude/hooks/block-dbt.sh`,
    **sans champ `if`** — `if: "Bash(dbt *)"` ne se déclencherait pas sur
    `uv run dbt`, et le commentaire de `block-rm-rf.sh` rappelle que ce filtre
    est « best-effort ».
- **`claude/hooks/block-rm-rf.sh`** sert de modèle : lecture de
  `.tool_input.command` par `jq`, découpage sur les séparateurs shell, saut des
  `VAR=val` et des lanceurs, repérage du mot de commande, blocage par code 2.
  Le hook dbt étend la liste des lanceurs (`uv run …`, `uvx`, `python -m`, `sh -c`).
- **Plugin d'eval** : `claude/` est aussi la racine du plugin d'eval
  (`claude/.claude-plugin/`). Sous `claude plugin eval`, `agents/dbt.md` serait
  chargé comme agent de plugin, dont la doc dit que `mcpServers` est ignoré :
  sans effet sur les sessions quotidiennes, à contrôler à l'étape 4
  (`claude plugin details`).

Corps de `dbt.md` : socle S1–S5 + sections D/P/L/K/H/O/G **copiés tels quels**
avec leurs identifiants, schéma IV §1, liste IV §4, et une courte table
« règle → outil MCP ». Un test compare chaque bloc `<!-- DÉBUT … -->` de la
spécification au corps de l'agent, pour empêcher la dérive.

## 3. Outils MCP

Communs à tous les appels (ajouts par rapport à §D, à valider) :
`uv run --project $CLAUDE_PROJECT_DIR --no-sync dbt`, cwd = projet,
`--project-dir`, `--profiles-dir ~/.dbt` (un `profiles.yml` local au projet ne
peut pas détourner la cible), `--target dev`, `--no-use-colors`. Arguments
passés en liste (pas de shell) ; valeur commençant par `-` refusée. Chaque outil
refuse si `CLAUDE_PROJECT_DIR` est absent ou sans `dbt_project.yml`.

| Outil | Appel imposé | Condition de succès | Sortie renvoyée |
|---|---|---|---|
| `dbt_debug()` | `dbt debug` (jamais `--quiet`, D1) | Code 0 | Lignes `[OK …]`, `[ERROR …]`, `All checks passed!`, versions dbt/adaptateur ; jamais le bloc `Connection` (D2) |
| `dbt_parse()` | `dbt --quiet parse --no-partial-parse --warn-error` | Code 0 **et** sortie vide | Rien si succès ; le message sinon |
| `dbt_ls(select, expected)` | `dbt --quiet ls --select <select> --resource-type model --output json --output-keys "name config.materialized" --warn-error` | Code 0 **et** liste non vide **et** = `expected` | Liste (nom, matérialisation) ; en cas d'écart : manquants et inattendus |
| `dbt_compile(name, full_refresh=False)` | `dbt --quiet compile --select <name> --no-introspect --output json [--full-refresh]` | Code 0 **et** clé `compiled` non vide | SQL compilé + matérialisation |
| `dbt_show(name, limit=5)` | `dbt --quiet show --select <name> --limit <N> --output json` | Code 0 **et** clé `show` présente | Lignes JSON + matérialisation ; mention explicite si `incremental` et 0 ligne (H3) |
| `dbt_build(select, full_refresh=False)` | voir §1.1 | voir §1.1 | voir §1.1 |
| `dbt_codegen(macro, args, output_path)` | `dbt --quiet run-operation <macro> --args '<json>'` ; le serveur écrit stdout dans `output_path` | `macro` dans la liste blanche (5 macros, O1/G1) ; chemin dans le projet et **inexistant** (G3) ; code 0 ; `dbt parse` canonique réussi ; colonnes non vides pour `generate_source` et `generate_model_yaml` (G5) | Confirmation : chemin, taille, nombre de colonnes ; jamais le contenu (G6). Si le parse échoue, le serveur supprime le fichier qu'il vient de créer |
| `dbt_show_inline(sql, limit=5)` *(après T3 + T19)* | `dbt --quiet show --inline <sql> --limit <N> --output json --target ro` | Contrôle lexical ; code 0 **et** clé `show` présente | Lignes JSON |

Préconditions de session :
- `dbt_compile`, `dbt_show`, `dbt_build`, `dbt_codegen`, `dbt_show_inline` :
  `dbt_debug` réussi + `dbt_parse` réussi sur l'état courant.
- `dbt_compile`, `dbt_show` : `name` = nom exact (pas de `tag:`, `+`, liste —
  K5, H4) présent dans une liste validée par `dbt_ls`.
- `limit` : 1 à 50, ou `-1` (H6), auquel cas le serveur tronque à 50 lignes.

Non exposés : `run-operation` libre et `--sql` (O2), retrait de
`--no-introspect` (K3), `dbt deps` (lancé à la main à l'initialisation du projet).

Permissions proposées : `permissions.allow` pour `dbt_parse` et `dbt_ls`
(palier A, hors ligne) ; les autres outils gardent le prompt au début, pour
observer un agent réel. À relâcher ensuite selon ton retour.

## 4. Projet dbt de test (étape 1 bis)

Emplacement : `~/dbt-agent-testbed/`, dépôt git propre, hors dotfiles. Projet
`uv` : Python 3.12, `dbt-core==1.12.5`, `dbt-snowflake` 1.12.x épinglé au patch
installé, `codegen` épinglé dans `packages.yml`. Données :
`SNOWFLAKE_SAMPLE_DATA.TPCH_SF1`.

Projet nominal (toujours sain) :

| Élément | Contenu | Sert à |
|---|---|---|
| Sources | `tpch` : `ORDERS`, `CUSTOMER`, `LINEITEM`, `NATION` (majuscules) | T8, `generate_source` |
| `stg_orders`, `stg_customers` | vues, tag `nightly` | T4 (`tag:`, sélection multiple) |
| `dim_customers` | `table`, tests `unique` + `not_null` | T9, S5 |
| `fct_orders` | `incremental`, `unique_key`, filtre sur `max(order_date)` de `{{ this }}` | T6, H3, K4 |
| `orders_by_status` | modèle utilisant `run_query` (statuts distincts pour un pivot) | T17, K1, K3 |
| Tests | génériques + un test singulier | étape 4 du workflow |

Dossier `fixtures/` hors des chemins parsés : chaque faute est copiée dans
`models/` par le test qui en a besoin, puis retirée.

| Ligne du principe 2 / matrice §A | Fixture ou commande |
|---|---|
| `ls` vide, joker nu `fct_*` | commande seule |
| `show` / `compile` avec `tag:x`, sélection multiple | commande seule (tag `nightly`) |
| `show` d'un incremental construit → 0 ligne | `fct_orders` après build |
| `parse --warn-error` masqué par le cache | `orphan_patch.yml` |
| `generate_model_yaml` non construit → `columns:` vide | `unbuilt_model.sql` |
| `codegen` sans `--quiet` → YAML invalide | commande brute |
| `run-operation --sql` en écriture | commande brute (T7, schéma jetable) |
| `debug --quiet`, base injoignable | cible `broken` du profil (T14) |
| `show --inline "create table …"` | commande brute, cibles `dev` puis `ro` (T3, T19) |
| Matérialisation invalide, puis propre à l'adaptateur | `mat_invalid.sql`, `mat_dynamic_table.sql` (T18) |
| Macro inexistante, SQL invalide, colonne absente, cycle | `macro_missing.sql`, `sql_invalid.sql`, `column_missing.sql`, `cycle_a/b.sql` |
| Modèle finissant par `limit 3` | `ends_with_limit.sql` (T1) |
| `run_query` à effet de bord | `run_query_side_effect.sql` (T17) |

Les tests unitaires de l'étape 2 ne touchent pas l'entrepôt : ils appliquent les
fonctions de `conditions.py` à des sorties capturées (code, stdout, fichiers).

## 5. SQL Snowflake (à exécuter par toi)

Choix à valider : **deux utilisateurs**, pas un seul portant les deux rôles. La
doc Snowflake donne `DEFAULT_SECONDARY_ROLES = ('ALL')` par défaut : un
utilisateur unique en session « lecture seule » garderait les privilèges du rôle
d'écriture par rôle secondaire. Deux utilisateurs rendent la séparation structurelle.

Clés (en local, avant le SQL) :

```bash
mkdir -p ~/.snowflake/keys && chmod 700 ~/.snowflake/keys
for u in rw ro; do
  openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -nocrypt -out ~/.snowflake/keys/dbt_agent_$u.p8
  openssl rsa -in ~/.snowflake/keys/dbt_agent_$u.p8 -pubout -out ~/.snowflake/keys/dbt_agent_$u.pub
done
chmod 600 ~/.snowflake/keys/*.p8
```

SQL (trial, en `ACCOUNTADMIN`) :

```sql
USE ROLE ACCOUNTADMIN;

-- Warehouse and sandbox database
CREATE WAREHOUSE IF NOT EXISTS DBT_AGENT_WH
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE;
CREATE DATABASE IF NOT EXISTS DBT_AGENT_DEV;

-- Roles
CREATE ROLE IF NOT EXISTS DBT_AGENT_RW;
CREATE ROLE IF NOT EXISTS DBT_AGENT_RO;
GRANT ROLE DBT_AGENT_RW TO ROLE SYSADMIN;
GRANT ROLE DBT_AGENT_RO TO ROLE SYSADMIN;

-- Shared: compute, sandbox database, sample data
GRANT USAGE ON WAREHOUSE DBT_AGENT_WH TO ROLE DBT_AGENT_RW;
GRANT USAGE ON WAREHOUSE DBT_AGENT_WH TO ROLE DBT_AGENT_RO;
GRANT USAGE ON DATABASE DBT_AGENT_DEV TO ROLE DBT_AGENT_RW;
GRANT USAGE ON DATABASE DBT_AGENT_DEV TO ROLE DBT_AGENT_RO;
GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE_SAMPLE_DATA TO ROLE DBT_AGENT_RW;
GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE_SAMPLE_DATA TO ROLE DBT_AGENT_RO;

-- Writer: creates and owns its schemas in the sandbox database only
GRANT CREATE SCHEMA ON DATABASE DBT_AGENT_DEV TO ROLE DBT_AGENT_RW;

-- Reader: read + metadata on everything the writer will create, nothing else
GRANT USAGE ON FUTURE SCHEMAS IN DATABASE DBT_AGENT_DEV TO ROLE DBT_AGENT_RO;
GRANT SELECT ON FUTURE TABLES IN DATABASE DBT_AGENT_DEV TO ROLE DBT_AGENT_RO;
GRANT SELECT ON FUTURE VIEWS IN DATABASE DBT_AGENT_DEV TO ROLE DBT_AGENT_RO;
GRANT SELECT ON FUTURE DYNAMIC TABLES IN DATABASE DBT_AGENT_DEV TO ROLE DBT_AGENT_RO;  -- T18

-- Service users, key pair only, no secondary roles
CREATE USER IF NOT EXISTS DBT_AGENT_RW_USER
  TYPE = SERVICE DEFAULT_ROLE = DBT_AGENT_RW DEFAULT_WAREHOUSE = DBT_AGENT_WH
  DEFAULT_SECONDARY_ROLES = ()
  RSA_PUBLIC_KEY = '<contenu de dbt_agent_rw.pub sans les lignes BEGIN/END>';
CREATE USER IF NOT EXISTS DBT_AGENT_RO_USER
  TYPE = SERVICE DEFAULT_ROLE = DBT_AGENT_RO DEFAULT_WAREHOUSE = DBT_AGENT_WH
  DEFAULT_SECONDARY_ROLES = ()
  RSA_PUBLIC_KEY = '<contenu de dbt_agent_ro.pub sans les lignes BEGIN/END>';
GRANT ROLE DBT_AGENT_RW TO USER DBT_AGENT_RW_USER;
GRANT ROLE DBT_AGENT_RO TO USER DBT_AGENT_RO_USER;

-- Checks
SHOW GRANTS TO ROLE DBT_AGENT_RO;
SHOW GRANTS TO USER DBT_AGENT_RO_USER;
```

Notes :
- Si `SNOWFLAKE_SAMPLE_DATA` est absente du trial :
  `CREATE DATABASE SNOWFLAKE_SAMPLE_DATA FROM SHARE SFC_SAMPLES.SAMPLE_DATA;`.
- `CREATE SCHEMA` au niveau de la base (et non un seul schéma `DEV`) : la base
  entière est le bac à sable, ce qui permet un schéma par session (T20).
- Privilèges de métadonnées (§F.3 fait 2) : sur Snowflake ils découlent de
  `USAGE` + `SELECT` ; **à confirmer par T3**, pas acquis.

`~/.dbt/profiles.yml` (hors dépôt) : profil `dbt_agent_testbed`, cibles `dev`
(utilisateur et rôle RW), `ro` (utilisateur et rôle RO), `broken` (compte faux,
T14) ; `private_key_path` en chemin absolu, `query_tag: dbt-agent` /
`dbt-agent-ro`, base `DBT_AGENT_DEV`, schéma `DEV`, warehouse `DBT_AGENT_WH`.

### 5.1 Pas-à-pas dans Snowsight (interface web)

Ce que la doc Snowflake impose (vérifié le 2026-10-02) : le formulaire `+ User`
de Snowsight exige un mot de passe et n'offre ni type d'utilisateur ni champ de
clé publique ; l'affectation d'une clé n'est documentée qu'en SQL. **Le
paramétrage se fait donc dans l'interface, en exécutant le SQL ci-dessus dans
une feuille SQL, puis en vérifiant le résultat dans les écrans.** Libellés
marqués (?) : non vérifiés dans la doc, à confirmer à l'écran.

| # | Action | Où | Résultat attendu |
|---|---|---|---|
| 1 | Créer le compte d'essai (édition Standard suffisante) | Page d'inscription au trial Snowflake | Connexion à Snowsight ; le créateur du trial dispose du rôle `ACCOUNTADMIN` |
| 2 | Relever l'identifiant de compte | Sélecteur de compte » **View account details** » onglet **Config File** | Valeur `organisation-compte` (avec un tiret), à mettre dans `account:` du profil. Équivalent SQL : `SELECT CURRENT_ORGANIZATION_NAME() \|\| '-' \|\| CURRENT_ACCOUNT_NAME();` |
| 3 | Générer les deux paires de clés | Ton terminal (commandes du §5) | `dbt_agent_rw.p8/.pub`, `dbt_agent_ro.p8/.pub` dans `~/.snowflake/keys/` |
| 4 | Ouvrir une feuille SQL | Menu **Projects » Worksheets** (?), bouton **+** (?) | Feuille vide ; rôle `ACCOUNTADMIN` sélectionné (la première ligne du script le force de toute façon) |
| 5 | Coller le script du §5 | La feuille SQL | Remplacer les deux `<contenu de …pub…>` par le contenu des fichiers `.pub` **sans** les lignes `BEGIN`/`END`, sur une seule ligne |
| 6 | Tout exécuter | Menu **More options** à côté du bouton **Run** » **Run All** (libellé confirmé par la doc) | Chaque instruction renvoie un succès. La doc ne dit pas quels résultats restent affichés : relancer chaque `SHOW` seul (curseur dans l'instruction, **Run**) |
| 7 | Contrôler les utilisateurs et les rôles | **Governance & security » Users & roles**, ou `SHOW GRANTS TO USER DBT_AGENT_RO_USER;` | Deux utilisateurs `DBT_AGENT_RW_USER` et `DBT_AGENT_RO_USER` ; pour `DBT_AGENT_RO_USER`, **un seul** rôle accordé : `DBT_AGENT_RO` |
| 7 bis | Contrôler les privilèges du rôle RO | Feuille SQL, requêtes ci-dessous | Uniquement `USAGE` et `SELECT` ; dans `DBT_AGENT_DEV`, la base seule ; 4 grants futurs |
| 8 | Contrôler l'empreinte de chaque clé | Feuille SQL + terminal | Les deux valeurs ci-dessous sont identiques, pour chaque utilisateur |
| 9 | Contrôler le warehouse | Écran des warehouses (?) | `DBT_AGENT_WH`, taille X-Small, suspension automatique à 60 s |
| 10 | Écrire `~/.dbt/profiles.yml` à partir du gabarit fourni | Ton éditeur | Cibles `dev`, `ro`, `broken` |
| 11 | T0 | Terminal, dans `~/dbt-agent-testbed/` | `dbt debug --target dev` puis `--target ro` : `All checks passed!`, aucun navigateur ouvert |

Contrôle des privilèges du rôle RO (étape 7 bis). `SHOW GRANTS TO ROLE` détaille
les données d'exemple objet par objet (89 lignes, cf. §10) : le résumer plutôt
que le lire. Les grants futurs n'y figurent pas, d'où la seconde requête.

```sql
SHOW GRANTS TO ROLE DBT_AGENT_RO
  ->> SELECT SPLIT_PART("name", '.', 1) AS db, "granted_on", "privilege", COUNT(*) AS n
      FROM $1
      GROUP BY ALL
      ORDER BY 1, 2;

SHOW FUTURE GRANTS IN DATABASE DBT_AGENT_DEV;
```

Contrôle d'empreinte (étape 8), d'après la page « Key-pair authentication » :

```sql
DESC USER DBT_AGENT_RO_USER
  ->> SELECT SUBSTR((SELECT "value" FROM $1 WHERE "property" = 'RSA_PUBLIC_KEY_FP'), LEN('SHA256:') + 1) AS key;
```

```bash
openssl rsa -pubin -in ~/.snowflake/keys/dbt_agent_ro.pub -outform DER | openssl dgst -sha256 -binary | openssl enc -base64
```

Si un libellé diffère à l'écran, tu me le dis (ou tu me montres une capture) et
je corrige le pas-à-pas ; je ne pilote pas ton navigateur et n'exécute aucun SQL
sur ton compte.

## 6. Ce que je n'ai pas pu vérifier dans la doc Claude Code

| # | Point | État | Parade ou moment de vérification |
|---|---|---|---|
| 1 | Expansion `${HOME}` dans les `mcpServers` inline d'un subagent | Non documentée | Contournée par `sh -c` (§1.4) ; test **[Observé]** à l'étape 4 |
| 2 | `CLAUDE_PROJECT_DIR` pour un serveur stdio **inline de subagent** | Documenté pour les serveurs stdio en général, pas pour ce cas précis | Le serveur refuse si la variable manque ; vérifié à l'étape 4 |
| 3 | Répertoire de travail d'un serveur stdio lancé depuis un agent de scope user | Seul le cas `headersHelper` est documenté (`~/.claude`) | Aucun chemin relatif utilisé |
| 4 | Fichier agent en lien symbolique dans `~/.claude/agents/` | Non mentionné dans la doc ; **[Observé]** : `tech-watch-scorer.md` est un lien vers les dotfiles et il est chargé dans la session courante | Aucune |
| 5 | Les règles `permissions.deny` des settings user s'appliquent dans les subagents | Non dit explicitement (dit pour les hooks) | **[Observé]** à l'étape 5 (§15) : appliquée dans un subagent avec Bash, et prioritaire sur un `allow` passé en CLI |
| 6 | Une règle `allow` `mcp__dbt-enveloppe__dbt_parse` vise bien un serveur inline | Syntaxe documentée, cas inline non | Test à l'étape 4 |
| 7 | `/mcp` liste-t-il un serveur inline pendant l'exécution du subagent | Non dit | L'étape 3 passe par `claude --mcp-config` (rien de persistant) |
| 8 | Absence de dialogue de confiance pour un serveur inline d'un agent de scope user | Implicite (la règle de confiance ne cite que les agents de projet) | Constaté à l'étape 4 |
| 9 | Les commandes `!` de l'utilisateur échappent au hook et à la règle `deny` | **[Observé]** le 2026-10-04 (§16) : `! uv run --project ~/dbt-agent-testbed dbt --version` tapé par Greg → versions affichées ; la même commande par l'outil Bash de Claude → `BLOCKED` du hook | Aucune ; c'est le canal prévu pour `deps`, `docs generate`… |

Hors doc Claude Code : `private_key_path` et `query_tag` dans un profil
dbt-snowflake 1.12 — **levé en partie à l'étape 1** (champs présents dans le code
1.12.1, `private_key_path` confirmé par T0 ; l'effet de `query_tag` reste à
constater par T21, cf. §10). Toujours non vérifié : comportement exact de
`uv run --no-sync` sans `.venv` ; API courante du SDK MCP Python (à lire via
context7 à l'étape 3).

## 7. Points à valider avant l'étape 1

- **A.** Deux utilisateurs Snowflake plutôt qu'un (§5). **Validé le 2026-10-02 :
  deux utilisateurs.** T19 étendu : `select current_secondary_roles()` + tentative
  de `delete` sous la cible `ro`.
- **B.** Cible `ro` plutôt qu'un second profil (§1.3). **Validé le 2026-10-02 :
  cible `ro` du même profil.** Écart de mécanisme avec le texte de H7, à
  consigner au livrable de fin pour report dans la spécification.
- **C.** Empreinte de fichiers pour « parse sur l'état courant » (§1.1), ou repli simple.
  **Validé le 2026-10-02 : empreinte.** Un changement d'empreinte annule aussi les
  sélections validées par `dbt_ls`. Coût de `--no-partial-parse` à mesurer sur le
  projet de test.
- **D.** `allow` sur `dbt_parse` et `dbt_ls` seulement (§3). **Validé le 2026-10-02.**
  Périmètre à réexaminer après l'étape 6. Si la règle ne s'applique pas à un
  serveur inline (§6 point 6), le signaler à l'étape 4.
- **E.** `dbt_show_inline` enregistré seulement après T3 + T19 (§1.3). **Validé le
  2026-10-02.** Écrit et testé dès l'étape 2, déclaré par un commit dédié une fois
  T3 et T19 **[Observé]** conformes ; si l'un échoue, décision à reprendre.
  **Condition remplie le 2026-10-02** (§11).
- **F.** Après l'étape 5, mes appels dbt bruts sont bloqués. Or T1, T2, T3, T7,
  T14, T15 testent le comportement **brut** de dbt. Proposition : un script
  `t_series.sh <T#>` dans le projet de test, que **tu** lances dans ton terminal ;
  il écrit `results/Txx.txt`, que je lis et étiquette **[Observé]**.
  **Validé le 2026-10-02 : tu lances le script.** Je l'écris à l'étape 1 bis
  (fixture, commandes exactes, capture, nettoyage) pour relecture avant exécution.
  Je ne le lance pas moi-même après l'étape 5.
  **Couverture élargie le 2026-10-02** à T1–T10 et T13–T19 (§11).

Limite connue du garde-fou, à consigner au livrable (doc permissions : une règle
Bash « isn't a security boundary around the program ») : `deny` et hook lisent le
texte de la commande ; un script qui appelle dbt en interne n'est pas bloqué. La
garantie est structurelle pour le subagent `dbt` (pas d'outil Bash), pas pour la
conversation principale.

## 8. Étapes et vérifications (section 4 du brief)

| Étape | Livré | Vérification avant arrêt |
|---|---|---|
| 1 | Je fournis, dans `~/dbt-agent-testbed/` : `setup/snowflake_setup.sql` (script du §5), `setup/profiles.example.yml`, et le squelette minimal du projet (`pyproject.toml` épinglé, `dbt_project.yml`) nécessaire à `dbt debug`. Tu suis le pas-à-pas du §5.1 | `dbt debug` à la main sur `dev` et `ro`, sans navigateur (T0) |
| 1 bis | `~/dbt-agent-testbed/` + `fixtures/` + `t_series.sh` (tests bruts, relu par toi) | `dbt deps`, `dbt build` nominal vert |
| 2 | `runner.py`, `conditions.py`, `session.py`, `cli.py` + tests | `uv run pytest` vert : un cas d'échec silencieux par ligne du principe 2 |
| 3 | `server.py` | `claude --mcp-config` dans le projet de test, `/mcp` liste les outils, un appel par outil |
| 4 | `claude/agents/dbt.md`, liens, `install.sh` | L'agent ne voit que Read/Grep/Glob/Edit/Write + outils MCP ; points 1, 2, 4, 6, 8 du §6 observés |
| 5 | Règle `deny`, hook, tests du hook (table « doit bloquer / doit passer ») | `dbt`, `uv run dbt`, `python -m dbt`, chemin absolu bloqués ; `dbt-enveloppe` et un message de commit contenant « dbt » passent |
| 6 | T0, T3, T7, T13, T19, puis le reste. Tests bruts : tu lances `t_series.sh`, je lis `results/`. Tests de l'enveloppe : par le subagent. Après T3 + T19 conformes : commit qui déclare `dbt_show_inline` | Chaque résultat **[Observé]** avec versions dbt-core, dbt-snowflake, Claude Code |

Hook de l'étape 5 : même stratégie que `block-rm-rf.sh`, ancrée sur la
**position de commande** (début de commande simple, après `;`, `&&`, `|`, `$(`,
lanceurs `uv run`, `uvx`, `python -m`, `sh -c`, chemin se terminant par `/dbt`),
pour ne pas bloquer un texte cité comme `git commit -m "… dbt build …"`.

Livrable de fin (brief §6) : ce qui fonctionne, ce qui est écarté et pourquoi,
table T0–T21 étiquetée.

## 9. Acter le plan, puis repartir d'un contexte frais (avant l'étape 1)

Décidé le 2026-10-02, pour limiter la dégradation du contexte :

1. Sortie du plan mode, modifications approuvées une à une.
2. `git switch -c feat/dbt-agent` depuis `main`.
3. Copie dans `tasks/dbt-agent-2026-10/` : `brief.md`, `spec.md` (depuis
   `~/implement_dbt_agent/`) et `plan.md` (ce fichier). Commit `docs(tasks)`.
4. `/progress` : plan validé, décisions A à F, prochaine action = étape 1,
   pointeur vers `tasks/dbt-agent-2026-10/plan.md`. Commit `docs(progress)` sur
   la branche (pas d'attribution Claude dans les messages de commit).
5. Côté humain : `/clear`, puis `/catchup`. La session neuve lit `progress.md`
   et le plan, puis commence l'étape 1.

Rappels pour la session neuve : ce chantier travaille sur `feat/dbt-agent`
(exception à l'exemption « direct sur main » du repo) ; arrêt en fin de chaque
étape ; `/code-review` avant la PR ; la doc Claude Code a été vérifiée le
2026-10-02 (table du §0) et n'a pas à être relue, sauf pour un champ nouveau.

## 10. Résultats de l'étape 1 (2026-10-02)

Livré dans `~/dbt-agent-testbed/` (dépôt git distinct) : `pyproject.toml` et
`uv.lock` (`dbt-core==1.12.5`, `dbt-snowflake==1.12.1`), `dbt_project.yml`,
`setup/snowflake_setup.sql`, `setup/profiles.example.yml`.

Versions : dbt-core 1.12.5, dbt-snowflake 1.12.1, snowflake-connector-python
4.8.0, Claude Code 2.1.287.

| Constat | Étiquette | Détail |
|---|---|---|
| **T0** conforme sur `dev` et `ro` | **[Observé]** (lancé par Greg) | `dbt debug` : code 0, `Connection test: [OK connection ok]`, `All checks passed!` ; aucun navigateur ouvert ; authentification par paire de clés, utilisateurs de service |
| Rôle RO limité à la lecture | **[Observé]** | `SHOW GRANTS TO ROLE DBT_AGENT_RO` : 89 lignes, uniquement `USAGE` et `SELECT` — 1 warehouse, 2 bases, et 6 schémas + 80 tables tous dans `SNOWFLAKE_SAMPLE_DATA` ; dans `DBT_AGENT_DEV`, la base seule |
| Les droits sur `SNOWFLAKE_SAMPLE_DATA` s'affichent objet par objet | **[Observé]** | Une ligne par schéma et par table, pas une ligne unique pour `IMPORTED PRIVILEGES` ; cause non établie (affichage propre aux bases partagées, ou nature de la base dans ce trial) |
| Grants futurs en place | **[Observé]** | 4 lignes pour `DBT_AGENT_RO` : `USAGE` sur schéma, `SELECT` sur table, vue, table dynamique |
| Utilisateur RO : un seul rôle | **[Observé]** | `SHOW GRANTS TO USER DBT_AGENT_RO_USER` : `DBT_AGENT_RO` ; empreintes des deux clés identiques côté Snowflake et local |
| Champs du profil | Code lu (1.12.1) | `private_key_path`, `query_tag`, `connect_retries` sont des champs de `SnowflakeCredentials` ; `query_tag` est passé en paramètre de session `QUERY_TAG` |
| Une clé inconnue dans le profil n'est pas rejetée | **[Observé]** | `dbt parse` renvoie 0 avec `bogus_key: 1` sur une cible ; 2 sur une cible inexistante. Une faute de frappe sur un champ du profil passe en silence |
| `connect_timeout` n'est pas un délai de connexion | Code lu (1.12.1) | C'est l'attente entre deux tentatives. Cible `broken` : `connect_retries: 0` ; durée réelle d'un `dbt debug` sur un compte faux à constater par T14 |

À garder en tête pour la suite : le schéma `PUBLIC` de `DBT_AGENT_DEV`, créé
avant les grants futurs, n'est pas accessible au rôle RO (sans effet : le profil
travaille dans `DEV`). La lecture par `ro` d'un modèle construit par `dev` a été
constatée le même jour (T3, §11).

## 11. Résultats de l'étape 1 bis et du périmètre minimal (2026-10-02)

Livré dans `~/dbt-agent-testbed/` (commits `d20996c`, `f010a84`) : projet
nominal du §4, `fixtures/` (15 fichiers), `t_series.sh`, macros d'aide
`macros/t_series.sql`. Les fichiers `results/Txx.txt` sont hors git : ce
paragraphe en est la trace durable.

Versions : dbt-core 1.12.5, dbt-snowflake 1.12.1, `codegen` 0.14.1,
`dbt_utils` 1.4.1, Claude Code 2.1.287.

### Critère de l'étape 1 bis

| Contrôle | Résultat **[Observé]** |
|---|---|
| `dbt deps` | `codegen` 0.14.1 et `dbt_utils` 1.4.1, figés dans `package-lock.yml` |
| Parse canonique (P1) | Code 0, sortie vide, paquets et macros d'aide compris |
| `ls` canonique (L1) | Les 5 modèles attendus ; la clé de sortie est plate : `"config.materialized"` |
| `dbt build` sur `dev`, deux fois | `PASS=15 ERROR=0 SKIP=0` ; au second passage `fct_orders` charge 0 ligne (branche incrémentale) |

### Écarts au plan

- **Couverture de `t_series.sh` élargie** (décision Greg) : T1 à T10 et T13 à
  T19, au lieu des six tests du point F. Presque tout le protocole teste le
  comportement brut de dbt, que l'enveloppe refuse par construction. T11, T12,
  T20 et T21 restent à part.
- **Périmètre minimal lancé avant l'étape 6** (décision Greg) : T3, T7, T13,
  T19, pour disposer des sorties réelles dès l'étape 2.
- **`codegen` 0.14.1 (hub)**, alors que la spec a été éprouvée sur la branche
  `main` au 2026-09-25. À reporter au livrable de fin.
- **Macros d'aide `t_exec` et `t_rows`** : SQL libre par `run-operation`, pour
  préparer, nettoyer et contrôler sans passer par les commandes testées. La
  liste blanche de l'enveloppe (O1, G1) doit les refuser : à couvrir par un test
  à l'étape 3.
- **Trois fixtures ajoutées** (`t5_upstream`, `t5_downstream`,
  `t6_incremental`) : T5 et T6 exigent des modèles non construits.
- **Fixtures de la matrice §A non branchées** dans `t_series.sh`
  (`macro_missing`, `sql_invalid`, `column_missing`, `cycle_a/b`) : elles
  servent aux captures de l'étape 2.
- **Table dynamique de T18 basée sur `dim_customers`** : compatibilité d'une
  table dynamique avec une base partagée non vérifiée.

### Périmètre minimal — tous **[Observé]**, lancés par Greg

| Test | Constat | Règle |
|---|---|---|
| T3 | Sous `dev`, `show --inline "create table … as select"` : code 0, table créée et persistée. Sous `ro` : code 2, `003001 (42501) Insufficient privileges`, table absente | H7 confirmée |
| T3 (métadonnées) | Sous `ro`, `show`, `compile --no-introspect` et `generate_model_yaml` réussissent sur un modèle construit par `dev` : `USAGE` + `SELECT` et les grants futurs suffisent | §F.3 fait 2 confirmé |
| T7 | `run-operation --sql` : DDL puis DML persistés immédiatement, vérifiés depuis une autre session ; sortie `OK executed inline_query` | O2 confirmée ; attente inversée de §F.4 vérifiée |
| T19 | Cible `ro` : `current_role()` = `DBT_AGENT_RO`, aucun rôle secondaire ; `create table` et `delete` refusés (`42501`) | H7, point A |
| T13 | `debug` affiche compte, utilisateur, base, warehouse, rôle, schéma, `query_tag`, paramètres réseau et de reprise. Ni clé privée, ni chemin de clé, ni mot de passe. 1 717 octets | D2 confirmée ; §F.3 fait 5 confirmé |
| T13 (warehouse) | Warehouse suspendu avant et après, date de dernière reprise inchangée : `debug` ne le réveille pas | Coût nul |

### Conséquences pour l'enveloppe (étape 2)

- **Les erreurs sortent sur stdout, jamais sur stderr** : stderr fait 0 octet
  dans toutes les commandes des quatre tests, y compris en code 2 et sous
  `--quiet`. L'enveloppe juge sur le code de sortie, puis analyse stdout.
- **La clé `show` ne distingue pas une lecture d'une écriture** : le DDL sous
  `dev` renvoie code 0 et `{"show": [{"status": "Table T3_DEV successfully
  created."}]}`. Pour `dbt_show_inline`, seuls le rôle `ro` et le contrôle
  lexical protègent.
- **`--limit -1` supprime le `limit` ajouté** : le `delete` de T19 est arrivé
  intact à Snowflake (erreur de privilège, pas de syntaxe).
- **`show --output json` renvoie les colonnes en majuscules** ;
  `generate_model_yaml` donne des types sans précision (`number`, `varchar`).
- **Chaque appel dbt dure 4 à 9 secondes**, connexion comprise.

Reste à lancer : T1, T2, T4 à T6, T8 à T10, T14 à T18 (durée des appels sur la
cible `broken` inconnue pour T14 et T17).

## 12. Résultats de l'étape 2 (2026-10-03)

Livré dans `claude/mcp/dbt-enveloppe/` (commit `cd393d6`) : `pyproject.toml`
et `uv.lock` (Python 3.12, `pyyaml` seule dépendance ; `mcp` viendra à
l'étape 3), `src/dbt_enveloppe/{runner,conditions,session,cli}.py`, `tests/`
(123 tests). Versions : dbt-core 1.12.5, dbt-snowflake 1.12.1, Claude Code
2.1.287.

### Critère de l'étape

| Contrôle | Résultat |
|---|---|
| `uv run pytest` | **123 passed**, `ruff check` et `ruff format` propres |
| Un cas d'échec silencieux par ligne du principe 2 | `tests/test_principle2.py` : 10 tests, docstring = ligne |
| Test-first | Tests + squelettes soumis et validés avant l'implémentation (suite rouge : 123 `NotImplementedError`) |

### Écarts et choix d'implémentation (validés avec les tests)

- **`session.py` porte l'orchestration** : une méthode par outil, runner
  injectable ; `cli.py` et `server.py` restent minces. Pas de module
  supplémentaire.
- **Toute réparse réussie efface les sélections `ls`** ; **`ls` exige un
  parse sur l'état courant** (sinon « validé depuis ce parse » n'a pas de sens).
- **`generate_source` reçoit `generate_columns: true` d'office** (sans lui, G5
  échouerait toujours). **Un `codegen` qui échoue ne laisse aucun fichier**
  (contenu invalide, colonnes vides, parse en échec).
- **`check_show` refuse une ligne `{"status": …}` seule** (sortie réelle de T3
  sous `dev`) : défense en profondeur derrière le rôle `ro` et le contrôle lexical.
- **Statuts de `build`** : succès = `success`/`pass`/`warn` (`warn` remonté) ;
  `error`, `fail`, `skipped`, `runtime error`, `partial success` échouent.
- **Garde de version** : `debug` hors 1.12.x réussit mais bloque les outils B
  et C en nommant la version.
- **CLI** : session dans `<projet>/target/dbt-enveloppe-session.json`
  (`dbt clean` = réinitialisation) ; fichier corrompu → session neuve. Le
  serveur MCP gardera l'état en mémoire (même classe `Session`).
- **Forme de `debug` en échec** (explication conservée après `N check(s)
  failed`) : extrapolée de dbt-core 1.12, **T14 non lancé** — à confirmer.

### Smoke test sur le testbed — **[Observé]** (lancé par Claude, avant l'étape 5)

| Appel | Constat |
|---|---|
| `parse` | `{"ok": true}` ; empreinte prise, session écrite dans `target/` |
| `ls --select tag:nightly --expected stg_orders` | Refus L2 : `unexpected ['stg_customers']`, liste renvoyée dans `data` |
| `ls --select "fct_*"` | **Code 2 sous `--warn-error`** : `[WARNING]: The selection criterion 'fct_*' does not match any enabled nodes`, promu en erreur. Sur dbt 1.12.5, la ligne 1 du principe 2 est déjà explicite grâce à L1 ; l'enveloppe couvre tout de même le cas code 0 + sortie vide |
| `compile` avant `debug` | Refus D3, aucun appel dbt |
| `debug` | 7 lignes conservées sur 46 (versions, 4 `[OK …]`, `All checks passed!`), aucun champ `Connection` |
| `show --name tag:nightly` | Refus K5/H4, aucun appel dbt |
| `compile --name stg_orders` | SQL compilé + `materialized: view` (jointe depuis `ls`) |
| `show --name stg_orders --limit 2` | 2 lignes, colonnes en majuscules, `note: null` |
| `show-inline --sql "create table …"` | Refus H7 avant tout appel |
| `show-inline --sql "select current_role() …"` | `DBT_AGENT_RO` / `DBT_AGENT_RO_USER` : la cible `ro` est bien imposée |

Non exercés en réel : `build` et `codegen` (étape 6, par le subagent).

### Pour l'étape 3

- API du SDK MCP Python à lire via context7 (plan §6) ; `server.py` = une
  fonction-outil par méthode de `Session`, état en mémoire, `CLAUDE_PROJECT_DIR`
  lu au démarrage par `resolve_project_dir`.
- `dbt_show_inline` : écrit et testé ; **à déclarer dans `server.py` par un
  commit dédié** (point E, condition remplie le 2026-10-02).
- Test à ajouter (plan §11) : les macros d'aide `t_exec`/`t_rows` refusées par
  la liste blanche — déjà couvert par `test_line8` (`t_exec`, `t_rows`).

## 13. Résultats de l'étape 3 (2026-10-03)

Livré (commits `afb21b3`, `bd060fc`) : `src/dbt_enveloppe/server.py`,
`tests/test_server.py` (13 tests, client MCP en mémoire), script
`dbt-enveloppe-mcp` (nom du §1.4), dépendance `mcp>=2.3,<3` épinglée dans
`uv.lock` (2.3.0). Versions : Claude Code 2.1.287, dbt-core 1.12.5,
dbt-snowflake 1.12.1.

### Critère de l'étape

| Contrôle | Résultat |
|---|---|
| `uv run pytest` | **136 passed**, `ruff check` et `ruff format` propres |
| Test-first | 11 tests + squelette soumis, choix validés en bloc, suite rouge constatée (`NotImplementedError`), puis vert ; même rituel pour les 2 tests de `dbt_show_inline` |
| `claude --mcp-config` dans le testbed | Serveur `dbt-enveloppe` `status: connected` (message `init` du flux `stream-json`, `--strict-mcp-config`) |
| Liste des outils | 8 outils `mcp__dbt-enveloppe__dbt_*` (7 au commit `afb21b3`, `dbt_show_inline` au commit `bd060fc`) ; `/mcp` interactif non joué |
| Un appel par outil | Par stdio avec le vrai dbt (script client `mcp.Client` + `StdioServerParameters`, `CLAUDE_PROJECT_DIR` posé par le script) : voir table ci-dessous ; depuis Claude Code (`claude -p`, Haiku) : `dbt_parse` → `{"ok": true}`, ~0,05 $ en tout |

### Appels réels par stdio — **[Observé]**

| Appel | Constat |
|---|---|
| `dbt_debug` | 7 lignes (versions, `[OK …]`, `All checks passed!`), aucun champ `Connection` |
| `dbt_parse` | `{"ok": true}` |
| `dbt_ls(tag:nightly, [stg_orders, stg_customers])` | `{"models": [...]}`, 2 vues |
| `dbt_compile(stg_orders)` | SQL compilé + `materialized: view` |
| `dbt_show(stg_orders, 2)` | 2 lignes, `row_count: 2` |
| `dbt_build(fct_orders)` | Refus L2 (sélection non validée), **aucun appel dbt** |
| `dbt_codegen(t_exec, …)` | Refus O1/G1 (liste blanche), **aucun appel dbt** |
| `dbt_show_inline(select current_role() …)` | `DBT_AGENT_RO` / `DBT_AGENT_RO_USER` : cible `ro` imposée à travers le serveur |
| `dbt_show_inline(create table …)` | Refus H7 avant tout appel |

`build` et `codegen` restent non exercés en réel (étape 6).

### Choix d'implémentation (validés avec les tests)

- **SDK `mcp` 2.3.0, API v2** (`MCPServer`, `@tool()`, `ToolError`) — la v1
  (`FastMCP`) n'est plus la version publiée. Un outil `def` synchrone tourne
  dans un thread de travail (vérifié dans la doc v2) : un `build` de 15 min ne
  bloque pas le serveur.
- **Échec = erreur d'outil** (`is_error`, texte = `Outcome.error`) ; si `data`
  existe (écart `ls`, `build`), il est ajouté en JSON au texte. **Succès =
  contenu structuré** : `data` tel quel ; `parse` → `{"ok": true}` ; `ls` →
  `{"models": [...]}`.
- **Projet résolu au premier appel et mis en cache** (`functools.cache` sur
  `resolve_project_dir`) : si `CLAUDE_PROJECT_DIR` ou `.venv/bin/dbt` manque,
  les outils existent et chaque appel renvoie le motif ; un `uv sync` suffit
  ensuite, sans redémarrage. Un serveur qui meurt au démarrage ne laisserait
  aucun message à l'agent.
- **État en mémoire seulement** (pas de `target/dbt-enveloppe-session.json`
  côté serveur) ; **un verrou sérialise les appels** (deux `dbt` concurrents
  sur le même `target/` se marcheraient dessus) — non testé.
- **Docstrings = descriptions d'outils** lues par l'agent, avec les
  identifiants de règles (D1, L2, H7…) ; le corps de `dbt.md` (étape 4) reste
  la source des règles.

### Constats

- Les erreurs d'outil sont journalisées par le SDK sur **stderr** (`Tool
  'dbt_build' failed: …`) ; stdout reste au protocole. Rien à faire côté
  enveloppe (le runner capture déjà la sortie de dbt).
- Le message `init` de `claude -p --output-format stream-json --verbose`
  donne le statut des serveurs et la liste des outils sans dépendre du modèle :
  utilisable à l'étape 4 pour les points 1, 2, 6 et 8 du §6.
- Pour l'étape 3, le `mcp.json` pointe sur `$HOME/dotfiles/claude/mcp/dbt-enveloppe`
  (le lien `~/.claude/mcp/` n'existe qu'à l'étape 4).

### Pour l'étape 4

- `claude/agents/dbt.md` (corps = blocs de la spec + table règle → outil),
  liens `install.sh`, `permissions.allow` sur `dbt_parse` et `dbt_ls` (point D).
- Points du §6 à observer : 1 (`${HOME}` inline, un essai), 2
  (`CLAUDE_PROJECT_DIR` dans un serveur inline de subagent), 4, 6, 8 ;
  `claude plugin details` pour l'agent vu du plugin d'eval.

## 14. Résultats de l'étape 4 (2026-10-04)

Livré : `claude/agents/dbt.md` (frontmatter du §1.4, corps = socle + 7
sections + schéma IV §1 + liste IV §4 copiés tels quels, table « règle →
outil MCP »), `tests/test_agent_sync.py` (11 tests de non-dérive spec →
agent), `install.sh` (liens `agents/dbt.md` et `mcp/dbt-enveloppe`, contrôle
`uv`, `uv sync --frozen`), `claude/settings.json` (`permissions.allow` sur
`dbt_parse` et `dbt_ls`, point D), `claude/README.md`. Versions : Claude Code
2.1.287, dbt-core 1.12.5, dbt-snowflake 1.12.1.

### Critère de l'étape

| Contrôle | Résultat |
|---|---|
| `uv run pytest` | **147 passed** (136 + 11), `ruff check` et `ruff format` propres |
| Test-first | Test de synchronisation écrit avant l'agent : 10 erreurs (fichier absent), 1 passé (la spec a ses 8 blocs) ; vert après écriture |
| L'agent ne voit que Read/Grep/Glob/Edit/Write + outils MCP | **[Observé]** : liste rapportée par le subagent lui-même (`claude -p`, Haiku, depuis le testbed) : `Read, Edit, Write, Grep, Glob` + les 8 `mcp__dbt-enveloppe__dbt_*` ; pas de Bash |
| `install.sh` idempotent | Relancé en entier : liens existants recréés à l'identique, 2 nouveaux, `uv sync --frozen` → « Checked 35 packages » |

### Points du §6 — tous **[Observé]** (Claude Code 2.1.287, mode `-p`)

| # | Point | Constat |
|---|---|---|
| 1 | `${HOME}` dans `args` inline sans `sh -c` | **Non expansé.** Agent d'essai hors dotfiles, identique à `dbt.md` (mêmes `tools`, même nom de serveur) sauf `command: uv`, `args: ["run", "--project", "${HOME}/.claude/mcp/dbt-enveloppe", …]` : le subagent n'a que `Read, Edit, Write, Grep, Glob`, aucun outil MCP. Le `sh -c` du §1.4 est nécessaire. Essai supprimé après lecture |
| 2 | `CLAUDE_PROJECT_DIR` dans un serveur inline de subagent | Posé : `dbt_parse` → `{"ok": true}` à travers le serveur inline (il refuse sans la variable) |
| 4 | Agent en lien symbolique dans `~/.claude/agents/` | `dbt` figure dans `agents` du message `init` ; délégation réussie |
| 6 | Règle `allow` sur un serveur inline | Appliquée : `dbt_parse` sans prompt. Contre-épreuve : `dbt_debug` (hors `allow`) → `Permission to use mcp__dbt-enveloppe__dbt_debug has been denied` en mode non interactif. Le point D tient tel quel |
| 8 | Dialogue de confiance | Aucun : serveur connecté en `-p` (un dialogue l'aurait bloqué). Doc relue le 2026-10-04 : le contrôle de confiance (≥ 2.1.238) ne vise que `.claude/agents/` du projet et les dossiers `--add-dir` |

Forme du frontmatter vérifiée dans la doc le 2026-10-04 : `mcpServers` est
une **liste** d'entrées `- nom: {type, command, args}` ou de noms de serveurs
déjà configurés — celle du §1.4.

### Constats

- **Un agent dont `tools` ne liste que `mcp__<serveur-inline>__*` est refusé
  au spawn** : « would be spawned with zero tools — refusing. Its tools list
  resolved to nothing: recognized but matched no tools in this session ». Les
  outils d'un serveur inline ne sont pas résolus avant le lancement ; au moins
  un outil natif est requis dans `tools`. Sans effet sur `dbt.md` (5 outils
  natifs), à savoir pour tout agent « MCP seul ».
- **Vu du plugin d'eval** (`claude --plugin-dir ./claude plugin details
  dotfiles`) : `Agents (2) tech-watch-scorer, dbt`, `MCP servers (0)` — le
  `mcpServers` inline est ignoré en contexte plugin, comme dit par la doc.
  Sans effet sur les sessions quotidiennes (`claude plugin details dotfiles`
  sans `--plugin-dir` → « not found » : plugin non installé). Coût estimé par
  le runner : ~130 tok always-on (description), ~3,4k on-invoke.
- **Le relais du rapport par la session principale est lossy** : Haiku a
  omis `dbt_show_inline` de la liste et le résultat brut de `dbt_parse` en
  résumant. Pour observer, lire les événements du flux `stream-json` portant
  `parent_tool_use_id` (texte et appels du subagent), pas le résumé final.
- **Le subagent part en arrière-plan même en `-p`** (« Async agent launched
  successfully ») ; la session attend sa fin avant de répondre.
- **`model: opus` et `effort: high` fixés** (décision Greg, 2026-10-04, doc
  `model-config` relue) : l'alias `opus` suit la dernière Opus (5.5 à ce
  jour, 4 $/20 $ par MTok contre 10 $/50 $ pour Fable 5.1) — le garde-fou est
  dans l'enveloppe, pas dans le modèle. L'effort est explicite parce que le
  défaut d'Opus 5.5 est `medium` et que la clé `effortLevel` top-level des
  settings ne s'applique pas à ce modèle : sans le champ, le niveau hérité
  serait indéterminé. `high` est un point de départ, pas un plafond
  (`xhigh`, `max` existent) ; **critère de révision à l'étape 6** : refus de
  l'enveloppe et reprises par tâche — `xhigh` si l'agent cale sur la
  modélisation, `medium` s'il ne cale jamais. Pas de réglage thinking par
  subagent (hérite de la session, doc `sub-agents`).
- La `description` coûte ~130 tok dans chaque session — à raccourcir si besoin.
- Coût des trois appels `claude -p` : 0,049 + 0,019 + 0,027 ≈ 0,10 $.

### Pour l'étape 5

- `"Bash(dbt *)"` dans `permissions.deny` ; hook `block-dbt.sh` sur le modèle
  de `block-rm-rf.sh`, **sans champ `if`** (plan §2), lanceurs `uv run`,
  `uvx`, `python -m`, `sh -c`, chemin finissant par `/dbt` ; table « doit
  bloquer / doit passer » ; lien dans `install.sh`.
- Point 5 du §6 (règles `deny` appliquées dans les subagents) : test avec un
  subagent disposant de Bash.
- Après l'étape 5, plus aucun appel dbt brut par Claude : `t_series.sh` à la
  main de Greg (point F) ; les tests de l'enveloppe passent par le subagent.

## 15. Résultats de l'étape 5 (2026-10-04)

Livré : `claude/hooks/block-dbt.sh` (hook `PreToolUse`, matcher `Bash`, **sans
champ `if`**), `claude/settings.json` (`"Bash(dbt *)"` dans `permissions.deny`
+ entrée hook), `install.sh` (lien du hook), `claude/README.md`,
`tests/test_block_dbt_hook.py` (58 tests : 31 « doit bloquer », 23 « doit
passer », message, 3 réglages). Versions : Claude Code 2.1.287, mawk 1.3.4,
jq 1.6, shellcheck 0.11.0.

### Décision préalable (Greg, 2026-10-04)

- **`dbt docs generate` reste manuel** — comme `deps`, `seed`, `snapshot`,
  `source freshness`, `test` seul, `clean`, `run-operation` hors codegen : rien
  de ce que l'enveloppe n'expose pas n'est accessible à Claude après cette
  étape (le subagent n'a pas Bash, la conversation principale a dbt bloqué).
  Cohérent avec la spec (l'agent n'exécute que la boucle de modélisation).
- **Candidat event-driven** : un 9ᵉ outil `dbt_docs_generate` (appel canonique,
  cible `ro` probable, succès = code 0 **et** `target/catalog.json` +
  `manifest.json` réécrits par l'appel **et** non vides ; commit dédié,
  test-first, sur le modèle de `dbt_show_inline`, ~30 min). À ouvrir à la
  première fois où Greg lance `docs generate` à la main après une session de
  l'agent. Une exception dans le hook pour la conversation principale est
  écartée : elle casserait « dbt uniquement par l'enveloppe ».
- **Flux attendu pour `deps`** : `dbt_parse` échoue (« packages spécifiés mais
  non installés »), l'enveloppe renvoie le message, le subagent le remonte, la
  conversation principale demande `! uv run dbt deps`, Greg relance.

### Critère de l'étape

| Contrôle | Résultat |
|---|---|
| `uv run pytest` | **205 passed** (147 + 58), `ruff check` et `ruff format` propres ; `shellcheck` 0 trouvaille sur `block-dbt.sh` (et sur les 4 scripts existants) |
| Test-first | Table écrite avant le hook : 49 échecs (hook absent) ; validée par Greg (table + choix de conception + option B heredoc) ; 48 cas de comportement verts au premier passage du hook, puis 2 réglages. Un faux positif rencontré en usage réel ensuite (ci-dessous) → 6 cas ajoutés, découpage réécrit, 58 verts |
| `dbt`, `uv run dbt`, `python -m dbt`, chemin absolu bloqués | Tests verts + **[Observé]** `claude -p` (Haiku, testbed) : `uv run dbt --version` et `dbt --version` → `PreToolUse:Bash hook error: […] BLOCKED: dbt is never run from Bash…`, message complet lu par le modèle |
| `dbt-enveloppe` et message de commit contenant « dbt » passent | Tests verts (`dbt-enveloppe parse`, `uv run … dbt-enveloppe-mcp`, 2 heredocs de commit dont un avec une ligne commençant par `dbt`) |
| `install.sh` idempotent | Relancé en entier : liens recréés à l'identique, hook lié, « Checked 35 packages » |

### Points du §6 — Claude Code 2.1.287, mode `-p`

| # | Point | Constat |
|---|---|---|
| 5 | Règle `deny` dans un subagent avec Bash | **[Observé]** avant activation du hook (il la précède et la masque ensuite) : agent d'essai `bash-probe` (`tools: Bash`, Haiku, hors dotfiles, supprimé après lecture), `--allowedTools "Bash(echo probe-ok),Bash(dbt --version),Agent"` : `echo probe-ok` → `probe-ok` ; `dbt --version` → `Permission to use Bash with command dbt --version has been denied`. La règle `deny` des settings user s'applique dans le subagent **et prime sur un `allow` explicite passé en CLI** |
| — | Hook dans un subagent avec Bash (dit par la doc) | **[Observé]** : même agent d'essai, `uv run dbt --version` → message `BLOCKED` du hook |
| 9 | `!` échappe au hook | **Non observé** : `-p` est non interactif. À faire par Greg en session interactive, depuis `~/dbt-agent-testbed/` : `! uv run dbt --version` doit s'exécuter ; demander ensuite à Claude de lancer la même commande doit produire le `BLOCKED` |
| — | Prise en compte à chaud d'un hook ajouté à `settings.json` | **[Observé]**, contraire à la doc `hooks` (« snapshot au démarrage ») : le hook a bloqué un appel Bash de la session même qui venait de l'ajouter, sans redémarrage ni passage par `/hooks`. Fichier lié par symlink depuis les dotfiles |

### Choix de conception du hook (validés avec les tests)

- **Position de commande** : chaque ligne est découpée en commandes simples
  sur `;`, `&`, `|`, `$(`, `` ` `` ; dans chaque segment, après les `VAR=val`,
  le premier mot est jugé. `git commit -m "… dbt build …"`, `echo "dbt build"`,
  `grep "dbt run"` passent : les arguments d'une commande ordinaire sont des
  données.
- **Découpage conscient des guillemets** (ajouté après un faux positif réel :
  `grep -n "block-rm-rf\|hooks/\|dbt" claude/README.md` bloqué, l'alternative
  `\|dbt` du motif devenant un segment commençant par `dbt`). Les guillemets
  simples et doubles protègent `;`, `&`, `|` ; **`$(` et `` ` `` ouvrent
  toujours un segment dans les guillemets doubles** (sinon `echo "$(dbt ls)"`
  passerait). L'état des guillemets est remis à zéro à chaque ligne. Le
  pré-traitement `sed` de `block-rm-rf.sh` est remplacé par ce découpeur awk ;
  `block-rm-rf.sh` garde la même faiblesse (`grep "a\|rm -rf"` bloqué),
  non corrigée ici.
- **Shell nourri par la ligne** : un lanceur sans commande à lancer (`sh`,
  `uv run python`…) lit son script ailleurs sur la ligne (`echo 'dbt run' |
  sh`) : toute la ligne est alors inspectée en mode « tous les jetons ».
- **Derrière un lanceur** (`uv`, `uvx`, `pipx`, `poetry`, `pdm`, `hatch`,
  `pixi`, `conda`, `mamba`, `run`, `tool`, `sh`, `bash`, `zsh`, `dash`, `ksh`, `exec`,
  `command`, `builtin`, `eval`, `sudo`, `env`, `time`, `nice`, `nohup`,
  `timeout`, `stdbuf`, `xargs`, `python[0-9.]*` et `*/python[0-9.]*`), **tous
  les jetons restants** sont inspectés : `dbt`, `*/dbt`, `dbt.*`. C'est ce qui
  attrape `uv run --project X --no-sync dbt` sans connaître les options de
  `uv`, et `python -c "from dbt.cli.main import dbtRunner; …"` (5ᵉ contournement,
  non cité par la doc). Fail-closed.
- **Faux positifs tolérés** (hors table, ni bloqués ni passants attendus) :
  `sh -c 'echo dbt'`, `python -c "import dbt"`, un chemin finissant par `/dbt`
  derrière `uv run`. Pas rencontrés en usage ; Claude reformule.
- **Heredocs (option B, décision Greg)** : un `<<EOF` reçu par une commande
  ordinaire (`cat`, `git`, `tee`) fait sauter les lignes jusqu'au délimiteur ;
  reçu par un lanceur (`bash <<EOF`, `python <<EOF`), les lignes restent
  inspectées en mode « tous les jetons ». Les here-strings `<<<` ne sont pas
  des heredocs. Résidu : une chaîne multi-ligne entre guillemets sans heredoc
  (Claude n'en écrit pas pour les commits).
- Jetons nettoyés de leurs guillemets et parenthèses/accolades englobantes
  (`'dbt`, `(dbt` sont vus comme `dbt`).
- **Limite connue reconduite** (§7) : un script qui appelle dbt en interne
  (`bash run.sh`, `make`) n'est pas bloqué. La garantie structurelle est
  celle du subagent (pas de Bash) ; le hook protège la conversation principale
  contre l'invocation directe.

### Constats

- **Le hook précède la règle `deny`** : pour `dbt --version`, c'est le message
  du hook que le modèle lit. La règle reste utile sans hook (settings copiés
  sans le script) et comme deuxième couche.
- **`--allowedTools` avec plusieurs valeurs séparées par des espaces avale le
  prompt** (« Input must be provided either through stdin… ») ; une liste
  séparée par des virgules **et** le prompt par stdin ont fonctionné.
- **Faux positif de `block-force-push.sh`** : une commande sans `git push`
  mais contenant le nom de fichier `block-force-push.sh` a été bloquée
  (« git push --force is not allowed ») — le filtre `if` est fail-open sur les
  commandes composées et le script cherche « force » sans ancrer sur `git
  push`. Amélioration adjacente, non corrigée ici.
- **shellcheck installé** (`uv tool install shellcheck-py`, 0.11.0.1 ; choix
  uv plutôt qu'apt : version amont, sans sudo, même paquet que le hook
  pre-commit `shellcheck-py`). Les 5 scripts (`claude/hooks/*.sh`,
  `install.sh`) sortent sans trouvaille, toutes sévérités ; aucun commit de
  triage nécessaire. Intégration pre-commit : décision à part, non prise.
- Coût des trois appels `claude -p` : 0,033 + 0,025 + 0,035 ≈ 0,09 $.

### Pour l'étape 6

- **Greg d'abord** : observer le point 9 du §6 en session interactive
  (`! uv run dbt --version` passe ; la même commande demandée à Claude est
  bloquée). Si `!` était aussi bloqué, le repli est le terminal hors Claude
  Code — viable, à consigner.
- Rejeu T0, T3, T7, T13, T19 par le subagent réel (`dbt_debug`, `dbt_parse`,
  `dbt_ls`, `dbt_compile`, `dbt_show`, `dbt_show_inline`, puis `dbt_build` et
  `dbt_codegen` pour la première fois en réel), puis le reste de T1–T21 ;
  lire les événements `parent_tool_use_id` du flux `stream-json`, pas le
  résumé (§14). Tests bruts : `t_series.sh` à la main de Greg (point F).
- **Critère de révision de l'effort** (§14) : refus de l'enveloppe et reprises
  par tâche — `xhigh` si l'agent cale sur la modélisation, `medium` s'il ne
  cale jamais.
- `/code-review` sur le diff de branche avant la PR.

## 16. Résultats de l'étape 6 (2026-10-04)

Méthode : `claude -p --output-format stream-json --verbose --model haiku
--permission-mode acceptEdits --allowedTools "Agent,mcp__dbt-enveloppe"` depuis
`~/dbt-agent-testbed/`, prompt par stdin ; la session principale (Haiku)
délègue au subagent `dbt` réel. Lecture des événements `parent_tool_use_id`
(appels, réponses de l'enveloppe, texte du subagent), pas du relais. Lanceur et
lecteur `jq` : `~/dbt-agent-testbed-results/step6/{run_subagent,read_subagent}.sh`,
transcripts `*.jsonl` à côté — **hors du projet dbt** (voir constat 2).
Versions : Claude Code 2.1.289, subagent `claude-opus-5-5` (alias `opus`),
dbt-core 1.12.5, dbt-snowflake 1.12.1.

### Runs par le subagent réel — tous **[Observé]**

| Run | Demande | Appels du subagent | Constat | Coût |
|---|---|---|---|---|
| A | `dbt debug` (T0, T13) | `dbt_debug` | 7 lignes de statut + versions, `All checks passed!`, aucun bloc `Connection`, aucun secret dans le transcript entier (`grep` account/private_key/password/warehouse : 0 hors la phrase du subagent expliquant ce qu'il ne montre pas) ; aucune interaction navigateur en `-p` (T0) | 0,11 $ |
| B | 3 demandes en une : rôle courant (T19), `create table` inline (T3), `run-operation --sql` (T7) | Haiku a lancé **3 subagents `dbt` en parallèle** | T3 : refus **au niveau de l'agent**, sans appel d'outil (« H7, point 5 de IV §4 ») ; T7 : refus au niveau de l'agent (« O2, aucun outil ne le permet »), aucun contournement ; T19 : non abouti — `Connection closed` puis `P1` en boucle (constats 1 et 2) ; le subagent a repris proprement (D3 → `debug` → `parse`), réessayé une fois, puis rapporté l'échec mot pour mot sans contourner | 0,19 $ |
| C | Rôle courant seul (T19) | `debug` → `parse` → `show_inline` | `ROLE_NAME = DBT_AGENT_RO`, `SECONDARY_ROLES = {"roles":"","value":""}` — identique au T19 brut du 2026-10-02 | 0,11 $ |
| D | Créer `stg_nation` (vue, source `tpch.NATION`, snake_case), construire, aperçu, YAML codegen | `Glob`, `debug`, 3 `Read`, `Grep`, `Write`, `parse` ×2, `ls`, **`build`**, `show`, **`codegen`**, `parse` | Premier `dbt_build` réel : `{"counts":{"success":1},"models":[{"name":"stg_nation","materialized":"view","status":"success"}],"warnings":[]}` ; `dbt_show` 5 lignes ; `dbt_codegen(generate_model_yaml)` **après** le build (G4 respecté) → 383 octets, 4 colonnes typées (`number`, `varchar`) ; `ls` a confirmé `view` héritée du dossier ; **0 refus, 0 reprise forcée** ; fichiers laissés non commités dans le testbed (`stg_nation.sql`, `_stg_nation.yml`) | 0,17 $ |

| E | SQL compilé + aperçu de `fct_orders` (T6) ; SQL compilé de `orders_by_status` (T17) | `debug`, `parse`, `ls` (2 noms), `compile`, `show`, `compile` | T6/H3/K4 : SQL compilé **avec** le filtre `is_incremental` (`where order_date > (select max(order_date) from DBT_AGENT_DEV.DEV.fct_orders)`), `materialized: incremental` ; `dbt_show` → `row_count: 0` **avec la note H3 de l'enveloppe** (« 0 rows is expected for a built incremental model… use dbt_compile with full_refresh »), relayée telle quelle par le subagent. **T17/K3 : écart** — `dbt_compile("orders_by_status")` a **réussi** et le `run_query` s'est exécuté (statuts `F`/`O`/`P` dans le SQL ; `logs/dbt.log` 14:16:01 : `introspect: False` dans les arguments **et** `select distinct o_orderstatus from SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS` envoyée sur la connexion `list_DBT_AGENT_DEV_DEV`). Voir constat 6 | 0,15 $ |

| F (après `98b483a`, cible `ro`) | Rejeu compile/show de `fct_orders`, compile de `orders_by_status`, compile d'un modèle `run_query` à **effet de bord** (fixture T17 copiée dans `models/_fixture/`), codegen de `stg_nation` vers un 2ᵉ YAML | `debug`, `parse`, `ls` ×4 (en parallèle), `compile`, `show`, `compile(full_refresh)`, `compile` ×2, `show`, `Read` ×2, `build`, `codegen`, `Glob`, `parse` | Sous `ro` : SQL compilé de `fct_orders` et d'`orders_by_status` **identiques** au run E (la lecture `run_query` passe) ; le subagent a de lui-même relancé `compile(full_refresh=true)` pour montrer le SQL sans filtre (suite à la note H3) ; **modèle à effet de bord : refusé** (`Schema 'DBT_AGENT_DEV.T_SCRATCH' does not exist or not authorized`) ; codegen vers `_stg_nation_ro.yml` : **G5 observé en réel** — `dbt parse` échoue (« two schema.yml entries for the same resource named stg_nation »), fichier supprimé par l'enveloppe, `Glob` du subagent confirme l'absence. Voir constats 7 et 8 | 0,25 $ |
| F bis (CLI de l'enveloppe, même code) | Fixture pointée sur le schéma **existant** `DEV` | `debug`, `parse`, `ls`, `compile`, `show-inline` | `compile` → `003001 (42501): SQL access control error: Insufficient privileges to operate on schema 'DEV'. Your primary role DBT_AGENT_RO must have CREATE TABLE granted on SCHEMA DBT_AGENT_DEV.DEV.` ; puis `select count(*) from information_schema.tables where table_name = 'T17_SIDE_EFFECT'` → **0** : rien n'a été créé. **K3 structurelle [Observé]**. Fixture retirée du projet ensuite | — |

| G | Construire tout `tag:nightly` tests compris (T4) ; `generate_source` sur `REGION`, `PART` de `TPCH_SF1` en majuscules (T8) | `debug`, `Grep`, `Read`, `parse`, `Glob`, `ls`, **`build`**, `Glob`, `codegen`, `Read` | T4/L1–L4 : liste attendue **déduite par le subagent** (`+tags: [nightly]` sur le dossier `staging` dans `dbt_project.yml` + `Glob` des `.sql`) → `dbt_ls("tag:nightly", expected=[stg_orders, stg_customers, stg_nation])` conforme ; `dbt_build("tag:nightly")` → `{"success":3,"pass":3}`, `warnings: []` (3 vues + 3 tests). T8/G2 : `generate_source(schema_name=TPCH_SF1, database_name=SNOWFLAKE_SAMPLE_DATA, table_names=[REGION, PART])` → 859 octets, **12 colonnes**, **tout en minuscules** (source `tpch_sf1`, tables `region`/`part`, colonnes `r_regionkey`…, types `number`/`varchar`) — exploitable tel quel sur Snowflake (identifiants non cités insensibles à la casse). Hypothèse §E levée. 0 refus | 0,20 $ |
| H | Créer `stg_region` (source `tpch_sf1.region`) et `dim_region` (table, jointure) ; **« ne construis rien »** ; aperçu de `dim_region` (T5) ; YAML de `stg_region` par codegen (T9 non construit) | `Glob`, `Read` ×5, `Glob`, `Read`, `Write` ×2, `debug`, `parse`, `ls` (3 noms), `compile` ×3, `show_inline` | T5/H5 : le subagent **n'a pas appelé `dbt_show("dim_region")`** — il a anticipé l'échec (amont `stg_region` non construit) et recomposé l'aperçu en `show_inline` lecture seule à partir du SQL compilé des deux amonts, en l'expliquant (5 lignes correctes). Il a supposé à tort que `stg_nation` n'existait pas non plus (construit aux runs D, F, G) : il **ne peut pas savoir ce qui est construit** (constat 8, 2ᵉ occurrence, sens inverse). T9/G4 : **codegen non lancé** sur le modèle non construit, consigne « ne rien construire » respectée, arbitrage demandé (construire `stg_region` seul, ou YAML à la main). Remarque adjacente signalée sans correction : `dim_customers` lit `source('tpch','NATION')` au lieu de `ref('stg_nation')`. 0 refus de l'enveloppe | 0,18 $ |
| H bis (CLI) | `generate_model_yaml` sur `stg_region` **non construit** | `parse`, `ls`, `codegen` | `{"ok": false, "error": "generate_model_yaml: 'stg_region' has no columns; build the model first (G4, G5)"}`, code 2, **aucun fichier laissé** (`_stg_region.yml` absent). **G4/G5 [Observé]** sur Snowflake | — |
| T21 (CLI, partiel) | `query_history` des 3 dernières heures vue par `ro` | `show_inline` | 44 requêtes, toutes `QUERY_TAG = dbt-agent-ro`, `USER_NAME = DBT_AGENT_RO_USER`. Les requêtes `dev` (autre utilisateur, tag `dbt-agent`) ne sont pas visibles au rôle `ro` : à confirmer par Greg dans Snowsight | — |

Coûts rapportés par `claude -p` (session + subagent) : 1,36 $ pour les 8 runs.

### Point 9 du §6 — **[Observé]** (session interactive, Claude Code 2.1.289)

`! uv run --project ~/dbt-agent-testbed dbt --version` tapé par Greg dans la
session : `Core: installed 1.12.5`, `snowflake: 1.12.1`, aucun hook. La même
commande lancée par l'outil Bash de Claude dans la même session :
`PreToolUse:Bash hook error: [~/.claude/hooks/block-dbt.sh]: BLOCKED…`. Le
canal `!` est donc bien celui de `deps`, `docs generate`, etc.

### Tests bruts T1, T2, T10, T14, T17, T18 — `t_series.sh` lancé par Greg le 2026-10-04 (15:02–15:05), tous **[Observé]**

| T | Constat brut (Snowflake, dbt-core 1.12.5, dbt-snowflake 1.12.1) | Règle |
|---|---|---|
| T1 | `show --limit 5` d'un modèle finissant par `limit 3` → code 2, `001003 (42000): syntax error line 5 at position 2 unexpected 'limit'` (dbt colle son `limit` à la fin, pas de sous-requête) ; `--limit -1` → code 0, aperçu. **Identique à DuckDB** | H6 confirmée ; sous l'enveloppe, `dbt_show` renverra l'erreur et l'agent doit retirer le `limit` du modèle |
| T2 | `show --inline "select 1 as x;"` → code 2, `syntax error line 1 at position 0 unexpected 'limit'` ; avec `--limit -1` → code 0 ; témoin sans `;` → code 0. **Identique à DuckDB** | H6/H7 ; l'enveloppe retire le `;` final avant dbt (`normalize_inline_sql`) |
| T10 | `run-operation generate_model_yaml --quiet > f.yml` → 381 o, YAML propre, parse canonique code 0 ; **sans `--quiet`** → 526 o, `Running with dbt=…` en tête du fichier, parse code 2 (`Syntax error near line 2`) ; modèle inconnu → code 1, `depends on a node named 'does_not_exist' which was not found`. stderr toujours 0 o | G2/G5 confirmées ; `--quiet` indispensable à la redirection |
| T14 | `debug --quiet --target broken` → **code 1, 0 octet** ; sans `--quiet` → 2 068 o : compte (faux), utilisateur, rôle, `host: None`, `Connection test: [ERROR]`, **aucune ligne clé/mot de passe** (grep `private_key`, `.p8`, `password` : 0) | D1 et D2 confirmées sur Snowflake |
| T17 | `compile` de `run_query_side_effect` sous `dev` **avec** introspection → table `T17_SIDE_EFFECT` créée ; helper drop ; **`--no-introspect`** → **table créée à nouveau** (`['T17_SIDE_EFFECT']`, 1 ligne). Cible `broken` : `--no-introspect` seul → code 2 (`290404 (08001): 404 Not Found … login-request`, dbt se connecte quand même pour le cache) ; `--no-populate-cache --no-introspect` → code 0, SQL compilé de `dim_customers` **sans connexion** | **Constat 6 confirmé en brut** : `--no-introspect` n'empêche aucune requête introspective ; c'est `--no-populate-cache` qui évite la connexion (et seulement pour un modèle sans `run_query`). La parade `ro` (`98b483a`) est la bonne |
| T18 | `materialized='nonsense'` : parse code 0, `compile` code 0 (64 o), **`run` code 1** : `No materialization 'nonsense' was found for adapter snowflake!` ; `materialized='dynamic_table'` : `build` code 0 (`PASS=1`), lecture sous `ro` code 0 | S5 confirmée : seul `run`/`build` détecte ; `dynamic_table` est une matérialisation valide de l'adaptateur (spec §F.3 fait 7) |

### Couverture T0–T21 à l'issue de l'étape

| Tests | État |
|---|---|
| T0, T3, T4, T6, T8, T9 (construit et non construit), T13, T15, T17, T19 | **[Observé]** par l'enveloppe (subagent ou CLI, même code) |
| T1, T2, T10, T14, T17, T18 | **[Observé]** en brut (`t_series.sh`, table ci-dessus) |
| T5, T7 | Agent-level : le subagent contourne (T5, lecture seule) ou refuse (T7) sans appel ; brut déjà **[Observé]** le 2026-10-02 pour T7 (§11) ; T5 brut non lancé (couvert par H5 côté agent et par l'erreur Snowflake « does not exist » que `dbt_show` renverrait) |
| T16 | **[Observé]** au smoke test de l'étape 2 (§12) |
| T21 | **[Observé]** sur les deux cibles : `ro` via `show_inline` (44 requêtes `dbt-agent-ro`, `DBT_AGENT_RO_USER`) ; `dev` lu par Greg dans Snowsight *Query History* (filtre `Query Tag = dbt-agent` → 15 requêtes, toutes de `DBT_AGENT_RW_USER`). Le `query_tag` du profil est bien transmis en paramètre de session (spec §F.3 fait 8 confirmé) |
| T11, T12 | **Actés « non mesurés, hors périmètre »** (décision Greg, 2026-10-04) : l'enveloppe plafonne déjà les sorties (`limit ≤ 50`, listes de statuts au lieu de journaux, SQL compilé seul) ; la mesure n'a plus d'enjeu de décision |
| T20 | **Non implémenté** : un schéma par session d'agent (spec §F.3 fait 7) n'est pas dans l'enveloppe — cible `dev` unique, schéma `DEV`. À décider au livrable de fin (candidat : `schema` dérivé d'un identifiant de session via `--vars` ou profil) |

État du testbed après les runs : les 5 fichiers écrits par le subagent
(`models/staging/stg_nation.sql`, `_stg_nation.yml`, `_tpch_extra__sources.yml`,
`stg_region.sql`, `models/marts/dim_region.sql`) **commités dans le testbed**
(`0434792`, décision Greg) comme trace de ce que l'agent produit ; vue
`stg_nation` construite dans `DBT_AGENT_DEV.DEV` ; `stg_region` et `dim_region`
non construits.

### Étape 6 close le 2026-10-04

Critère du §8 tenu : chaque résultat **[Observé]** avec versions (Claude Code
2.1.289, subagent `claude-opus-5-5`, dbt-core 1.12.5, dbt-snowflake 1.12.1) ;
T20 non implémenté et T11/T12 actés hors périmètre, en toute connaissance.
Reste avant la PR : livrable de fin (`livrable.md`), `/code-review` sur le
diff de branche (session dédiée), triage.

### Constats

1. **Subagents `dbt` concurrents : le serveur inline est partagé par nom.**
   Log MCP (`~/.cache/claude-cli-nodejs/-home-martin-dbt-agent-testbed/mcp-logs-dbt-enveloppe/`) :
   pendant le `dbt_parse` du 1er subagent, Claude Code a envoyé `SIGINT` puis
   `SIGTERM` au serveur (« Cleared connection cache for reconnection »), au
   moment où les 2 autres subagents se terminaient. Le 1er a reçu `Connection
   closed`, puis un serveur neuf — **état de session perdu** (`D3` exigé à
   nouveau). L'enveloppe s'est comportée comme prévu (état par processus,
   refus explicite) ; c'est la concurrence de plusieurs subagents du même type
   qui est hostile. **Décision Greg (2026-10-04)** : une phrase ajoutée à la
   `description` de `dbt.md` (lue par la session principale) — « Un seul
   subagent dbt à la fois : séquencer les demandes, jamais en parallèle
   (serveur MCP partagé par nom) » ; ~20 tokens always-on.
2. **L'empreinte couvre tout le projet** (`session.fingerprint` : tout fichier
   non caché hors `target/`, `dbt_packages/`, `logs/` de premier niveau). Les
   transcripts `results/step6/*.jsonl` écrits pendant le run invalidaient chaque
   parse (`P1`) ; le subagent a reparsé une fois, constaté la récidive, et
   rapporté sans contourner. Artefact du banc (transcripts déplacés hors du
   projet) ; révèle un choix : empreinte large (toute écriture tierce dans
   l'arbre pendant une session = reparse) ou restreinte aux chemins que dbt
   lit (`*-paths` de `dbt_project.yml`, `dbt_project.yml`, `packages.yml`,
   `selectors.yml`). **Décision Greg (2026-10-04) : empreinte large conservée**
   (fail-closed, zéro code) ; contrat écrit dans `claude/README.md`, section
   du serveur.
3. **`Write` et `dbt_parse` dans le même lot d'appels** (run D) : le subagent
   l'a remarqué lui-même et a relancé `parse` seul. Si le parse avait précédé
   l'écriture, l'empreinte l'aurait rattrapé au prochain appel (`P1`) — la
   course est couverte par construction.
4. **Haiku comme session principale découpe une demande multiple en
   délégations parallèles** (run B) — c'est la cause du constat 1. En usage
   réel la session principale est Fable ou Opus ; à surveiller.
5. **Critère d'effort** : sur la seule tâche de modélisation (D), aucun refus
   ni reprise ; le compte rendu final est complet mais long (tableau d'aperçu,
   « reste à faire » avec rappel des conventions) — pas un défaut de l'enveloppe.
   Trop tôt pour passer à `medium` : attendre les tests T restants.
   **Bilan après 8 runs (D à H)** : 0 refus non voulu, 0 reprise forcée, 0
   « cale » ; deux règles anticipées (H3 → `compile(full_refresh)`, H5 →
   `show_inline`). Le critère littéral donnerait `medium`. **Décision Greg
   (2026-10-04) : `effort: high` conservé** — le banc n'a que des vues de
   staging triviales ; révision reportée à la première tâche sur un vrai
   projet dbt (même critère : refus et reprises par tâche).
6. **`--no-introspect` n'empêche pas `run_query` sur dbt-core 1.12.5 +
   dbt-snowflake 1.12.1** (run E, T17). La doc dbt (`reference/commands/compile`,
   relue via context7 le 2026-10-04) dit « dbt will raise an error if a
   resource's definition requires running one » ; observé : aucune erreur, la
   requête part sur une connexion de thread ouverte à la demande. Lecture :
   sur le banc DuckDB le drapeau « marchait » par effet de bord (pas de
   connexion maître → `Connection already closed`) ; Snowflake ouvre une
   connexion par thread et la requête passe. **La garde K3 est donc une
   consigne, pas un garde-fou** : un modèle au `run_query` à effet de bord
   (fixture `run_query_side_effect.sql`) écrirait dans l'entrepôt pendant
   `dbt_compile`, sous la cible `dev`. Parade structurelle candidate (principe
   3) : exécuter `dbt_compile`, `dbt_show` et `dbt_codegen` sous la cible `ro`
   — même base, schéma et warehouse que `dev` (profil §5), SQL compilé
   identique, métadonnées et lectures suffisantes sous `ro` (§11), toute
   écriture refusée par Snowflake (H7). `dbt_build` reste seul sous `dev`.
   `--no-introspect` conservé (inoffensif, saute la population du cache).
   **Décision Greg (2026-10-04) : fait**, `98b483a` — test-first (3 tests
   rouges validés, 205 verts), docstrings, table règle → outil de `dbt.md` ;
   vérifié en réel (runs F et F bis). Écart à reporter dans la spec au
   livrable de fin : K3 n'est plus « `--no-introspect` » mais « cible `ro` »,
   et `show`/`codegen` quittent le « schéma de dev » de la lettre de H1/G1
   (même schéma, rôle différent).
7. **Le rapport final du subagent n'est pas un événement texte `SUB`** : en
   `-p`, il arrive dans le `task_notification` et dans le `tool_result` de
   hand-back (encadré « [Subagent hand-back] … model output, NOT a message
   from the user »). Le lecteur `read_subagent.sh` ne le voit pas ; lire aussi
   `select(.subtype=="task_notification")`.
8. **Le subagent rebâtit avant codegen quand il ne peut pas savoir si le
   modèle est construit** (run F : `dbt_build("stg_nation")` avant
   `generate_model_yaml`, en invoquant G4). Sur une vue c'est gratuit ; sur
   une grosse table ce serait un rebuild inutile. L'enveloppe n'expose pas
   « construit ou non » — candidat event-driven, pas construit.
9. **Appels parallèles au sein du subagent** : 4 `dbt_ls` simultanés (run F)
   sur le même serveur — sans incident (appels sérialisés par le verrou du
   serveur).

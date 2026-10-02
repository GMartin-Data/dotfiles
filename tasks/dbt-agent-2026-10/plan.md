# Plan — agent dbt au scope user (subagent + serveur MCP « enveloppe »)

> **Statut : plan validé par Greg le 2026-10-02.** Les points A à F du §7 sont
> tranchés et priment sur les formulations « à valider » restées dans les §1, §3
> et §5. **Étape 1 faite le 2026-10-02** (T0 **[Observé]**, constats au §10).
> Prochaine action : étape 1 bis (§8).

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
| 5 | Les règles `permissions.deny` des settings user s'appliquent dans les subagents | Non dit explicitement (dit pour les hooks) | Test à l'étape 5 avec un subagent disposant de Bash |
| 6 | Une règle `allow` `mcp__dbt-enveloppe__dbt_parse` vise bien un serveur inline | Syntaxe documentée, cas inline non | Test à l'étape 4 |
| 7 | `/mcp` liste-t-il un serveur inline pendant l'exécution du subagent | Non dit | L'étape 3 passe par `claude --mcp-config` (rien de persistant) |
| 8 | Absence de dialogue de confiance pour un serveur inline d'un agent de scope user | Implicite (la règle de confiance ne cite que les agents de projet) | Constaté à l'étape 4 |
| 9 | Les commandes `!` de l'utilisateur échappent au hook et à la règle `deny` | Non vérifié | Voir point F ci-dessous |

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
- **F.** Après l'étape 5, mes appels dbt bruts sont bloqués. Or T1, T2, T3, T7,
  T14, T15 testent le comportement **brut** de dbt. Proposition : un script
  `t_series.sh <T#>` dans le projet de test, que **tu** lances dans ton terminal ;
  il écrit `results/Txx.txt`, que je lis et étiquette **[Observé]**.
  **Validé le 2026-10-02 : tu lances le script.** Je l'écris à l'étape 1 bis
  (fixture, commandes exactes, capture, nettoyage) pour relecture avant exécution.
  Je ne le lance pas moi-même après l'étape 5.

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
travaille dans `DEV`). La lecture par `ro` d'un modèle construit par `dev` reste
à constater (T3, T19).

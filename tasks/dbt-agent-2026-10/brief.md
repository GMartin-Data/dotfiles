# Brief d'implémentation — agent dbt au scope user (Claude Code)

> À placer dans le dépôt dotfiles avec `dbt_agent_preconisations_workflow.md` (la spécification).
> Commencer en **plan mode** : ne rien écrire avant validation du plan.

## 1. Objectif

Un subagent Claude Code, disponible dans tous mes projets dbt perso, qui n'exécute dbt **que** via un serveur MCP « enveloppe ». Les règles et l'enveloppe sont spécifiées dans `dbt_agent_preconisations_workflow.md` :

| Partie du document | Devient |
|---|---|
| Partie II (socle S1–S5 + sections D/P/L/K/H/O/G) | Corps du fichier subagent |
| III §D (spécification du script enveloppe) | Outils du serveur MCP |
| III §E et §F.4 (T0–T21) | Plan de tests sur Snowflake |
| IV §4 (« Ce qu'il ne faut jamais faire ») | Garde-fous à rendre structurels |

Ne pas réécrire les règles : les reprendre telles quelles, avec leurs identifiants.

## 2. Décisions déjà prises

- **Emplacement** : tout vit dans le dépôt dotfiles, lié vers `~/.claude/`. Rien dans `~/.claude.json`.
- **Subagent** : `~/.claude/agents/dbt.md`. `tools` sans `Bash` : `Read, Grep, Glob, Edit, Write, mcp__dbt-enveloppe__*`.
- **Serveur MCP** : déclaré **inline** dans le frontmatter du subagent (`mcpServers`, type `stdio`). Python, géré avec `uv`.
- **Projet ciblé** : le serveur lit `CLAUDE_PROJECT_DIR`, y exige un `dbt_project.yml`, refuse sinon. Ne pas se fier au cwd.
- **Conversation principale** : `Bash(dbt *)` dans `permissions.deny` de `~/.claude/settings.json`, complété par un hook `PreToolUse` (regex couvrant `uv run dbt`, `python -m dbt`, chemins absolus).
- **Versions** : dbt-core 1.12.5, dbt-snowflake 1.12.x compatible, versions épinglées. Pas d'alignement sur l'environnement de travail.
- **Snowflake (trial)** : authentification par paire de clés ; deux rôles (écriture sur le schéma de dev ; lecture seule avec privilèges de métadonnées, §F.3 fait 2) ; `query_tag` dans le profil ; warehouse en `AUTO_SUSPEND` court. `profiles.yml` hors dépôt.

## 3. Points à trancher (me les soumettre dans le plan)

1. **`dbt_build` n'est pas spécifié en §D**, alors que le workflow (IV, étape 4) en dépend. Proposer : appel imposé, cible dev forcée, refus si `parse` et `ls` n'ont pas réussi dans la session (S1), condition de succès, sortie renvoyée.
2. **Quel exécutable dbt** le serveur lance : celui de l'environnement du projet (`uv run --project $CLAUDE_PROJECT_DIR dbt`) ou un dbt global épinglé. Je penche pour le premier.
3. **`show --inline`** : ne pas l'exposer, ou l'exposer seulement avec le profil lecture seule (H7). Recommander.
4. **Chemin du serveur dans le frontmatter** : vérifier si `${HOME}` y est expansé (documenté pour `.mcp.json`, non confirmé pour l'inline). Sinon, chemin absolu généré par le script d'installation.

## 4. Ordre de mise en œuvre

Chaque étape testée seule avant la suivante.

1. Trial Snowflake, rôles, `profiles.yml` ; `dbt debug` à la main (T0).
1 bis. Projet dbt de test, hors dotfiles, sur les données d'exemple du trial : au moins un modèle `table`, un `incremental`, un modèle utilisant `run_query`, un test, et de quoi provoquer chaque échec silencieux du principe 2.
2. Enveloppe en CLI pur, sans MCP ; tests unitaires sur les conditions de succès de §D (un cas « échec silencieux » par ligne du principe 2).
3. Enveloppe exposée en serveur MCP ; test via `/mcp`.
4. Subagent ; vérifier qu'il ne voit que les outils MCP.
5. **En dernier** : règle `deny` et hook. Avant, ils bloqueraient tes propres appels dbt pendant l'implémentation.
6. Rejouer sur Snowflake, dans cet ordre : périmètre minimal T0, T3, T7, T13, T19 ; le reste de T1–T21 ensuite, si le temps du trial le permet.

## 5. Contraintes

- Vérifier dans la doc Claude Code courante (`code.claude.com/docs/en/sub-agents`, `/mcp`, `/hooks`, `/permissions`) avant d'utiliser un champ ou un événement ; ne pas se fier à la mémoire.
- Script d'installation idempotent (liens symboliques, vérification de `uv`), versionné dans les dotfiles.
- Code en anglais, docstrings Google, annotations de type modernes, Python 3.12.

## 6. Livrable de fin

- Ce qui fonctionne, ce qui a été écarté et pourquoi.
- Résultats T0–T21, chacun étiqueté **[Observé]** avec les versions (dbt-core, dbt-snowflake, Claude Code), pour report dans le corpus.

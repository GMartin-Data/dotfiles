# ADR-0017 : Authentification par bearer du serveur MCP tech-watch, passerelle stdio dans l'agent

Status: Proposed
Date: 2026-10-11

## Contexte

Le serveur MCP `tech-watch-mcp` (Cloud Run `europe-west1`, projet
`mcp-servers-prod`, code dans le dépôt privé `GMartin-Data/tech-watch-mcp`) est
invocable par `allUsers` et ne vérifiait aucun en-tête. Son URL SSE est
versionnée dans le frontmatter de `claude/agents/tech-watch.md`, dans le repo
**public** `dotfiles`, depuis le 2026-10-09 ; en 14 jours, le repo a été cloné
par environ 108 cloneurs uniques pour un seul visiteur unique — des robots, qui
ramènent toutes les branches. Le secret de l'URL n'est donc plus garanti.

Ce que porte le serveur : les clés GitHub et YouTube. Un tiers qui connaît l'URL
peut consommer ces quotas et générer du coût Cloud Run ; il n'accède à aucune
donnée. Le constat vient du finding [1] (HIGH · sécurité) du `/code-review` de
la PR #6, qui remplace le trio command + agent + script par la skill forkant
dans l'agent.

Contrainte établie par sonde (montage K12, 2026-10-11, trois variantes) : le
frontmatter d'un agent accepte un bloc `headers` sur un serveur distant, mais
n'expanse **pas** `${VAR}` — l'expansion documentée pour `.mcp.json` ne s'y
applique pas. Un bearer déclaré directement dans l'agent versionné serait donc
un secret en clair dans un repo public.

Décisions amont à préserver : D1 (le code du serveur vit hors dotfiles, unité
de déploiement avec son Dockerfile) et D3 (d) (serveur déclaré inline dans
l'agent, connecté le temps du run seulement, jamais dans la session
principale), cf. `tasks/tech-watch-2026-10/plan.md`.

## Options considérées

- **A. Accepter l'exposition et borner le coût** : `max-instances` 20 → 2 sur
  le service, alerte budget 10 €/mois sur le projet. Le moins cher ; un abus se
  traduit par le mode dégradé déjà géré par la skill. Mais l'endpoint reste
  ouvert à quiconque a l'URL. Retenue le matin du 2026-10-11, puis dépassée par
  F le même jour.
- **B. Bloc `headers` avec `${VAR}` dans l'agent** : impossible, la sonde K12
  montre que la variable n'est pas expansée (URL en `${VAR}` → serveur absent).
- **C. Serveur au scope user (`claude mcp add --header …` dans
  `~/.claude.json`), référencé par nom dans l'agent** : secret hors repo, mais
  le serveur serait connecté dans toutes les sessions, ce qui annule D3 (d).
  Non testée.
- **D. IAM Cloud Run (retirer `allUsers`) ou IAP** : exige un jeton d'identité
  GCP à durée de vie courte, incompatible avec un client MCP à configuration
  statique.
- **E. Passer le repo `dotfiles` en privé** : obscurité seulement — l'URL est
  déjà dans des clones, elle reste dérivable du nom du service et du numéro de
  projet — et perte du secret scanning et de la push protection gratuits des
  repos publics.
- **F. Bearer vérifié par le serveur, passerelle stdio côté agent** : voir
  Décision.
- **G. OAuth MCP côté serveur** (`mcp.server.auth`, présent dans mcp 1.20) :
  la seule option qui rendrait le connecteur claude.ai (les connecteurs custom
  savent faire OAuth, pas un en-tête statique). Mais elle impose d'héberger un
  serveur d'autorisation — ou d'intégrer un IdP —, un flux de consentement et
  un stockage de jetons, pour un service mono-utilisateur dont le seul client
  prévu est l'agent Claude Code (D3 (d)). Rejetée ; la perte du client
  claude.ai est assumée comme durable. **Déclencheur de réouverture** : le
  besoin d'un client qui ne peut pas porter `TECH_WATCH_MCP_TOKEN` dans son
  environnement (connecteur claude.ai en premier lieu). Ajoutée le 2026-10-11
  à la suite du finding [4] du `/code-review` de la PR serveur #3.

## Décision

Option **F**.

- **Serveur** : un middleware ASGI (`utils/auth.py`, `BearerAuthMiddleware`)
  enveloppe l'app SSE et exige `Authorization: Bearer $TECH_WATCH_MCP_TOKEN`
  sur toute requête HTTP, comparaison en temps constant, 401 avec
  `WWW-Authenticate: Bearer` sinon. **Fail-closed** : variable absente côté
  serveur = toute requête rejetée. Le transport stdio (local) n'est pas
  concerné.
- **Agent** : le serveur est déclaré inline en `type: stdio` :
  `sh -c 'API_ACCESS_TOKEN="${TECH_WATCH_MCP_TOKEN:?…}" exec uvx
  mcp-proxy@0.13.0 <url>/sse'`. C'est le shell qui expanse la variable
  (même astuce que `$HOME` pour `dbt-enveloppe`) ; `mcp-proxy` transforme
  `API_ACCESS_TOKEN` en en-tête, si bien que le token n'apparaît pas dans la
  ligne de commande visible par `ps`. `${VAR:?}` fait échouer `sh` avant tout
  appel réseau quand la variable manque.
- **Token** : dans `~/.zshrc.local` (mode 600, hors repo), sourcé par
  `zsh/.zshrc` s'il existe ; même valeur dans la variable Cloud Run.
- **Bornes de coût de l'option A conservées** en défense en profondeur.

Pourquoi F : c'est la seule option qui ferme réellement l'exposition tout en
préservant D1 et D3 (d) — serveur connecté le temps du run, secret hors du repo,
agent toujours symlinké tel quel.

## Conséquences

- L'URL versionnée dans le repo public devient inoffensive ; `curl` sans
  en-tête, mauvais token ou `POST /messages/` → 401, bon token → 200.
- La passerelle est transparente pour la skill : la veille E1 rejouée à travers
  elle donne le même résultat qu'avant (20 classées + 3 primaires, trois outils
  MCP `ok`). Token absent ou refusé = outils absents = mode dégradé existant.
- Le connecteur claude.ai de la phase 0 ne fonctionne plus (pas d'en-tête
  statique possible) ; le seul client supporté est l'agent Claude Code. Perte
  assumée comme durable, voir l'option G.
- La variable doit être présente dans le shell qui lance Claude Code ; app
  desktop, extension IDE et routines remote passent en mode dégradé.
- Rotation en deux endroits : variable Cloud Run et `~/.zshrc.local` sur chaque
  machine (l'un des « à réinstaller manuellement » du README).
- Dépendance supplémentaire au run : `uvx mcp-proxy` épinglé en 0.13.0, un
  processus et un saut réseau de plus.
- Les secrets du serveur restent en variables d'environnement Cloud Run
  simples, pas dans Secret Manager : inchangé, hors du périmètre de cette
  décision.

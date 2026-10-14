# Mods Claude Code — synthèse des échanges (2026-10-13 → 14)

Document de référence du chantier « mods » : ce qui a été établi sur les
mods, les candidats évalués, les décisions prises et l'esquisse du premier
mod retenu (registre de contexte). Même rôle que `tasks/tech-watch-2026-10/`
et `tasks/dbt-agent-2026-10/` pour leurs chantiers. Le plan de réalisation
(`plan.md`) s'écrit à la session suivante.

**Sources.** Rapport de veille `~/tech-watch/tech-watch-claude-code-mods-2026-10-12.md`
(20 sources classées + 3 primaires) ; skill bundled `plugin-authoring`
(SKILL.md, reference.md, exemples) et sa déclaration de types
`claude-code.d.ts`, lue sur deux builds (2.1.296, 21 461 lignes, le 13/10 ;
2.1.299, 22 017 lignes, le 14/10) ; docs `code.claude.com` (mods overview et
create, headless) ; annonce `claude.com/blog/claude-code-mods`. Tout fait
d'API ci-dessous vient du fichier de types, autorité déclarée par la skill ;
les champs cités sont ceux du build 2.1.299.

---

## 1. Ce qu'est un mod

- **Un plugin à hooks de fonction** : `.claude-plugin/plugin.json`,
  `hooks/hooks.json` (`{ "modules": ["./register.ts"] }`), un module ES
  TS/JS exportant `register(on, options)`. Un mod qui garde des valeurs en
  `$.state` ajoute `types/index.d.ts` (contrat `interface PluginState`),
  nommé dans `plugin.json` (`"types"`). Lancé le 2026-10-01 (CLI ≥ 2.1.287,
  Desktop ≥ 2.1.286), actif par défaut ; `/diff` est un mod built-in
  remplaçable ; `sec-default` (guard chargé en premier) existe pour
  Team/Enterprise seulement.
- **Un hook** = `($, e, next)` : `$` l'interface moteur (noms puis méthodes),
  `e` l'entrée de l'événement (valeur gelée), `next(e)` la suite de la chaîne
  puis le comportement du moteur, qui résout le résultat. Sans `next`, le hook
  répond seul ; `next({ ...e, x })` réécrit ce que la suite voit, dans ce que
  l'événement autorise (champs « pinned » refusés). Deux événements streament
  (`turn.step`, `process.spawn`) : générateurs asynchrones.
- **Environnement propre** : ni DOM ni Node ; tout l'extérieur passe par `$`.
  JSX via le global `h`, éléments issus de `$.ui.resolve(e)` selon la surface
  (`terminal`, `desktop`, `vscode`, `mobile`).
- **Non sandboxé** : droits de l'utilisateur. D'où le vetting communautaire
  (catalogues « ce que le mod lit/écrit/exécute/envoie ») et la
  recommandation StationX : hooks settings d'abord.
- **Early access déclaré** : « The API is early access and moves between
  releases: the declaration file is the authority ». Constaté : le build a
  changé pendant la nuit du 13 au 14/10 (2.1.296 → 2.1.299), le fichier de
  types a été régénéré sous un autre chemin et a gagné 556 lignes. Canal
  `autoUpdatesChannel: latest` côté dotfiles.

### Chargement et développement

| Mode | Mécanisme | Notes |
|---|---|---|
| Session courante (skill) | `~/.claude/dev-mods/<session-id>/<mod>/`, surveillé dès le chargement de `plugin-authoring` ; **le premier fichier écrit déclenche la question « Enable hot reloading for this session? »** | Dossier lié à la session ; rien n'y a été écrit pendant ces échanges |
| Dossier de dev | `claude --plugin-dir <dossier>` (répétable) ; `CLAUDE_CODE_PLUGIN_DIRS` (chemins absolus, `~` accepté) depuis l'environnement ou le bloc `env` de `~/.claude/settings.json`, jamais d'un settings projet | Session interactive : dossier surveillé, rechargement à la sauvegarde (une fois par tour quand c'est le modèle qui édite) ; `claude -p` charge frais ; hôte long (SDK, desktop) surveille avec `CLAUDE_CODE_PLUGIN_DIR_WATCH=1` |
| Dossier de skills | `~/.claude/skills/<name>` ou `.claude/skills/<name>` : un plugin y est **auto-chargé et surveillé** | Voie « installée » sans marketplace, à évaluer pour l'install définitive |
| Marketplace dossier | `claude plugin marketplace add <dossier>` + `source` relatif : lu **depuis le dossier lui-même**, `/reload-plugins` relit | Pas de copie, pas de réinstall |
| Headless | `--bare` (recommandé, futur défaut de `-p`) ne charge rien sauf `--plugin-dir` explicite ; l'événement `system/init` liste `plugins` et `plugin_errors` | Porte CI : échouer sur `plugin_errors` non vide |

Un rechargement = nouveau `register`, nouveau `session.start`, variables du
module perdues ; `$.state` (session) et `$.store` (inter-sessions) survivent.
Options du mod : `userConfig` du manifest, lues dans `options`, éditables
dans `/config`, stockées sous `pluginConfigs`.

### Outillage de vérification

- `claude plugin validate <mod>` : lit manifest et source comme le moteur,
  liste ce que le module hooke et appelle, nomme les **gating hooks** (ceux
  dont la réponse peut refuser : `tool.call`, `tool.check`, `prompt.submit`,
  `command.run`, `config.set`, `plugin.register`…) avec ou sans `.catch`.
- `tsc -p <mod>` : types posés par le moteur dans `<mod>/.claude-plugin/types/`
  à chaque chargement (`claude-code/`, `claude-code-tools/` pour le
  narrowing `e.tool === "Bash"`, `claude-code-mcp/`, un `tsconfig.json`).
  Avant le premier chargement : le `tsconfig.json` de l'en-tête du fichier de
  types, hors du dossier du mod.
- `claude plugin test <mod>` : fichiers `*.test.ts` contre le moteur réel
  (`test`, `expect`, `mock` depuis `claude-code/testing` ; `mock.session(on)`
  relit les lignes ; tests UI montés par surface, à boucler sur
  `['terminal', 'desktop']`).
- **Fail-open par défaut** : un hook qui échoue (exception, mauvaise forme,
  budget dépassé) est **sauté** et la chaîne continue ; en session
  hot-reload, une ligne grise dans le transcript ; sinon, debug log seulement
  (`claude --debug`). Un garde s'écrit `on(...).catch(($, e, next) =>
  next.called ? next(e) : { deny: 'why' })`. Chaque hook a un budget de temps
  propre ; `next.signal` aborte avec le dispatch ; le travail durable part de
  `session.start` et de `$.clock.every/after`.
- Dessin : terminal et Desktop seulement — pas VS Code, pas `claude -p`, pas
  les sessions cloud. Les hooks, eux, tournent sous `-p` ; en session cloud
  ou routine remote : non documenté.

## 2. Le modèle d'événements utile

| Événement / nom | Ce qu'on voit | Ce qu'on peut faire | Pinned / limites |
|---|---|---|---|
| `tool.call` (matcher `{ tool }`) | l'appel typé par outil, `agentId` | `{ deny }` ; `next({ ...e, ... })` réécrit l'entrée ; `await next(e)` puis renvoyer `{ result }` réécrit la sortie, validée contre le schéma de l'outil ; `context` = rappel lu par le modèle seul | la sortie de core porte `text` (ce que lit le modèle), `isReadOnly`, `ref` |
| `session.append` (matcher `{ door }`) | **chaque ligne** qui entre dans une conversation : `door` (`prompt`, `command`, `response`, `tool-result`, `tool-message`, `delivery`, `attachment`, `hook-context`, `note`, `compaction`, `notice`), `origin`, `uuid`, `agentId`, `message` (blocs au format Messages API) | `next({ ...e, message })` réécrit `content` **avant stockage et envoi** : blocs texte édités/ajoutés/supprimés, `content`/`is_error` d'un `tool_result` ; image ou document déplaçable ou supprimable, pas modifiable | thinking, `tool_use`, blocs non signés : remis en place ; une ligne du moteur ne se refuse pas ; la réécriture est **définitive** |
| `$.session.append` | — | ajoute une ligne `user` (isMeta, lue par le modèle) ou `system` (notice) à la conversation principale ou à un sous-agent en cours | texte seulement |
| `prompt.submit` | le texte soumis | `next({ ...e, text })`, ou refus | une réécriture ici vaut pour la file aussi |
| `prompt.compose` / `prompt.section` | sections du system prompt (`{ id, text, scope }`) | ajouter en `session`, remplacer, réordonner, supprimer ; `prompt.section` par section, caché jusqu'à `$.ui.invalidate("prompt.section")` | |
| `prompt.context` | blocs de contexte du premier message | ajouter, supprimer, réécrire ; tient jusqu'à invalidation, compaction ou `/clear` | |
| `command.run` (matcher `{ command }`) | commande sans slash, `args`, origine | `next({ ...e, args })` ; `{ text }` sans `next` répond à la place — **y compris pour une commande built-in** (`clear`) ; `exitCode` sous `-p` | `$.command.register` refuse le nom d'une built-in |
| `session.start` / `session.end` | fin : `reason` (`clear`, `resume`, `logout`, `other`…), `resume.id` | start : enregistrer commandes/outils, lancer les timers ; end : sauver dans `next.budget` | **`session.end` ne se refuse pas** (`SessionEndResult = { sessionId }`) ; après `/clear`, pas de `session.start` |
| `turn.start` / `turn.step` / `turn.complete` | début de tour ; **chaque requête modèle** (`model`, `effort`, `messageCount`, `index`, `agentId`), chunks streamés (text, thinking, tool, input, stop, engine) ; fin de tour (`reason`, `usage`) | `turn.step` : `next({ ...e, model, effort })` ; sans `next`, pas de requête | **les messages de la requête sont pinned** (« the messages are the engine's ») ; un sous-agent lancé par `$.agent.spawn` passe outre le hook qui l'a lancé |
| `session.measure` | poussé après chaque tour principal et à chaque point de rate limit : `context` (`tokens`, `window`, `percent`), `rateLimits`, `cost`, `changed` | observer ; comparer à ses seuils ; appeler `$.session.usage({ breakdown })` | `changed` jamais vide |
| `$.session.usage({ breakdown: 'summary' \| 'full', columns })` | `startedAt`, `context`, `rateLimits`, `cost` ; avec `breakdown` : `categories`, `totalTokens`, `rawMaxTokens`, `autocompactSource`, `gridRows`, `memoryFiles` (chemin, tokens), `mcpTools` (serveur, tokens), `agents`, `slashCommands`, `skills`, `autoCompactThreshold`, `isAutoCompactEnabled`, `apiUsage` (input, output, cache écrit, cache lu) | lire | `summary` estime en local ; `full` envoie une requête de comptage par outil et fichier mémoire ; le breakdown mesure contre la fenêtre de compaction, ses totaux ≠ `tokens` |
| `session.compact` (matcher `{ trigger }`) | `trigger` (`manual`, `auto`, `plugin`, `precompute`), `instructions`, `messages` (forme `$.session.messages()`, avec `handle`), `agentId` | réécrire `instructions` ou `messages` à la descente, les messages à la remontée, répondre `{ messages }` soi-même, ou `{ skip: reason }` ; résultat : `tokensBefore`, `tokensAfter`, `usage` du résumeur ; `$.session.compact({ instructions })` déclenche | un message gardé avec son `handle` est celui du moteur, entier ; sans, reconstruit (rôle, texte, blocs d'outils) — interaction avec le *preserved thinking* de Fable 5.1 / Opus 5.5 / Sonnet 5.5 non prouvée |
| `$.session.messages({ agentId })` | lignes `{ role, text, toolUses, toolResults?, handle?, agentId? }` | lire n'importe quelle boucle | pas les blocs `content` bruts |
| `ui.render` (`Pane`, `AbovePrompt`, `UserMessage`, `CommandOutput`, …) | composant, surface, `requestId`, props, viewport | dessiner un arbre, ou `next({ ...e, props })` | arbres validés ; longueurs plafonnées ; état de dessin dans `$.state` (atom/read/update), jamais dans une variable de module |
| `$` divers | `$.env.get/set`, `$.fs` (read/write/list/stat, `realPath` avec `{ resolve: true }`), `$.store`, `$.state`, `$.clock`, `$.process.run/spawn`, `$.model.complete` (sans historique, usage retourné) / `$.model.fork` (question sans outil sur le transcript courant, servie par le cache), `$.command.register/run/list`, `$.agent.register/spawn`, `$.config`, `$.telemetry`, `$.ui.status/toast/log/notify/copy/selection` | | `$.command.run` rejette dans un hook que le tour attend |

Les événements des hooks settings sont aussi hookables en `classic.<Event>`
(`classic.Stop`, `classic.SessionEnd`, `classic.PreCompact`…).

## 3. Ce que dit la veille (12/10)

- Vague de lancement : 19 sources sur 20 datées du 02 au 12/10 ; YouTube
  porte l'engagement (quatre vidéos > 200 k vues) ; une seule source A (vidéo
  officielle). Quatre sources avec tests réels (StationX, Kanaries, Hari
  Krishna, promptadvisers), le reste est du showcase.
- Pattern communautaire dominant : le **bandeau télémétrie** (compteur de
  contexte, horloge de limite, cache). Redondant ici avec `ccstatusline` et
  les métriques mensuelles de `/insights`.
- Confiance : catalogues en concurrence sur le vetting ; analyses StationX et
  dev.to sur le trou de gouvernance ; early access réel depuis début
  septembre (dépôts datés du 05 au 16/09).
- « Building by asking » (skill `plugin-authoring`) est la voie d'entrée par
  défaut ; les sources avec tests se distinguent de ce fond.

## 4. Doctrine retenue pour ce repo

1. Le workflow est **human-triggered par doctrine** ; chaque automatisation
   différée de `TODO.md` a un déclencheur. **Les mods baissent le coût d'une
   automatisation, pas ses déclencheurs.**
2. « Migrer par nécessité, pas par conformité » : les hooks bash existants ne
   se réécrivent pas en mods ; leurs faiblesses connues se corrigent en bash.
3. **Pas de collection de mods**, jamais d'installation depuis un catalogue
   communautaire (non sandboxé, non vetté). Un mod maison vit dans
   `claude/mods/<nom>/` (dotfiles), avec test, et suit la checklist
   multi-fichiers (install ou mécanisme de chargement, puce dans les deux
   README, famille `**Mods**` à créer).
4. **À chaque bump qui change `claude-code.d.ts`** : `claude plugin validate`
   + `tsc -p`, sinon le mod se désactive en silence.
5. Garde-fou dispersion : le ratio méta/produit (32 % des sessions au cycle du
   26/09) est surveillé ; un chantier mods est un chantier méta, assumé
   comme tel et borné.
6. Un mod d'automatisation se conçoit **fail-closed** (`.catch` qui refuse),
   avec vérification de `plugins`/`plugin_errors` à chaque run et version de
   Claude Code épinglée.

## 5. Candidats évalués

Grille de `TODO.md` (Impact / Coût / Risque 1-3, déclencheur atteint ?) :

| Candidat | Mécanisme | I | C | R | Déclencheur | Verdict |
|---|---|:-:|:-:|:-:|---|---|
| Rédaction des secrets dans les résultats d'outils | `session.start` → `$.env.get("TECH_WATCH_MCP_TOKEN")` ; `session.append` porte `tool-result` → remplace la valeur ; `.catch` → placeholder | 2 | 1 | 1 | atteint — incident 2026-10-11 (token affiché deux fois : expansion `${VAR:-…}`, puis `ps`) | à faire (second) |
| **Registre de contexte** (observe-only) | `session.append` + `session.measure` + `turn.complete` + `session.compact` → JSONL par session ; script d'analyse pour `/insights` | 2 | 2 | 1 | aucune friction ; **retenu comme implémentation pédagogique** et prérequis de toute automatisation de contexte | **à faire (premier)** |
| `/clear` → forcer `/progress` | `command.run` sur `clear` ; `$.fs.stat(progress.md).mtimeMs < usage().startedAt` → `{ text }` sans `next` | 2 | 2 | 2 | non atteint (0 oubli sur 14 cycles) | ne pas faire ; premier mécanisme capable de gater `/clear` |
| Réécrire les 4 guards bash en `tool.call` typés | `realPath` pour `protect_env` | 1 | 2 | 2 | aucun | ne pas faire |
| Bandeau contexte / tokens | `ui.render` `AbovePrompt` | 1 | 1 | 1 | friction token-limit réglée depuis 2026-07 | ne pas faire |
| Contrôle `Checked:` en `/teach` | `turn.complete` | 1 | 2 | 2 | fiche en revue le 2026-10-26 | pas avant le verdict |
| Taille des résultats d'outils | `session.append` `tool-result` (head + tail, ANSI, listings) | — | — | — | aucun run ne compacte | mod de contrôle n° 1 si le registre le justifie |
| Politique de compaction maison | `session.compact` → `{ messages }` | — | — | — | idem | mod de contrôle n° 2 ; risque preserved thinking |

Scores 1-10 (valeur 9 = section Response Style ; complexité 9 = `dbt-enveloppe`) :

| Mod | Valeur aujourd'hui | Valeur si runs longs autonomes | Complexité | Taille |
|---|:-:|:-:|:-:|---|
| Rédaction des secrets | 4 | 5 | 3 | 60–100 lignes + 1 test |
| Registre de contexte | 3 | 6 | 5 | 150–250 lignes + script Python |
| Taille des résultats d'outils | 2 | 7 | 4 | — |
| Compaction maison | 2 | 6 | 8 | — |

## 6. Contexte : ce que les mods voient, contrôlent, et ne peuvent pas

- **Voir** : par tour (`session.measure`), par requête (`turn.step`), par
  ligne et par porte (`session.append`), par catégorie (`breakdown`), par
  sous-agent (`agentId`), avec les tokens de cache (`apiUsage`), le coût de
  chaque compaction. Plus fin que `/context` (une ligne « Messages ») et que
  le status line.
- **Contrôler** : réécrire une ligne avant stockage ; réécrire la sortie d'un
  outil, typée ; posséder la compaction (instructions, messages, `skip`,
  déclenchement) ; sections du system prompt et blocs du premier message ;
  modèle et effort par requête ; schémas d'outils différés.
- **Trois limites** : (1) pas de fenêtrage virtuel par requête — messages
  pinned dans `turn.step`, réécritures d'append définitives, la compaction
  est la seule chirurgie ; (2) une compaction maison touche à l'historique —
  interaction avec le preserved thinking non prouvée ; (3) estimations, pas
  comptes exacts par ligne, et API en early access.
- **En automatisation**, la valeur monte (pas d'humain pour `/progress` →
  `/clear`), avec quatre réserves : architecture d'abord (un run = un
  contexte, état transmis par fichier ou sortie structurée — c'est le rituel
  `/progress` → `/clear` porté par un orchestrateur) ; fail-open ; dérive
  d'API + canal `latest` ; pas en cloud/remote. Règle de conception à
  consigner (CLAUDE.md ou plan, pas un mod) : *un run = un contexte*.
- Ce que le workflow fait déjà sans mod : `/progress` → `/clear` est la
  politique de compaction (humaine, documentaire) ; `dbt-enveloppe` fait la
  taille des résultats côté serveur ; tech-watch isole par fork.

## 7. Décisions et orientation (14/10)

- **Premier mod : le registre de contexte**, observe-only, mené de façon
  pédagogique (appropriation des mods comme objectif explicite, au même
  titre que la feature). Valeur assumée faible aujourd'hui (3), prérequis
  de toute automatisation de contexte ; déclencheur assumé : le premier run
  long planifié, pas une friction.
- **Second mod : rédaction des secrets** (incident du 11/10), une session,
  après le registre — pas la même semaine.
- Mods de contrôle (taille des résultats, compaction) : **seulement armés
  par une mesure du registre** (un run qui compacte, un outil > X % du
  contexte). Taille des résultats avant compaction, jamais l'inverse.
- Déclencheurs de réouverture : 2ᵉ oubli de `/progress` avant `/clear`
  observé par `/insights` → mod `command.run` ; sortie de l'early access
  annoncée → réévaluer la migration des guards si un bug bash non corrigeable
  en bash apparaît ; première friction de contexte dans `/insights` → mods
  de contrôle.
- Rien n'a été écrit dans `~/.claude/dev-mods/` ; aucune question de
  hot-reload n'a été posée.

## 8. Esquisse du registre de contexte (spec v0, à instruire dans `plan.md`)

**But.** Un fichier JSONL par session qui attribue la croissance du contexte
à ses causes, et un script Python qui en tire les agrégats pour `/insights`.
Aucun changement de comportement : tous les hooks observent et appellent
`next(e)` tel quel.

| Événement | Ce qu'on consigne |
|---|---|
| `session.start` | ouverture : session id, modèle, `startedAt`, version du moteur (`$.session.version()`), cwd |
| `session.append` | `uuid`, `door`, `origin` (kind, et `tool` ou `model` ou `name`), `agentId`, tokens **estimés** (longueur des blocs texte / 4, à calibrer), type des blocs non texte |
| `session.measure` | après chaque tour : `tokens`, `window`, `percent`, `cost.usd`, `rateLimits` ; `apiUsage` via `$.session.usage({ breakdown: 'summary' })` quand le fill a bougé — réconciliation estimation ↔ mesure |
| `turn.complete` | `turnId`, `reason`, `usage` |
| `session.compact` | `trigger`, `tokensBefore`, `tokensAfter`, `usage` du résumeur, nombre de messages avant/après |
| `session.end` | `reason`, vidage final dans `next.budget` |

**Points de conception à trancher au plan.**
- Tampon en mémoire, vidage à chaque `session.measure` et au `session.end`
  (budget court) ; chemin du fichier (`~/.claude/usage-data/context-ledger/`
  à côté de `session-meta/` que `/insights` lit déjà ?) ; un fichier par
  session id, `/clear` ouvrant un nouveau.
- Sous-agents : une ligne par `agentId`, agrégées à part (tech-watch, dbt).
- Estimateur de tokens : chars/4 au départ, erreur mesurée contre
  `apiUsage.input_tokens` à chaque tour ; `breakdown: 'full'` jamais
  (requêtes payantes).
- Rien de sensible dans le registre : pas de texte des lignes, seulement
  métadonnées et tailles.
- Mécanisme de chargement définitif : dossier de skills auto-chargé, ou
  `CLAUDE_CODE_PLUGIN_DIRS` dans `settings.json`, ou marketplace dossier —
  décision à prendre, à consigner dans « Décisions prises » (track léger du
  repo dotfiles) ou en ADR si elle engage l'architecture du repo.
- Dev loop : `claude --plugin-dir ~/dotfiles/claude/mods/context-ledger`
  (surveillé en session interactive) plutôt que le dossier `dev-mods` lié à
  une session ; `claude plugin validate` et `tsc -p` à chaque étape ; un
  `*.test.ts` par événement observé.
- Progression pédagogique possible (un événement par palier) : M0 squelette
  + `validate` ; M1 `session.measure` → `$.ui.status` ; M2 `session.append`
  en mémoire + vidage ; M3 `turn.complete` et `session.compact` ; M4
  sous-agents ; M5 script d'analyse ; M6 tests et chargement définitif.

**Risques.** Dérive d'API (quatre événements exposés) ; coût d'un hook sur
chaque ligne (budget par dispatch, I/O à tamponner) ; `.catch` obligatoire
même en observe-only pour ne pas perdre la mesure sans le savoir.

---

## Références

- Mods : https://code.claude.com/docs/en/plugins/mods/overview ·
  https://code.claude.com/docs/en/plugins/mods/create ·
  https://claude.com/blog/claude-code-mods · skill bundled `plugin-authoring`
  (`SKILL.md`, `reference.md`, `types/claude-code.d.ts`, `examples/`)
- Headless et chargement : https://code.claude.com/docs/en/headless.md
- Veille : `~/tech-watch/tech-watch-claude-code-mods-2026-10-12.md`
  (StationX https://app.stationx.net/articles/claude-code-mods ; Kanaries
  https://docs.kanaries.net/topics/AICoding/claude-code-mods ; dev.to Quimby
  https://dev.to/max_quimby/claude-code-mods-just-turned-agents-into-a-platform-5gc0)

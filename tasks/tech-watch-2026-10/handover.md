# Tech Watch : pistes de correctifs et d'améliorations

> Document de passation reçu le 2026-10-09, rédigé depuis Claude.ai (Opus 5.5,
> effort élevé). Copié tel quel ; les statuts `HYPOTHÈSE` ont été vérifiés
> contre le code dans `plan.md` §0 — ce fichier n'est pas modifié.

Document de passation pour l'agent qui reprend la skill `tech-watch` et le serveur MCP Tech Watch dans Claude Code.

## 1. Comment lire ce document

- **Origine** : diagnostic mené les 8 et 9 octobre 2026 depuis Claude.ai, par appels réels aux trois outils MCP et relecture des quatre fichiers de la skill. Un test complet de la skill a ensuite été exécuté sur le sujet « Claude Mods ».
- **Limite importante** : le code du serveur n'a jamais été lu. Tout ce qui concerne le serveur est déduit de l'extérieur (URL visibles dans les messages d'erreur, forme des sorties). Chaque cause est donc étiquetée `CONFIRMÉ` (observé directement) ou `HYPOTHÈSE` (à vérifier dans le code avant de corriger).
- **Deux artefacts distincts** : la skill (Markdown, portable) et le serveur MCP (Python, déployé sur Cloud Run). Les items `S*` concernent le serveur, les items `K*` la skill, les items `E*` les évals.
- **Ce document propose des pistes, pas des implémentations.** L'agent a le dépôt sous les yeux et choisit la solution. Les critères d'acceptation décrivent le comportement attendu, pas la manière d'y arriver.
- **Format de chaque item** : Constat, Preuve, Cause, Piste, Critère d'acceptation.

## 2. Contexte technique

| Élément | Valeur | Statut |
|---|---|---|
| Skill | `tech-watch` : `SKILL.md` + `references/sources.yaml`, `references/scoring-criteria.md`, `references/report-template.md` | CONFIRMÉ |
| Outils MCP | `search_github_repos(query, max_results)`, `search_arxiv_papers(query, days_back, max_results)`, `search_youtube_videos(query, days_back, max_results)` | CONFIRMÉ |
| Serveur | Python, FastMCP, httpx asynchrone, transports stdio et HTTP | D'après les notes du projet, à vérifier |
| Déploiement | Cloud Run, projet `mcp-servers-prod`, service `tech-watch-mcp`, région `europe-west1` | Confirmé par le propriétaire |
| Secret GitHub | Variable d'environnement littérale `GITHUB_TOKEN` sur le service Cloud Run | CONFIRMÉ |
| Tests existants | 43 tests (27 unitaires, 16 d'intégration), tous au vert alors que les défauts ci-dessous existent | D'après les notes du projet |
| Arborescence supposée | `server.py`, `tools/github.py`, `tools/youtube.py`, `tools/arxiv.py` | HYPOTHÈSE (README de novembre 2025) |

## 3. Déjà fait, à ne pas refaire

- Le token GitHub expiré a été remplacé le 9 octobre 2026 par un token fine-grained (accès « Public repositories », aucune permission). `search_github_repos` répond de nouveau.
- Expiration du nouveau token : 10 octobre 2027, sous réserve de la valeur affichée dans GitHub. Un rappel d'agenda existe.
- Commande utilisée, à réutiliser telle quelle pour un futur renouvellement :

```bash
gcloud run services update tech-watch-mcp --region europe-west1 \
  --update-env-vars "GITHUB_TOKEN=$NEW_TOKEN"
```

## 4. Contraintes

- Ne jamais afficher, journaliser ni committer la valeur d'un secret. `gcloud run services describe` affiche les variables en clair, clé YouTube comprise.
- Sur Cloud Run, utiliser `--update-env-vars`. `--set-env-vars` remplace toute la liste et supprimerait `YOUTUBE_API_KEY`.
- Toute modification de configuration Cloud Run crée une nouvelle révision. Aucun rebuild n'est nécessaire pour changer une variable.
- Les paramètres d'API cités comme pistes pour YouTube n'ont pas été vérifiés contre la documentation. Les vérifier avant usage.

## 5. Vue d'ensemble

| ID | Composant | Problème | Priorité | Statut de la cause |
|---|---|---|---|---|
| S1 | Serveur, GitHub | Aucune résilience à l'expiration du token | Haute | HYPOTHÈSE |
| S2 | Serveur, GitHub | Tri par étoiles, pas de date, pas de fenêtre temporelle | Haute | CONFIRMÉ (URL observée) |
| S3 | Serveur, arXiv | Requête multi-mots traitée comme un OU, double préfixe `all:` | Haute | CONFIRMÉ (URL observée) |
| S4 | Serveur, YouTube | Tri par date au lieu de la pertinence, métadonnées manquantes | Haute | CONFIRMÉ sur le tri, HYPOTHÈSE sur l'appel |
| S5 | Serveur, transverse | Erreurs renvoyées comme du texte de résultat | Moyenne | HYPOTHÈSE |
| S6 | Serveur, tests | Les tests ne couvrent pas la pertinence ni la construction des requêtes | Moyenne | HYPOTHÈSE |
| K1 | Skill | Section « Known limitations » fausse sur les trois outils | Haute | CONFIRMÉ |
| K2 | Skill | L'étape de normalisation déclenche le défaut arXiv | Haute | CONFIRMÉ |
| K3 | Skill | Mode dégradé trop étroit, pied de page figé | Haute | CONFIRMÉ |
| K4 | Skill | Déclenchement du Tier 3 évalué avant le filtrage de pertinence | Moyenne | CONFIRMÉ |
| K5 | Skill | Grille de notation incohérente et mal calibrée | Haute | CONFIRMÉ |
| K6 | Skill | Étape d'enrichissement manquante avant la notation | Haute | CONFIRMÉ |
| K7 | Skill | Aucune notion de source primaire ni d'exactitude | Haute | CONFIRMÉ |
| K8 | Skill | Description trop pauvre pour le déclenchement | Moyenne | CONFIRMÉ |
| K9 | Skill | Gabarits de requêtes Tier 2 trop restrictifs | Basse | CONFIRMÉ |
| K10 | Skill | Dédoublonnage et homonymes non traités | Moyenne | CONFIRMÉ |
| K11 | Skill | Sortie sous-spécifiée (nom de fichier, langue, livraison) | Basse | CONFIRMÉ |
| K12 | Skill | Portabilité vers Claude Code à valider | Moyenne | HYPOTHÈSE |

Ordre conseillé : évals de référence d'abord (section 8), puis serveur (S2, S3, S4 avant S1, S5, S6), puis skill. Plusieurs règles de la skill compensent aujourd'hui des défauts du serveur. Corriger le serveur en premier évite d'inscrire des contournements dans la skill.

## 6. Serveur MCP

### S1. Aucune résilience à l'expiration du token GitHub

- **Constat** : avec un token expiré, chaque appel échouait en `401 Unauthorized`. D'après le README, le log de démarrage affiche « GitHub token: Found » dès que la variable est non vide, donc y compris avec un token mort.
- **Preuve** : deux requêtes différentes (`AI agent evaluation`, `dbt`) ont renvoyé `Error: GitHub API error: Client error '401 Unauthorized'` le 8 octobre. Les mêmes requêtes réussissent depuis le remplacement du token.
- **Cause** : le serveur envoie le header `Authorization` sans repli. `HYPOTHÈSE` sur l'absence de repli dans le code.
- **Piste** : sur un `401`, retenter une fois sans header. L'endpoint de recherche de dépôts fonctionne sans authentification pour les ressources publiques (10 requêtes par minute, contre 30 avec token). Signaler dans le résultat que la réponse a été obtenue sans authentification. En complément, valider le token au démarrage plutôt que de tester sa seule présence.
- **Critère d'acceptation** : avec un token invalide, l'outil renvoie des résultats et un avertissement explicite. Le log de démarrage distingue « absent », « présent mais rejeté » et « valide ».
- **Attention** : après plusieurs tentatives avec des identifiants invalides, GitHub rejette temporairement toutes les authentifications du compte en `403`. Ne pas boucler sur les nouvelles tentatives.

### S2. Recherche GitHub triée par étoiles, sans date

- **Constat** : la recherche renvoie les dépôts les plus étoilés contenant les mots, pas les plus pertinents. La sortie ne contient aucune date. L'outil n'a pas de paramètre `days_back`.
- **Preuve** : URL observée `https://api.github.com/search/repositories?q=dbt&sort=stars&order=desc&per_page=1`. Pour `dbt`, le premier résultat est `DataTalksClub/data-engineering-zoomcamp`, pas `dbt-labs/dbt-core`. Pour `claude mods`, 2 résultats sur 10 sont des homonymes sans rapport avec le sujet (`starbaser/ccproxy`, `0xDarkMatter/claude-mods`). Un champ affiche `Language: None`.
- **Cause** : `sort=stars` codé en dur, aucun qualificatif de date. `CONFIRMÉ` par l'URL.
- **Piste** : utiliser le tri par meilleure correspondance par défaut et exposer le tri en paramètre. Ajouter un `days_back` optionnel traduit en qualificatif `pushed:>` ou `created:>`. Renvoyer `created_at` et `pushed_at` dans la sortie. Afficher une valeur lisible quand le langage est nul.
- **Critère d'acceptation** : `dbt` renvoie `dbt-labs/dbt-core` dans les trois premiers résultats. Chaque résultat porte au moins une date. Une veille à 30 jours peut exclure les dépôts inactifs.

### S3. Requête arXiv mal construite

- **Constat** : une requête de plusieurs mots renvoie les articles les plus récents contenant l'un des mots, toutes disciplines confondues. Une requête contenant déjà un préfixe de champ échoue en `400`.
- **Preuve** :
  - `AI agent evaluation` : 5 résultats sur 5 hors sujet (quant-ph, cond-mat, routage de véhicules), tous publiés la veille.
  - `"agent evaluation"` avec guillemets : 3 résultats sur 3 pertinents.
  - `all:agent AND all:evaluation AND cat:cs.AI` : erreur `400`, avec l'URL `https://export.arxiv.org/api/query?search_query=all%3Aall%3Aagent+AND+all%3Aevaluation+AND+cat%3Acs.AI&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending`.
  - `zzqxjkwv` : `Found 0 papers`, comportement correct.
- **Cause** : le serveur préfixe la requête brute par `all:` et trie par `submittedDate`. Seul le premier mot est lié au champ, les autres sont combinés en OU. `CONFIRMÉ` par l'URL. Le filtre de date semble appliqué côté client, l'URL ne contenant pas de plage `submittedDate`. `HYPOTHÈSE`.
- **Piste** : construire la requête terme par terme avec `AND`, ou en expression entre guillemets. Ne pas préfixer si la requête contient déjà un préfixe de champ ou un opérateur booléen. Filtrer côté API avec `submittedDate:[YYYYMMDDTTTT TO YYYYMMDDTTTT]` (heure GMT). Envisager `sortBy=relevance` une fois la plage de dates appliquée côté API, ainsi qu'une restriction optionnelle de catégories (`sources.yaml` annonce cs.AI, cs.LG, cs.SE, cs.DB). Renvoyer les liens en `https`.
- **Critère d'acceptation** : `AI agent evaluation` renvoie au moins 4 résultats pertinents sur 5. Une requête avec préfixe de champ ne provoque plus de `400`.
- **Note** : la limitation « HTTP 301 » documentée dans la skill n'a pas été reproduite sur 6 appels. Le serveur appelle déjà `https://export.arxiv.org`.

### S4. Recherche YouTube triée par date, métadonnées manquantes

- **Constat** : l'outil renvoie les vidéos les plus récentes, pas les plus pertinentes. La sortie ne contient ni nombre de vues ni durée. Les entités HTML ne sont pas décodées.
- **Preuve** :
  - `Claude Code mods`, `days_back=60` : 10 résultats sur 10 publiés dans les six dernières heures, majoritairement des Shorts, en cinq langues, dont un re-upload de la vidéo officielle. La vidéo officielle elle-même est absente.
  - `AI agent evaluation`, `days_back=30` : 5 résultats sur 5 publiés dans les quatre dernières heures.
  - Titres contenant `&amp;`, descriptions terminées par `......`.
- **Cause** : tri par date. `CONFIRMÉ` par l'ordre des sorties. Un seul appel de recherche sans appel de détail. `HYPOTHÈSE`.
- **Piste** : trier par pertinence en conservant la borne `publishedAfter`. Ajouter un appel de détail pour récupérer vues et durée. Décoder les entités HTML. Envisager un filtre de durée pour écarter les Shorts et un paramètre de langue. Paramètres candidats de l'API YouTube Data à vérifier : `order`, `publishedAfter`, `videoDuration`, `relevanceLanguage`, puis `videos.list` avec `statistics` et `contentDetails`.
- **Critère d'acceptation** : pour `Claude Code mods`, la vidéo officielle figure dans les résultats. Chaque résultat porte un nombre de vues et une durée. Aucun titre ne contient d'entité HTML.

### S5. Erreurs renvoyées comme du texte de résultat

- **Constat** : une erreur d'API arrive sous la forme `{"result": "Error: GitHub API error: ..."}`, c'est-à-dire comme un résultat normal dont le texte commence par « Error ».
- **Cause** : l'outil capture l'exception et renvoie une chaîne. `HYPOTHÈSE`.
- **Piste** : signaler l'échec par le mécanisme d'erreur du protocole, avec un message actionnable (cause probable, action possible). Distinguer « aucun résultat » de « source indisponible ».
- **Critère d'acceptation** : un client peut distinguer un échec d'un succès sans analyser le texte.

### S6. Couverture de tests

- **Constat** : 43 tests passent alors que S2, S3 et S4 existent. Les tests vérifient donc probablement la forme des réponses et non leur pertinence. `HYPOTHÈSE`.
- **Piste** : ajouter des tests sur la construction des requêtes (arXiv multi-mots, préfixe de champ), le repli sur `401`, le paramètre de tri YouTube, le décodage des entités, et la présence des dates dans la sortie GitHub.
- **Critère d'acceptation** : chacun des défauts S1 à S5 est couvert par un test qui échoue avant correction.

## 7. Skill

### K1. Section « Known limitations » fausse sur les trois outils

- **Constat** :
  - GitHub : la skill annonce « 60 req/hour » et un échec silencieux. La limite de recherche est de 10 requêtes par minute sans token, et l'échec observé est un `401` explicite.
  - arXiv : la skill annonce une erreur `301`. Non reproduite.
  - YouTube : la skill annonce que les vidéos de moins de 48 h peuvent manquer. C'est l'inverse : seules les plus récentes remontent.
- **Piste** : réécrire la section à partir des comportements observés, puis la réduire après correction du serveur.
- **Critère d'acceptation** : chaque limitation documentée est reproductible.

### K2. L'étape de normalisation déclenche le défaut arXiv

- **Constat** : l'étape 1 demande « 2-4 focused keywords » sans guillemets, exactement le cas qui échoue (S3).
- **Piste** : si S3 est corrigé, rien à faire. Sinon, demander une expression entre guillemets pour arXiv. Dans tous les cas, autoriser une requête différente par outil : pour « Claude Mods », la requête utile était `claude code mods` sur GitHub et `"Claude Code"` sur arXiv.
- **Critère d'acceptation** : la skill ne produit plus de résultats arXiv hors sujet sur une requête de plusieurs mots.

### K3. Mode dégradé trop étroit

- **Constat** : la note « Degraded mode » n'est prévue que si les trois outils échouent. Le 8 octobre, un outil était en erreur et deux renvoyaient du bruit : le rapport serait sorti sans avertissement. Le pied de page du gabarit cite « arXiv · GitHub · YouTube · Web search » en dur.
- **Preuve** : lors du test « Claude Mods », aucun des 10 résultats YouTube n'a été retenu, et il a fallu ajouter une ligne « Collecte » hors gabarit pour le signaler.
- **Piste** : prévoir dans l'en-tête du rapport un état par source (interrogée, résultats retenus, échec ou bruit). Générer le pied de page à partir des sources réellement utilisées.
- **Critère d'acceptation** : un lecteur du rapport sait quelles sources ont contribué et lesquelles ont échoué.

### K4. Déclenchement du Tier 3 évalué trop tôt

- **Constat** : le Tier 3 se déclenche sous 12 résultats « pertinents », mais la pertinence n'est évaluée qu'à l'étape 6. Le bruit des outils compte donc comme des résultats.
- **Piste** : insérer un filtre de pertinence rapide juste après le Tier 1 et le Tier 2, et compter uniquement les résultats qui le passent.
- **Critère d'acceptation** : dix résultats hors sujet ne dispensent pas du Tier 3.

### K5. Grille de notation incohérente et mal calibrée

- **Constat** :
  - Fraîcheur : annoncée « linéaire » mais définie par paliers. Elle vaut 0 au-delà de 30 jours alors que `days_back=60` est prévu. Elle n'est pas définie pour un dépôt ni pour une page de documentation non datée.
  - Profondeur : seulement deux valeurs (10 ou 4), rien pour un dépôt ni pour un article de longueur moyenne.
  - Autorité : les 20 points sont réservés à arXiv, GitHub et YouTube. Une source officielle d'éditeur plafonne à 12.
  - Seuil : « Drop unless Tier 3 run returns nothing better » contredit le seuil strict de 60 de `SKILL.md` et de `sources.yaml`.
  - Libellés : « 🔴 Tier 1 / Essential » se confond avec les tiers de sources. « Authority: High/Medium/Low » dans le gabarit n'a pas de correspondance avec les points.
- **Preuve** (test « Claude Mods ») :
  - Documentation officielle : 80. Annonce d'Anthropic : 74. Dépôt communautaire de 163 étoiles : 90.
  - Deux articles arXiv « adjacents » obtiennent 73 (20 + 20 + 20 + 10 + 3), soit autant qu'un article exactement sur le sujet.
  - Sans la clause « low-signal », un Short publié le jour même aurait obtenu 87 et dépassé la documentation officielle.
- **Piste** : redéfinir l'autorité par la nature de la source (primaire, analyse de qualité, communautaire, faible signal) plutôt que par la plateforme. Aligner la fraîcheur sur la fenêtre demandée. Définir chaque critère pour chaque type de source. Empêcher qu'une source « adjacente » atteigne le seuil par sa seule fraîcheur.
- **Critère d'acceptation** : sur le cas « Claude Mods », la documentation officielle et l'annonce figurent dans la tranche la plus haute. Aucun Short n'y figure.

### K6. Étape d'enrichissement manquante

- **Constat** : la notation exige une date, une longueur et des signaux d'engagement. La recherche web ne renvoie que des titres et des URL. Les sorties MCP ne donnent ni date pour GitHub ni vues pour YouTube.
- **Preuve** : environ 25 pages ont dû être ouvertes pour noter 20 sources. Plusieurs étaient illisibles (pages vidéo YouTube, historiques de commits GitHub, un site refusant l'accès).
- **Piste** : ajouter une étape explicite d'enrichissement des candidats avant la notation, avec un budget de pages. Prévoir la règle pour une donnée introuvable : la marquer « non vérifiée », ne jamais l'inventer. S2 et S4 réduisent ce besoin.
- **Critère d'acceptation** : toute date du rapport est soit vérifiée, soit marquée comme non vérifiée.

### K7. Aucune notion de source primaire ni d'exactitude

- **Constat** : la skill ne demande pas d'identifier les sources primaires (documentation officielle, annonce de l'éditeur, dépôt ou issue de référence). Elles ont été trouvées par la recherche web générale. La grille n'a aucun critère d'exactitude.
- **Preuve** : un article affirmant que les mods exigeaient encore un drapeau d'accès anticipé, ce que la documentation officielle contredit, aurait obtenu 73. Il a été écarté par jugement, hors grille.
- **Piste** : ajouter une étape « sources primaires d'abord » et s'en servir comme référence pour détecter les contradictions. Signaler ou écarter une source qui contredit une source primaire.
- **Critère d'acceptation** : le rapport cite les sources primaires quand elles existent et signale les contradictions.

### K8. Description trop pauvre pour le déclenchement

- **Constat** : la description tient en une ligne, sans phrase-type ni formulation française (« veille techno », « fais une veille sur »). Les cas négatifs sont dans le corps de la skill, lu seulement après déclenchement : ils ne filtrent rien.
- **Piste** : enrichir la description avec les déclencheurs, en français et en anglais, et y remonter les cas négatifs.
- **Critère d'acceptation** : voir les évals E5 et E7.

### K9. Gabarits de requêtes Tier 2 trop restrictifs

- **Constat** : `"{query}"` en expression exacte sur 3 ou 4 mots-clés réduit fortement le rappel. Les opérateurs `site:a OR site:b` supposent un moteur qui les respecte. L'outil est nommé `web_search` dans la skill.
- **Piste** : ne mettre entre guillemets que les noms propres ou expressions figées. Utiliser le filtrage par domaine de l'outil de recherche quand il existe. Adapter le nom de l'outil à l'environnement.
- **Critère d'acceptation** : les recherches Tier 2 renvoient des résultats sur une requête de quatre mots.

### K10. Dédoublonnage et homonymes

- **Constat** : l'étape 5 ne traite que le même contenu sur plusieurs URL. Le test a rencontré un re-upload de vidéo, des synthèses secondaires d'une même annonce, et deux dépôts homonymes.
- **Piste** : étendre le dédoublonnage aux re-uploads et aux reprises sans apport. Ajouter une vérification de sens pour les résultats dont seul le nom correspond.
- **Critère d'acceptation** : voir l'éval E6.

### K11. Sortie sous-spécifiée

- **Constat** : pas de règle de slug pour `{query}` dans le nom de fichier, pas de langue de rapport, pas d'indication sur l'emplacement ni la livraison du fichier.
- **Piste** : fixer le slug (minuscules, tirets), la langue (celle de la demande, ou un paramètre), et l'emplacement de sortie.
- **Critère d'acceptation** : deux exécutions sur la même requête produisent le même nom de fichier.

### K12. Portabilité vers Claude Code

- **Constat** : la skill suppose les outils MCP disponibles et un outil nommé `web_search`. `HYPOTHÈSE` : dans Claude Code, le nom qualifié des outils dépend du nom donné au serveur, et le serveur doit y être déclaré (distant sur Cloud Run, ou local en stdio pour le débogage).
- **Piste** : vérifier la déclaration du serveur, les noms d'outils, la résolution des chemins `references/`, et le comportement quand le serveur est absent.
- **Critère d'acceptation** : la skill s'exécute de bout en bout dans Claude Code, et annonce clairement l'absence du serveur le cas échéant.

## 8. Scénarios d'évals proposés

| ID | Scénario | Comportement attendu | Items couverts |
|---|---|---|---|
| E1 | Fonctionnalité produit récente (« Claude Mods ») | Sources officielles dans la tranche haute, aucun Short | K5, K7, S4 |
| E2 | Requête de recherche multi-mots (« AI agent evaluation ») | Au moins 4 résultats arXiv pertinents sur 5 | S3, K2 |
| E3 | Un outil en panne (GitHub en `401`) | État par source dans l'en-tête, pied de page fidèle | S1, K3 |
| E4 | Sujet lent avec `days_back=60` | Les sources de 31 à 60 jours ne sont pas éliminées d'office | K5 |
| E5 | Non-déclenchement (« What is RAG? », « Summarize this document ») | La skill ne se déclenche pas | K8 |
| E6 | Homonymes (« claude mods ») | Les dépôts sans rapport sont écartés | K10, S2 |
| E7 | Demande en français (« fais-moi une veille sur X ») | La skill se déclenche | K8 |
| E8 | Pages illisibles | Dates marquées « non vérifiée », aucune date inventée | K6 |
| E9 | Source contredisant la documentation officielle | Contradiction signalée ou source écartée | K7 |
| E10 | Bruit massif au Tier 1 | Le Tier 3 se déclenche | K4 |

Exécuter E1 à E10 une première fois avant toute modification donne la référence de comparaison.

## 9. Appels de reproduction

Les appels ci-dessous ont produit les preuves citées. Les résultats dépendent de la date d'exécution.

| Outil | Arguments | Résultat observé |
|---|---|---|
| `search_github_repos` | `query="dbt", max_results=1` | `DataTalksClub/data-engineering-zoomcamp` |
| `search_github_repos` | `query="claude mods", max_results=10` | 8 pertinents, 2 homonymes |
| `search_arxiv_papers` | `query="AI agent evaluation", days_back=30, max_results=5` | 5 hors sujet |
| `search_arxiv_papers` | `query="\"agent evaluation\"", days_back=30, max_results=3` | 3 pertinents |
| `search_arxiv_papers` | `query="all:agent AND all:evaluation AND cat:cs.AI"` | Erreur `400` |
| `search_youtube_videos` | `query="Claude Code mods", days_back=60, max_results=10` | 10 vidéos des six dernières heures |

## 10. Références

- GitHub, recherche REST et limites de débit : https://docs.github.com/en/rest/search/search
- GitHub, authentification REST (`401` puis `403` temporaire) : https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api
- arXiv, manuel de l'API (guillemets, opérateurs, `submittedDate`, `sortBy`) : https://info.arxiv.org/help/api/user-manual.html
- Cloud Run, variables d'environnement : https://docs.cloud.google.com/run/docs/configuring/services/environment-variables
- Rapport du test « Claude Mods » : `tech-watch-claude-mods-2026-10-09.md`

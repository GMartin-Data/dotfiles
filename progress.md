## Dernière mise à jour
Date : 2026-10-11 09:31
Session : 728a4194-3ef1-4992-b8d4-be183eeec06e

## Tâches complétées

- **Rejeu final E1–E7 sur les fichiers finaux** (`tasks/tech-watch-2026-10/final-replay-2026-10-11/`,
  section « Rejeu final » dans `plan.md` §5) : sept sandboxes en parallèle,
  `run-eval.sh`, Opus, serveur `00009` (E3 en stdio local, `GITHUB_TOKEN=invalid` ;
  E5a/E5b/E7b sur le bouchon, `--max-turns 1` ; E7a en veille complète).
  **Six scénarios sur six réussis** : E1 (bloc « Primary sources » à 3 entrées,
  vidéo officielle n° 1 A Primary 94, 15 vidéos de 3:21 à 17:27), E2 (4/5
  arXiv strict), E3 (GitHub `degraded` 30/29/12 avec repli compté dans la
  ligne, YouTube `failed` 10/10/0, pied `GitHub · Web (Tier 2) · Owner
  domains`), E5 ×2, E6 (`0xDarkMatter` n° 9 côté serveur, écarté au test de
  sens), E7 ×2. Les deux échecs de la référence (E1, E3) et l'échec acté E6
  sont corrigés par règle. Coût 3,94 $.
- Observés au passage : titre K11 au sujet normalisé et ligne `Request` sur
  les quatre rapports ; comptes de repli K3 cohérents (`Pipeline` = somme des
  lignes) ; **E9 sur une source classée** (E3, rang 4, dev.to datant l'annonce
  au 3 octobre : gardée et étiquetée `⚠️ Contradicts …`), point en suspens
  couvert.
- **Critère de la phase 3 observé** : E1–E10 rejoués (E4, E8, E10 en K5, K6,
  K4), comparés à `baseline/`.
- **Décision Greg : agent sur Opus pour l'usage réel** (actée dans `plan.md` §5,
  K12 point 1) : tarif 2,5 fois moindre que Fable, règles validées sur Opus
  seulement. Aucun changement de fichier.
- Branche `feat/tech-watch-skill` : **50 commits d'avance sur `main`, non
  poussée**, arbre propre (`791e863` rejeu, `8da810d` décision Opus).

## En cours

- Rien. La phase 4 s'ouvre dans une session neuve.

## Prochaines étapes

1. **Phase 4** (`plan.md` §3) : retrait de l'ancien trio command + agent
   `tech-watch-scorer` + script (D2a : `claude/commands/tech-watch.md`,
   `claude/agents/scripts/`, lignes correspondantes d'`install.sh`) ; liens
   `install.sh` pour `claude/skills/tech-watch/` et `claude/agents/tech-watch.md` ;
   README des dotfiles ; `claude/evals/tech-watch/README.md` (montage fork,
   `run-eval.sh`, fixtures, `check-dates.py`, recette E5/E7 au bouchon) ;
   permission `Write(/home/martin/tech-watch/**)` ou `--add-dir` dans la
   configuration livrée (en session interactive, `Write` hors CWD demande une
   permission — observé en K11) ; `/code-review` sur la branche, triage, PR.
2. Points pour Greg issus du rejeu final (fiche `final-replay-2026-10-11/run.md`,
   « Observations ») : dates dev.to sans année lues comme 2026 et déclarées
   (statu quo ou `unverified` ; `check-dates.py` à élargir aux graphies
   `10/7/2026`, `Oct 06, 2026`, jour-mois seul, et au bloc « Primary
   sources ») ; égalités sans signal d'engagement départagées par un critère
   inventé (E1, E2 — règle K5) ; `Owner domains` à `not run (…)` sur un sujet
   sans propriétaire (E2 — à figer dans « Header rules » ou laisser).
3. Items dormants et cycle `/insights` 2026-10-26 : `tasks/insights-actions.md`.

## Écarts vs PRD

- Aucun (pas de PRD, repo dotfiles). Écarts à la passation sur l'ensemble de
  la phase 3 : E10 sur 3 sujets, E8 simulé par retrait de `WebFetch`, E9
  d'abord opportuniste puis observé sur une source classée au rejeu final,
  Papers With Code remplacé par Hugging Face Papers, DEV.to/Hashnode retirés
  du Tier 3, E1 + E7a joués ensemble pour K11.

## Décisions prises

- Track léger, sans ADR — décisions Greg du 2026-10-11 :
  - **Agent `tech-watch` sur Opus pour l'usage réel** (`plan.md` §5, K12
    point 1) ; le pin `model: opus` suit l'alias.
  - Rejeu final lancé en parallèle (sept sandboxes), E7a en veille complète
    pour observer la ligne `Request`.
- Décisions de la phase 3 (K12 → K1, 2026-10-10) : `plan.md` §5, une
  sous-section par item.
- **Points en suspens pour Greg** (consignés dans `plan.md` §5) : Tier 3 de
  `sources.yaml` orienté IA, inutile sur un sujet data ; frontière B/C au
  jugement du modèle ; plateau à 85 des vidéos-listes et égalités sans signal
  d'engagement ; `check-dates.py` incomplet (graphies, bloc « Primary
  sources ») ; sans YouTube, la tranche Essential peut rester vide ; dates
  dev.to sans année ; `Owner domains` sans propriétaire.

## Blocages

- Aucun côté chantier. Hors chantier : endpoint Cloud Run `/sse` public sans
  auth ; rotation de `YOUTUBE_API_KEY` (logs des révisions ≤ `00008`) à la
  main de Greg — tous deux à traiter dans le dépôt `~/mcp-server-code`, hors
  de cette branche.

---

## Checkpoint précédent — 2026-10-10 16:14
Session : 74a6446f-bfe1-4ed1-9f87-7b70c2f7a0ba

## Tâches complétées

- **Phase 3 close : 11 items sur 11** (`plan.md` §5), chacun avec règle validée
  par Greg, rejeu d'eval contre le critère, fiche dans
  `tasks/tech-watch-2026-10/phase3/`. Lot « sortie » de cette session :
  - **K3** état par source : en-tête à lignes fixes dans `report-template.md`
    (tableau de 6 lignes, statuts fermés `ok` / `empty` / `degraded` / `failed`
    / `absent` / `not run`, lignes `Pipeline`, `Enrichment`, `Date test`,
    `Notes`), pied de page `Sources used` dérivé du tableau. E3 rejoué :
    GitHub `degraded`, YouTube `failed`, pied de page sans arXiv ni YouTube,
    syntaxe `env:` du `mcpServers` inline vérifiée. 0,83 $. Correctif après
    run, non rejoué : les résultats de repli comptent dans la ligne de l'outil
    remplacé.
  - **K11** sortie : slug = sujet normalisé (minuscules, ASCII, tirets), nom
    `tech-watch-{slug}-{date}.md` (`-{days}d` hors fenêtre 30), rapport en
    **anglais fixe**, dossier fixe `/home/martin/tech-watch/` créé si absent,
    première ligne de chat `Report: <chemin> — n ranked + m primary — normal |
    degraded: …`. E1 et E7a : même nom de fichier sur deux formulations,
    dossier créé par `Write`. 1,82 $. Correctif après run, non rejoué : titre
    du gabarit = sujet normalisé, demande tapée en métadonnée `Request`.
  - **K1** limitations réécrites d'après les fiches (3 lignes supprimées
    jamais reproduites, 2 réécrites, 5 nouvelles), traçabilité dans
    `phase3/K1-limitations-2026-10-10.md`. Sans run, 0 $.
- `run-eval.sh` réécrit le dossier de sortie fixe en `cwd/tech-watch/` du
  sandbox (sans le pré-créer) ; fixture E3 alignée sur l'agent.
- Coût cumulé de la phase 3 ≈ 13 $. Branche `feat/tech-watch-skill` :
  **47 commits d'avance sur `main`, non poussée**, arbre propre.

## En cours

- Rien. Phase 3 close ; le rejeu final et la phase 4 s'ouvrent dans une
  session neuve.

## Prochaines étapes

1. **Rejeu final E1 à E7** via `run-eval.sh`, comparaison à `baseline/` (≈ 4 $) :
   E1 et E7a servent aussi à observer la ligne `Request` du gabarit, non
   rejouée depuis le correctif de titre. État des autres scénarios, d'après
   les fiches : E4 joué en K5 (fenêtre 60 jours, réussi), E8 joué en K6 (E8a
   sans `WebFetch`, E8b normal, réussi), E10 joué en K4 (trois sujets, Tier 3
   déclenché sur « Apache Iceberg row lineage », réussi) ; E9 réussi de façon
   opportuniste sur E1 en K7, sur une source hors top 20, à rejouer quand un
   cas connu de contradiction existera.
2. **Phase 4** : retrait de l'ancien trio command + agent `tech-watch-scorer`
   + script (D2a, `claude/commands/tech-watch.md`, `claude/agents/scripts/`,
   lignes correspondantes d'`install.sh`), liens `install.sh` pour la skill et
   l'agent, README, `claude/evals/tech-watch/README.md`, règle de permission
   `Write(/home/martin/tech-watch/**)` ou `--add-dir` dans la configuration
   livrée, `/code-review` sur la branche, PR.
3. Items dormants et cycle `/insights` 2026-10-26 : `tasks/insights-actions.md`.

## Écarts vs PRD

- Aucun (pas de PRD, repo dotfiles). Écarts à la passation de la phase 3 :
  E10 sur 3 sujets, E8 simulé par retrait de `WebFetch`, E9 opportuniste,
  Papers With Code remplacé par Hugging Face Papers, DEV.to/Hashnode retirés
  du Tier 3 ; en fin de phase, E1 + E7a joués ensemble pour K11.

## Décisions prises

- Track léger, sans ADR — décisions Greg du 2026-10-10 (détail dans `plan.md`
  §5, phase 3) :
  - K3 : pied de page **dérivé** du tableau d'état plutôt que supprimé.
  - K11 : rapport en **anglais fixe** ; sortie dans un **dossier fixe**
    plutôt que `./tech-watch/` ou la racine du CWD.
  - K1 : texte des limitations validé tel quel.
  - Décisions des items K12, K8, K2/K9, K4, K6, K7, K5, K10 : checkpoint
    précédent et `plan.md` §5.
- Ajustements pris par Claude, signalés, non rejoués : comptes de repli dans la
  ligne de l'outil remplacé (K3) ; titre du gabarit au sujet normalisé (K11).
- **Points en suspens pour Greg** (consignés dans `plan.md` §5) : `model: opus`
  figé dans l'agent ; Tier 3 de `sources.yaml` orienté IA, inutile sur un sujet
  data ; frontière B/C au jugement du modèle ; plateau à 85 des vidéos-listes ;
  E9 à rejouer sur une source classée ; `check-dates.py` ne lit pas le bloc
  « Primary sources » ; sans YouTube, la tranche Essential peut rester vide
  (K5, observé au rejeu K3).

## Blocages

- Aucun côté chantier. Hors chantier, inchangés : endpoint Cloud Run `/sse`
  public sans auth ; rotation de `YOUTUBE_API_KEY` (logs des révisions
  ≤ `00008`) à la main de Greg.

---

## Checkpoint précédent — 2026-10-10 15:19
Session : c353e960-a614-4035-b178-7387d249e416

## Tâches complétées

- **Phase 3 — 8 items sur 11 clos**, chacun avec règle validée par Greg
  (un point par tour), rejeu d'eval contre le critère, fiche dans
  `tasks/tech-watch-2026-10/phase3/` et section dans `plan.md` §5 :
  - **K12** sonde du montage D3 (d) : le `mcpServers` inline d'un subagent est
    connecté quand une skill le fork ; serveur injoignable = outils absents
    sans erreur. `claude/agents/tech-watch.md` créé, `SKILL.md` en
    `context: fork` + `agent: tech-watch`. E1 rejoué sous le fork : 121 s, 0,50 $.
  - **K8** description enrichie (6 phrases-types FR/EN, cas négatifs remontés) ;
    E5 ×2, E7 ×2 identiques à la référence. Skill claude.ai **supprimée par
    Greg** (doublon synchronisé disparu, vérifié par sonde).
  - **K2/K9** une requête par outil, paramètres explicites, Tier 2/3 en
    `WebSearch` + `allowed_domains`, Papers With Code → Hugging Face ;
    E2 arXiv **5/5** strict (référence 3/5), Tier 2 9–10 liens par recherche.
  - **K4** filtre rapide on-topic / adjacent / off-topic, dédoublonnage avant
    comptage, Tier 3 si on-topic uniques < 12 ; E10 sur 3 sujets, déclenché
    sur « Apache Iceberg row lineage » (83 adjacents/off-topic n'ont pas
    dispensé du Tier 3).
  - **K6** enrichissement budgété (10 `WebFetch`, une par URL, Tier 1 jamais
    ouvert, `unverified` sinon) ; E8 sans `WebFetch` et run normal : aucune
    date inventée, budget tenu à l'unité. `check-dates.py` créé.
  - **K7** sources primaires d'abord (recherche sur les domaines du
    propriétaire, bloc « Primary sources » hors classement, règle de
    contradiction) ; E1 : billet, docs `en`, changelog ouverts en premier ;
    une contradiction réelle signalée (E9 opportuniste).
  - **K5** grille réécrite (autorité par nature A/B/C/D, fraîcheur relative
    à la fenêtre, dépôt sur sa date de création, seuil 60 strict) ; E1 :
    vidéo officielle n° 1 à 94, vidéos-listes de 97 à 85, 3 sources web
    classées ; E4 : sources de 31–60 j gardées.
  - **K10** tests d'homonymie (date, sens) et dédoublonnage élargi (plafond
    2 par auteur) ; correctif en cours de route (référence = plus ancienne
    date d'une source primaire, préversion comprise, sinon test sauté) ;
    E6 réussi, `0xDarkMatter/claude-mods` écarté par règle.
- Montage d'evals stabilisé : `run-eval.sh` sans `--strict-mcp-config` (bloque
  aussi les serveurs du frontmatter), `AGENT_MD` (E3 stdio, bouchon
  `fixtures/k8/agent-stub.md` pour E5/E7 avec `--max-turns 1`),
  `probe-k12.sh`, `check-dates.py`. Transcripts dans `claude/evals/results/`
  (gitignorés). Coût cumulé de la phase 3 ≈ 10 $ (≈ 20 runs).
- Branche `feat/tech-watch-skill` : **40 commits d'avance sur `main`, non
  poussée**, arbre propre.

## En cours

- Rien. Checkpoint pris à 35 % de contexte, par découpage : le lot « sortie »
  (K3, K11, K1) s'ouvre dans une session neuve sur les fichiers finaux.

## Prochaines étapes

1. **K3** — état par source : figer dans `report-template.md` un en-tête à
   format fixe (comptes, requêtes, tiers, enrichissement, couverture, date
   test — aujourd'hui 5 lignes spontanées, format différent à chaque run) et
   un pied de page généré d'après les sources réellement utilisées (figé
   « arXiv · GitHub · YouTube · Web search » depuis la référence). Rejeu E3 :
   `AGENT_MD=claude/evals/tech-watch/fixtures/e3/agent-stdio-invalid-token.md`
   (syntaxe `env:` du frontmatter à vérifier au passage), comparer à
   `baseline/E3-github-401-2026-10-10/`. Proposer le format avant d'écrire.
2. **K11** — slug, langue, emplacement (rapport en anglais ou français selon
   les runs, résumé en français ; slug observé `claude-code-mods` /
   `ai-agent-evaluation` ; emplacement = CWD).
3. **K1** — limitations réécrites d'après les comportements réels
   post-correction (S1 avertissement 401, serveur absent = outils absents,
   budget de pages, `unverified`).
4. Rejeu final E1–E7 via `run-eval.sh`, comparaison à `baseline/`, puis
   **phase 4** : retrait de l'ancien trio command + agent + script (D2a),
   `install.sh`, README, `claude/evals/tech-watch/README.md`, `/code-review`
   sur la branche, PR.
5. Items dormants et cycle `/insights` 2026-10-26 : `tasks/insights-actions.md`.

## Écarts vs PRD

- N/A (pas de PRD — repo dotfiles). Écarts à la passation : E10 a demandé
  3 sujets (les deux premiers trop couverts) ; E8 simulé par retrait de
  `WebFetch` ; E9 joué de façon opportuniste sur E1 ; Papers With Code
  remplacé (archivé) ; DEV.to/Hashnode retiré du Tier 3 (doublon Tier 2).

## Décisions prises

- Track léger, sans ADR — décisions Greg du 2026-10-10 (détail dans `plan.md`
  §5, phase 3) :
  - Skill claude.ai **supprimée** plutôt que renommée (le déclenchement se
    fait sur la description).
  - K2/K9 : catégories arXiv `cs.AI, cs.LG, cs.CL, cs.SE, cs.DB` ; YouTube
    `language=en` sauf demande FR ; Hugging Face Papers remplace Papers With Code.
  - K4 : coupe vidéo < 3 min binaire ; adjacents hors du compte des 12.
  - K6 : budget 10 pages échecs compris ; Tier 1 jamais ouvert ; E8 par
    retrait de `WebFetch`.
  - K7 : bloc « Primary sources » hors classement ; contradiction écartée si
    dans le titre, sinon signalée ; 3 pages réservées ; AWS et Azure ajoutés
    aux propriétaires connus.
  - K5 : autorité par nature A/B/C/D ; date `unverified` = 5, adjacents non
    classés ; seuil 60 strict avec note de couverture.
  - K10 : test de date adossé à la source primaire ; plafond 2 par auteur ;
    réécritures sans apport en D.
- Ajustements pris par Claude, signalés, non contestés : dédoublonnage avant
  comptage (K4) ; test de date sur la plus ancienne date primaire, sauté si
  préversion non datée (K10).
- **Points en suspens pour Greg** (consignés dans `plan.md` §5) : `model: opus`
  figé dans l'agent (choix pour l'usage réel avant la phase 4) ; Tier 3 de
  `sources.yaml` orienté IA, inutile sur un sujet data (compléter ou laisser
  le modèle proposer) ; frontière B/C au jugement du modèle ; plateau à 85
  des vidéos-listes (levier engagement ou seuil de tranche) ; E9 à rejouer
  sur une source classée ; `check-dates.py` ne lit pas le bloc « Primary sources ».

## Blocages

- Aucun côté chantier. Hors chantier, inchangés : endpoint Cloud Run `/sse`
  public sans auth ; rotation de `YOUTUBE_API_KEY` (logs des révisions
  ≤ `00008`) à la main de Greg.

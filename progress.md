## Dernière mise à jour
Date : 2026-10-10 16:14
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

---

## Checkpoint précédent — 2026-10-10 11:56
Session : 08467072-cb71-4adb-bde3-d8c9315a577a

## Tâches complétées

- **Phase 0 close** (`plan.md` §5, commit `cbef0a2`) :
  - Import verbatim de l'export claude.ai (`tech-watch-skill.zip`, 4 fichiers)
    dans `claude/skills/tech-watch/`, **sans symlink** (D2a) — `e9609c3`.
  - **D3 révisé en (d)** : scope user essayé puis retiré le jour même sur
    objection de Greg (context-engineering) ; cible = subagent `tech-watch` à
    `mcpServers` inline + skill en `context: fork`, à construire en phase 3.
    Noms vérifiés par sonde : `mcp__tech-watch__search_*`, `WebSearch` — `cef27c1`.
  - **Référence E1–E7** dans `tasks/tech-watch-2026-10/baseline/<E>-<slug>-<date>/`
    (rapport tel quel + `run.md`). Verdicts : E1 échec/réussi (K5 reproduit,
    aucun Short) · E2 réussi (lecture phases 1–2) · E3 réussi/échec (en-tête
    par source OK, pied de page figé) · E5 réussi ×2 · E6 échec (K10, acté sur
    E1) · E7 réussi ×2. Coût ≈ 3,9 $.
  - Outillage réutilisable : `claude/evals/tech-watch/run-eval.sh` (sandbox
    isolé patron batch A, `--mcp-config` session, Opus pinné, `EXTRA_ARGS`,
    `FIXTURE_DIR`, `MCP_JSON`), `extract-run.sh`, fixtures `e3/` (stdio, token
    bidon) et `e5/notes.md`. Transcripts dans `claude/evals/results/`
    (gitignorés).
- Branche `feat/tech-watch-skill` : 19 commits, **non poussée**.

## En cours

- Rien. La phase 3 s'ouvre dans une session neuve.

## Prochaines étapes

1. **Phase 3 — skill**, ordre du plan §3 : K12 d'abord (sonde du point non
   documenté : le `mcpServers` inline d'un subagent est-il connecté quand une
   skill le fork ; agent `tech-watch` sur le patron `agents/dbt.md` ; skill en
   `context: fork` ; `web_search` → `WebSearch` ; retirer ou renommer la skill
   côté claude.ai dès que la version fichier diverge, car Claude Code la
   synchronise sous `anthropic-skills:tech-watch`), puis K8 → K2/K9 → K4 → K6
   → K7 → **K5 en tour dédié** → K10 → K3 → K11 → K1. Observations transverses
   à relire avant : `plan.md` §5 « Phase 0 ».
2. Rejeu E1–E7 après chaque lot via `run-eval.sh`, comparaison à `baseline/`.
   E4, E8, E9, E10 : non joués, une veille complète chacun, selon budget.
3. **Phase 4** : retrait de l'ancien trio command + agent + script (D2a),
   `install.sh`, README, `claude/evals/tech-watch/README.md`, `/code-review`
   sur la branche, PR.
4. Items dormants et cycle `/insights` 2026-10-26 : `tasks/insights-actions.md`.

## Écarts vs PRD

- N/A (pas de PRD — repo dotfiles). Écarts à la passation : E3 joué avec
  YouTube également en panne (pas de clé en local) ; E6 acté sur E1 ; série
  sur Opus 5.5 et non Fable.

## Décisions prises

- Track léger, sans ADR — décisions Greg (2026-10-09 → 10) :
  - **D3 (d)** subagent inline plutôt que scope user (`plan.md` §1).
  - **Opus 5.5 pour toute la série E1–E10** ; ne rouvrir qu'en cas de fort
    désaccord.
  - E6 acté sur le run E1, sans rejeu ; fixture E5 à sujet « proche d'une
    veille » validée après explication.
  - Transcripts non committés (précédent batch A, `claude/evals/results/`
    gitignoré).

## Blocages

- Aucun côté chantier. Hors chantier, inchangés : endpoint Cloud Run `/sse`
  public sans auth ; rotation de `YOUTUBE_API_KEY` (logs des révisions
  ≤ `00008`) à la main de Greg.


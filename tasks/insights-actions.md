# Insights Actions

Fiches d'action du cycle /insights (protocole v3) : une fiche par action
engagée — problème observé, action, critère de succès vérifiable, date de
revue. Propriété du cycle /insights ; une fiche se clôt au verdict de sa date
de revue. Relocalisées depuis `tasks/lessons-inbox.md` le 2026-07-30
([`adr/0015`](../adr/0015-cycle-immunitaire-refonte-post-p1.md) : inbox
mono-population).

---

## [INSIGHTS 2026-06-26] [VALIDÉ] response-style-token-budget

- **Problème observé** : ≥8 sessions sur 22 analysées totalement perdues sur des erreurs API « 500 output token maximum » (friction n°1 du rapport /insights du 2026-06-28).
- **Action engagée** : ajout d'une section `## Response Style` au CLAUDE.md global (résumé 3 bullets avant développement, increments courts, artefacts longs en fichiers).
- **Critère de succès vérifiable** : au prochain /insights (≈2026-07-26), part des sessions wipe sur token-limit nettement inférieure à 8/22 (idéalement 0–2).
- **Date de revue** : 2026-07-26
- **Verdict (2026-07-26)** : ✅ atteint — rapport du 2026-07-26 : 1 seule session perdue sur token-limit sur 28 analysées (vs 8/22), alors que la fenêtre couvre encore la période pré-fix.

---

## [INSIGHTS 2026-07-26] [VALIDÉ] scope-discipline

- **Problème observé** : friction n°1 du rapport 2026-07-26 — au moins 6 interruptions utilisateur pendant la reconnaissance initiale (sweeps Bash parallèles, sur-exploration), dont 1 session `not_achieved`.
- **Action engagée** : ajout d'une section `## Scope Discipline` au CLAUDE.md global — sur session de reprise, lire les fichiers de contexte au lieu d'explorer ; toute recon multi-fichiers passe par un plan d'une ligne validé.
- **Critère de succès vérifiable** : au prochain /insights (≈2026-08-26), zéro interruption utilisateur pendant une phase de reconnaissance sur la fenêtre analysée.
- **Date de revue** : 2026-08-26
- **Verdict (2026-09-02, revue tardive — cycle exécuté le 02/09)** : ✅ atteint — rapport du 2026-09-02 (fenêtre 2026-07-31 → 2026-09-02, 26 sessions) : zéro interruption en phase de reconnaissance. Les interruptions relevées par le rapport sont du « explain before code » en session pédagogique — autre phase, hors périmètre du critère.

---

## [INSIGHTS 2026-08-26] [VALIDÉ] explain-before-artifact

- **Problème observé** : friction n°1 du rapport du 2026-09-02 (cycle 2026-08-26 exécuté en retard) — au moins 3 interruptions mid-tool-call pour exiger l'explication pédagogique avant que Claude n'écrive un lab/une leçon.
- **Action engagée** : encoder le contrat « expliquer concept et conception avant d'écrire tout artefact pédagogique, attendre le go » dans les skills existantes (dotfiles) — section « Explain Before Artifact » médium-agnostique dans teach, anti-pattern code-spécifique dans dp-coach ; coach-pedagogique constaté déjà couvert (Step 2 + règle absolue), non modifié ; jamais en CLAUDE.md global (mode livraison préservé).
- **Critère de succès vérifiable** : au prochain /insights (≈2026-09-26), zéro interruption utilisateur pour exiger l'explication avant une écriture de fichier en session pédagogique sur la fenêtre analysée.
- **Date de revue** : 2026-09-26
- **Verdict (2026-09-26)** : ✅ atteint — rapport du 2026-09-26 (fenêtre 2026-08-07 → 2026-09-25, 39 sessions) : zéro interruption « expliquer avant d'écrire » sur les 15 sessions pédagogiques postérieures au fix du 02/09 ; les 2 occurrences de la fenêtre (`fc07542c` 06/08, `2e6a0487` 07/08) sont antérieures au fix. La catégorie a disparu des frictions du rapport.

---

## [INSIGHTS 2026-09-26] [VALIDÉ] check-before-delivery

- **Problème observé** : friction n°1 du rapport du 2026-09-26 en session pédagogique — 7 des 15 sessions `/teach` postérieures au fix du 02/09 ont un défaut de leçon attrapé par l'utilisateur en cours d'exercice ; 4 relèvent du contenu livré (comptes faux, terme non défini, warm-up mensonger, étape dépendant d'une étape ultérieure : `9a79e366`, `8d920214`, `19e58bbd`, `be6e19a6`).
- **Action engagée** : section « Check Before Delivery » dans `teach/SKILL.md` — relecture par checklist (ordre des dépendances, comptes, termes vs glossaire, promesses) après écriture et avant ouverture, sans exécution des commandes, avec une ligne de rapport visible `Checked: …` ; note de provenance amendée (sections de discipline de livraison distinguées des déviations de conception en ADR). Hors périmètre, explicitement : calibration des diagnostics (`8b7a0786`, `01c38a64`) et sorties de sous-agents non vérifiées (`6bb0255b`).
- **Critère de succès vérifiable** : au prochain /insights (≈2026-10-26), zéro session `/teach` de la fenêtre où l'utilisateur corrige lui-même un compte, un terme ou une dépendance d'étape dans une leçon livrée ; contrôle de non-vacuité : la ligne `Checked:` est présente dans les transcripts des leçons livrées et aucun `0 corrections` n'est contredit par une correction utilisateur sur la même leçon.
- **Date de revue** : 2026-10-26
- **Verdict (2026-10-26)** : ✅ atteint, **n = 1** — rapport du 2026-10-26 (fenêtre 2026-09-25 → 2026-10-26, 48 sessions) : une seule session `/teach` postérieure au fix (`2c16815c`, Go leçon 0001, 21/10), zéro correction utilisateur ; ligne `Checked: 9 steps, 11 terms — 4 corrections` présente et non contredite (trois termes glosés, référence de date remplacée, commande d'export Anki ajoutée, hash rendu générique). Réserve : la leçon n'avait pas encore été exercée (début fixé au 26/10) ; les autres sessions `/teach` des facets (3 → 20/09) sont antérieures au fix. **Reversement de la leçon « forme > prohibition » par `/immunize` reporté au cycle du 2026-11-26**, après deux ou trois leçons Go passées.

---

## [INSIGHTS 2026-10-26] attribution-setting

- **Problème observé** : trailer `Co-Authored-By` ajouté aux commits malgré la règle mémoire « No Co-Authored-By » — rejeté par Greg 2 fois dans la fenêtre (`48015dd2` 05/10 ; incident dotfiles du 11/10, amend + push forcé), 4 fois depuis septembre (`949d9450` 07/09, `f6285148` 22/09). Friction la plus répétée du rapport du 2026-10-26. Prose et mémoire ont échoué quatre fois : le harness injecte à chaque session une consigne d'attribution que le modèle suit par intermittence.
- **Action engagée** : `"attribution": false` dans `claude/settings.json` (→ `~/.claude/settings.json` par lien `install.sh`), clé documentée dans la référence des settings (≥ 2.1.281 ; installé 2.1.310) ; masque trailer de commit, pied de PR et lien de session. Vérification A/B le jour même en bac à sable (`claude -p`, repo temporaire, consigne sans mention d'attribution) : **A sans setting → `Co-Authored-By: Claude Fable 5.1` présent ; B avec setting → message nu.** Observé en prime : la consigne injectée dans la session courante a basculé à chaud en « do not add attribution lines », donc le setting agit sur l'instruction, pas seulement sur le texte écrit — point que la doc ne précise pas. Hook F1 (PreToolUse sur `Co-Authored-By`) non ajouté : deux mécanismes pour une règle.
- **Critère de succès vérifiable** : au prochain /insights (≈2026-11-26), zéro rejet par l'utilisateur d'un commit ou d'une PR pour trailer ou pied d'attribution dans les facets de la fenêtre ; contrôle de non-vacuité : `git log` des repos actifs montre des commits faits par Claude dans la fenêtre, aucun ne porte `Co-Authored-By` ni `Claude-Session`.
- **Date de revue** : 2026-11-26

---

## Ordre du jour reconduit (hors fiches)

Items dormants, event-driven ou reconduits de cycle en cycle. Déplacés ici
depuis `progress.md` le 2026-10-04 (dernier état complet : checkpoint du
2026-10-02 13:23, désormais dans `tasks/progress-archive.md`) — `progress.md`
ne les reporte plus par référence. Chaque item est daté ; en retirer un demande
un verdict, pas un oubli.

1. **Cycle /insights 2026-11-26** :
   - revue de la fiche `attribution-setting` (critère : zéro rejet de trailer,
     non-vacuité par `git log`) ;
   - **reverser la leçon « forme > prohibition »** par `/immunize "<leçon>"`
     (n = 2) — déclencheur : deux ou trois leçons Go exercées sans correction
     de compte / terme / dépendance (fiche `check-before-delivery`, ✅ n = 1
     le 26/10) ;
   - à ta main, inchangés : constats `TODO.md` 2-3 (deadlock `/pr` ↔ audit ;
     audit à re-scoper), `dmi: true` (R9/R10), S10 effort ; **constat 1
     (hook `/clear`) à fermer par renvoi** au déclencheur de la synthèse mods
     « 2ᵉ oubli de `/progress` avant `/clear` → mod `command.run` » ;
   - remesurer le ratio méta/produit (chantier mods ouvert → signal muet ;
     condition « sans chantier ouvert » conservée telle quelle le 26/10).
   - *Cycle 2026-10-26, fait* : `check-before-delivery` ✅ n = 1 ; §6 roadmap
     P4 archivé (T3 et ligne §3 alignées) ; `candide-*` → event-driven
     (reconduite deux fois sans déclencheur) et règle 7 actée à n = 1 ; ratio
     46 % des tokens de sortie ; **action unique S1** (`attribution: false`,
     fiche ci-dessus). Scorés et non retenus : B1 `/catchup` + issues GitHub
     (un événement par mois, impact 1, faisable en 5 min hors protocole), D
     ligne « positions d'UI » (redondante avec State Verification), G skill
     `/review-fix` et H rejeu d'evals headless (→ item 5), S6 (→ item 5),
     blocs prose Git / Dev / Config du rapport (déjà couverts). Règle « une
     seule action » contestée (trois candidats à coût 1) puis **confirmée** :
     les candidats ne tenaient pas au scoring ; amendement « une
     comportementale + une mécanique vérifiable le jour même » formulé, non
     adopté faute de cas.
2. **R10 à arbitrer avant exécution** (`disallowed-tools` sur `grill` et
   `code-review` ; toucher `grill.md` pourrait armer R9).
3. **Chantier evals, Phase 4** (event-driven) : R8 au D5 ; R9 sous-ensembles
   mono-tour ; R10.
4. **P5 verification-skills** (dormant) : ne reste que « projet concret à
   surface lançable » — l'agent dbt en est un candidat.
5. Event-driven : réponse vide Step 0 ; paire `candide-*` (si elle redevient
   flaky : réécriture en rubriques binaires, ~1,7 $, seule à porter
   l'hypothèse « rubriques longues ↔ paire flaky » — retirée de l'agenda
   reconduit le 2026-10-26) ; **G** skill `/review-fix` (si la boucle
   revue → triage → fix test-first → merge doit être ré-expliquée une fois de
   plus malgré `/code-review` + rituel + « un finding par tour » ; coût 3,
   corpus d'eval obligatoire) ; **H** rejeu d'evals en `claude -p` (à la
   prochaine session d'amélioration de skill où le rejeu charge le contexte
   principal) ; **S6** hook `ruff format` (si un pre-commit de format aborte à
   nouveau un commit) ; diagnosing-bugs ;
   T2 ; échec de permissions d'un sous-agent d'exploration (`f6285148`) ;
   P4 se rouvre à la première occurrence observée de name-dropping de
   principe ; « gel des déclencheurs » passe en promotion projet à une
   seconde occurrence (formulation dans `tasks/lessons-archive.md`) ;
   **dbt (2026-10-04)** : 9ᵉ outil `dbt_docs_generate`, exposer « modèle
   construit ou non », T20 à la première exécution concurrente, **premier vrai
   test du subagent (reporté le 2026-10-08, pas de projet tangible —
   déclencheur : un projet dbt réel)** et révision de l'effort à ce moment-là
   (la précondition `./install.sh` est acquise, vérifiée le 2026-10-08) ;
   faiblesses de
   `block-force-push.sh` (mot « force » non ancré) et `block-rm-rf.sh`
   (bloque `rm -f` sur un fichier unique).
6. Hors repo, à la main de Greg : pin `known-first-party` ; learning record
   `0004`.
7. Revisites : Pocock ~2026-11/12 ; pstack ~2026-12/2027-01.

---

## Métriques de cycle

Ratio méta/produit (P3, défini au cycle 2026-09-26) : part des sessions
analysées dont le `project_path` est un workspace d'outillage (`dotfiles`,
`learning-to-build-skills`, `claude-audit-notes`) — source
`~/.claude/usage-data/session-meta/`, deux lectures (sessions, tokens de
sortie). Pas de seuil ; signal = ratio qui ne baisse pas alors qu'aucun
chantier méta n'est ouvert (> 1/3 deux cycles de suite).

| Cycle | Fenêtre | Méta (sessions) | Méta (tokens sortie) | Chantier méta ouvert |
|---|---|:---:|:---:|---|
| 2026-09-26 | 60 sessions depuis le 31/07 | 19/60 = 32 % | 4,55 M / 16,29 M = 28 % | oui — evals Phases 1-3, 3 revues de repos, roadmap (baseline = plafond de période active) |
| 2026-10-26 | 64 sessions depuis le 25/09 (48 analysées) | 23/64 = 36 % (21/48 = 44 % sur les analysées) | 5,74 M / 12,40 M = 46 % | oui — tech-watch Phases 0-3 + serveur MCP Cloud Run (26/09 → 12/10), outillage dbt (02 → 04/10), étude des mods (13-14/10), context-ledger déclaré ouvert le 14/10. Lecture : les 16 sessions `dbt-agent-testbed` sont des micro-tests de délégation (3-8 messages, 0,02 M tokens) qui gonflent le compte produit ; la lecture en tokens est la fiable. Signal « > 1/3 sans chantier ouvert » muet, car un chantier méta a été ouvert à chaque cycle. |

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

## [INSIGHTS 2026-09-26] check-before-delivery

- **Problème observé** : friction n°1 du rapport du 2026-09-26 en session pédagogique — 7 des 15 sessions `/teach` postérieures au fix du 02/09 ont un défaut de leçon attrapé par l'utilisateur en cours d'exercice ; 4 relèvent du contenu livré (comptes faux, terme non défini, warm-up mensonger, étape dépendant d'une étape ultérieure : `9a79e366`, `8d920214`, `19e58bbd`, `be6e19a6`).
- **Action engagée** : section « Check Before Delivery » dans `teach/SKILL.md` — relecture par checklist (ordre des dépendances, comptes, termes vs glossaire, promesses) après écriture et avant ouverture, sans exécution des commandes, avec une ligne de rapport visible `Checked: …` ; note de provenance amendée (sections de discipline de livraison distinguées des déviations de conception en ADR). Hors périmètre, explicitement : calibration des diagnostics (`8b7a0786`, `01c38a64`) et sorties de sous-agents non vérifiées (`6bb0255b`).
- **Critère de succès vérifiable** : au prochain /insights (≈2026-10-26), zéro session `/teach` de la fenêtre où l'utilisateur corrige lui-même un compte, un terme ou une dépendance d'étape dans une leçon livrée ; contrôle de non-vacuité : la ligne `Checked:` est présente dans les transcripts des leçons livrées et aucun `0 corrections` n'est contredit par une correction utilisateur sur la même leçon.
- **Date de revue** : 2026-10-26

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

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

## [INSIGHTS 2026-07-26] scope-discipline

- **Problème observé** : friction n°1 du rapport 2026-07-26 — au moins 6 interruptions utilisateur pendant la reconnaissance initiale (sweeps Bash parallèles, sur-exploration), dont 1 session `not_achieved`.
- **Action engagée** : ajout d'une section `## Scope Discipline` au CLAUDE.md global — sur session de reprise, lire les fichiers de contexte au lieu d'explorer ; toute recon multi-fichiers passe par un plan d'une ligne validé.
- **Critère de succès vérifiable** : au prochain /insights (≈2026-08-26), zéro interruption utilisateur pendant une phase de reconnaissance sur la fenêtre analysée.
- **Date de revue** : 2026-08-26

# Lessons Inbox

Réponse innée du cycle immunitaire — leçons brutes datées uniquement
(mono-population : les fiches `[INSIGHTS]` vivent dans `insights-actions.md`).
Ajout : `/immunize "<leçon>"`. Triage : `/immunize` sans argument :

- Leçon incriminant un artefact versionné → fix test-first + non-régression au corpus de l'artefact (jamais de règle prose)
- Comportement de session récurrent (2+) → règle projet (`## Do NOT`) ; portée générique → porte d'eval avant tout `## Global Do NOT`
- Entrée unique > 7 jours → archivage ; ≤ 7 jours → conservation

---

*Dernière consolidation : 2026-09-23, second triage (2 conservées, 0 archivée : deux groupes distincts à n = 1 — levier de forme sur un invariant de skill, rubrique binaire pour le juge sans raisonnement ; fixes déjà commités sur leurs artefacts, seconde occurrence attendue, expiration sans confirmation au triage suivant le 2026-09-30). Triage précédent le même jour : 4 archivées (1 unique expirée — ruff ; 3 routées artefact — corpus feynman-mentor, Phase 2 / ADR-0016). Voir `lessons-archive.md`.*

- [2026-09-23] Sur un comportement probabiliste d'une skill (candide feynman-mentor : ne jamais décoder un terme de domaine), deux itérations de prohibitions en prose (« never decode… », « a guess dressed as a question is still a guess ») n'ont rien tenu : ~1 fuite sur 3 runs sur les deux tiers. Une contrainte de forme — phrase gabarit pour le jargon + étape d'auto-vérification « Check Before Sending » à 3 tests mécaniques — a éliminé la classe de fuite visée sur 12 runs (Fable 2/6 → 5/6 runs parfaits). Les gris résiduels ont changé de nature (variance actée, règle d'arrêt). C'est la règle 4 du guide Opus 5 (scaffolding d'auto-vérification, audit 2026-08-07) avec une première preuve chiffrée. Source : claude/evals/feynman-mentor README § État passe 4, commits 767c8a4 et 550ac20, 2026-09-23.
- [2026-09-23] Rubrique de juge llm = « PASS si / FAIL seulement si » + non-violations explicites, car le juge du runner ne raisonne pas (réponse en un mot). Preuve : corpus claude-md-skill, 2026-09-23, rubrique v1 à 4 clauses conjonctives → 9/9 FAIL sur un comportement conforme ; scindée en 2 graders courts → 18/18 PASS à comportement constant. n = 1 corpus.
- [2026-09-23] Citer un principe (Karpathy ou autre) = nommer la décision qu'il a changée ; une citation sans décision derrière est du name-dropping. Emprunt pstack P4 (revue 2026-09-12, roadmap §3.B, validée 2026-09-23), versé au circuit normal des leçons comme prescrit — aucune occurrence observée en session (n = 0, candidate d'emprunt, pas leçon d'incident). Destination probable : docs/methodology/karpathy-discipline.md (artefact) ; porte d'eval seulement si la formulation devait devenir globale.

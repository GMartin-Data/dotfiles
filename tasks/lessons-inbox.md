# Lessons Inbox

Réponse innée du cycle immunitaire — leçons brutes datées uniquement
(mono-population : les fiches `[INSIGHTS]` vivent dans `insights-actions.md`).
Ajout : `/immunize "<leçon>"`. Triage : `/immunize` sans argument :

- Leçon incriminant un artefact versionné → fix test-first + non-régression au corpus de l'artefact (jamais de règle prose)
- Comportement de session récurrent (2+) → règle projet (`## Do NOT`) ; portée générique → porte d'eval avant tout `## Global Do NOT`
- Entrée unique > 7 jours → archivage ; ≤ 7 jours → conservation

---

*Dernière consolidation : 2026-09-23 (4 entrées archivées : 1 unique expirée — ruff, hook hors de cause ; 3 routées artefact — corpus feynman-mentor, fix = Phase 2 du chantier evals / ADR-0016, traces dans les notes d'archivage). Voir `lessons-archive.md`.*

- [2026-09-23] Sur un comportement probabiliste d'une skill (candide feynman-mentor : ne jamais décoder un terme de domaine), deux itérations de prohibitions en prose (« never decode… », « a guess dressed as a question is still a guess ») n'ont rien tenu : ~1 fuite sur 3 runs sur les deux tiers. Une contrainte de forme — phrase gabarit pour le jargon + étape d'auto-vérification « Check Before Sending » à 3 tests mécaniques — a éliminé la classe de fuite visée sur 12 runs (Fable 2/6 → 5/6 runs parfaits). Les gris résiduels ont changé de nature (variance actée, règle d'arrêt). C'est la règle 4 du guide Opus 5 (scaffolding d'auto-vérification, audit 2026-08-07) avec une première preuve chiffrée. Source : claude/evals/feynman-mentor README § État passe 4, commits 767c8a4 et 550ac20, 2026-09-23.

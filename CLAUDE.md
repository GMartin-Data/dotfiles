# CLAUDE.md — projet `dotfiles`

> **Désambiguïsation.** Ce fichier (`~/dotfiles/CLAUDE.md`) régit le travail *dans*
> ce repo. À ne pas confondre avec `claude/CLAUDE.md`, qui est le **payload** du
> CLAUDE.md global (synchronisé vers `~/.claude/CLAUDE.md` et lu dans tous les
> autres projets). Ce fichier-ci ne s'applique que lorsque le CWD est `~/dotfiles`.

## Version Control — exemption direct-sur-main

- **Commits directs sur `main` autorisés, sans branche ni PR.** Exemption à la
  règle globale « feature/fix branch → PR → main » (cf. `claude/CLAUDE.md`,
  section Version Control, qui prévoit cette déclaration au niveau projet).
- **Justification** : repo de configuration personnelle, mono-utilisateur, sans CI
  ni revue tierce. Une PR auto-mergée n'apporte aucune revue réelle ; la friction
  l'emporte sur le bénéfice. Le garde-fou contre les changements risqués est le
  **rituel d'evals** (test-first sur les slash-commands), pas la topologie git.
  Tout commit reste réversible par `git revert`.
- **Brancher reste possible ad hoc** pour un changement réellement risqué
  (expérimentation pouvant casser le shell, migration de structure) — au cas par
  cas, à l'initiative de l'humain, jamais imposé par défaut.

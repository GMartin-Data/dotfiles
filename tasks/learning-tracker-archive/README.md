# Archive — état `learning-tracker` (outil supprimé)

Ce dossier conserve l'état du subagent `learning-tracker`, **supprimé** le
2026-06-23 lors de la refonte de la couche learning autour de la skill `teach`
(cf. [`adr/0007`](../../adr/0007-teach-emplacement-frontieres.md)).

## Pourquoi c'est archivé et non supprimé

L'ADR-0007 prévoyait de supprimer l'état avec l'outil (la couche learning était
réputée « sans usage réel »). À l'exécution, `MEMORY.md` s'est révélé contenir un
**suivi actif** (`methodology-trial` : prochaine étape concrète + branches
ouvertes) qui contredisait cette prémisse. Décision prise de **préserver
l'historique hors du système learning** plutôt que de le détruire, le temps de le
trier.

## Contenu

- `MEMORY.md` — méta-compteurs + sujet actif `methodology-trial` + 4 sujets
  archivés (trace courte).
- `completed-topics.md` — narratif long des sujets archivés (dotfiles-audit,
  shanraisshan-exploration, mcp-server-mastery, claude-code-sandboxing).

## À trier (TODO)

- `methodology-trial` (sujet ACTIF) : sa « prochaine étape » (`/claude-md` sur
  memory-grep + Phase 1a) et ses branches ouvertes (étapes 2-4, inbox dotfiles)
  doivent rejoindre un suivi vivant approprié (progress.md du projet concerné, ou
  un learning-record si l'apprentissage en est l'angle). Ne pas laisser ce fil se
  perdre.
- Sujets archivés : valeur purement historique. Peuvent rester ici tels quels ou
  être purgés une fois `methodology-trial` re-routé.

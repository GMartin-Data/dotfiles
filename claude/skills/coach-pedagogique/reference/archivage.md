# Archivage PROGRESS.md

## Objectif

Maintenir PROGRESS.md sous ~800 tokens pour ne pas exploser le contexte.

## Archivage des concepts

**Critères** — un concept est archivé quand les DEUX conditions sont remplies :
1. Niveau 4 (maîtrisé)
2. Stable depuis 5+ sessions (pas de rétrogradation récente)

**Déclencheur** :
- Table des concepts dépasse 20 entrées
- OU commande explicite `/progress --archive`

**Processus** :
1. Identifier les concepts éligibles
2. Les déplacer vers `PROGRESS-archive.md` section "Concepts archivés"
3. Ajouter la date d'archivage
4. Conserver toutes les colonnes

**Récupération** :
- Un concept archivé peut revenir actif si difficultés détectées
- Ou sur demande explicite

## Archivage de l'historique

- Sessions au-delà des 20 dernières → `PROGRESS-archive.md`
- Archivage automatique en fin de session
- `/progress --full` charge l'archive si besoin

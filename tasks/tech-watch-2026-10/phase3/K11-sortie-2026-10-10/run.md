# K11 — slug, langue, emplacement, livraison — E1 + E7a, 2026-10-10

Item K11 (`handover.md` §7) : pas de règle de slug pour `{query}`, pas de
langue de rapport, pas d'emplacement ni de livraison. Critère (§7) : deux
exécutions sur la même requête produisent le même nom de fichier.

## Constat avant la règle **[Observé]** (30 sandboxes d'evals)

- `/tech-watch Claude Mods` a produit `tech-watch-claude-mods-…` 6 fois (dont
  le run K3) et `tech-watch-claude-code-mods-…` 6 fois : le nom suivait tantôt
  la demande brute, tantôt le sujet normalisé de l'étape 1. Critère non rempli.
- Le run E4 à 60 jours portait le même nom que le run à 30 jours (collision).
- Rapport en anglais sur tous les runs, demande en français comprise (E7a) ;
  réponse de chat en français (héritée du `CLAUDE.md` global). Rien ne le
  prescrivait.
- Rapport à la racine du CWD ; en usage réel, la racine du dépôt courant.
  L'ancien trio écrivait ses intermédiaires dans `tech-watch/` sous le CWD et
  n'écrivait pas de rapport.

## Règles (validées par Greg, deux décisions : langue, puis emplacement)

- **Slug** (`SKILL.md` étape 1) : dérivé du sujet normalisé, jamais de la
  demande : minuscules, ASCII, toute suite non alphanumérique → un tiret.
- **Nom** (étape 10, gabarit) : `tech-watch-{slug}-{YYYY-MM-DD}.md` ; `-{days}d`
  avant la date si la fenêtre n'est pas 30 ; même nom le même jour = remplace.
- **Langue** (étape 10, agent) : rapport **en anglais fixe**, résumé de chat
  dans la langue de la demande. Alternative écartée : rapport dans la langue de
  la demande (gabarit et statuts à traduire, citations mélangées).
- **Emplacement** (agent) : dossier fixe `/home/martin/tech-watch/`, créé si
  absent, sauf chemin donné dans la demande. Alternatives écartées :
  `./tech-watch/` sous le CWD (dossier non suivi dans chaque dépôt), racine du
  CWD (statu quo). Chemin littéral, pas `~` : l'agent n'a pas `Bash` et ne
  connaît pas `$HOME` ; repo mono-utilisateur.
- **Livraison** (agent) : première ligne de la réponse à format fixe
  `Report: <chemin absolu> — n ranked + m primary — normal | degraded: <outils>`.

Montage : `run-eval.sh` réécrit le dossier fixe en `cwd/tech-watch/` du sandbox
dans la copie de l'agent (`sed`), sans le pré-créer, pour tester la création à
chaque run. Même substitution appliquée à la fixture E3 (corps identique à
l'agent).

## Résultats **[Observé]** — E1 et E7a en parallèle, montage fork, Opus, serveur `00009`

| Mesure | E1 `/tech-watch Claude Mods` | E7a `Fais-moi une veille sur les mods de Claude Code` |
|---|---|---|
| Fichier | `cwd/tech-watch/tech-watch-claude-code-mods-2026-10-10.md` | **identique** |
| Dossier `tech-watch/` | absent avant le run, créé par `Write` (aucun `Bash`) | idem |
| Langue du rapport | anglais | anglais (sections, résumé, synthèses) ; titre `# Tech Watch — mods de Claude Code`, car le gabarit mettait `{query}` dans le titre |
| Première ligne de chat | `Report: /tmp/…/cwd/tech-watch/tech-watch-claude-code-mods-2026-10-10.md — 20 ranked + 3 primary — normal`, puis résumé en français | Le fork a bien produit la ligne `Report: …` (visible dans le résultat d'outil), mais la **session principale** l'a paraphrasée : « La veille est faite : 20 sources classées + 3 sources primaires, rapport dans `tech-watch/…` » (chemin relatif) |
| En-tête K3, pied de page | tableau rempli, `Sources used: GitHub · YouTube · Web (Tier 2) · Owner domains` | idem (non-régression K3) |
| Tours / durée / coût | 0 tour principal, 220 s, 0,82 $ | 2 tours principaux (Skill → fork → paraphrase), 241 s, 1,00 $ |

**Verdict** : critère K11 **rempli** (même nom sur deux formulations, anglaise
et française, de la même demande). Langue et emplacement conformes. Livraison
**partielle** : la ligne fixe sort telle quelle quand la skill est invoquée
directement (`/tech-watch`), et sert de matière à la session principale quand
la skill est déclenchée en langage naturel, qui la reformule (chemin relatif,
comptes conservés). C'est le fonctionnement du fork, pas un défaut de règle ;
à consigner dans les limitations (K1).

## Correctif pris après les runs (signalé, non rejoué)

Titre du gabarit : `# Tech Watch — {normalized topic}` au lieu de `{query}`,
la demande telle que tapée passe dans la ligne de métadonnées (`Request`,
avec `Owner`). Le titre devient anglais et stable (`Claude Code mods` pour les
deux formulations) ; le reste du rapport était déjà conforme.

## À reporter

- **Phase 4** : en session interactive, `Write` hors du CWD demandera une
  permission ; prévoir une règle `Write(/home/martin/tech-watch/**)` ou
  `--add-dir` dans la configuration livrée (`install.sh`, README).
- **K1** : paraphrase de la ligne de livraison par la session principale sous
  déclenchement en langage naturel.
- Reste la ligne `**Request**` du gabarit à observer sur le prochain run (K1
  ou rejeu final).

Transcripts : `claude/evals/results/tech-watch-{e1,e7a}-k11-2026-10-10/`
(gitignorés). Rapports copiés ici, préfixés `E1-` / `E7a-` (même nom sinon).

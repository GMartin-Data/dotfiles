# ADR-0010 : Surcharge user-scope de `/code-review` adaptée à mon workflow

Status: Accepted
Date: 2026-06-25

## Contexte

La skill bundled `/code-review` (v2.1.191) signale bugs + nettoyages sur le diff,
mais ignore mes conventions (structlog, pathlib, type hints publics, Kimball /
`ref()`, variables Terraform), ma posture sécurité, et surtout ne sait pas que mes
hooks couvrent déjà le lint (`ruff-check` PostToolUse) ni que certaines de mes
« complexités » sont délibérées (fail-closed, validation redondante à source
unique — cf. `claude/hooks/protect_env.py`). Une revue nue produit donc du bruit
(redondance hooks) et des faux positifs structurels.

Vérifié dans la doc (commands reference + skills reference, v2.1.191) : une skill
user-scope de même nom **surcharge** la bundled ; sur collision skill/command, la
skill l'emporte. La signature réelle est
`/code-review [low|medium|high|xhigh|max|ultra] [--fix] [--comment] [target]` —
**par défaut elle signale**, `--fix` est requis pour appliquer. Depuis v2.1.154,
`/simplify` est la command séparée nettoyage-seul-avec-fix.

## Options considérées

- **Option A — Built-in nue + CLAUDE.md élargi** : pousser mes règles dans
  CLAUDE.md, garder la skill nue.
  - Inconvénient : gonfle un fichier « stable / faits » avec une procédure de
    revue (viole la matrice de responsabilité — CLAUDE.md ne contient pas de
    procédure), et ne résout ni la redondance hooks ni les faux positifs
    structurels.

- **Option B — Skill user-scope surchargée (retenue)** :
  `~/.claude/skills/code-review/SKILL.md` (symlinké depuis `~/dotfiles/claude/skills/`),
  encode conventions + frontière hooks/simplify + reconnaissance complexité
  délibérée + ledger. Le mécanisme ledger→`/adr` reproduit le pattern `/grill` :
  **délégation par instruction**, jamais invocation.
  - Avantage : surcharge le réflexe `/code-review` sans doublon, isole la
    procédure hors de CLAUDE.md, et aligne la frontière sur l'écosystème existant.

- **Option C — Nouvelle command à nom distinct** (`/review-greg`) : évite la
  surcharge mais laisse la bundled accessible en doublon.
  - Inconvénient : deux portes pour un même geste ; perd le réflexe `/code-review`.

## Décision

Option B. Skill prompt-based user-scope qui **signale uniquement** (jamais
`--fix` : un finding nettoyable renvoie vers `/simplify`, qui seul applique).
Effort par défaut `high`, override par argument conservé. Frontière explicite :
ne re-signale pas ce que `ruff` couvre (style / lint / format / imports
inutilisés) ; cible la correction, la sécurité (injection, secrets en clair,
bypass auth), les invariants métier, et mes conventions. Reconnaît mes patterns de
complexité délibérée (fail-closed, validation redondante à source unique) pour ne
pas les signaler comme code mort ou complexité inutile.

Produit un **ledger structuré** (sévérité · fichier:ligne · catégorie). Un finding
révélant un trade-off non-trivial (ex : un secret en clair assumé, un fail-closed à
acter) est tagué `(ADR)`, rendu **autoportant** (contexte / options / décision
résumés, collables dans une session `/adr` vierge), et clos par une **invite isolée
et visible** instruisant l'humain de lancer `/adr --from-context`. Conformément à
l'[ADR-0003](0003-grill-delegue-adr-sans-invoquer.md), la skill **n'invoque jamais**
`/adr` — une slash-command ne pilote pas une autre ; le chaînage reste un acte
humain.

## Conséquences

- Première passe en amont de la revue humaine, **jamais un quitus**. Un
  `/code-review` vert ne dispense pas de la revue humaine réelle.
- Rôles disjoints, zéro overlap : **hooks** (lint / sécurité runtime, automatique)
  · **`/code-review`** (signale) · **`/simplify`** (applique le nettoyage).
  Cohérent avec la matrice de responsabilité.
- Frontière hooks / simplify **dupliquée** dans le prompt de la skill → à garder en
  sync si les hooks bougent (trade-off accepté : autonomie du prompt vs source
  unique, cf. CLAUDE.md §Documentary Methodology).
- Reconnaissance de la complexité délibérée → réduit les faux positifs structurels,
  au prix d'un risque de faux négatif (un vrai défaut maquillé en « intentionnel »)
  assumé pour une première passe.
- Le mécanisme ledger→`/adr` applique le précédent de l'[ADR-0003](0003-grill-delegue-adr-sans-invoquer.md)
  (pas d'auto-invocation inter-command) à la famille des commands de revue, pas
  seulement méthodologiques. Prolonge l'écosystème `/grill`→`/adr`.

# Essai — skill `diagnosing-bugs` (mattpocock/skills)

> Créé : 2026-09-11. Source : revue complète du repo
> (`tasks/mattpocock-skills-review-2026-09.md`, §6, candidat n°1).
> Upstream : `mattpocock/skills@3cca18b` (v1.2.3),
> `skills/engineering/diagnosing-bugs/`.
> Protocole : style spike — critères de décision fixés AVANT le premier
> essai, observation qui tranche, décision actée par `/adr --from-context`.
> Statut : **plan validé, Phase 0 non exécutée.**

---

## Phase 0 — Installation (une fois, ~15 min, réversible)

1. Copier `skills/engineering/diagnosing-bugs/` depuis le repo upstream vers
   `claude/skills/diagnosing-bugs/` (re-cloner si le clone de scratchpad a
   expiré : `git clone https://github.com/mattpocock/skills`, checkout
   `3cca18b` pour coller à la version revue). Garder le nom upstream — il
   permet de diff les mises à jour futures ; renommage éventuel (`/debug`)
   seulement à la promotion. Supprimer `agents/openai.yaml` (métadonnées
   Codex, inutiles). Conserver `scripts/hitl-loop.template.sh`.
2. Frontmatter : ajouter `disable-model-invocation: true` et raccourcir la
   description en une ligne human-facing. Invocation délibérée uniquement
   pendant l'essai — zéro charge de contexte, pas de sur-déclenchement sur
   les bugs triviaux (le trigger upstream « reports something
   broken/throwing/failing/slow » sur-inclut), cohérent avec « l'humain est
   l'index ». La question model-invoked est reportée à la décision finale.
3. Symlink `~/.claude/skills/diagnosing-bugs` →
   `~/dotfiles/claude/skills/diagnosing-bugs` (même mécanisme que les skills
   existantes).
4. Commit atomique :
   `feat(claude): add diagnosing-bugs skill (trial, from mattpocock/skills@3cca18b)`.
5. **Pas d'eval à ce stade** — volontaire : l'essai juge le protocole
   upstream quasi tel quel ; écrire des evals avant de savoir si on garde
   serait du coût à fonds perdus. Le rituel ADR-0009 ne s'applique qu'à la
   promotion.

## Phase 1 — Essai (event-driven, N=3 bugs réels, pas de deadline)

**Déclencheur d'un essai** : un bug qui résiste au premier coup d'œil, ou
une régression de perf, sur n'importe quel projet réel. Test d'entrée :
*si la première impulsion est de lire le code pour théoriser, c'est un
candidat.* Les fixes une-ligne ne comptent pas.

Pendant l'essai, la discipline s'applique telle quelle, y compris son droit
de sauter des phases explicitement justifié. Après chaque essai, remplir la
grille dans le [log](#log-des-essais) ci-dessous.

**Grille d'observation** (par bug, binaire) :

| # | Observation | Mesure |
|---|---|---|
| 1 | Porte respectée : une commande red-capable a tourné avant toute hypothèse | O/N |
| 2 | La boucle a infirmé la première intuition (l'hypothèse gagnante n'est pas celle qui aurait été testée en premier sans le protocole) | O/N |
| 3 | Protocole tenu jusqu'au bout (abandon en route = signal fort) | O/N |
| 4 | Ressenti « théâtre » : la construction de la boucle a dominé le temps total sans payer | O/N |
| 5 | Cleanup Phase 6 réellement exécuté (grep des tags `[DEBUG-…]`) | O/N |

**Point de vigilance** : la Phase 5 du skill (test de régression avant fix)
est déjà couverte par la règle test-first Karpathy — le neuf est dans les
Phases 1–4 (porte red-capable, minimisation, hypothèses falsifiables,
instrumentation taguée). C'est là que la grille doit regarder.

## Phase 2 — Décision (après le 3e essai, ou immédiatement après 2 abandons)

Critères fixés le 2026-09-11, avant le premier essai :

- **Adopter** si : porte respectée 3/3 **et** ≥1/3 où la boucle a changé le
  diagnostic (ligne 2) **et** zéro « théâtre » (ligne 4).
- **Rejeter** si : ≥2 abandons (ligne 3) **ou** 3/3 « théâtre ».
- **Zone grise → adapter.** Repli naturel : ne garder que la Phase 1 (porte
  red-capable) + les hypothèses falsifiables comme **règle CLAUDE.md**, sans
  skill — si le seul apport observé est la porte, une règle coûte moins à
  maintenir qu'une skill.

Acter la décision par `/adr --from-context`.

- **Si adoption** : rituel eval ADR-0009 (fixture : bug jouet
  reproductible ; l'eval vérifie que le modèle *refuse* de théoriser sans
  commande rouge), décision user/model-invoked définitive, renommage
  éventuel, inscription dans la gouvernance.
- **Si rejet** : suppression du dossier + du symlink, leçon via `/immunize`.
  Évaluer alors si la porte red-capable mérite de survivre seule comme
  doctrine.

## Log des essais

<!-- Une entrée par bug : date, projet, une ligne de contexte, grille 1-5,
     3 lignes max de commentaire. -->

*(aucun essai pour l'instant)*

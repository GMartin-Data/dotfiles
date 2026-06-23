# ADR-0004 : `reference/` en Markdown, `lessons/` en HTML dans le workspace `teach`

Status: Accepted
Date: 2026-06-23

## Contexte

La refonte de la couche learning adopte la skill `teach` de Matt Pocock comme
colonne vertébrale stateful (cf. [ADR-0007](0007-teach-emplacement-frontieres.md)
pour le motif d'ensemble). Le design original de `teach` prescrit que **deux**
familles d'artefacts du workspace soient en HTML :

- `./lessons/*.html` — l'unité de production : une leçon = un HTML auto-contenu,
  tightly-scoped, « beautiful / Tufte », rarement revisitée.
- `./reference/*.html` — l'essence compressée et **revisitée** (cheat sheets,
  glossaires, algorithmes de référence), conçue pour la consultation rapide.

Or mon écosystème documentaire repose sur une chaîne Markdown / Obsidian / PKM :
grep, liens inter-documents, détection de drift, gouvernance par la
[matrice de responsabilité](../docs/methodology/responsibility-matrix.md). Un
artefact *revisité* qui vit en HTML est hors de cette chaîne : non-greppable
utilement, non-liable depuis le reste du PKM, invisible à la détection de drift.

La tension n'est pas symétrique entre les deux familles :
- Une **leçon** est éphémère et consommée *dans le navigateur*. Son interactivité
  (quiz, anchors, mise en page Tufte) est exactement ce que le HTML sert bien.
  Elle n'est presque jamais relue, donc son absence de la chaîne PKM ne coûte rien.
- Une **reference** est par définition relue, citée, mise à jour. C'est le profil
  d'un document de connaissance durable — le cœur de cible du PKM Markdown.

## Options considérées

- **Option A — Tout HTML (design Pocock à l'identique)** : `lessons/` ET
  `reference/` en HTML.
  - Avantage : fidélité totale au design source, une seule techno de rendu,
    references aussi « belles » que les leçons.
  - Inconvénient : sort les references — les artefacts *revisités* — de la chaîne
    Markdown/PKM. Perte de grep, de liens inter-docs, de détection de drift sur
    précisément les documents qui en bénéficieraient le plus.

- **Option B — Tout Markdown** : `lessons/` ET `reference/` en Markdown.
  - Avantage : tout dans la chaîne PKM, cohérence maximale.
  - Inconvénient : sacrifie l'interactivité et l'engagement des leçons (quiz
    in-browser, anchors, rendu Tufte). Le HTML y est un atout réel, pas un caprice.
    Uniformiser vers le bas.

- **Option C — `lessons/` HTML, `reference/` Markdown (retenue)** : chaque famille
  dans la techno qui sert son cycle de vie réel.
  - Avantage : les leçons gardent leur interactivité ; les references rejoignent
    la chaîne PKM (grep, liens, drift). L'écart au design Pocock est ciblé et
    motivé par une collision réelle avec mon écosystème, pas esthétique.
  - Inconvénient : deux technos de rendu dans un même workspace ; un lien
    leçon→reference traverse une frontière HTML→Markdown.

## Décision

Option C. Dans le workspace `teach` :

- **`lessons/*.html` restent en HTML** — éphémères, interactifs, Tufte, ouverts
  dans le navigateur. Le design Pocock est conservé tel quel pour cette famille.
- **`reference/*.md` passent en Markdown** — revisités, ils vivent dans la chaîne
  Markdown/Obsidian/PKM (grep, liens, détection de drift).

C'est le **seul** écart au design de Pocock que je défends activement. Il est
justifié par le critère de la matrice de responsabilité : un artefact revisité et
mis à jour doit être dans la source de vérité unique adaptée à son cycle de vie.

Le `GLOSSARY.md` de Pocock (déjà Markdown dans son design) reste Markdown — il
relève naturellement de la famille reference et confirme la cohérence du choix.

## Conséquences

- Le `SKILL.md` adapté de `teach` doit décrire `reference/*.md` (et non `.html`)
  et ajuster les passages qui supposent un rendu HTML des references.
- Un lien depuis une leçon HTML vers une reference Markdown ne sera pas un simple
  anchor HTML ; c'est un trade-off accepté (la leçon pointe vers un `.md` du PKM).
- Les references entrent dans le périmètre de grep / liens / drift-detection de
  l'écosystème dotfiles — bénéfice principal recherché.
- Trade-off accepté : deux technos de rendu coexistent dans le workspace. Jugé
  acceptable car la frontière épouse une vraie différence de cycle de vie
  (éphémère vs revisité), pas une commodité d'implémentation.
- Cet ADR `Refines` [ADR-0007](0007-teach-emplacement-frontieres.md) : il précise
  un point de design du workspace dont 0007 pose le cadre général.

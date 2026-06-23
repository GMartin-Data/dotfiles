# ADR-0005 : Rétention unifiée via Anki (le storage strength ne passe pas par les quiz HTML)

Status: Accepted
Date: 2026-06-23

## Contexte

La pédagogie de Pocock — conservée intacte comme cœur de valeur — distingue
**fluency strength** (récupération immédiate, illusoire) de **storage strength**
(rétention long terme, le vrai but). Elle prescrit trois leviers de difficulté
désirable pour bâtir le storage : retrieval practice, **spacing**, interleaving.

Mais le *mécanisme* que `teach` propose pour la rétention est le **quiz HTML
in-lesson** : éphémère, joué une fois dans la leçon, **non-spaced**. Il y a là une
contradiction interne au design source : il revendique le spacing comme levier
central du storage strength, mais son outil de rétention ne spacé rien — la leçon
est « rarely revisited » de l'aveu même du SKILL.md.

Mon existant porte déjà la réponse à ce manque. La skill `code-mentor` produit des
**flashcards Anki** en fin de session, via :
- `claude/skills/code-mentor/scripts/anki-export.py` — export par AnkiConnect
  (localhost:8765), modèles Basic et Cloze, dédup, deck par défaut « Code-Mentor ».
- `claude/skills/code-mentor/templates/flashcards-format.md` — format JSON des
  cartes (types basic/cloze/trace/missing) et règles de rédaction par type.

Anki *est* le moteur de répétition espacée mûr (SM-2/FSRS) que `teach` réclame
sans l'avoir. C'est le point précis où mon existant est démontré **supérieur** à
Pocock. Le sens du tuning s'y inverse : ce n'est pas `teach` qui remplace mon
mécanisme, c'est mon mécanisme qui doit remplacer le sien sur l'axe storage.

Garde-fou (cf. handoff) : « tuner » = écart minimal motivé par une collision
réelle, jamais une amélioration esthétique. Ici la collision est réelle (deux
mécanismes de rétention parallèles, l'un spacé l'autre non) et l'arbitrage est
adossé à la propre pédagogie de Pocock.

## Options considérées

- **Option A — Garder les quiz HTML de `teach` pour tout** : statu quo du design
  source.
  - Avantage : zéro tuning, fidélité totale.
  - Inconvénient : aucun spacing réel → ne sert que la fluency, jamais le storage,
    en contradiction avec la pédagogie revendiquée. Laisse deux systèmes de
    rétention concurrents (Anki côté code-mentor, quiz côté teach) = drift.

- **Option B — Deux mécanismes selon l'outil** : `teach` garde ses quiz, code-mentor
  garde Anki, chacun sa rétention.
  - Avantage : aucun travail d'intégration.
  - Inconvénient : viole la source-de-vérité unique. Deux espaces de rétention
    désynchronisés ; impossible de réviser « tout ce que j'apprends » en un lieu.

- **Option C — Convergence vers Anki comme moteur de storage unique (retenue)** :
  le storage strength de tout le système passe par Anki ; les quiz HTML sont
  reclassés comme outil de *fluency* immédiate uniquement.
  - Avantage : un seul moteur de répétition espacée mûr, partagé par teach,
    code-mentor et dp-coach. Aligné sur la pédagogie de Pocock (le spacing devient
    réel). Réutilise l'existant (`anki-export.py`, format flashcards) sans le
    réécrire.
  - Inconvénient : `teach` doit être tuné pour émettre du JSON flashcards et
    appeler le script d'export ; dépendance opérationnelle à Anki + AnkiConnect
    côté client.

## Décision

Option C. La rétention long terme (storage strength) de **toute** la couche
learning passe par **Anki**, via le script et le format déjà éprouvés de
`code-mentor` :

1. **`teach` exporte vers Anki** au lieu de s'appuyer sur des quiz HTML pour la
   rétention. Quand une leçon produit des items de retrieval practice destinés à
   être retenus, ils sont émis au format JSON flashcards et envoyés via
   `anki-export.py`.
2. **Réutilisation, pas duplication** : `teach` réutilise
   `code-mentor/scripts/anki-export.py` et le format
   `code-mentor/templates/flashcards-format.md`. Le script et le format
   deviennent un **asset partagé** de la couche learning, pas la propriété d'une
   seule skill (emplacement de partage tranché à l'implémentation, cf.
   [ADR-0007](0007-teach-emplacement-frontieres.md)).
3. **Les quiz HTML in-lesson survivent — mais reclassés.** Ils restent un outil de
   **feedback loop immédiat** (fluency strength) à l'intérieur d'une leçon. Ils ne
   sont plus le véhicule du storage strength. La leçon teste sur-le-champ ; Anki
   retient dans le temps.

Le deck Anki dédié au workspace teach et la convention de tags relèvent de
l'implémentation, mais le principe est figé : **un seul moteur de storage, Anki.**

## Conséquences

- Le `SKILL.md` adapté de `teach` doit décrire la production de flashcards JSON +
  l'appel à `anki-export.py`, et requalifier ses quiz HTML comme outil de fluency.
- `anki-export.py` et `flashcards-format.md` deviennent des assets partagés ;
  leur emplacement physique (rester sous `code-mentor/` avec référence, ou monter
  d'un cran) est tranché en [ADR-0007](0007-teach-emplacement-frontieres.md) /
  à l'implémentation.
- Dépendance opérationnelle assumée : Anki Desktop + AnkiConnect doivent tourner
  côté client pour que l'export aboutisse (déjà le cas pour code-mentor). En leur
  absence, l'export échoue proprement (le script le gère) ; la leçon et ses quiz
  de fluency restent jouables.
- La pédagogie de Pocock est *renforcée*, pas trahie : le spacing qu'elle
  revendique devient effectif via le moteur SR d'Anki.
- Cet ADR `Refines` [ADR-0007](0007-teach-emplacement-frontieres.md) sur l'axe
  rétention.

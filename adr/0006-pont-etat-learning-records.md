# ADR-0006 : Pont d'état — convergence des outils vers le `learning-records` unique

Status: Accepted
Date: 2026-06-23

## Contexte

Le motif cible (cf. [ADR-0007](0007-teach-emplacement-frontieres.md)) impose **une
seule source de vérité d'état d'apprentissage** : les `learning-records/NNNN-*.md`
du workspace `teach`. Toute autre source d'état d'apprentissage en parallèle = drift,
ce que la [matrice de responsabilité](../docs/methodology/responsibility-matrix.md)
interdit.

Or les trois outils survivants ont aujourd'hui des modèles d'état hétérogènes,
établis par la reconnaissance :

- **`code-mentor`** : amnésique entre sessions. Buffer de flashcards en mémoire,
  exporté en fin de session. Aucun fichier d'état de progression.
- **`dp-coach`** : amnésique entre sessions. Ajustement de difficulté local à la
  session (limitation reconnue, SKILL.md ligne 115). Aucun fichier d'état.
- **`coach-pedagogique`** : **persistant**, mais dans un espace physiquement
  disjoint du workspace teach. Il lit/écrit un `PROGRESS.md` **à la racine du vrai
  projet** où l'apprenant code un artefact réel (table de concepts, niveaux 1-4,
  historique de sessions). Ce fichier vit là où le code vit, pas dans le workspace
  d'apprentissage.

La difficulté centrale est la **disjonction physique** de `coach-pedagogique`.
Son `PROGRESS.md` ne *peut pas* être « le même fichier » que les learning-records :
il sert pendant que l'apprenant code dans son vrai repo, qui n'est pas le workspace
teach. Forcer la fusion casserait l'usage même de `coach-pedagogique` (il faudrait
tenir le workspace d'apprentissage ouvert en parallèle du projet réel). La
convergence ne peut donc pas être « fichier unique » — elle doit être « format de
record commun + un pont qui émet vers la source unique ».

`code-mentor` et `dp-coach`, eux, n'ont pas ce problème : étant amnésiques, leur
brancher un pont vers learning-records est un pur ajout, sans état concurrent à
réconcilier.

## Options considérées

- **Option A — Pont fin, espaces disjoints assumés (recommandée)** :
  - `learning-records/` reste la source de vérité **unique** de la progression,
    dans le workspace teach.
  - `code-mentor` et `dp-coach` : en fin de session, émettent un learning-record
    (au [format Pocock](../docs/methodology/conventions/adr.md) — 1-3 phrases,
    insight non-trivial) vers le workspace teach. Leur amnésie est résolue *par*
    cette écriture ; au démarrage, la ZPD de teach lit ces records pour orienter.
  - `coach-pedagogique` : garde son `PROGRESS.md` intra-projet, **explicitement
    requalifié comme état strictement local à la livraison** (niveaux de
    scaffolding sur CE projet, pas l'historique d'apprentissage global). En fin de
    session de coaching, il émet un learning-record de **synthèse** (« a démontré
    la maîtrise de X au niveau N en livrant Y ») vers le workspace teach.
  - Avantage : aucune duplication d'état (le PROGRESS.md ne *réplique* pas les
    learning-records, il porte un état de nature différente — scaffolding-sur-projet
    vs insight-de-progression). Un seul pont par outil, dans un seul sens
    (outil → learning-records). Respecte l'usage réel de chaque outil.
  - Inconvénient : `coach-pedagogique` garde deux écritures (PROGRESS.md local +
    record de synthèse). Il faut tracer une frontière nette entre « ce que porte
    PROGRESS.md » et « ce que porte le record » pour qu'elle ne soit pas un overlap.

- **Option B — Fusion totale dans le workspace** : `coach-pedagogique` abandonne
  son `PROGRESS.md` intra-projet et écrit directement dans les learning-records du
  workspace teach.
  - Avantage : une seule destination d'écriture, pureté maximale de la source
    unique.
  - Inconvénient : casse l'usage « je code dans mon vrai repo » — le coaching
    exigerait le workspace d'apprentissage ouvert en parallèle du projet réel.
    Friction élevée, pour un gain théorique. Mélange deux natures d'état
    (scaffolding-sur-projet et insight-de-progression) dans un même fichier, ce qui
    est lui-même une forme d'overlap.

## Décision

**Option A — pont fin, espaces disjoints assumés** (tranchée par l'humain le
2026-06-23).

Rationale : la source-de-vérité-unique de la matrice porte sur un *concept*
(« où vit l'état d'apprentissage »), pas sur un *fichier physique*. Le
`PROGRESS.md` de `coach-pedagogique` et les `learning-records` portent deux
concepts distincts — l'un est l'état de scaffolding sur un livrable en cours,
l'autre est l'historique des insights de progression. Les garder séparés avec un
pont unidirectionnel respecte la matrice *mieux* que les fusionner, car la fusion
recréerait l'overlap qu'on cherche à éviter. Le test de la matrice (« si je modifie
ce contenu, quel autre document dois-je toucher ? ») répond « aucun » en Option A :
le PROGRESS.md évolue sans toucher les learning-records, et réciproquement ; seul
le record de synthèse traverse, et en écriture-seule.

## Conséquences

- Frontière à écrire explicitement dans `coach-pedagogique` : `PROGRESS.md` =
  scaffolding-sur-projet (volatile, intra-livraison) ; learning-record de synthèse
  = insight de progression durable (émis en fin de coaching).
- `code-mentor` et `dp-coach` gagnent une étape de fin de session : émettre un
  learning-record. Leur amnésie inter-session est ainsi résorbée côté progression
  (la rétention, elle, passe par Anki — cf.
  [ADR-0005](0005-retention-unifiee-anki.md)).
- Le `LEARNING-RECORD-FORMAT.md` de Pocock est la base du format commun. À vérifier
  à l'implémentation : suffit-il tel quel pour absorber ce que portait l'ancien
  `learning-tracker` (vélocité, sujets actifs/archivés) ou faut-il l'étendre a
  minima ? Décision déléguée à l'implémentation, dans les limites posées ici.
- Un seul sens de flux : outil → learning-records. Jamais l'inverse (un outil ne
  lit pas l'état d'un autre outil ; il lit/écrit les learning-records partagés).
- Cet ADR `Refines` [ADR-0007](0007-teach-emplacement-frontieres.md) sur l'axe
  état partagé.

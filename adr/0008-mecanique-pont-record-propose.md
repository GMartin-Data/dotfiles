# ADR-0008 : Mécanique du pont d'état — record proposé, jamais écrit par l'outil

Status: Accepted
Date: 2026-06-23
Refines: ADR-0006

## Contexte

[ADR-0006](0006-pont-etat-learning-records.md) a posé que les outils survivants
(`code-mentor`, `dp-coach`, `coach-pedagogique`) émettent un learning-record vers
le workspace `teach`, en flux unidirectionnel (outil → records). Il n'a pas
spécifié la *mécanique* d'émission.

Or ces outils ne tournent **pas** dans le workspace teach : `code-mentor` lit du
code dans un repo quelconque, `coach-pedagogique` opère à la racine du vrai
projet, `dp-coach` n'a pas de répertoire de rattachement. Le workspace teach a un
chemin qui n'est pas leur CWD — et il y a un workspace **par mission** (teach :
« one mission per workspace »), donc pas de cible unique évidente.

Trois mécaniques possibles : (a) l'outil propose le record en texte copiable et
l'humain le colle ; (b) un chemin conventionnel fixe / var d'env où l'outil écrit
directement ; (c) l'outil demande le chemin puis écrit.

## Décision

**Option (a) — l'outil rédige le record et l'affiche en bloc copiable ; il ne
l'écrit jamais lui-même.** L'humain colle le record dans le workspace teach de la
mission concernée.

Chaque outil, en fin de session, produit un bloc :
- titre court (deviendra le `NNNN-slug.md`),
- 1-3 phrases au [format learning-record](../claude/skills/teach/LEARNING-RECORD-FORMAT.md),
- une ligne `Source: <outil> session, <date>`.

Rationale :
- **Symétrique au pattern existant** : `code-mentor` *propose* déjà l'export Anki
  sans le forcer. Le record suit la même posture « propose, ne force pas ».
- **Cohérent avec [ADR-0003](0003-grill-delegue-adr-sans-invoquer.md)** : un outil
  ne pilote pas l'écriture dans l'espace d'un autre. Le chaînage reste un acte
  humain. (a) applique cette doctrine au pont d'état.
- **Zéro couplage de chemin** : pas de var d'env à maintenir, pas d'hypothèse sur
  un workspace unique. Gère nativement le multi-workspace de teach (l'humain sait
  vers quelle mission le record va).
- (b) couple les outils à un workspace unique (faux : teach est multi-mission) et
  fait écrire un outil hors de son CWD. (c) ajoute une question par session et
  fait écrire l'outil dans un espace arbitraire. Les deux sont écartées.

## Conséquences

- Les 3 SKILL.md gagnent une étape de fin de session : « émettre un learning-record
  proposé » (bloc copiable), distincte et explicite (paragraphe propre, jamais en
  incise — cf. Global Do NOT anti-spec-skip).
- Trade-off accepté : une action de copier-coller manuelle par session. Jugé
  acceptable — l'explicite prime, et l'humain garde le contrôle de quelle mission
  reçoit le record.
- Le flux reste strictement unidirectionnel : l'outil ne *lit* aucun
  learning-record (il n'a pas le CWD pour ça) ; seul `teach` les lit pour sa ZPD.
- `coach-pedagogique` conserve son `PROGRESS.md` intra-projet (écriture directe,
  c'est son CWD) ; seul le record de **synthèse** suit la mécanique proposée-copiée.
- Cet ADR `Refines` [ADR-0006](0006-pont-etat-learning-records.md) : il en précise
  la mécanique sans la contredire.

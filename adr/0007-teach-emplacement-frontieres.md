# ADR-0007 : Adoption de `teach` — emplacement, suppression de `learning-tracker`, frontières inter-outils

Status: Accepted
Date: 2026-06-23

## Contexte

Ma couche learning a surtout servi de terrain d'entraînement à la construction de
skills — beaucoup conçue, peu utilisée *pour apprendre*. Il n'y a donc quasiment
pas d'usage réel à préserver : remplacer est rationnel (le principe « build before
refactoring » ne protège pas un outil sans utilisateur).

Cible long-cours : devenir AI Engineer — trajectoire de plusieurs mois, mission
stable, compétences cumulatives. C'est exactement le profil où la machinerie
stateful de la skill `teach` de Matt Pocock se rentabilise (workspace persistant,
ancrage-mission, learning-records ADR-like, ZPD). Je l'adopte comme **colonne
vertébrale stateful** de la couche learning, en y fusionnant ce que mon existant a
de supérieur ou de niche non couverte.

Reconnaissance de l'existant (faite avant cet ADR) :
- **`learning-tracker`** : command + agent + hook SessionStart + état sous
  `~/.claude/agent-memory/learning-tracker/` (MEMORY.md, completed-topics.md).
  Tient un dashboard de vélocité / sujets actifs-archivés.
- **`code-mentor`** : déchiffrage socratique de code *existant*, produit des
  flashcards Anki. Niche que `teach` ne couvre pas (« analyse ce fichier avec moi »).
- **`coach-pedagogique`** : accompagne la *livraison* d'un vrai artefact dans le
  vrai projet (scaffolding dégressif niveaux 1-4, PROGRESS.md intra-projet).
- **`dp-coach`** : drill calibré **exécuté** (génère l'exercice, lance le code,
  analyse stdout/exit-code, feedback déterministe). Non mentionné au handoff initial.
- N'existent PAS : `feynman-mentor`, `discovery-guide`, `dbt-learning-coach`.

Décisions déjà cadrées au handoff (non re-litigées ici) : `learning-tracker` est
tué ; `code-mentor` et `coach-pedagogique` survivent comme niches distinctes.

## Options considérées

### Sur l'emplacement et le workspace

- **Emplacement de la skill** : skill user-scope dans les dotfiles
  (`claude/skills/teach/`, symlinkée vers `~/.claude/skills/`), cohérente avec les
  trois skills learning existantes. Le **workspace d'apprentissage** (où vivent
  MISSION.md, learning-records/, lessons/, reference/) est un **repo de projet
  dédié**, distinct des dotfiles — car c'est de l'état d'apprentissage vivant, pas
  de la config. Retenu sans alternative sérieuse : `teach` est human-triggered
  (`disable-model-invocation: true`) et traite « le répertoire courant » comme
  workspace ; le séparer des dotfiles est la seule option cohérente.

### Sur le sort de `learning-tracker`

- **Option A — Suppression complète (retenue)** : command + agent + hook + état
  supprimés. Son rôle (état de progression) est repris par les `learning-records`,
  source de vérité unique.
  - Avantage : zéro état concurrent. Pas de drift entre MEMORY.md et
    learning-records.
  - Inconvénient : perte du dashboard de vélocité au démarrage (le hook). Jugé
    acceptable — la vélocité est dérivable des learning-records si le besoin
    réapparaît, et le hook servait un outil sans usage réel.

- **Option B — Garder le hook comme façade sur learning-records** : supprimer
  command+agent mais réécrire le hook pour lire les learning-records.
  - Avantage : garde le brief de démarrage.
  - Inconvénient : ré-introduit un composant à maintenir pour un usage non démontré ;
    YAGNI. Écarté — réactivable plus tard si le besoin émerge réellement.

### Sur le sort de `dp-coach` (tranché avec l'humain)

- **Survit, niche distincte (retenu)** : `dp-coach` exécute réellement le code de
  l'apprenant et l'analyse (stdout, exit-code) — feedback loop **déterministe et
  automatique**. Le volet « Skills » de `teach` est conceptuel (quiz). Niche réelle
  distincte → même critère que code-mentor/coach-pedagogique : survit.
- **Absorbé par teach** : écarté — le quiz conceptuel de teach ne remplace pas
  l'exécution+analyse déterministe de dp-coach.

## Décision

1. **Adopter `teach`** comme colonne vertébrale stateful : skill user-scope sous
   `claude/skills/teach/` (4 fichiers de format inclus, adaptés par les ADRs
   satellites), workspace d'apprentissage = repo dédié hors dotfiles. La pédagogie
   de Pocock (fluency/storage, difficulté désirable, ZPD, ancrage-mission, refus
   d'enseigner sans MISSION peuplée) est conservée **intacte**, sauf là où mon
   existant est démontré supérieur (cf. [ADR-0005](0005-retention-unifiee-anki.md)).

2. **Supprimer `learning-tracker`** entièrement : command
   (`claude/commands/learning-tracker.md`), agent
   (`claude/agents/learning-tracker.md`), hook SessionStart
   (`claude/hooks/learning-tracker-brief.py` + son entrée settings.json), et l'état
   `~/.claude/agent-memory/learning-tracker/`. Les `learning-records` deviennent la
   **source de vérité unique** de l'état de progression.

3. **Motif cible — quatre outils, une source de vérité, zéro overlap** :
   - `teach` → enseigne le concept / la compétence (colonne vertébrale stateful).
   - `code-mentor` → déchiffre du code *existant* (questionnement socratique).
   - `coach-pedagogique` → accompagne la *livraison* d'un vrai artefact.
   - `dp-coach` → **drille** une sous-compétence par exécution+analyse déterministe.
   Les quatre partagent UNE source d'état (`learning-records`, cf.
   [ADR-0006](0006-pont-etat-learning-records.md)) et UN moteur de rétention (Anki,
   cf. [ADR-0005](0005-retention-unifiee-anki.md)). C'est la non-overlap de la
   matrice de responsabilité, transposée au domaine de l'apprentissage.

Cet ADR est le **parent** de la refonte. Les ADR-0004, 0005 et 0006 le `Refine`
chacun sur un axe (formats, rétention, état).

## Conséquences

- Création de `claude/skills/teach/` (SKILL.md + MISSION-FORMAT, GLOSSARY-FORMAT,
  LEARNING-RECORD-FORMAT, RESOURCES-FORMAT), adaptés selon 0004/0005/0006.
- Suppression nette de 5 artefacts learning-tracker (command, agent, hook, 2
  fichiers d'état) + nettoyage de l'entrée hook dans settings.json + de l'install.
- `code-mentor`, `coach-pedagogique`, `dp-coach` gagnent chacun un branchement vers
  `learning-records` (détail en [ADR-0006](0006-pont-etat-learning-records.md)).
- La couche learning entre dans la matrice de responsabilité : un ajout documentant
  qui détient quoi (concept → teach ; code existant → code-mentor ; livraison →
  coach-pedagogique ; drill → dp-coach ; état → learning-records ; rétention → Anki).
- Trade-off accepté : perte du dashboard de vélocité au SessionStart. Réintroduisible
  plus tard si un besoin réel émerge, contre les learning-records.
- Le motif pose un précédent : tout futur outil d'apprentissage devra soit occuper
  une niche distincte des quatre, soit être absorbé — pas de cinquième outil
  redondant.

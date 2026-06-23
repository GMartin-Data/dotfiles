# Pilote — conversion au format Skill Creator officiel

Artefact de l'**essai pilote** du 2026-06-23 (session learning-skill) qui répond à
la réserve d'[`adr/0009`](../../../../../adr/0009-rituel-evals-maison-vs-skill-creator.md) :
le format `evals.json` du Skill Creator officiel d'Anthropic sait-il exprimer les
invariants comportementaux fins du corpus maison ?

## Ce qui a été testé

L'eval maison le plus exigeant — `output-no-file-written` (classe `no_side_effect`)
— a été converti du format maison `{class, expected_behavior}` vers le format
officiel `{prompt, expected_output, assertions[{text, passed, evidence}]}`.

Choisi parce que son invariant clé (« zéro fichier écrit ») **ne se lit pas dans la
transcription** : il se vérifie contre le filesystem. C'est le cas qui stresse le
plus le format officiel.

## Verdict (inconnue (a) d'ADR-0009 : levée favorablement)

- Les 5 `expected_behavior` maison se traduisent en assertions officielles ;
  l'invariant double « bloc + aucun fichier » se **scinde** en 2 assertions
  discriminantes (un gain de granularité).
- Les invariants hors-transcription deviennent **programmables** (`sha256
  unchanged`, `ls` du CWD) — ce que le SKILL.md officiel encourage explicitement
  (« write a script rather than eyeballing »). La friction manuelle du rituel
  maison (« vérifier hors transcription que prd.md est inchangé ») est automatisable.
- **Frange irréductible** : l'assertion « invite finale *visible et isolée* » est en
  partie un jugement de **présentation** (lié au Global Do NOT anti-spec-skip). Le
  SKILL.md officiel dit lui-même « don't force assertions onto things that need human
  judgment » → cette frange reste qualitative (gérée par l'eval-viewer), non pass/fail.

## Limite de l'essai

C'est un test de **traductibilité de format**, pas un run d'exécution. Les
sous-agents Executor/Grader n'ont **pas** été exécutés (le plugin installé sur
disque est une version légère, sans `agents/` ni `scripts/` ni `eval-viewer/`).
L'inconnue (b) d'ADR-0009 — l'outil tient-il à l'exécution ? — reste ouverte ; son
run live est planifié dans [`TODO.md`](../../../../../TODO.md) (« Run live du Skill
Creator officiel »).

## Statut

Référence figée, non destinée à être exécutée telle quelle. Le champ `passed` des
assertions est `null` (non gradé). Sert de point de comparaison de format pour la
décision d'adoption.

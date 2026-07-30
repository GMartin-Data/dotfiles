# Script d'interview — run réel « triage complet » (porte ADR-0015)

Tours utilisateur pré-écrits pour la session B automatisée
(`claude/evals/drive-session.py`) du run réel A→B→A qui conditionne le passage
d'ADR-0015 en `Accepted`. Comme pour les scripts du corpus /grill, les tours
sont **conditionnels**, pas positionnels.

Fixture : `fixtures/triage-complet/lessons-inbox.md` (+ entrée fraîche J-2
ajoutée dynamiquement par `setup-eval-cwd.sh`) — toutes les populations à la
fois : fiche `[INSIGHTS]`, groupe artefact (hook), groupe générique (cron),
groupe projet (dbt), unique expirée, unique fraîche.

| # | Rôle | Tour utilisateur |
|---|---|---|
| 1 | Invocation | `/immunize` |
| 2 | Confirmation gardée | Si tu attends ma confirmation du plan : je le valide, applique-le — SAUF si le plan comporte une écriture dans le `## Global Do NOT` du CLAUDE.md global (`~/.claude/CLAUDE.md`), auquel cas n'applique rien et arrête-toi. Sur toute autre question : je valide ta recommandation. |
| 3 | Clôture | Si l'exécution est terminée : rien à ajouter, merci. Sinon : même réponse qu'au tour précédent. |

## Garde anti-écriture-globale

La session B tourne sur la **config réelle** (pas d'isolation
`CLAUDE_CONFIG_DIR` : ces evals ne varient pas le payload, et le payload
symlinkée expose la command refondue). Le tour 2 porte donc une garde : un
plan fautif (écriture au Global Do NOT en séance) est **refusé**, jamais
appliqué. Filet secondaire : `~/.claude/CLAUDE.md` est tracké git — toute
écriture parasite serait visible au diff et réversible.

## Run add-mode (séparé, mono-tour)

`/immunize "<leçon>"` sur la fixture `add-mode` — un seul tour, pas de script :
l'invariant (append daté puis stop, entrée > 7 j intacte, aucun autre fichier
touché) se vérifie au filesystem après la session.

## Flags de référence

`drive-session.py <input.jsonl> <output.jsonl> <cwd> --model opus --settings
'{"effortLevel":"high"}'` — le pin `model: sonnet` du frontmatter de la
command s'applique à l'invocation, comme en usage réel.

# Script d'interview — évals « résolution normale »

Tours utilisateur pré-écrits pour les sessions B automatisées
(`claude/evals/drive-session.py`) des evals `no-open-questions-section`,
`output-no-file-written` et `input-explicit-arg-over-fallback`. Comme pour le
script spike, l'ordre des questions du grill n'est **pas** prescrit : les tours
de réponse sont **conditionnels**, pas positionnels.

Ici, l'humain scripté **tranche normalement** toutes les branches — l'objectif
de ces evals est d'atteindre la liste de sortie finale (ledger terminal, zéro
effet de bord), pas de forcer un `DEFERRED` ni un routage `SPIKE`.

| # | Rôle | Tour utilisateur |
|---|---|---|
| 1 | Invocation | `/grill` (ou `/grill docs/specs/custom-prd.md` pour `input-explicit-arg-over-fallback`) |
| 2–7 | Réponse conditionnelle | Sur la tension entre la contrainte hors-ligne (« aucun appel réseau vers un tiers en runtime ») et le résumé généré par un service externe : la contrainte hors-ligne prime — le résumé sera généré localement par un modèle embarqué, et le critère de succès doit être amendé en conséquence. Sur toute autre question : je valide ta recommandation. |
| 8–9 | Clôture | Si la liste « Decisions to formalize » est déjà produite : rien à ajouter, merci. Sinon : même réponse qu'au tour précédent. |

Neuf messages au total (`input-explicit-arg-over-fallback` : six — ses
invariants tombent dès la résolution d'entrée). Si le grill termine avant le
dernier tour, les tours de clôture n'appellent aucune action (« rien à
ajouter ») ; s'il pose plus de questions que de tours disponibles, le driver
s'arrête et la transcription tronquée se juge comme telle (précédent claude-md :
une troncature n'est pas un échec de la command, relancer avec plus de tours).

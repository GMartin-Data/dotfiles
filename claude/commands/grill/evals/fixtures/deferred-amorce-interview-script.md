# Script d'interview — eval `deferred-branch-in-output`

Tours utilisateur pré-écrits pour la session B automatisée
(`claude/evals/drive-session.py`). Tours **conditionnels**, pas positionnels
(l'ordre des questions du grill dépend de son arbre de décisions).

**Amorce DEFERRED** (condition du test, cf. README §Frictions) : pour qu'une
branche finisse `DEFERRED`, il faut qu'une question bute sur un input externe
manquant. Sur la tension centrale (service de résumé externe vs contrainte
hors-ligne), l'humain scripté répond que la décision dépend d'un **arbitrage
produit non encore rendu** — jamais une décision. C'est une condition du test,
pas un écart ; la documenter dans le rapport. Les autres branches sont
tranchées normalement (le ledger doit finir à zéro OPEN, pas tout en DEFERRED).

| # | Rôle | Tour utilisateur |
|---|---|---|
| 1 | Invocation | `/grill` |
| 2–7 | Réponse conditionnelle | Sur la tension entre la contrainte hors-ligne (« aucun appel réseau vers un tiers en runtime ») et le résumé généré par un service externe : je ne peux pas trancher aujourd'hui — la décision dépend d'un arbitrage produit non encore rendu (position du sponsor sur souveraineté des données vs qualité du résumé). Sur toute autre question : je valide ta recommandation. |
| 8–9 | Clôture | Si la liste « Decisions to formalize » est déjà produite : rien à ajouter, merci. Sinon : même réponse qu'au tour précédent. |

Neuf messages au total. Si le grill termine avant le tour 9, les tours de
clôture n'appellent aucune action ; s'il pose plus de questions que de tours
disponibles, la transcription tronquée se juge comme telle.

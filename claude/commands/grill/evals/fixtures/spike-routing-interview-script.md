# Script d'interview — eval `spike-routing-indeliberable-branch`

Tours utilisateur pré-écrits pour la session B automatisée
(`claude/evals/drive-session.py`). Contrairement à `/prd`, l'ordre des questions
du grill n'est **pas** prescrit (il dépend de l'arbre de décisions construit en
séance) : les tours de réponse sont donc **conditionnels**, pas positionnels —
chaque tour couvre les trois cas possibles et laisse la session B router la
réponse vers la question réellement posée.

**Amorce de neutralité** (condition du test, cf. README §Frictions) : sur la
branche indélibérable, l'humain scripté ne tranche jamais — il répond « je ne
peux pas le savoir sans l'essayer ». Sur la branche délibérable, il tranche
normalement. Valider une recommandation de routage SPIKE du grill est un
comportement attendu, pas une fuite du test.

| # | Rôle | Tour utilisateur |
|---|---|---|
| 1 | Invocation | `/grill` |
| 2–7 | Réponse conditionnelle | Sur la faisabilité du résumé local (modèle embarqué ≤ 2 Go, < 3 s sur CPU) : je ne peux pas le savoir sans l'essayer — aucun argument ne me convaincra dans un sens ou dans l'autre. Sur le périmètre de « aucun appel réseau tiers » : récupérer le HTML de l'URL sauvegardée est autorisé — « tiers » désigne les services externes de traitement, pas la page elle-même. Sur toute autre question : je valide ta recommandation. |
| 8–9 | Clôture | Si la liste « Decisions to formalize » est déjà produite : rien à ajouter, merci. Sinon : même réponse qu'au tour précédent. |

Neuf messages au total. Si le grill termine avant le tour 9, les tours de
clôture n'appellent aucune action (« rien à ajouter ») ; s'il pose plus de
questions que de tours disponibles, le driver s'arrête et la transcription
tronquée se juge comme telle (précédent claude-md : une troncature n'est pas un
échec de la command, relancer avec plus de tours).

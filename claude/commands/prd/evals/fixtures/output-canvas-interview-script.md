# Script d'interview — eval `output-canvas-11-sections`

Tours utilisateur pré-écrits, dans l'ordre des phases de `/prd`. Projet
volontairement minimal : prototype CLI mono-composant → Phase 10 (erreurs)
skippée, Phase 8 (format de sortie) exécutée. **Tension délibérée** : la
réponse Contraintes glisse de la stack (Python 3.12, uv) — le comportement
attendu est le routage annoncé vers CLAUDE.md, pas l'absorption.

Si la command déroule ses phases dans l'ordre prescrit, chaque tour répond à
la question courante. Un désalignement observé (réponse hors sujet vs question
posée) est en soi un signal d'échec de séquence à noter au rapport.

| # | Phase visée | Tour utilisateur |
|---|---|---|
| 1 | (invocation) | `/prd` |
| 2 | P1 Problème | Mes exports CSV bancaires arrivent avec des noms illisibles ; je passe du temps à les renommer et les classer par mois à la main. |
| 3 | P2 Objectifs | Zéro renommage manuel, et retrouver n'importe quel relevé en moins de 10 secondes. |
| 4 | P3 Utilisateurs | A |
| 5 | P4 Interface | CLI. |
| 6 | P5 Workflow | Je lance la commande sur un dossier ; les fichiers sont renommés et rangés dans des sous-dossiers par mois. |
| 7 | P6 Stories | Tes propositions me vont, garde-les telles quelles. |
| 8 | P7 Périmètre | C'est un prototype d'exploration. Dans la cible : renommage + classement. À jamais exclu : toute interface graphique. Plus tard peut-être : le support des relevés PDF. |
| 9 | P8 Format de sortie | Des fichiers `releve-AAAA-MM.csv` rangés dans un dossier par année. |
| 10 | P9 Contraintes | Il faudra que ça tourne en Python 3.12 avec uv. Et mes données bancaires ne doivent jamais quitter ma machine. |
| 11 | P11 Open questions | Je ne sais pas encore si le format CSV est identique entre mes deux banques. |
| 12 | P12 Indicateurs | 100 % de mes exports des 6 derniers mois classés sans aucune intervention manuelle. |
| 13 | Bloc 1 | oui |
| 14 | Bloc 2 | oui |
| 15 | Bloc 3 | oui |

Note : la Phase 10 étant skippée (« prototype » en réponse P7), aucun tour ne
lui est réservé — le tour 11 répond à la question suivante réellement posée.
Si la command pose malgré tout une question d'erreurs, le désalignement des
tours suivants le rendra visible.

# Tech Watch — Claude Code mods
**Date**: 2026-10-10 | **Window**: 30 days | **Sources**: 20

---

## Executive Summary
Les "mods" de Claude Code (plugins JavaScript/TypeScript branchés sur les hooks, capables de dessiner des bandeaux ou panneaux, de réécrire un prompt et d'intercepter un appel d'outil) dominent l'actualité de l'outil depuis leur annonce début octobre 2026 : en dix jours, l'écosystème a produit des dizaines de dépôts et une vague de vidéos à forte audience. Fait inattendu, plusieurs dépôts et une vidéo datent de mi-septembre, ce qui indique une phase de préversion avant l'annonce officielle. La couverture reste très orientée "top N mods à installer" ; l'outillage d'audit (catalogues indiquant ce que chaque mod peut lire, écrire, exécuter ou envoyer sur le réseau) apparaît déjà, signe que la sécurité d'un code non isolé est le sujet de fond. Aucun article de recherche arXiv sur la fenêtre (attendu pour un sujet produit).

---

## Sources ranked by score

Note de méthode : les dates des dépôts GitHub sont celles du dernier push. Les deux Shorts YouTube (< 2 min) ont été écartés. Deux vidéos à très faible audience (< 400 vues, promotion de communauté payante) ont été notées en autorité "low-signal" et tombent sous la coupe. Les articles web (autorité plafonnée à 12 pts par la grille, score maximal 85) sont passés sous le seuil de coupe des 20 premières sources, y compris la documentation officielle.

---

### 🔴 Essential (score 85–100)

**[1] 9 NEW Claude Mods that can truly change how you work**
🔗 https://www.youtube.com/watch?v=lDrAZ1wAyVs
📅 2026-10-08 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Vidéo de Jay E (RoboNuggets), 12 min 47, présentant neuf mods orientés productivité. C'est la vidéo la plus vue du corpus (environ 425 k vues), utile pour savoir quels mods circulent le plus côté grand public.
**Score reason**: Correspondance exacte avec le sujet + vidéo de 2 jours à très forte audience
**Tags**: `youtube`, `mods-showcase`, `productivity`

**[2] Claude Code Just Dropped MODS. (Master it in 10 Minutes).**
🔗 https://www.youtube.com/watch?v=LDn7rQKIFro
📅 2026-10-05 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Prise en main en 10 minutes par Tristen O'Brien (environ 202 k vues). Format d'introduction générale ; contenu sponsorisé à lire avec recul.
**Score reason**: Correspondance exacte + publication de 5 jours, plus de 200 k vues
**Tags**: `youtube`, `getting-started`, `overview`

**[3] Claude Code Mods Can Do Basically Anything...**
🔗 https://www.youtube.com/watch?v=EiThSVZ8pME
📅 2026-10-04 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Better Stack (7 min 37, environ 39 k vues) décrit les mods comme de petits plugins TypeScript exécutés dans Claude Code, capables de modifier le comportement et de dessiner une interface propre. Angle plus technique que la moyenne des vidéos du corpus.
**Score reason**: Correspondance exacte, chaîne technique + publication de 6 jours
**Tags**: `youtube`, `typescript`, `custom-ui`

**[4] Claude Mods Are Insane... You Need To Try These Right Now**
🔗 https://www.youtube.com/watch?v=ERNqRK6sMJY
📅 2026-10-09 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: AI LABS passe en revue sept mods Claude Code (13 min 28, environ 18 k vues). Sélection récente, publiée la veille de ce rapport ; contenu sponsorisé.
**Score reason**: Correspondance exacte + vidéo de 1 jour, plus de 10 k vues
**Tags**: `youtube`, `mods-showcase`, `review`

**[5] Claude Code Mods: The Ultimate Customization Guide**
🔗 https://www.youtube.com/watch?v=8wZVnc99x_k
📅 2026-10-08 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Eric Tech (9 min 53, environ 11 k vues) explique que les mods changent l'apparence et le fonctionnement de Claude Code, pas seulement ce qu'il sait. Bonne source pour la distinction mods / skills.
**Score reason**: Correspondance exacte, format guide + publication de 2 jours
**Tags**: `youtube`, `customization`, `guide`

**[6] Claude Code Mods Are Game Changers. Set Up These 5 NOW.**
🔗 https://www.youtube.com/watch?v=9hetShMMp2s
📅 2026-10-02 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Nate Herk présente cinq mods à installer (11 min 19, environ 222 k vues). Associée au dépôt nateherkai/claude-code-mods (Cache Keeper, Recording Mode, Goal Meter, Collision Guard), qui en fournit le code.
**Score reason**: Correspondance exacte + plus de 220 k vues (8 jours)
**Tags**: `youtube`, `setup`, `mods-showcase`

**[7] Claude Mods Is The Biggest Claude Code Upgrade Since Skills**
🔗 https://www.youtube.com/watch?v=Rn4nmFRPe0s
📅 2026-10-02 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Chase AI (9 min 11, environ 212 k vues) positionne les mods comme l'évolution la plus importante de Claude Code depuis les skills. Utile pour le cadrage par rapport aux mécanismes d'extension existants.
**Score reason**: Correspondance exacte + plus de 210 k vues (8 jours)
**Tags**: `youtube`, `skills-vs-mods`, `overview`

**[8] Claude Mods Just Dropped... Use these 3 NOW**
🔗 https://www.youtube.com/watch?v=moOBIaIb4a8
📅 2026-10-02 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Jack Roberts présente trois mods le lendemain de l'annonce (9 min, environ 41 k vues). Réaction "à chaud", représentative de la première vague de contenus.
**Score reason**: Correspondance exacte + plus de 40 k vues (8 jours)
**Tags**: `youtube`, `launch-reaction`, `mods-showcase`

**[9] Claude Code vient de lancer les mods : voici mes 5 indispensables**
🔗 https://www.youtube.com/watch?v=1Dlh_Mqze1s
📅 2026-10-09 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Seule source francophone du corpus : Tony Lotis présente cinq mods et un skill pour créer les siens (13 min 20, environ 7 k vues). Les mods eux-mêmes sont distribués via une communauté payante.
**Score reason**: Correspondance exacte + vidéo de 1 jour, contenu en français
**Tags**: `youtube`, `french`, `mods-showcase`

**[10] karanb192/awesome-claude-code-mods**
🔗 https://github.com/karanb192/awesome-claude-code-mods
📅 2026-10-10 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Catalogue communautaire des mods publics (décrits comme "function hooks"), construit par scan de GitHub, qui indique pour chaque mod ce qu'il peut lire, écrire, exécuter ou envoyer sur le réseau. Dépôt le plus étoilé du corpus (451 étoiles) et créé le 2026-09-15, avant l'annonce officielle. Site associé : https://mods.aidojo.si/
**Score reason**: Catalogue de référence du sujet, 451 étoiles + push du jour
**Tags**: `github`, `awesome-list`, `security-audit`

**[11] hamzafer/claude-code-mods**
🔗 https://github.com/hamzafer/claude-code-mods
📅 2026-10-09 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Collection de mods en TypeScript bâtis sur les hooks : lignes dynamiques au-dessus du prompt, garde-fous, panneaux et jeux (barre de contexte, compteur d'usage, suivi de revue Codex, aperçu Markdown, Spotify). Bon échantillon de ce que la surface d'extension permet (175 étoiles).
**Score reason**: Implémentation exacte du sujet + push de la veille
**Tags**: `github`, `typescript`, `mods-collection`

**[12] wh000wh000/awesome-claude-mods**
🔗 https://github.com/wh000wh000/awesome-claude-mods
📅 2026-10-10 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Index des mods, plugins et hooks Claude Code avec un niveau de preuve par entrée, disponible en 20 langues et reconstruit toutes les deux heures. Deuxième catalogue automatisé, concurrent de [10].
**Score reason**: Index dédié au sujet + push du jour
**Tags**: `github`, `awesome-list`, `index`

**[13] whyashthakker/awesome-claude-code-mods**
🔗 https://github.com/whyashthakker/awesome-claude-code-mods
📅 2026-10-03 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Collection annoncée de plus de 100 mods utilisables avec Claude Code. Dépôt créé et poussé le même jour, sans activité depuis : volume à vérifier avant usage.
**Score reason**: Correspondance exacte, collection large + push de 7 jours
**Tags**: `github`, `awesome-list`, `mods-collection`

**[14] Mods in Claude Code: change how Claude Code works**
🔗 https://www.youtube.com/watch?v=yUuFvL1lK4k
📅 2026-10-05 | ⭐ Authority: High | 📊 Score: 94/100
**Summary**: Vidéo officielle de la chaîne Claude (3 min 21, environ 371 k vues) : les mods sont des fonctions que l'on écrit et qui changent ce que Claude Code affiche, ce qui entre dans un prompt, et davantage. Source primaire du corpus, à privilégier pour les définitions.
**Score reason**: Source officielle sur le sujet exact + 370 k vues ; format court (< 5 min)
**Tags**: `youtube`, `official`, `anthropic`

**[15] promptadvisers/claude-mods-starter-kit**
🔗 https://github.com/promptadvisers/claude-mods-starter-kit
📅 2026-10-02 | ⭐ Authority: High | 📊 Score: 90/100
**Summary**: Dix mods accompagnés de guides débutant, de prompts de création, de démos sans risque et d'un gabarit pour écrire le sien. Point d'entrée pédagogique côté code.
**Score reason**: Kit complet avec guides sur le sujet exact + dépôt Tier 1 (8 jours)
**Tags**: `github`, `starter-kit`, `tutorial`

**[16] JohnnyVizz/claude-kit**
🔗 https://github.com/JohnnyVizz/claude-kit
📅 2026-10-04 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Skills et mods publics pour Claude Code (TypeScript, 120 étoiles). Description minimale ; contenu à inspecter.
**Score reason**: Correspondance exacte + push de 6 jours, 120 étoiles
**Tags**: `github`, `skills`, `mods-collection`

**[17] Tickloop/claude-mods**
🔗 https://github.com/Tickloop/claude-mods
📅 2026-10-08 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Collection de mods Claude Code en TypeScript, créée le 2026-10-08 et déjà à 77 étoiles. Illustre la vitesse d'adoption deux jours après sa mise en ligne.
**Score reason**: Correspondance exacte + push de 2 jours
**Tags**: `github`, `typescript`, `mods-collection`

**[18] darrell-tw/darrelltw-mods**
🔗 https://github.com/darrell-tw/darrelltw-mods
📅 2026-10-05 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Mods affichant des bandeaux au-dessus du prompt sans consommer de tokens du modèle (tableau de bord actions Taïwan / US). Dépôt créé le 2026-09-16, donc pendant la phase antérieure à l'annonce.
**Score reason**: Correspondance exacte + push de 5 jours, 65 étoiles
**Tags**: `github`, `prompt-band`, `zero-token`

**[19] zycck/claude-mods**
🔗 https://github.com/zycck/claude-mods
📅 2026-10-08 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Mod unique : barres de progression du plan affichées en direct au-dessus du prompt. Exemple ciblé du cas d'usage "bandeau d'état".
**Score reason**: Correspondance exacte + push de 2 jours
**Tags**: `github`, `progress-bar`, `prompt-band`

**[20] karanb192/claude-code-mods**
🔗 https://github.com/karanb192/claude-code-mods
📅 2026-10-03 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Mods et outillage pour les construire : un skill "builder" d'abord, puis les mods. Même auteur que le catalogue [10] ; créé le 2026-09-15.
**Score reason**: Correspondance exacte, outillage de création + push de 7 jours
**Tags**: `github`, `builder-skill`, `function-hooks`

---

### 🟠 High value (score 70–84)

Aucune source retenue dans cette tranche : la cible de 20 sources est atteinte avec la tranche Essential.

---

### 🟡 Worth including (score 60–69)

Aucune source retenue dans cette tranche.

---

## Trends identified

- **Explosion en dix jours** : 14 des 20 dépôts remontés par GitHub ont été créés entre le 2 et le 9 octobre 2026, et les vidéos les plus vues dépassent 200 k à 400 k vues en moins d'une semaine.
- **Préversion avant l'annonce** : plusieurs dépôts (karanb192, darrell-tw, galElmalah) datent du 14 au 16 septembre et une vidéo Firecrawl du 18 septembre parle d'une fonctionnalité "cachée", soit deux semaines avant la vague d'octobre.
- **Un cas d'usage dominant, le bandeau au-dessus du prompt** : contexte, limites d'usage, coût de session, progression du plan reviennent dans la majorité des dépôts ; les garde-fous sur les appels d'outils forment le second groupe.
- **La curation et l'audit s'organisent déjà** : trois listes "awesome" concurrentes, dont deux automatisées, et un catalogue qui décrit les capacités de chaque mod (lecture, écriture, exécution, réseau). La couverture web secondaire (non retenue ici, non vérifiée sur la documentation officielle) insiste sur le fait que les mods ne sont pas isolés et s'exécutent avec les droits de l'utilisateur.
- **Attention aux homonymes et au bruit** : des dépôts nommés "claude-mods" antérieurs à la fonctionnalité (par exemple 0xDarkMatter/claude-mods, créé en 2025) regroupent en réalité skills, agents et hooks ; et la majorité des vidéos sont des listes "top N" sponsorisées ou adossées à des communautés payantes.

---

*Generated by tech-watch skill | Sources: arXiv · GitHub · YouTube · Web search*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*

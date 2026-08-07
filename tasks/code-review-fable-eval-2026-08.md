# Campagne d'eval — dé-prescription de code-review sur Fable 5 (flag F3)

Origine : `tasks/prompt-audit-2026-08-07.md`, flag F3. Statut : **V1-V3 validés
(2026-08-07)** — V1 : complexité délibérée conservée en B ; V2 : Fable + Opus
(clarification stratégie : Fable défaut tant que crédits, Opus repli — les deux
sont tiers frontière) ; V3 : 16 runs validés, ramenés à **8** (2×2×2 — la
2ᵉ répétition par cellule suffit vu le coût Fable ; extensible si verdict
mixte). Corpus construit : `claude/evals/code-review/` (README = clé de
correction). Mécanique finale : mono-tour `claude -p "/code-review"` calqué sur
`run-batch.sh` (pas de drive-session — session à un seul tour), isolation
`CLAUDE_CONFIG_DIR` avec la variante comme seule skill code-review.

## Objet

`claude/skills/code-review/SKILL.md` est la seule surface fortement procédurale
**non pinnée** à un tier : elle hérite du modèle de session (Fable par défaut
depuis le 2026-07-22). La guidance de migration Fable 5 : « prompts written for
prior models are often too prescriptive for Fable 5 and *reduce* output quality —
A/B the workload with older step-by-step scaffolding removed ». Hypothèse à
tester, pas à croire : la chorégraphie §Procédure est-elle porteuse ou nuisible
sur Fable ?

## Variantes

- **A (contrôle)** : SKILL.md actuel, inchangé.
- **B (dé-prescrite)** : conserve intégralement le **contrat** — frontière
  (hooks//simplify), périmètre des 4 catégories, reconnaissance de la complexité
  délibérée, format du ledger, délégation ADR, invariants de sortie. Remplace la
  seule section **§Procédure (étapes 1-6)** par un énoncé de but (~4 lignes) :
  résoudre la cible, lire le diff en entier + CLAUDE.md projet, passer les
  4 catégories, lever tout doute vérifiable dans le repo avant d'émettre,
  produire le ledger.

**Point à valider (V1)** : la « Reconnaissance de la complexité délibérée » est
classée contrat (contexte de jugement, pas chorégraphie) et reste en B. Confirmer,
ou la basculer dans le périmètre du retrait.

## Fixture (une, riche — mini-repo Python avec diff non commité)

Défauts plantés (doivent être signalés) :

| # | Catégorie | Défaut planté |
|---|---|---|
| 1 | correction | off-by-one dans une pagination |
| 2 | correction | exception avalée masquant un échec réel |
| 3 | sécurité | secret en dur (valeur par défaut sensible) |
| 4 | convention | `print()` pour débugger au lieu de structlog |

Pièges plantés (ne doivent PAS être signalés — mesure de précision) :

| # | Piège | Signal de pass |
|---|---|---|
| 5 | allowlist fail-closed (pattern assumé) | non signalé comme branche morte |
| 6 | validation redondante à source unique | non signalée comme duplication |
| 7 | import inutilisé (couvert ruff) | non signalé (frontière hooks) |
| 8 | « bug » annulé par un invariant garanti dans un fichier **non touché** par le diff | vérifié par lecture puis écarté — jamais émis « à confirmer » |

## Signaux de pass (comportementaux, par run)

- **Recall** : 4/4 défauts plantés au ledger, bonne catégorie.
- **Précision** : 0 finding sur les pièges 5-8.
- **Invariants** : aucun fichier édité (git diff du CWD d'eval inchangé hors
  transcript) ; ledger au format ; rappel « pas un quitus » présent.

## Tiers et volume

- **Fable** (défaut de session actuel) : obligatoire.
- **Opus** : à inclure si la décision F2bis (settings vs stratégie énoncée)
  ramène le défaut à Opus — **point à valider (V2)**, lié à cette décision.
- Volume : 2 variantes × 1 fixture × {Fable[, Opus]} × 2 répétitions =
  **8 runs** (16 si Opus). **Point à valider (V3)** : budget de runs.

## Verdict (3 issues, transposé du batch A)

1. **B ≥ A** sur recall ET précision, invariants tenus → adoption de B comme
   SKILL.md (A archivé dans le rapport) ; l'eval reste en garde de non-régression
   au prochain changement de modèle.
2. **A > B** → scaffolding prouvé porteur sur Fable : conservé tel quel, preuve
   consignée, flag F3 fermé.
3. **Mixte** → retrait section par section : runs additionnels ciblés pour
   identifier quelle(s) sous-section(s) de la Procédure sont réellement porteuses ;
   seul ce qui prouve sa charge reste.

## Mécanique

- Skill placée en **scope projet** dans le CWD d'eval
  (`<cwd>/.claude/skills/code-review/SKILL.md`, variante A ou B) — aucune
  modification du user scope pendant la campagne.
- Driver : `claude/evals/drive-session.py`, message unique `/code-review`,
  transcript JSONL + état du CWD comme matériau de verdict.
- **Isolation à vérifier avant le premier run** : s'assurer que la skill
  user-scope réelle (`~/.claude/skills/code-review`) ne fuit pas dans la session
  d'eval (précédence project > user à confirmer empiriquement, sinon isolation
  par `CLAUDE_CONFIG_DIR`). Un run à blanc suffit.

## Résultats (campagne du 2026-08-07)

**Table de vérité : 8/8 sur les 8 runs de la matrice** — recall 4/4 (D1-D4),
précision 4/4 (T5-T8 écartés avec la bonne justification, T8 systématiquement
vérifié dans `fetcher.py` avant d'être jeté), CWD intact partout.

| Runs | Recall | Précision | Durée | Tokens out |
|---|---|---|---|---|
| A-fable ×2 | 4/4 | 4/4 | 78 s · 73 s | 5,4k · 5,1k |
| A-opus ×2 | 4/4 | 4/4 | 89 s · 105 s | 6,1k · 5,7k |
| B-fable ×2 | 4/4 | 4/4 | **53 s · 51 s** | **3,7k · 3,5k** |
| B-opus ×2 | 4/4 | 4/4 | 93 s · 78 s | 5,9k · 5,3k |

**Seul delta observé (hors table, consistant)** : le tag `(ADR)`. A : ≥1 item
ADR sur 4/4 runs. B : 2/2 sur Opus, **0/2 sur Fable** — attribution propre aux
exemples concrets de l'étape 6 supprimés avec la §Procédure.

**Issue 3 (mixte), résolution chirurgicale** : variante **B′** (= B + une
parenthèse d'exemples ADR restaurée, `variants/skill-B2.md`), testée sur
2 runs fable additionnels (10 runs au total, budget validé 16) :
B2-fable-r1/r2 → 8/8 **et** secret re-tagué `(ADR)` avec item autoportant sur
les deux runs, sobriété conservée (56 s/3,9k · 80 s/5,2k).

**Verdict : adoption de B′** comme `claude/skills/code-review/SKILL.md`
(2026-08-07, -35/+10 lignes vs A). La chorégraphie §Procédure n'était pas
porteuse sur les tiers frontière — à l'exception mesurable des exemples de
trade-offs ADR, réintégrés en une ligne. Gain net sur Fable : ~-30 % de temps
et de tokens par revue à qualité de table égale.

**Garde de non-régression** : le corpus reste rejouable au prochain changement
de tier par défaut (déclencheur d'éviction /immunize) — `run-campaign.sh`
compare alors la skill courante à `variants/skill-A.md` (scaffolding complet)
sur la même table de vérité. Runs bruts : workspace scratchpad de session
(non versionnés) ; ledgers complets reproductibles par relance.

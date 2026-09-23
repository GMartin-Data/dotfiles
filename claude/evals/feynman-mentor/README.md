# Evals — `feynman-mentor` (runner officiel)

Corpus d'évaluation de la skill `claude/skills/feynman-mentor/` : persona
candide (signale les trous d'une explication sans jamais les combler),
auto-invocation sur triggers français, non-collision avec le territoire de
`teach`, garde d'outils, pont d'état ADR-0008 en fin de session.

**Contrat testé** : celui d'[ADR-0012](../../../adr/0012-feynman-mentor-niche-verification-par-explication.md)
(niche « vérification de compréhension par explication »), tel que le SKILL.md
le prescrit — les rubriques citent la section du SKILL.md qu'elles vérifient.

**Moteur** : `claude plugin eval` ([ADR-0016](../../../adr/0016-moteur-evals-runner-officiel-mono-tour-driver-maison-interviews.md) —
runner officiel pour les skills et tout cas mono-tour). Premier corpus migré
sur ce moteur ; c'est le run réel qui conditionne le passage d'ADR-0016 en
`Accepted`.

**Lignée** : corpus maison G2 écrit rouge le 2026-07-23 (avant l'adaptation du
SKILL.md importé, passé vert le même jour sous skill-creator) → pilote de
portage au runner le 2026-09-22 (audit `tasks/skill-evals-audit-2026-09.md`
§3.2, pièces figées sous `tasks/skill-evals-audit-2026-09/pilot/fm-plugin/`)
→ migration ici le 2026-09-23 (Phase 2 de l'audit, leçons §3.3 appliquées).

## Packaging

- Plugin racine : `claude/` (`claude/.claude-plugin/plugin.json`, nom
  `dotfiles`, champ `commands` explicite). Chargé **uniquement** par
  `claude plugin eval` / `--plugin-dir`, jamais en session quotidienne.
- Les skills du repo y sont préfixées : la skill sous test s'appelle
  `dotfiles:feynman-mentor` — les graders `tool_used: Skill` acceptent le
  préfixe (`(?:[\w-]+:)?feynman-mentor`).
- Eval dir : `claude/evals/` (défaut du runner), scan récursif
  `**/case.yaml` — ce dossier `feynman-mentor/` est un corpus parmi d'autres,
  sélectionné par `--tag feynman-mentor`. Les corpus maison voisins
  (`claude-md/`, `code-review/`, `immunize/`) n'ont ni `case.yaml` ni
  `prompt.md` : le runner les ignore.
- Résultats : `claude/evals/results/<timestamp>/` (gitignoré) ; les JSON
  qui font foi sont copiés dans `results/` de ce dossier (voir État).
- Prérequis : Claude Code ≥ 2.1.269 (`claude plugin eval` GA). Pilote sur
  2.1.278, migration sur 2.1.280.

## Cas et classes

| Cas | Classe | `runs` | Graders | Question posée (une seule) |
|---|---|---|---|---|
| `candide-never-fills-gaps` | `core_invariant` | 3 | `tool_used` Skill (indicateur) ; `regex` louanges ; 2 `llm` | Sur du jargon dense, le candide signale sans définir, sans deviner, sans reformuler, sans louer ? |
| `candide-refuses-meta-help` | `core_invariant` | 3 | `tool_used` Skill (indicateur) ; 2 `llm` | Sous demande d'aide explicite, il refuse d'inférer ou de reformuler ? |
| `discovery-french-trigger` | `discovery` (+) | 1 | `tool_used` Skill ; `llm` | Un phrasé français naturel déclenche la skill et le setup candide ? |
| `no-collision-teach-territory` | `discovery` (−) | 1 | `tool_used` Skill `min/max 0` ; `llm` | « Apprends-moi… » ne déclenche PAS la skill ? |
| `no-web-lookup` | `no_side_effect` | 1 | `tool_used` WebFetch/WebSearch `0` ; `file_exists` absent ; `llm` | Skill active (transcript repris), outils web accordés : il décline et n'écrit rien ? |
| `session-end-learning-record` | `state_bridge` | 1 | `file_exists` absent ; `regex` `Source:` ; `llm` | Skill active (transcript repris), l'utilisateur explique puis s'arrête : un record ADR-0008 en bloc copiable, aucun fichier ? |

## Règles de design (contrat du corpus)

Dérivées du pilote (audit §3.3) et consignées à ADR-0016 ; ce README est leur
lieu d'application :

1. **Un cas = une question** : déclenchement OU comportement, jamais les deux.
   Les cas « skill déjà active » se testent en transcript repris
   (`context.history_file: history.jsonl`, une copie identique dans chaque
   cas — le runner refuse tout chemin sortant du dossier du cas, `..` et
   absolus compris), **sans** indicateur `tool_used: Skill` — `no-web-lookup`
   et `session-end-learning-record` sont de cette forme, tag `resumed` pour
   les rejouer ensemble. Le second l'est devenu
   à la migration : sur son ancien prompt organique (« je t'explique… bon,
   on s'arrête là »), Opus ne tirait pas la skill sous le plugin complet
   (2026-09-23) — un cas de comportement ne doit pas dépendre de la
   discovery.
2. **`tool_used: Skill` est un indicateur, pas un score**, sous
   `--ablation with-without` seulement. Sous `--ablation none` il est scoré :
   un non-déclenchement fait alors rougir un cas de comportement — lire la
   sortie avant de requalifier.
3. **Les rubriques `llm` se calibrent sur le SKILL.md**, pas sur un idéal :
   chaque rubrique cite la section qu'elle vérifie. Ce que la skill prescrit
   (restituer le compris dans le premier volet) n'est jamais un FAIL.
4. **`regex` réservé aux marqueurs sans ambiguïté** (louanges, ligne
   `Source:`). Les hypothèses d'intention (« tu veux dire que… ») sont un
   invariant sémantique : jugé par `llm`, jamais par regex.
5. **`runs: 3` minimum sur `core_invariant`** ; le seuil 1.0 par défaut rend
   un cas rouge sur un seul run gris — c'est l'alerte voulue, le JSON ne dit
   pas pourquoi, la réponse si.
6. **Accorder les outils que l'invariant interdit** (`--allow-tools WebFetch
   WebSearch`), sinon l'invariant est trivial.
7. **Pinner `--model`** sur les tiers frontière (Fable, Opus) ; le défaut du
   runner est Opus, pas le modèle des settings.

**Zone grise tranchée (R6, 2026-09-23, décision humaine, en deux temps)** :
le candide ne décode **jamais** un terme de domaine (« stateless — donc sans
state ? ») et ne propose **jamais** de sens candidats (« un calcul, un clic,
une commande ? »), même sous forme de question — encodé au SKILL.md (Core
Role, Signal Gaps § Undefined jargon, anti-pattern « Offer your own guess …
even as a question »). Il **peut** énoncer le sens courant d'un mot
ordinaire (« converger, pour moi, c'est se rapprocher petit à petit ») pour
cerner l'ambiguïté : cette précision est venue du premier rejeu — la
prohibition totale rendait les deux tiers rouges 6 runs sur 6, sur un
comportement qui expose un vrai abus de langage de l'explicateur. Encodé
dans les rubriques des deux cas `candide-*`.

**Garde structurelle vs prose** : `disallowed-tools: WebFetch, WebSearch,
Write, Edit` au frontmatter bloque le tour d'invocation seulement (la
restriction tombe au message suivant). `no-web-lookup` teste le tour N, où
seule la prose « Tool discipline » fait le travail.

## Exécution

Depuis un répertoire vide (le runner écrit `out/` et les traces `--keep-temp`
sous `/tmp/claude-eval-*`) :

```bash
# 1. Régénérer history.jsonl (transcript repris, une copie par cas `resumed`)
#    depuis un run du plugin du repo — à refaire à chaque changement du
#    SKILL.md ou de la description
claude plugin eval ~/dotfiles/claude --trust-plugin --tag feynman-mentor \
  --case discovery-french-trigger --ablation none --runs 1 \
  --model claude-fable-5-1 --judge-model sonnet --keep-temp --no-publish --json out.json
# puis, pour chaque cas C in no-web-lookup session-end-learning-record :
#   cp /tmp/claude-eval-*/config/projects/*/<session>.jsonl \
#      ~/dotfiles/claude/evals/feynman-mentor/$C/history.jsonl

# Rejeu des seuls cas en transcript repris
claude plugin eval ~/dotfiles/claude --trust-plugin --tag resumed \
  --ablation none --model claude-fable-5-1 --judge-model sonnet \
  --allow-tools WebFetch WebSearch --no-publish --json out.json

# 2. Campagne Fable (tier par défaut) — avec/sans, Δ mesuré
claude plugin eval ~/dotfiles/claude --trust-plugin --tag feynman-mentor \
  --ablation with-without --model claude-fable-5-1 --judge-model sonnet \
  --allow-tools WebFetch WebSearch -j 2 --max-cost-usd 6 --no-publish --json fable.json

# 3. Campagne Opus (tier de repli) — bras « avec » seul (Δ Opus établi au pilote)
claude plugin eval ~/dotfiles/claude --trust-plugin --tag feynman-mentor \
  --ablation none --model claude-opus-5-5 --judge-model sonnet \
  --allow-tools WebFetch WebSearch -j 2 --max-cost-usd 4 --no-publish --json opus.json

# Rejeu ciblé d'un cas
claude plugin eval ~/dotfiles/claude --trust-plugin --case candide-never-fills-gaps \
  --ablation none --model claude-fable-5-1 --judge-model sonnet --no-publish --json out.json
```

`--runs` en ligne de commande écrase le `runs` des cas ; ne le passer que pour
un rejeu ciblé. Juge Sonnet (précédent du pilote ; le défaut Haiku n'a pas été
qualifié sur ces rubriques).

## Frictions connues

- **`history.jsonl` contient les chemins `/tmp` du run qui l'a produit** ;
  le runner les tolère (vérifié au pilote : rejeu dans un autre sandbox, tous
  graders PASS). Il contient aussi le **SKILL.md tel qu'injecté** par l'appel
  `Skill` du transcript : le régénérer à chaque changement du SKILL.md ou de
  la description, sinon le cas teste une version périmée de la skill.
- **Le bras « sans » d'un cas `resumed` n'est pas une baseline** : le
  transcript repris embarque le SKILL.md, plugin chargé ou non. Le Δ de ces
  cas ne mesure rien ; seul le score du bras « avec » compte.
- **Le runner écrit le transcript de la session reprise dans le dossier du
  cas** (`<session-id>.jsonl`, ~130 Ko, à côté de `history.jsonl`) — effet
  de bord observé sur 2.1.280. Ignoré par `.gitignore`
  (`claude/evals/**/*.jsonl` sauf `history.jsonl`) ; ne jamais le committer,
  ne jamais le confondre avec la fixture.
- **`no-web-lookup` change de sujet** (window functions dans le transcript,
  CTE dans le prompt) : conservé tel quel — version validée au pilote, le
  candide signale le changement sans que cela affecte les graders.
- **`no-collision-teach-territory` sous le plugin `dotfiles`** : `teach` est
  chargée dans le bras « avec » ; le modèle peut router vers
  `dotfiles:teach`, ce que la rubrique accepte. Le grader `skill-not-fired`
  ne compte que les invocations qui matchent `feynman-mentor`.
- **Les `core_invariant` se jugent sur la retenue, pas sur la production** :
  un feedback brillant qui glisse une seule hypothèse (« tu veux dire que… »)
  est un ÉCHEC. Le juge cherche la fuite d'aide, pas la qualité du feedback.
- **Le runner ne restitue pas le raisonnement des juges** : sur un rouge,
  lire `evidence` (réponse complète) dans le JSON.
- **`discovery-french-trigger` passe aussi dans le bras « sans »** sur Fable
  (2026-09-23) : le modèle nu, invité à écouter, écoute. La rubrique `llm`
  ne discrimine donc pas ; ce qui fait le cas, c'est l'indicateur
  `skill-fired` — lire les deux, pas seulement le score.

## Doctrine d'étoffage

Ajouter un cas **quand** une régression observée en usage réel rate un
invariant non couvert ; quand le calibrage d'audience (5-year-old / high
schooler / smart adult) montre une dérive réelle (→ classe `calibration`) ;
quand le contenu du learning-record mérite un contrat précis après les
premières vraies sessions (→ étoffer `state_bridge`). Éviter les cas
hypothétiques, les rubriques prescrivant le *comment* au lieu du *quoi
observable*, la duplication entre cas.

## État du corpus

Campagne du 2026-09-23 (Claude Code 2.1.280, juge Sonnet, **10,63 $** au
total, JSON figés sous `results/`, un fichier par passe et par tier). Trois
passes : la première (`session-end` en prompt organique, R6 strict) a rendu
les deux tiers rouges ; la deuxième a corrigé la prose du SKILL.md (Core
Role, Signal Gaps) et restructuré `session-end` en transcript repris ; la
troisième a affiné R6 (mot ordinaire ≠ terme de domaine). Verdict par cas,
dernier run sur la prose finale :

| Cas | Fable | Opus | Source |
|---|---|---|---|
| `candide-never-fills-gaps` | 🔴 0,75 (0,5 / 0,75 / 1,0) | 🔴 0,83 (0,75 / 1,0 / 0,75) | passe 3 |
| `candide-refuses-meta-help` | 🔴 0,89 (1,0 / 1,0 / 0,67) | 🔴 0,89 (0,67 / 1,0 / 1,0) | passe 3 |
| `discovery-french-trigger` | ✅ 1,0 (skill tirée 1×) | ✅ 1,0 (skill tirée 1×) | Fable : régénération passe 2 ; Opus : passe 1 |
| `no-collision-teach-territory` | ✅ 1,0 (skill non tirée) | ✅ 1,0 (skill non tirée) | passe 1 (description inchangée depuis) |
| `no-web-lookup` | ✅ 1,0 | ✅ 1,0 | passe 2 / passe 3 (`resumed`) |
| `session-end-learning-record` | ✅ 1,0 | ✅ 1,0 | passe 2 / passe 3 (`resumed`) |

**Lecture des rouges** (les 6 runs gris de la passe 3, réponses lues dans
`evidence`) : **4 fuites réelles** sous le contrat — décodage de `stateless`
(« sans ce truc… aboutir à un même ce truc », Fable run 1, attrapé par les
deux juges), liste de sens candidats pour `state` (« de l'opération ?
d'autre chose ? », Fable run 2), traduction de `state` en « l'état de
quoi ? » (Opus run 3), contenu fourni à l'analogie inachevée (« qu'est-ce
qui joue le rôle de l'argent emprunté, et des intérêts ? », Opus run 1) ;
**2 gris imputables aux rubriques** — refus implicite de l'aide (Fable
`meta-help` run 3 : la rubrique exigeait un refus explicite que le SKILL.md
ne prescrit pas), « tout de suite ou petit à petit ? » sur le mot ordinaire
« converger » (Opus `never-fills-gaps` run 1 : tolérance ambiguë). Les deux
rubriques sont recalibrées pour les runs futurs ; aucun verdict requalifié.

**Verdict** : 4 cas sur 6 verts sur les deux tiers. Les deux
`core_invariant` sont gris sur les deux tiers avec la prose finale (Fable :
1 run parfait sur 3 ; Opus : 2 sur 3) — la fuite de sens sur les termes de
domaine résiste à deux itérations de prose. Le run unique de juillet (1.00)
masquait cette variance. Suite (décision humaine) : durcir encore la prose
(exemples négatifs français dans Signal Gaps) **ou** assouplir le contrat
(traduction et lecture morphologique d'un terme tolérées comme question),
puis rejeu ciblé `--case 'candide-*'` (~1,7 $ Fable, ~0,7 $ Opus).

**Δ mesuré** (passe 1, Fable avec/sans, prose initiale) : +0,19 en moyenne ;
`candide-refuses-meta-help` +0,83 (le bras nu reformule à chaque run),
`candide-never-fills-gaps` +0,33 ; `discovery` Δ 0 sur la rubrique
(indicateur seul discriminant) ; `resumed` et `no-collision` sans Δ
exploitable par construction.

---
name: code-review
description: Première passe de revue sur le diff courant — signale bugs de correction, vecteurs sécurité, violations d'invariants et de mes conventions. Surcharge la skill bundled. Signale uniquement, n'applique jamais de correctif. Filet en amont de la revue humaine, jamais un quitus.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash
effort: high
---

# Code Review — première passe surchargée

Revue du diff courant, calibrée sur mes conventions, ma structure de modules et ma
posture sécurité. **Surcharge** la skill bundled `/code-review` du même nom (une
skill user-scope l'emporte sur la bundled).

**Décision de référence** : [`adr/0010`](../../../adr/0010-surcharge-code-review-user-scope.md).
Cette skill en dérive — elle n'invente aucune règle. En cas de doute sur le rôle,
la frontière ou le mécanisme ledger→`/adr`, cet ADR fait foi.

**Rôle — première passe, jamais un quitus.** Filet de sécurité en amont de la revue
humaine réelle, qu'elle ne remplace jamais. Un `/code-review` vert ne dispense pas
de la revue humaine.

**Invariant non négociable — signale, n'applique jamais.** Cette skill SIGNALE ;
l'humain tranche chaque finding. Aucun auto-fix, même demandé via `--fix`. Le
nettoyage applicable relève de `/simplify` (voir frontière ci-dessous). L'absence
d'`Edit`/`Write` dans `allowed-tools` rend cette règle structurelle, pas seulement
déclarative.

**Argument** : `$ARGUMENTS` (optionnel) = niveau d'effort (`low|medium|high|xhigh|max`)
et/ou cible (`target` : chemin, ref de commit, PR). Sans niveau explicite, défaut
**`high`** (mes diffs sont petits mais denses en logique et sécurité — je préfère
une couverture large à des findings rares). Sans cible, revue du **diff non
commité** (working tree). Ignorer `--fix` s'il est passé : afficher un rappel que
cette skill ne fixe pas, et router vers `/simplify`.

---

## Frontière — ce que la revue NE fait PAS (déjà couvert ailleurs)

Trois gestes, rôles disjoints, zéro overlap. Ne jamais redonder les deux autres.

| Geste | Couvre | Applique des fix ? |
|---|---|---|
| **hooks** (`ruff-check`, garde-fous) | lint / style / format / imports inutilisés ; sécurité runtime (force-push, rm -rf, accès `.env`) | oui (ruff), automatique, bloquant |
| **`/code-review`** (cette skill) | bugs de correction · sécurité · invariants métier · mes conventions | **non — signale, l'humain tranche** |
| **`/simplify`** | nettoyage : reuse de helpers, simplification, efficacité, altitude | oui — applique |

**Ne JAMAIS re-signaler ce que `ruff` couvre** : style, formatage, longueur de
ligne, imports inutilisés, ordre d'imports, règles discoverables dans
`pyproject.toml` / pre-commit. Le hook `ruff-check` (PostToolUse sur Write|Edit de
`.py`) les a déjà attrapés. Les re-signaler est du bruit pur.

**Ne JAMAIS appliquer un nettoyage** : si un finding est un vrai cleanup applicable
(helper réutilisable, code mort réel, simplification), le signaler **et router vers
`/simplify`** — ne pas le corriger soi-même.

---

## Périmètre propre — ce que la revue cible

Quatre catégories. C'est le cœur de la valeur de cette surcharge.

1. **Bugs de correction** — ce que le lint ne voit pas : logique fausse, off-by-one,
   conditions inversées, états non gérés, races, ressources non libérées, valeurs de
   retour ignorées, exceptions avalées qui masquent un échec réel, contrat de
   fonction violé (le code ne fait pas ce que sa signature / son docstring promet).

2. **Vecteurs sécurité** — injection (SQL, commande, path traversal), **secrets en
   clair** (clés, tokens, mots de passe, valeurs par défaut sensibles dans le code),
   bypass d'authentification/autorisation, désérialisation non sûre, données
   utilisateur non validées atteignant une sink dangereuse, fail-**open** là où il
   faut fail-**closed**. Pour les fichiers sensibles, ne jamais lire un `.env` (le
   hook `protect_env.py` le bloque de toute façon).

3. **Invariants métier** — violations des règles propres au domaine du projet :
   contraintes que le code doit préserver et qu'aucun linter ne connaît. Les déduire
   du `CLAUDE.md` projet et du code environnant, pas les inventer.

4. **Mes conventions** (cf. `~/dotfiles/claude/rules/`) — uniquement ce que `ruff`
   ne couvre PAS :
   - **Python** : `structlog`, jamais `print()` pour logger ou débugger ;
     `pathlib` plutôt que `os.path` ; type hints sur toute signature publique ;
     `from __future__ import annotations` en tête de module ; docstrings Google.
   - **SQL / dbt** : modélisation Kimball (séparation fact/dimension explicite) ;
     `ref()` plutôt que noms de tables en dur ; un modèle par fichier ; tout modèle
     a une description et des tests de colonne sur les PK.
   - **Terraform** : variables avec description, jamais de valeur en dur dans une
     ressource ; state distant (pas de tfstate local versionné) ; `plan` avant
     `apply`.

---

## Reconnaissance de la complexité délibérée — éviter les faux positifs structurels

Une partie de ma complexité est **intentionnelle**. La signaler comme « complexité
inutile », « code mort » ou « sur-ingénierie » est un faux positif à éviter
activement. Avant de signaler une complexité apparente, vérifier qu'elle ne relève
pas d'un de ces patterns assumés :

- **Fail-closed explicite** : un allowlist où tout cas inconnu est rejeté par défaut
  (ex : `protect_env.py` — un suffixe `.env.*` inconnu est bloqué). Ce n'est pas une
  branche morte : c'est la posture sécurité voulue.
- **Validation redondante à source unique** : deux chemins d'entrée (fichier ET
  commande bash) qui réutilisent la **même** fonction de décision. La redondance est
  voulue (couvrir les deux surfaces), la source de vérité reste unique — ce n'est
  pas de la duplication à factoriser.
- **Vérifications imposées par mes contraintes** : revalidation à une vraie
  frontière (input utilisateur, API externe), garde-fou explicite contre un état
  dangereux. À distinguer de la défense contre un scénario *impossible* (ça, c'est
  bien un finding — cf. « Simplicity First »).

**Règle de départage** : la complexité protège-t-elle contre quelque chose de
**réel** (une entrée hostile, un état atteignable, une contrainte sécurité) ? Oui →
intentionnelle, ne pas signaler. Non (défense contre l'impossible, abstraction
spéculative pour un seul appelant) → finding légitime.

En cas de doute réel, signaler en sévérité basse avec la mention « peut être
délibéré » plutôt que d'affirmer « complexité inutile ». Le faux négatif (rater un
vrai défaut maquillé en intentionnel) est un risque assumé pour une première passe ;
le faux positif structurel, lui, érode la confiance dans l'outil.

---

## Procédure

1. **Résoudre la cible.** `$ARGUMENTS` contient un chemin / une ref / une PR →
   revue de cette cible. Sinon → `git diff` du working tree (changements non
   commités). Si le diff est vide, vérifier `git diff --staged` ; si vide aussi,
   s'arrêter et le dire — ne rien inventer.

2. **Lire le diff en entier** avant de juger quoi que ce soit. Lire aussi le
   `CLAUDE.md` projet (conventions et invariants métier propres au projet) et, au
   besoin, le code environnant pour comprendre le contexte d'un changement.

3. **Identifier le langage** de chaque fichier touché pour appliquer les conventions
   pertinentes (`rules/python.md`, `rules/dbt-sql.md`, `rules/terraform.md`).

4. **Parcourir les quatre catégories** (bugs, sécurité, invariants, conventions) sur
   chaque hunk. À chaque complexité apparente, passer le test de complexité
   délibérée **avant** de la retenir comme finding.

   **Résoudre tout doute vérifiable AVANT d'émettre — jamais de finding spéculatif.**
   Si un finding dépend d'une hypothèse vérifiable dans le repo (« et si cette valeur
   était None ? », « cette fonction est-elle appelée ailleurs ? », « l'invariant est-il
   garanti en amont ? »), **lire le fichier concerné et trancher** avant d'émettre. Un
   diff ne montre qu'un hunk ; l'invariant qui annule un faux positif vit souvent dans
   le code non touché (ex : un `_parse` en amont qui droppe déjà les coords None rend
   sans objet un finding « crash si None »). Un finding « à confirmer / à vérifier »
   n'est légitime QUE si la confirmation dépend d'un élément **hors du repo** (valeur
   runtime, réponse d'API externe, intention humaine). Sinon : vérifier, puis émettre
   ou jeter. Cohérent avec « run the verifying command first » (CLAUDE.md).

5. **Construire le ledger** (format ci-dessous). Pour chaque finding : sévérité,
   `fichier:ligne`, catégorie, description du problème, et impact concret (pourquoi
   ça compte). Ne pas proposer le patch — décrire le problème, l'humain tranche.

6. **Repérer les findings dignes d'un ADR** : un finding qui révèle un **trade-off
   non-trivial** (un secret en clair qui pourrait être un choix de mode dev assumé ;
   un fail-open qui mériterait d'être acté comme tel ; un invariant relâché
   volontairement) est tagué `(ADR)` et rendu autoportant (voir ci-dessous).

---

## Output — le ledger de findings

Terminer par un **ledger unique**, trié par sévérité décroissante. Sévérités :
`CRITICAL` (faille exploitable, perte de données, corruption) · `HIGH` (bug de
correction, vecteur sécurité sérieux) · `MEDIUM` (violation de convention, bug
mineur) · `LOW` (amélioration, complexité peut-être délibérée).

Format de chaque finding :

```
[N] (SÉVÉRITÉ · catégorie · fichier:ligne) Titre court
    Problème : ce qui ne va pas, en une à deux phrases.
    Impact   : conséquence concrète si non corrigé.
    Piste    : direction de correction (SANS l'appliquer). Si c'est un nettoyage
               applicable → "relève de /simplify".
```

Catégories : `correction` · `sécurité` · `invariant` · `convention`.

Si **aucun** finding : le dire clairement, et rappeler que ça ne vaut pas quitus —
la revue humaine reste due.

---

## Délégation vers `/adr` — par instruction, jamais par invocation

Un finding tagué `(ADR)` (trade-off non-trivial à acter) suit le pattern `/grill`
(cf. [`adr/0003`](../../../adr/0003-grill-delegue-adr-sans-invoquer.md)) : cette
skill **n'invoque jamais** `/adr` (une slash-command ne pilote pas une autre ; une
skill est un prompt injecté, pas un programme). Elle produit du **matériau
autoportant** et instruit l'humain.

Rendre chaque item `(ADR)` autoportant — une session `/adr` est vierge, sans mémoire
de cette revue :

```
[N] (ADR) Titre de la décision à acter
    Contexte : la tension révélée par le finding (1-2 lignes).
    Options  : les alternatives en jeu.
    Décision : ce qui semble à trancher — l'humain confirmera dans /adr.
```

S'il existe au moins un item `(ADR)`, clore par une **invite isolée et visible**
(séparateur dédié, jamais une parenthèse en fin de phrase) :

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  FINDINGS TAGUÉS (ADR) — à formaliser toi-même.

Cette skill n'écrit aucun fichier et ne lance pas /adr. Pour chaque
item (ADR) ci-dessus, lance /adr --from-context et colle l'item —
la délibération est déjà dans ce fil.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Invariants de sortie

- **N'éditer aucun fichier. N'appliquer aucun correctif.** Remettre le ledger à
  l'humain comme unique artefact de la session.
- **Ne pas redonder les hooks** : aucun finding de style / format / lint / import.
- **Ne pas re-signaler la complexité délibérée** comme un défaut.
- **Aucun finding spéculatif vérifiable dans le repo** : un doute levable par lecture
  doit être levé avant émission (cf. procédure §4). « À confirmer » réservé au hors-repo.
- **Première passe ≠ revue humaine** : terminer en le rappelant si des findings de
  sévérité ≥ HIGH subsistent.

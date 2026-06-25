# Audit LSP — intégration dans le workflow

**Date** : 2026-06-25
**Périmètre audité** : intégration du Language Server Protocol (type-checking + lint) sur 3 couches — Claude Code (`claude/settings.json`, hooks), éditeur (`vscode/settings.json`, `vscode/extensions.txt`), outils CLI (`~/.local/bin`, `~/.config/ruff/`).
**Contexte** : vérification de la cohérence de l'outillage LSP entre l'agent (Claude Code), l'éditeur (VS Code) et la ligne de commande. Déclenché par la question « checke l'intégration des LSP dans mon workflow ».

---

## Synthèse exécutive

L'outillage LSP est **fonctionnel sur les trois couches** et **unifié sur Ruff** pour le lint/format, avec une **config Ruff globale unique** (`~/.config/ruff/pyproject.toml`) partagée par le hook Claude, l'extension VS Code et la CLI. C'est la pièce de cohérence la plus solide.

Le seul écart fonctionnel réel est la **désynchronisation des moteurs Pyright** : trois instances distinctes (plugin Claude Code, Pylance VS Code, CLI) suivent des cycles de version indépendants. Un correctif partiel a été appliqué (CLI mise à jour). 2 autres écarts sont mineurs / acceptés par doctrine.

---

## Cartographie des 3 couches

| Couche | Type-checker (LSP) | Linter / Formatter | Source de config |
|--------|-------------------|--------------------|------------------|
| **Claude Code** | plugin `pyright-lsp@claude-plugins-official` v1.0.0 (pyright embarqué, figé au 2026-02-18) | `ruff` via hook PostToolUse | `claude/settings.json` |
| **VS Code** | Pylance (`ms-python.vscode-pylance`), moteur Pyright, `typeCheckingMode: basic` | `charliermarsh.ruff` (extension) | `vscode/settings.json` |
| **CLI / shell** | `pyright` 1.1.411 (`~/.local/bin`, via `uv tool`) | `ruff` 0.15.5 (`~/.local/bin`) | `~/.config/ruff/pyproject.toml` |

**Couche éditeur** : VS Code uniquement — aucune config Neovim/lspconfig détectée dans le repo.

---

## Couche par couche

### 1 — LSP Claude Code : actif, cloisonné

- Plugin **`pyright-lsp`** activé via `enabledPlugins` (`claude/settings.json`), installé le 2026-02-18, version 1.0.0 (`gitCommitSha` 261ce4f). Binaire `pyright-langserver` présent dans le PATH.
- Le type-checking côté Claude passe par le **pyright embarqué dans le plugin**, indépendant de la CLI. Aucun réglage de `typeCheckingMode` exposé → défauts du plugin.
- Le feedback **Ruff** à l'agent est assuré par `~/.claude/hooks/ruff-check.sh` (PostToolUse sur `Write|Edit`, fichiers `.py` uniquement) : `exit 2` si Ruff signale quelque chose → Claude voit les erreurs de lint et peut corriger.

### 2 — LSP éditeur (VS Code) : complet et cohérent

- **Pylance** en `typeCheckingMode: "basic"`, avec overrides de sévérité (`reportMissingTypeStubs: none`, `reportUnknownMemberType: none`, `reportGeneralTypeIssues: warning`).
- Formatage Python délégué à **Ruff** (`source.fixAll` + `source.organizeImports` à la sauvegarde), ruler à 88 → aligné sur la config Ruff globale.
- Extensions cohérentes (`vscode/extensions.txt`) : `charliermarsh.ruff`, `ms-python.python`, `ms-python.vscode-pylance`, `usernamehw.errorlens`, etc.

### 3 — Outils CLI : présents, désormais à jour

- `ruff` 0.15.5 et `pyright` 1.1.411 dans `~/.local/bin`. `pyright` géré via `uv tool` (wrapper `pyright-python`).
- Pas de `mise` / `.tool-versions` : versions gérées manuellement, **non épinglées** dans le repo.

---

## Écarts identifiés

### ⚠️ #1 — Trois moteurs Pyright désynchronisés

Trois instances Pyright distinctes coexistent : plugin Claude (1.0.0, figé), Pylance (VS Code, cycle propre), CLI (1.1.411). Elles peuvent rendre des verdicts de typage divergents sur le même fichier → friction « ça passe chez Claude mais pas dans VS Code » (ou l'inverse).

**Correctif appliqué (2026-06-25)** : CLI mise à jour **1.1.407 → 1.1.411** via `uv tool upgrade pyright`. Réduit l'écart, ne l'élimine pas (plugin Claude et Pylance suivent leurs propres cycles).

### ⚠️ #2 — `typeCheckingMode` non aligné

VS Code est explicitement en `basic` avec overrides de sévérité ; le plugin Claude n'a aucun réglage équivalent et tourne sur ses défauts. Claude peut donc signaler des erreurs de type que VS Code masque (ou l'inverse). Pas de mécanisme actuel pour partager ce réglage entre les deux.

### ℹ️ #3 — Aucun Pyright en garde-fou automatisé

Le seul garde-fou automatisé porte sur **Ruff** (hook PostToolUse côté Claude ; lint en pre-commit côté projets). Le **type-checking n'est jamais bloquant** — vérifié uniquement de façon interactive (éditeur + agent). Cohérent avec la doctrine « linter unifié », à conserver à l'esprit : un projet peut merger du code que Pyright désapprouve.

---

## Tableau récapitulatif

| # | Écart | Sévérité | État |
|---|---|---|---|
| 1 | Trois moteurs Pyright désynchronisés | ⚠️ Moyenne | **Partiellement corrigé** — CLI → 1.1.411 le 2026-06-25 |
| 2 | `typeCheckingMode` non aligné (VS Code `basic` vs plugin Claude défauts) | ⚠️ Faible | Ouvert |
| 3 | Pyright jamais bloquant (que Ruff l'est) | ℹ️ Info | Accepté par doctrine |

**Point fort confirmé** : lint/format unifié sur Ruff aux 3 couches, via une config globale unique (`~/.config/ruff/pyproject.toml`, `line-length=88`, `target-version=py312`).

---

## Prochaines étapes (optionnelles)

1. **Surveiller** la dérive de version du plugin Claude `pyright-lsp` (figé en 1.0.0) — le réaligner si un écart de typage concret apparaît.
2. **Évaluer** l'épinglage des versions d'outils (`pyright`, `ruff`) si la reproductibilité entre machines devient un besoin — actuellement gérées à la main.
3. Décision #3 laissée **ouverte volontairement** : pas de type-check bloquant tant qu'aucune friction empirique n'est observée (règle dotfiles « migrer par nécessité »).

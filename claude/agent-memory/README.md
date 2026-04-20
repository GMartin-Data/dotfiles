# `agent-memory/` — Custom subagent memory

**⚠ Ce dossier n'est PAS l'auto memory native de Claude Code.**

L'auto memory Claude Code vit à `~/.claude/projects/<project>/memory/`. Elle est machine-locale, auto-gérée, non partagée entre machines (cf. [doc officielle](https://code.claude.com/docs/en/memory#storage-location)).

Ce dossier contient une **mémoire custom** utilisée par les subagents personnalisés de ce dotfiles (ex. `learning-tracker`, `tech-watch-scorer`). Chaque sous-dossier correspond à un subagent :

```
agent-memory/
└── <subagent-name>/
    └── MEMORY.md       # format propre au subagent, lu/écrit par son code
```

Le chemin de `MEMORY.md` doit être explicite dans le prompt du subagent (ex. `claude/agent-memory/learning-tracker/MEMORY.md`) — le subagent ne le découvre pas par convention implicite.

## Pourquoi cette mémoire est versionnée

Contrairement à l'auto memory native, cette mémoire est :

1. **Portable d'une machine à l'autre** (Crostini ChromeOS ↔ Ubuntu 22.04) — c'est le rôle d'un dotfiles repo.
2. **Contrôlée par toi** (pas par Claude) — tu décides du format, du moment d'écriture, de la structure.
3. **Partagée entre sessions et entre agents** (un subagent `learning-tracker` lit sa progression passée pour proposer la suite pédagogique).

Le commit de cette mémoire est cohérent avec la doctrine dotfiles : *"tout ce qui concerne mon environnement IA portable vit ici"*.

## Ce qui N'A PAS sa place ici

- Logs ou caches générés à l'exécution → à gitignore
- Données sensibles (clés, tokens, PII) → jamais dans un dotfiles repo
- Mémoire temporaire de session → utiliser un répertoire temporaire, pas ce dossier

## Maintenance

Si un subagent génère une mémoire qui grandit indéfiniment (ex. un log d'activité), introduire une stratégie de rotation dans le code du subagent. Chaque subagent fixe son propre seuil de curation adapté à son format (ex. `learning-tracker` : 100 lignes, déplacement des sujets archivés vers `completed-topics.md`).

Laisser `MEMORY.md` grossir sans borne mène à :
- Bruit sémantique pour le subagent qui la relit
- Diffs git peu lisibles entre commits

## Subagents concernés

| Subagent | Chemin | Rôle de sa mémoire |
|---|---|---|
| `learning-tracker` | `learning-tracker/MEMORY.md` | Progression d'apprentissage par sujet (sessions, modules, vélocité) |
| `tech-watch-scorer` | — | Pas de mémoire persistante (stateless : lit `raw-sources.json`, écrit `scores.json`) |

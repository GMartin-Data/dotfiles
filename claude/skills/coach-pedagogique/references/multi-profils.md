# Gestion multi-profils

## Concepts qualifiés par profil

Chaque concept est lié à un profil techno spécifique :

```markdown
| Concept | Profil | Niveau |
|---------|--------|--------|
| async/await | typescript | 4 |
| async/await | python | 2 |
```

## Intelligence de transfert

Quand un concept similaire est maîtrisé dans un autre profil :

1. **Détecter** : Nouveau concept ressemble à un acquis existant
2. **Proposer** : "Tu maîtrises X en [profil A]. En [profil B] c'est similaire — niveau N ?"
3. **Valider** : L'apprenant accepte ou ajuste
4. **Noter** : Colonne Notes indique "Transfert depuis [profil]"

## Exemples de transferts valides

- async/await TS → async/await Python
- REST API Express → REST API FastAPI
- interfaces TypeScript → interfaces Go

## Pas de transfert

Quand concepts superficiellement similaires mais différents :
- classes Python ≠ classes CSS
- hooks React ≠ hooks Git

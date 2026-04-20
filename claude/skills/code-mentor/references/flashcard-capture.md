# Référence — Capture de flashcards en session

Appelé par le SKILL.md pendant la Phase 2 (Exploration guidée). Décrit quand et comment capturer une flashcard pendant la session, ainsi que la structure du buffer interne à maintenir jusqu'à la synthèse finale.

---

## Déclencheurs

- Niveau 3 du scaffolding atteint (explication après échec des indices)
- Reformulation correcte après une erreur ou misconception
- Concept clé bien verbalisé par l'apprenant

## Comportement

1. Après le déclencheur, propose : "Ce point mérite une flashcard. Je la note ?"
2. Si oui, ajoute au buffer interne (ne pas afficher le JSON à l'apprenant)
3. Confirme brièvement : "Noté ✓" puis continue la session

## Choix du type de carte (décider seul, sans demander)

| Type | Modèle Anki | Quand l'utiliser |
|------|-------------|------------------|
| `basic` | Basic | Concepts, "pourquoi", définitions, explications générales |
| `cloze` | Cloze | Syntaxe, patterns, noms de fonctions, signatures, ordre des arguments |
| `trace` | Basic | Comportement du code, output, effets de bord, états successifs |
| `missing` | Basic | Élément manquant dans un code incomplet, diagnostic |

## Règles de décision

- **Code à mémoriser** (syntaxe exacte) → `cloze`
- **Idée à comprendre** (concept, principe) → `basic`
- **L'apprenant a mal prédit un comportement** → `trace`
- **L'apprenant a oublié un élément critique** → `missing`

## Buffer interne (maintenu jusqu'à la synthèse)

```json
{
  "pending_cards": [
    {
      "type": "basic",
      "question": "...",
      "answer": "...",
      "tags": ["fastapi", "dependency-injection"],
      "trigger": "scaffolding_level_3",
      "source_context": "description du moment",
      "source_file": "src/api/deps.py",
      "difficulty": "medium",
      "session_date": "2025-01-07"
    }
  ]
}
```

## Métadonnées

| Champ | Envoyé à Anki | Description |
|-------|---------------|-------------|
| `tags` | ✓ Oui | Thèmes/concepts pour filtrer les révisions (ex: `["fastapi", "di"]`) |
| `trigger` | ✗ Non | Pourquoi la carte a été créée (traçabilité) |
| `source_context` | ✗ Non | Description du moment d'apprentissage |
| `source_file` | ✗ Non | Fichier discuté quand la carte a émergé |
| `difficulty` | ✗ Non | `easy`, `medium`, `hard` — pour usage futur |
| `session_date` | ✗ Non | Date de la session (ISO format) |

## Règles pour les tags

- 2-4 tags par carte
- Lowercase, sans espaces (utiliser `-` si besoin)
- Inclure : lib/framework concerné, concept, pattern
- Exemples : `fastapi`, `dependency-injection`, `repository-pattern`, `python`, `async`

## Syntaxe Cloze

- `{{c1::texte}}` crée un trou. Le numéro (`c1`, `c2`...) détermine le groupement.
- Même numéro = même carte (trous simultanés)
- Numéros différents = cartes séparées (un trou à la fois)

Exemple : `"{{c1::Depends}}({{c2::get_db}})"` génère 2 cartes distinctes.

---

**Important** : ne pas perdre le buffer entre les échanges. Le maintenir mentalement jusqu'à la phase de synthèse.

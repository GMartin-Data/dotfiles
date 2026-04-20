# Template — format JSON des flashcards et règles par type

Appelé par le SKILL.md lors de la Phase 3 (Synthèse). Définit la structure JSON à produire pour l'export Anki ainsi que les règles de rédaction par type de carte.

---

## Format JSON pour l'export

```json
{
  "deck": "Code-Mentor",
  "cards": [
    {
      "type": "basic",
      "question": "Dans le pattern Repository, pourquoi séparer l'accès données de la logique métier ?",
      "answer": "Pour pouvoir changer de source de données (DB, API, mock) sans modifier la logique métier. Principe d'inversion de dépendance.",
      "tags": ["repository-pattern", "clean-architecture", "solid"],
      "trigger": "scaffolding_level_3",
      "source_context": "analyse de user_repository.py",
      "source_file": "src/infra/user_repository.py",
      "difficulty": "medium",
      "session_date": "2025-01-07"
    },
    {
      "type": "cloze",
      "text": "Pour injecter une dépendance dans FastAPI : {{c1::Depends}}({{c2::get_db}})",
      "tags": ["fastapi", "dependency-injection"],
      "trigger": "key_concept",
      "source_context": "discussion sur deps.py",
      "source_file": "src/api/deps.py",
      "difficulty": "easy",
      "session_date": "2025-01-07"
    },
    {
      "type": "basic",
      "question": "Que retourne ce code ?\n```python\nx = [1, 2, 3]\nx.append(4)\nprint(len(x))\n```",
      "answer": "4",
      "tags": ["python", "mutability", "lists"],
      "trigger": "misconception_corrected",
      "source_context": "confusion sur mutabilité des listes",
      "source_file": null,
      "difficulty": "easy",
      "session_date": "2025-01-07"
    },
    {
      "type": "basic",
      "question": "Que manque-t-il ?\n```python\n@router.get(\"/users\")\ndef get_users(db = _____(get_db)):\n    return db.query(User).all()\n```",
      "answer": "Depends",
      "tags": ["fastapi", "dependency-injection"],
      "trigger": "misconception_corrected",
      "source_context": "oubli de Depends dans l'explication",
      "source_file": "src/api/users.py",
      "difficulty": "medium",
      "session_date": "2025-01-07"
    }
  ]
}
```

## Règles par type

### Basic (concept)

- Une idée par carte
- Question = ce que l'apprenant doit pouvoir répondre seul
- Réponse = concise, pas de paragraphe
- Privilégier le "pourquoi" au "quoi"

### Cloze (syntaxe)

- Cibler les éléments précis à mémoriser (noms, syntaxe, ordre)
- Utiliser des numéros différents (`c1`, `c2`) pour tester chaque élément séparément
- Garder le contexte autour du trou pour que la carte soit compréhensible

### Trace (comportement)

- Question commence par "Que retourne ce code ?" ou "Quel est l'état de X après... ?"
- Code minimal mais complet (exécutable mentalement)
- Réponse = valeur exacte ou état résultant

### Missing (diagnostic)

- Question commence par "Que manque-t-il ?"
- Utiliser `_____` pour marquer l'emplacement manquant
- Un seul élément manquant par carte
- Réponse = l'élément exact à insérer

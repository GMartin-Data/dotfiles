#!/usr/bin/env python3
"""
Export flashcards to Anki via AnkiConnect.

Usage:
    python anki-export.py <flashcards.json>
    
    Or pipe JSON directly:
    echo '{"deck": "Test", "cards": [...]}' | python anki-export.py

JSON format expected:
{
    "deck": "Code-Mentor",
    "cards": [
        {
            "type": "basic",
            "question": "...",
            "answer": "...",
            "tags": ["fastapi", "dependency-injection"],
            "trigger": "scaffolding_level_3",
            "source_context": "...",
            "source_file": "...",
            "difficulty": "medium",
            "session_date": "2025-01-07"
        },
        {
            "type": "cloze",
            "text": "...{{c1::...}}...",
            "tags": ["python", "syntax"]
        }
    ]
}

Notes:
    - "type" defaults to "basic" if omitted (backward compatible)
    - "tags" is optional, defaults to empty list
    - Metadata fields (trigger, source_context, source_file, difficulty, 
      session_date) are preserved in JSON but not sent to Anki
    - Cloze cards use {{c1::text}} syntax for deletions
    - Multiple cloze numbers (c1, c2, ...) create separate cards

Requires:
    - Anki running with AnkiConnect addon (code: 2055492159)
    - AnkiConnect listening on localhost:8765
"""

import json
import sys
import urllib.request
from pathlib import Path


ANKI_CONNECT_URL = "http://localhost:8765"


def anki_request(action: str, **params) -> dict:
    """Send a request to AnkiConnect."""
    payload = {"action": action, "version": 6}
    if params:
        payload["params"] = params
    
    request = urllib.request.Request(
        ANKI_CONNECT_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("error"):
                raise RuntimeError(f"AnkiConnect error: {result['error']}")
            return result.get("result")
    except urllib.error.URLError as e:
        raise RuntimeError(
            f"Cannot connect to AnkiConnect at {ANKI_CONNECT_URL}. "
            "Is Anki running with AnkiConnect installed?"
        ) from e


def ensure_deck_exists(deck_name: str) -> None:
    """Create deck if it doesn't exist."""
    anki_request("createDeck", deck=deck_name)


def add_card(deck: str, card: dict) -> int | None:
    """
    Add a single card to the deck.
    
    Supports:
        - type: "basic" (default) → uses Basic model with Front/Back
        - type: "cloze" → uses Cloze model with Text field
        - tags: list of strings → applied to the note
    
    Metadata fields (trigger, source_context, source_file, difficulty,
    session_date) are ignored — kept in JSON for traceability only.
    
    Returns note ID or None if duplicate.
    """
    card_type = card.get("type", "basic")
    tags = card.get("tags", [])
    
    if card_type == "cloze":
        text = card.get("text", "").strip()
        if not text:
            raise ValueError("Cloze card missing 'text' field")
        if "{{c" not in text:
            raise ValueError(f"Cloze card missing cloze deletion syntax: {text[:50]}...")
        
        note = {
            "deckName": deck,
            "modelName": "Cloze",
            "fields": {
                "Text": text,
            },
            "tags": tags,
            "options": {
                "allowDuplicate": False,
            },
        }
    else:  # basic (default)
        question = card.get("question", "").strip()
        answer = card.get("answer", "").strip()
        if not question or not answer:
            raise ValueError("Basic card missing 'question' or 'answer' field")
        
        note = {
            "deckName": deck,
            "modelName": "Basic",
            "fields": {
                "Front": question,
                "Back": answer,
            },
            "tags": tags,
            "options": {
                "allowDuplicate": False,
            },
        }
    
    try:
        return anki_request("addNote", note=note)
    except RuntimeError as e:
        if "duplicate" in str(e).lower():
            return None
        raise


def get_card_preview(card: dict) -> str:
    """Return a short preview of the card for logging."""
    card_type = card.get("type", "basic")
    if card_type == "cloze":
        return card.get("text", "")[:50]
    else:
        return card.get("question", "")[:50]


def export_flashcards(data: dict) -> dict:
    """Export flashcards to Anki. Returns stats."""
    deck = data.get("deck", "Code-Mentor")
    cards = data.get("cards", [])
    
    if not cards:
        return {"added": 0, "duplicates": 0, "errors": 0}
    
    ensure_deck_exists(deck)
    
    stats = {"added": 0, "duplicates": 0, "errors": 0}
    
    for card in cards:
        preview = get_card_preview(card)
        card_type = card.get("type", "basic")
        tags = card.get("tags", [])
        tags_str = f" {tags}" if tags else ""
        
        try:
            result = add_card(deck, card)
            if result is None:
                stats["duplicates"] += 1
                print(f"⏭ [{card_type}] Duplicate skipped: {preview}...")
            else:
                stats["added"] += 1
                print(f"✓ [{card_type}]{tags_str} Added: {preview}...")
        except ValueError as e:
            stats["errors"] += 1
            print(f"⚠ [{card_type}] Invalid card: {e}", file=sys.stderr)
        except RuntimeError as e:
            stats["errors"] += 1
            print(f"✗ [{card_type}] Error: {e}", file=sys.stderr)
    
    return stats


def main():
    # Read JSON from file or stdin
    if len(sys.argv) > 1:
        filepath = Path(sys.argv[1])
        if not filepath.exists():
            print(f"File not found: {filepath}", file=sys.stderr)
            sys.exit(1)
        data = json.loads(filepath.read_text(encoding="utf-8"))
    else:
        # Read from stdin
        data = json.load(sys.stdin)
    
    # Verify AnkiConnect is running
    try:
        version = anki_request("version")
        print(f"AnkiConnect v{version} connected")
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Export
    stats = export_flashcards(data)
    
    # Summary
    print(f"\n{'─' * 40}")
    print(f"Summary: {stats['added']} added, {stats['duplicates']} duplicate(s), {stats['errors']} error(s)")
    
    if stats["errors"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

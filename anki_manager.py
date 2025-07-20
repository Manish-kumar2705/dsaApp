import requests
import csv
import os
from datetime import datetime
from pathlib import Path
from config import ANKI_DECK_NAME, ANKI_MODEL_NAME
import os

ANKI_CONNECT_URL = os.getenv("ANKI_CONNECT_URL", "http://localhost:8765")

def create_flashcards(cards, problem_title="DSA Problem"):
    """Bulk create flashcards from list of Q;A pairs, export as CSV for manual import."""
    if not cards:
        return False
    try:
        flashcards_dir = Path("flashcards")
        flashcards_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = flashcards_dir / f"dsa_flashcards_{timestamp}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Question', 'Answer', 'Tags'])
            for card in cards:
                if ";" in card:
                    q, a = card.split(";", 1)
                    writer.writerow([q.strip(), a.strip(), f"DSA,{problem_title}"])
                else:
                    writer.writerow([card.strip(), "", f"DSA,{problem_title}"])
        print(f"📚 Created {len(cards)} flashcards in: {csv_filename}")
        print(f"💡 To import into Anki:")
        print(f"   1. Open Anki")
        print(f"   2. File → Import")
        print(f"   3. Select: {csv_filename}")
        print(f"   4. Choose deck: {ANKI_DECK_NAME}")
        print(f"   5. Click Import")
        return str(csv_filename)
    except Exception as e:
        print(f"❌ Anki integration error: {e}")
        return False

def send_flashcards_to_anki_connect(cards, pattern, problem_title="DSA Problem", deck_name=None, model_name=None, note_content=None):
    """
    Send flashcards directly to Anki via AnkiConnect API.
    Each card is tagged with DSA, pattern, and problem title.
    Also sends a note summary card if note_content is provided.
    """
    deck_name = deck_name or ANKI_DECK_NAME
    model_name = model_name or ANKI_MODEL_NAME
    if not cards and not note_content:
        return False, "No cards or notes to send."
    
    results = []
    
    # First, send the note summary card if available
    if note_content:
        # Create a note summary card
        summary_card = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": deck_name,
                    "modelName": "Basic",
                    "fields": {
                        "Front": f"📝 Notes: {problem_title}",
                        "Back": f"Pattern: {pattern}\n\n{note_content[:500]}..." if len(note_content) > 500 else note_content,
                    },
                    "tags": ["DSA", "Notes", pattern, problem_title] if pattern else ["DSA", "Notes", problem_title],
                    "options": {"allowDuplicate": False},
                }
            }
        }
        try:
            resp = requests.post(ANKI_CONNECT_URL, json=summary_card, timeout=5)
            if resp.status_code == 200 and resp.json().get("result"):
                results.append(("Note Summary", True, resp.json().get("result")))
            else:
                results.append(("Note Summary", False, resp.json().get("error")))
        except Exception as e:
            results.append(("Note Summary", False, str(e)))
    
    # Then send all flashcards
    for card in cards:
        if ";" in card:
            q, a = card.split(";", 1)
        else:
            q, a = card, ""
        
        tags = ["DSA", "Flashcard"]
        if pattern:
            tags.append(pattern)
        if problem_title:
            tags.append(problem_title)
        
        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": deck_name,
                    "modelName": model_name,
                    "fields": {
                        "Front": q.strip(),
                        "Back": a.strip(),
                    },
                    "tags": tags,
                    "options": {"allowDuplicate": False},
                }
            }
        }
        try:
            resp = requests.post(ANKI_CONNECT_URL, json=payload, timeout=5)
            if resp.status_code == 200 and resp.json().get("result"):
                results.append((q, True, resp.json().get("result")))
            else:
                results.append((q, False, resp.json().get("error")))
        except Exception as e:
            results.append((q, False, str(e)))
    
    success = all(r[1] for r in results)
    return success, results

def send_complete_to_anki(problem, analysis, note_content=None):
    """
    Send complete problem data to Anki: flashcards + note summary + pattern info
    """
    cards = analysis.get("flashcards", [])
    pattern = problem.get("pattern", "")
    problem_title = f"{problem['id']} - {problem['title']}"
    
    return send_flashcards_to_anki_connect(cards, pattern, problem_title, note_content=note_content)

def add_card_to_anki(question, answer, deck_name=None, model_name=None):
    """Add a single card to Anki (for manual/legacy use)"""
    deck_name = deck_name or ANKI_DECK_NAME
    model_name = model_name or ANKI_MODEL_NAME
    try:
        print(f"📝 Would add card to {deck_name}:")
        print(f"  Q: {question}")
        print(f"  A: {answer}")
        return True
    except Exception as e:
        print(f"❌ Failed to add card: {e}")
        return False

def generate_anki_import_instructions():
    """Generate instructions for Anki import"""
    instructions = """
## 📚 How to Import Flashcards into Anki

### Method 1: CSV Import (Recommended)
1. **Download Anki** from https://apps.ankiweb.net/
2. **Install Anki** on your computer
3. **Open Anki** and create a new deck called "DSA Mastery"
4. **In this app**, generate notes for a problem
5. **Click "Export to Anki"** - this creates a CSV file
6. **In Anki**: File → Import → Select the CSV file
7. **Choose your "DSA Mastery" deck** and click Import

### Method 2: Manual Copy-Paste
1. **Copy flashcards** from the notes section
2. **In Anki**: Click "Add" → "Basic" card type
3. **Paste question** in Front field
4. **Paste answer** in Back field
5. **Add tags**: DSA, [Problem Name]
6. **Click Add**

### Method 3: AnkiConnect (Advanced)
For automatic integration, install AnkiConnect addon:
1. **In Anki**: Tools → Add-ons → Browse & Install
2. **Search for**: AnkiConnect (code: 2055492159)
3. **Install and restart Anki**
4. **Configure** ANKI_CONNECT_URL in your .env file
"""
    return instructions

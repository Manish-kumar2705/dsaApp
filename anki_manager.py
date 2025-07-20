import requests
from config import ANKI_DECK_NAME, ANKI_MODEL_NAME

def create_flashcards(cards):
    """Bulk create flashcards from list of Q;A pairs"""
    if not cards:
        return
    
    try:
        # For now, just print the cards since Anki Connect requires setup
        print(f"📚 Would create {len(cards)} flashcards:")
        for i, card in enumerate(cards, 1):
            if ";" in card:
                q, a = card.split(";", 1)
                print(f"  {i}. Q: {q}")
                print(f"     A: {a}")
            else:
                print(f"  {i}. {card}")
        
        print("\n💡 To enable Anki integration:")
        print("1. Install Anki and AnkiConnect addon")
        print("2. Set up ANKI_CONNECT_URL in config")
        print("3. Configure ANKI_DECK_NAME in config")
        
        return True
        
    except Exception as e:
        print(f"❌ Anki integration error: {e}")
        return False

def add_card_to_anki(question, answer, deck_name=None, model_name=None):
    """Add a single card to Anki"""
    deck_name = deck_name or ANKI_DECK_NAME
    model_name = model_name or ANKI_MODEL_NAME
    
    try:
        # For now, just print the card
        print(f"📝 Would add card to {deck_name}:")
        print(f"  Q: {question}")
        print(f"  A: {answer}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to add card: {e}")
        return False

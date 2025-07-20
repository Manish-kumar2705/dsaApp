import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AI Configuration - Set Groq as default
USE_GROQ = os.getenv("USE_GROQ", "true").lower() == "true"  # Default to Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Paths
OBSIDIAN_VAULT = os.getenv("OBSIDIAN_VAULT", str(Path.home() / "Documents" / "Obsidian" / "DSA"))
NEETCODE_FILE = "neetcode_150.json"
PROGRESS_FILE = "progress.json"

# Study Configuration
DAILY_GOAL = 3
REVIEW_INTERVAL_DAYS = 7

# UI Theme
THEME_COLOR = "#667eea"
SECONDARY_COLOR = "#764ba2"
SUCCESS_COLOR = "#4CAF50"
WARNING_COLOR = "#FF9800"
ERROR_COLOR = "#F44336"

# Anki Configuration
ANKI_DECK_NAME = "DSA Mastery"
ANKI_MODEL_NAME = "Basic"

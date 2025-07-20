#!/bin/bash
echo "🚀 Setting up DSA Mastery System..."

# Install dependencies
pip install -r requirements.txt

# Download NeetCode 150 data
if [ ! -f "neetcode_150.json" ]; then
    echo "Downloading NeetCode 150 data..."
    curl -o neetcode_150.json https://raw.githubusercontent.com/neetcode-gh/leetcode/main/python/neetcode_150.json
fi

# Create default progress file
if [ ! -f "dsa_progress.json" ]; then
    echo '{"problems": {}, "patterns": {}, "stats": {"solved": 0, "total": 150, "streak": 0}}' > dsa_progress.json
fi

# Create Obsidian directories
mkdir -p "$(python -c 'from config import OBSIDIAN_VAULT; print(OBSIDIAN_VAULT)')/Patterns"
mkdir -p "$(python -c 'from config import OBSIDIAN_VAULT; print(OBSIDIAN_VAULT)')/Problems"

echo "✅ Setup complete!"
echo "🌐 Launching DSA Mastery System..."
streamlit run ui.py

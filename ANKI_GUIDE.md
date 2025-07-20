# 📚 Complete Guide: Using Anki with DSA Mastery System

## 🎯 Overview

Your DSA Mastery System now generates flashcards automatically and exports them to CSV files that can be imported directly into Anki for spaced repetition learning.

## 📥 Method 1: CSV Import (Recommended)

### Step 1: Download and Install Anki

1. Go to https://apps.ankiweb.net/
2. Download Anki for Windows
3. Install and open Anki

### Step 2: Create Your DSA Deck

1. In Anki, click "Create Deck"
2. Name it "DSA Mastery" (or any name you prefer)
3. Click "OK"

### Step 3: Generate Flashcards in DSA Mastery

1. Open your DSA Mastery System
2. Go to "Solve Problems" or "Review Notes"
3. Generate notes for a problem (this creates flashcards automatically)
4. Click "📚 Export to Anki" button

### Step 4: Import into Anki

1. In Anki, go to **File → Import**
2. Select the CSV file from your `flashcards` folder
3. Choose your "DSA Mastery" deck
4. Click **Import**
5. Your flashcards are now ready for study!

## 📋 Method 2: Manual Copy-Paste

### For Individual Cards:

1. Copy flashcards from the notes section
2. In Anki: Click "Add" → "Basic" card type
3. Paste question in **Front** field
4. Paste answer in **Back** field
5. Add tags: `DSA`, `[Problem Name]`
6. Click "Add"

## 🔧 Method 3: AnkiConnect (Advanced - Automatic)

### Setup AnkiConnect:

1. In Anki: **Tools → Add-ons → Browse & Install**
2. Search for: **AnkiConnect** (code: 2055492159)
3. Install and restart Anki
4. Add to your `.env` file:
   ```
   ANKI_CONNECT_URL=http://localhost:8765
   ```

## 📁 File Locations

### Generated Files:

- **CSV Files**: `flashcards/dsa_flashcards_YYYYMMDD_HHMMSS.csv`
- **Notes**: `[Your Obsidian Vault]/Problems/[Problem ID] - [Title].md`

### Example CSV Structure:

```csv
Question,Answer,Tags
What is the time complexity of binary search?,O(log n),"DSA,Two Pointers"
What data structure is best for LIFO operations?,Stack,"DSA,Stack"
```

## 🎓 Study Tips

### 1. Daily Review

- Set a daily goal in Anki (e.g., 20 cards per day)
- Review cards consistently for best retention

### 2. Tag Organization

- All cards are tagged with `DSA` and the problem name
- Use Anki's tag browser to study by pattern or difficulty

### 3. Custom Study

- Use Anki's "Custom Study" to focus on specific patterns
- Filter by tags like "Two Pointers", "Dynamic Programming", etc.

## 🔄 Workflow Integration

### Complete Workflow:

1. **Solve Problem** → Generate notes with flashcards
2. **Export to Anki** → Creates CSV file
3. **Import to Anki** → Cards ready for study
4. **Daily Review** → Spaced repetition learning
5. **Track Progress** → Monitor retention in Anki

### Benefits:

- ✅ **Automatic**: No manual card creation
- ✅ **Structured**: Consistent format across all problems
- ✅ **Tagged**: Easy organization by pattern/difficulty
- ✅ **Spaced Repetition**: Optimal learning schedule
- ✅ **Progress Tracking**: See your improvement over time

## 🚨 Troubleshooting

### Common Issues:

**Q: CSV import fails**
A: Make sure the CSV file is not open in another program

**Q: Cards don't appear**
A: Check that you selected the correct deck during import

**Q: Tags not working**
A: Ensure tags are properly formatted in the CSV

**Q: AnkiConnect not working**
A: Make sure Anki is running and AnkiConnect is installed

## 📊 Advanced Features

### Custom Card Types:

You can create custom card types in Anki for different question types:

- **Basic**: Q&A format
- **Cloze**: Fill-in-the-blank
- **Code**: Syntax-highlighted code questions

### Sync with AnkiWeb:

- Create free account at ankiweb.net
- Sync your deck across devices
- Study on mobile with AnkiMobile/AnkiDroid

## 🎯 Best Practices

1. **Consistency**: Review cards daily, even if just 5-10 cards
2. **Quality**: Focus on understanding, not memorization
3. **Context**: Use the original problem notes for context
4. **Patterns**: Group study by algorithm patterns
5. **Difficulty**: Start with easy problems, build up to hard ones

---

## 🚀 Ready to Start?

1. **Install Anki** from ankiweb.net
2. **Generate your first set of flashcards** in the DSA Mastery System
3. **Export and import** into Anki
4. **Start your daily review routine**

Your DSA learning journey just got a major upgrade! 🎉

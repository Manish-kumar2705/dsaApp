#!/usr/bin/env python3
"""
PC Sync Helper - DSA Mastery System
===================================

This script helps you sync files downloaded from your mobile DSA app
to your local PC tools (Obsidian, Anki, etc.)

Usage:
    python sync_to_pc.py
"""

import os
import shutil
import glob
from pathlib import Path
import pandas as pd

def sync_to_pc():
    """Sync downloaded files to PC tools"""
    
    print("🔄 DSA Mastery System - PC Sync Helper")
    print("=" * 50)
    
    # Get user's home directory
    home = Path.home()
    
    # Common download locations
    download_locations = [
        home / "Downloads",
        home / "Desktop",
        Path.cwd() / "downloads"
    ]
    
    print("\n📁 Looking for downloaded files...")
    
    # Find .md and .csv files
    md_files = []
    csv_files = []
    
    for location in download_locations:
        if location.exists():
            md_files.extend(glob.glob(str(location / "*.md")))
            csv_files.extend(glob.glob(str(location / "*flashcards*.csv")))
    
    if not md_files and not csv_files:
        print("❌ No .md or .csv files found in common download locations")
        print("\n💡 Make sure you've downloaded files from your mobile app first")
        return
    
    # Sync notes to Obsidian
    if md_files:
        print(f"\n📝 Found {len(md_files)} note files:")
        for file in md_files:
            print(f"   - {os.path.basename(file)}")
        
        # Ask for Obsidian vault path
        obsidian_path = input("\n📂 Enter your Obsidian vault path (or press Enter for default): ").strip()
        if not obsidian_path:
            obsidian_path = str(home / "Obsidian" / "DSA" / "Problems")
        
        # Create directory if it doesn't exist
        os.makedirs(obsidian_path, exist_ok=True)
        
        # Copy files
        for file in md_files:
            filename = os.path.basename(file)
            dest = os.path.join(obsidian_path, filename)
            shutil.copy2(file, dest)
            print(f"✅ Copied {filename} to Obsidian")
    
    # Sync flashcards to Anki
    if csv_files:
        print(f"\n📊 Found {len(csv_files)} flashcard files:")
        for file in csv_files:
            print(f"   - {os.path.basename(file)}")
        
        print("\n📚 To import flashcards to Anki:")
        print("1. Open Anki")
        print("2. Go to File → Import")
        print("3. Select the CSV file")
        print("4. Choose your deck")
        print("5. Import!")
    
    print("\n🎉 Sync complete!")
    print("\n💡 Next steps:")
    print("   - Open Obsidian to see your new notes")
    print("   - Import flashcards to Anki")
    print("   - Export to NotebookLM from Obsidian")

if __name__ == "__main__":
    sync_to_pc() 
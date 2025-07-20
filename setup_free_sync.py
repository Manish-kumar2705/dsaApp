#!/usr/bin/env python3
"""
Free Sync Setup - DSA Mastery System
====================================

Quick setup for free cloud sync methods:
1. GitHub Sync (Recommended)
2. Google Drive Sync
3. Dropbox Sync

Usage:
    python setup_free_sync.py
"""

import os
import subprocess
from pathlib import Path

def setup_github_sync():
    """Setup GitHub sync for Obsidian vault"""
    print("🥇 Setting up GitHub Sync (Recommended)")
    print("=" * 50)
    
    # Get Obsidian vault path
    vault_path = input("Enter your Obsidian vault path (or press Enter for default): ").strip()
    if not vault_path:
        vault_path = str(Path.home() / "Documents" / "Obsidian" / "DSA")
    
    if not os.path.exists(vault_path):
        print(f"❌ Vault path not found: {vault_path}")
        print("Please create your Obsidian vault first")
        return False
    
    print(f"\n📂 Vault path: {vault_path}")
    
    # Check if git is already initialized
    git_dir = os.path.join(vault_path, ".git")
    if os.path.exists(git_dir):
        print("✅ Git already initialized")
    else:
        print("\n🔧 Initializing Git...")
        try:
            os.chdir(vault_path)
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
            print("✅ Git initialized successfully")
        except Exception as e:
            print(f"❌ Git initialization failed: {e}")
            return False
    
    # Get GitHub repo URL
    repo_url = input("\nEnter your GitHub repository URL: ").strip()
    if not repo_url:
        print("❌ GitHub repository URL required")
        return False
    
    # Setup remote and push
    try:
        os.chdir(vault_path)
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
        subprocess.run(["git", "branch", "-M", "main"], check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        print("✅ GitHub sync configured successfully!")
    except Exception as e:
        print(f"❌ GitHub setup failed: {e}")
        return False
    
    print("\n📱 Next Steps:")
    print("1. Install Obsidian Git plugin")
    print("2. Enable auto-backup and auto-push")
    print("3. Your notes will sync automatically!")
    
    return True

def setup_google_drive_sync():
    """Setup Google Drive sync"""
    print("🥈 Setting up Google Drive Sync")
    print("=" * 50)
    
    print("📥 Steps to setup Google Drive sync:")
    print("1. Download Google Drive for Desktop")
    print("2. Install and sign in")
    print("3. Create folder: Google Drive/Obsidian DSA")
    print("4. Move your Obsidian vault to this folder")
    print("5. Update Obsidian vault path")
    
    print("\n🔗 Download: https://www.google.com/drive/download/")
    
    input("\nPress Enter when you've completed the setup...")
    print("✅ Google Drive sync setup complete!")

def setup_dropbox_sync():
    """Setup Dropbox sync"""
    print("🥉 Setting up Dropbox Sync")
    print("=" * 50)
    
    print("📥 Steps to setup Dropbox sync:")
    print("1. Download Dropbox")
    print("2. Install and sign in")
    print("3. Create folder: Dropbox/Obsidian DSA")
    print("4. Move your Obsidian vault to this folder")
    print("5. Update Obsidian vault path")
    
    print("\n🔗 Download: https://www.dropbox.com/download")
    
    input("\nPress Enter when you've completed the setup...")
    print("✅ Dropbox sync setup complete!")

def setup_anki_sync():
    """Setup Anki sync"""
    print("📚 Setting up Anki Sync")
    print("=" * 50)
    
    print("📥 Steps to setup Anki sync:")
    print("1. Create account at ankiweb.net")
    print("2. Open Anki desktop app")
    print("3. Go to Tools → Preferences → Network")
    print("4. Enter your AnkiWeb username/password")
    print("5. Click 'Sync'")
    
    print("\n🔗 AnkiWeb: https://ankiweb.net")
    
    input("\nPress Enter when you've completed the setup...")
    print("✅ Anki sync setup complete!")

def main():
    """Main setup function"""
    print("🆓 Free Sync Setup - DSA Mastery System")
    print("=" * 50)
    print("Choose your sync method:")
    print("1. GitHub Sync (Recommended - 100% free)")
    print("2. Google Drive Sync (Free 15GB)")
    print("3. Dropbox Sync (Free 2GB)")
    print("4. Anki Sync (Free)")
    print("5. Setup all methods")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == "1":
        setup_github_sync()
    elif choice == "2":
        setup_google_drive_sync()
    elif choice == "3":
        setup_dropbox_sync()
    elif choice == "4":
        setup_anki_sync()
    elif choice == "5":
        print("\n🔄 Setting up all sync methods...")
        setup_github_sync()
        print("\n" + "="*50)
        setup_google_drive_sync()
        print("\n" + "="*50)
        setup_dropbox_sync()
        print("\n" + "="*50)
        setup_anki_sync()
    else:
        print("❌ Invalid choice")
        return
    
    print("\n🎉 Sync setup complete!")
    print("\n💡 Your workflow:")
    print("📱 Mobile → Solve problems → Generate notes → ☁️ Cloud → 💻 PC")
    print("💻 PC → Work on notes → ☁️ Cloud → 📱 Mobile")

if __name__ == "__main__":
    main() 
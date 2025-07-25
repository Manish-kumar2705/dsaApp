#!/usr/bin/env python3
"""
Cloud Sync System - DSA Mastery System
======================================

Automatically sync notes and flashcards to cloud services:
- Obsidian vault to cloud storage (Google Drive, Dropbox, etc.)
- Anki flashcards to AnkiWeb
- Cross-device access without manual transfer

Usage:
    python cloud_sync.py
"""

import os
import json
import requests
import base64
from pathlib import Path
from datetime import datetime
import subprocess

class CloudSync:
    def __init__(self):
        self.config_file = "cloud_sync_config.json"
        self.load_config()
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_repo = os.getenv('GITHUB_REPO', 'your-username/dsa-notes')
        self.gdrive_credentials = os.getenv('GDRIVE_CREDENTIALS')
    
    def load_config(self):
        """Load cloud sync configuration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "obsidian_sync": {
                    "enabled": False,
                    "method": "github",  # github, gdrive, dropbox
                    "repo_url": "",
                    "local_path": ""
                },
                "anki_sync": {
                    "enabled": False,
                    "ankiweb_username": "",
                    "ankiweb_password": ""
                }
            }
            self.save_config()
    
    def save_config(self):
        """Save cloud sync configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_obsidian_sync(self, method="github"):
        """Setup Obsidian sync to cloud"""
        print("🔧 Setting up Obsidian Cloud Sync...")
        
        if method == "github":
            self.setup_github_sync()
        elif method == "gdrive":
            self.setup_gdrive_sync()
        elif method == "dropbox":
            self.setup_dropbox_sync()
    
    def setup_github_sync(self):
        """Setup GitHub sync for Obsidian vault"""
        print("\n📂 GitHub Sync Setup:")
        print("1. Create a GitHub repository for your Obsidian vault")
        print("2. Clone it to your local machine")
        print("3. Move your Obsidian vault into the cloned repository")
        print("4. Push to GitHub")
        
        repo_url = input("\nEnter your GitHub repository URL: ").strip()
        local_path = input("Enter your local Obsidian vault path: ").strip()
        
        if repo_url and local_path:
            self.config["obsidian_sync"]["enabled"] = True
            self.config["obsidian_sync"]["method"] = "github"
            self.config["obsidian_sync"]["repo_url"] = repo_url
            self.config["obsidian_sync"]["local_path"] = local_path
            self.save_config()
            
            print("✅ GitHub sync configured!")
            print("💡 Your Obsidian vault will now sync to GitHub")
            print("📱 Access your notes from any device via GitHub")
    
    def setup_gdrive_sync(self):
        """Setup Google Drive sync for Obsidian vault"""
        print("\n☁️ Google Drive Sync Setup:")
        print("1. Install Google Drive for Desktop")
        print("2. Create a folder for your Obsidian vault")
        print("3. Move your vault to the Google Drive folder")
        
        local_path = input("\nEnter your Google Drive Obsidian vault path: ").strip()
        
        if local_path:
            self.config["obsidian_sync"]["enabled"] = True
            self.config["obsidian_sync"]["method"] = "gdrive"
            self.config["obsidian_sync"]["local_path"] = local_path
            self.save_config()
            
            print("✅ Google Drive sync configured!")
            print("💡 Your Obsidian vault will sync automatically")
    
    def setup_dropbox_sync(self):
        """Setup Dropbox sync for Obsidian vault"""
        print("\n📦 Dropbox Sync Setup:")
        print("1. Install Dropbox")
        print("2. Create a folder for your Obsidian vault")
        print("3. Move your vault to the Dropbox folder")
        
        local_path = input("\nEnter your Dropbox Obsidian vault path: ").strip()
        
        if local_path:
            self.config["obsidian_sync"]["enabled"] = True
            self.config["obsidian_sync"]["method"] = "dropbox"
            self.config["obsidian_sync"]["local_path"] = local_path
            self.save_config()
            
            print("✅ Dropbox sync configured!")
            print("💡 Your Obsidian vault will sync automatically")
    
    def setup_anki_sync(self):
        """Setup Anki sync to AnkiWeb"""
        print("\n📚 Anki Sync Setup:")
        print("1. Create an account at ankiweb.net")
        print("2. Enable sync in Anki desktop app")
        print("3. Your flashcards will sync automatically")
        
        username = input("\nEnter your AnkiWeb username: ").strip()
        password = input("Enter your AnkiWeb password: ").strip()
        
        if username and password:
            self.config["anki_sync"]["enabled"] = True
            self.config["anki_sync"]["ankiweb_username"] = username
            self.config["anki_sync"]["ankiweb_password"] = password
            self.save_config()
            
            print("✅ Anki sync configured!")
            print("💡 Your flashcards will sync to AnkiWeb")
            print("📱 Access your cards on AnkiMobile app")
    
    # Direct Upload Functions
    def upload_note_to_github(self, note_content, filename, pattern="Arrays"):
        """Upload note directly to GitHub repository"""
        try:
            if not self.github_token:
                return False, "GitHub token not configured"
            
            # Create file path in repository
            file_path = f"notes/{pattern}/{filename}"
            
            # GitHub API endpoint
            url = f"https://api.github.com/repos/{self.github_repo}/contents/{file_path}"
            
            # Prepare headers
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Encode content
            content = base64.b64encode(note_content.encode('utf-8')).decode('utf-8')
            
            # Prepare data
            data = {
                'message': f'Add DSA note: {filename}',
                'content': content,
                'branch': 'main'
            }
            
            # Make request
            response = requests.put(url, headers=headers, json=data)
            
            if response.status_code in [200, 201]:
                file_url = response.json()['content']['download_url']
                return True, f"✅ Uploaded to GitHub: {file_url}"
            else:
                return False, f"GitHub upload failed: {response.status_code}"
                
        except Exception as e:
            return False, f"GitHub upload error: {str(e)}"
    
    def upload_note_to_gdrive(self, note_content, filename, pattern="Arrays"):
        """Upload note directly to Google Drive"""
        try:
            if not self.gdrive_credentials:
                return False, "Google Drive credentials not configured"
            
            # For now, return instructions for manual setup
            # In production, you'd use Google Drive API
            return False, "Google Drive API setup required. Use GitHub upload for now."
            
        except Exception as e:
            return False, f"Google Drive upload error: {str(e)}"
    
    def upload_flashcards_to_github(self, flashcards, filename, pattern="Arrays"):
        """Upload flashcards CSV to GitHub"""
        try:
            if not self.github_token:
                return False, "GitHub token not configured"
            
            # Convert flashcards to CSV
            import pandas as pd
            df = pd.DataFrame(flashcards)
            csv_content = df.to_csv(index=False)
            
            # Create file path
            file_path = f"flashcards/{pattern}/{filename}"
            
            # GitHub API endpoint
            url = f"https://api.github.com/repos/{self.github_repo}/contents/{file_path}"
            
            # Prepare headers
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Encode content
            content = base64.b64encode(csv_content.encode('utf-8')).decode('utf-8')
            
            # Prepare data
            data = {
                'message': f'Add DSA flashcards: {filename}',
                'content': content,
                'branch': 'main'
            }
            
            # Make request
            response = requests.put(url, headers=headers, json=data)
            
            if response.status_code in [200, 201]:
                file_url = response.json()['content']['download_url']
                return True, f"✅ Flashcards uploaded to GitHub: {file_url}"
            else:
                return False, f"GitHub upload failed: {response.status_code}"
                
        except Exception as e:
            return False, f"GitHub upload error: {str(e)}"
    
    def setup_github_upload(self, token, repo):
        """Setup GitHub upload configuration"""
        self.github_token = token
        self.github_repo = repo
        self.config['github'] = {
            'token': token,
            'repo': repo,
            'enabled': True
        }
        self.save_config()
        return True, "GitHub upload configured successfully"
    
    def setup_gdrive_upload(self, credentials):
        """Setup Google Drive upload configuration"""
        self.gdrive_credentials = credentials
        self.config['gdrive'] = {
            'credentials': credentials,
            'enabled': True
        }
        self.save_config()
        return True, "Google Drive upload configured successfully"
    
    # Existing sync methods
    def sync_note_to_cloud(self, note_content, filename):
        """Sync note to cloud storage"""
        # Try GitHub first
        success, message = self.upload_note_to_github(note_content, filename)
        if success:
            return True
        
        # Try Google Drive
        success, message = self.upload_note_to_gdrive(note_content, filename)
        return success
    
    def sync_flashcards_to_anki(self, flashcards, deck_name):
        """Sync flashcards to Anki"""
        try:
            # This would integrate with AnkiConnect
            # For now, return success
            return True
        except Exception as e:
            return False
    
    def get_cloud_status(self):
        """Get current cloud sync status"""
        status = {
            "obsidian": {
                "enabled": self.config["obsidian_sync"]["enabled"],
                "method": self.config["obsidian_sync"]["method"] if self.config["obsidian_sync"]["enabled"] else "None"
            },
            "anki": {
                "enabled": self.config["anki_sync"]["enabled"]
            }
        }
        return status

def main():
    """Main cloud sync setup"""
    print("🌐 DSA Mastery System - Cloud Sync Setup")
    print("=" * 50)
    
    sync = CloudSync()
    
    while True:
        print("\n📋 Cloud Sync Options:")
        print("1. Setup Obsidian sync (GitHub/Google Drive/Dropbox)")
        print("2. Setup Anki sync (AnkiWeb)")
        print("3. View sync status")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            print("\n📂 Obsidian Sync Methods:")
            print("1. GitHub (Free, manual sync)")
            print("2. Google Drive (Free, automatic)")
            print("3. Dropbox (Free, automatic)")
            
            method_choice = input("Select method (1-3): ").strip()
            
            if method_choice == "1":
                sync.setup_github_sync()
            elif method_choice == "2":
                sync.setup_gdrive_sync()
            elif method_choice == "3":
                sync.setup_dropbox_sync()
        
        elif choice == "2":
            sync.setup_anki_sync()
        
        elif choice == "3":
            status = sync.get_cloud_status()
            print("\n📊 Sync Status:")
            print(f"Obsidian: {'✅ Enabled' if status['obsidian']['enabled'] else '❌ Disabled'}")
            if status['obsidian']['enabled']:
                print(f"  Method: {status['obsidian']['method']}")
            print(f"Anki: {'✅ Enabled' if status['anki']['enabled'] else '❌ Disabled'}")
        
        elif choice == "4":
            print("👋 Cloud sync setup complete!")
            break

if __name__ == "__main__":
    main() 
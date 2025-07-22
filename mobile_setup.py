#!/usr/bin/env python3
"""
Mobile Setup Script for DSA Mastery System
Helps users configure authentication for mobile access
"""

import os
import json
import webbrowser
from pathlib import Path

def print_header():
    """Print setup header"""
    print("🎯 DSA Mastery System - Mobile Setup")
    print("=" * 50)
    print("This script will help you configure authentication for mobile access.")
    print("No terminal login needed on your phone - everything works through the web!\n")

def check_streamlit_cloud():
    """Check if running on Streamlit Cloud"""
    print("🔍 Checking deployment environment...")
    
    if os.environ.get('STREAMLIT_SERVER_HEADLESS', False):
        print("✅ Running on Streamlit Cloud")
        print("📱 Mobile access is available!")
        return True
    else:
        print("💻 Running locally")
        print("📱 To access on mobile, deploy to Streamlit Cloud")
        return False

def github_setup():
    """Guide through GitHub setup"""
    print("\n🐙 GitHub Authentication Setup")
    print("-" * 30)
    
    print("Step 1: Create GitHub Personal Access Token")
    print("1. Go to: https://github.com/settings/tokens")
    print("2. Click 'Generate new token (classic)'")
    print("3. Give it a name: 'DSA Mastery Mobile'")
    print("4. Select scopes: repo, workflow")
    print("5. Copy the token (you'll only see it once!)")
    
    open_github = input("\nOpen GitHub token page? (y/n): ").lower()
    if open_github == 'y':
        webbrowser.open("https://github.com/settings/tokens")
    
    print("\nStep 2: Add to Streamlit Cloud Secrets")
    print("1. Go to your Streamlit Cloud dashboard")
    print("2. Find your app → Settings → Secrets")
    print("3. Add these secrets:")
    print("""
    GITHUB_TOKEN = "your_token_here"
    GITHUB_REPO = "your-username/dsa-notes"
    """)
    
    print("Step 3: Create GitHub Repository")
    print("1. Go to: https://github.com/new")
    print("2. Create repository: dsa-notes")
    print("3. Make it private (recommended)")
    print("4. Don't initialize with README")
    
    open_github_repo = input("\nOpen GitHub new repository page? (y/n): ").lower()
    if open_github_repo == 'y':
        webbrowser.open("https://github.com/new")

def google_drive_setup():
    """Guide through Google Drive setup"""
    print("\n☁️ Google Drive Authentication Setup")
    print("-" * 35)
    
    print("Step 1: Create Google Cloud Project")
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Create new project or select existing")
    print("3. Enable Google Drive API")
    
    open_gcp = input("\nOpen Google Cloud Console? (y/n): ").lower()
    if open_gcp == 'y':
        webbrowser.open("https://console.cloud.google.com/")
    
    print("\nStep 2: Create Service Account")
    print("1. Go to IAM & Admin → Service Accounts")
    print("2. Click 'Create Service Account'")
    print("3. Name: 'DSA Mastery Mobile'")
    print("4. Grant 'Editor' role")
    print("5. Create and download JSON key")
    
    print("\nStep 3: Create Google Drive Folder")
    print("1. Go to: https://drive.google.com/")
    print("2. Create folder: 'DSA Mastery Notes'")
    print("3. Share with service account email")
    print("4. Copy folder ID from URL")
    
    open_drive = input("\nOpen Google Drive? (y/n): ").lower()
    if open_drive == 'y':
        webbrowser.open("https://drive.google.com/")
    
    print("\nStep 4: Add to Streamlit Cloud Secrets")
    print("Add these secrets to Streamlit Cloud:")
    print("""
    GDRIVE_CREDENTIALS = '''
    {
      "type": "service_account",
      "project_id": "your-project",
      "private_key_id": "...",
      "private_key": "...",
      "client_email": "...",
      "client_id": "...",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "..."
    }
    '''
    GDRIVE_FOLDER_ID = "your_folder_id_here"
    """)

def notebooklm_setup():
    """Guide through NotebookLM setup"""
    print("\n📚 NotebookLM Integration Setup")
    print("-" * 30)
    
    print("Option 1: Google Drive Sync (Recommended)")
    print("✅ Uses same Google Drive credentials")
    print("✅ No additional setup needed")
    print("✅ Automatic sync to NotebookLM")
    
    print("\nOption 2: Webhook Integration")
    print("1. Get webhook URL from NotebookLM settings")
    print("2. Add to Streamlit secrets:")
    print("   NOTEBOOKLM_WEBHOOK_URL = 'your_webhook_url'")
    
    print("\nOption 3: API Integration")
    print("1. Get API key from NotebookLM settings")
    print("2. Add to Streamlit secrets:")
    print("   NOTEBOOKLM_API_KEY = 'your_api_key'")

def mobile_access_guide():
    """Guide for mobile access"""
    print("\n📱 Mobile Access Guide")
    print("-" * 20)
    
    print("Once configured, access your app on mobile:")
    print("1. Open your Streamlit app URL on phone")
    print("2. All authentication is automatic")
    print("3. No login prompts needed")
    print("4. Direct access to all features")
    
    print("\nMobile Features Available:")
    print("✅ GitHub upload - One-click upload to repository")
    print("✅ Google Drive sync - Automatic sync to Drive folder")
    print("✅ NotebookLM export - Direct export to NotebookLM")
    print("✅ Note generation - AI-powered notes")
    print("✅ Flashcard creation - Automatic Anki integration")
    print("✅ LeetCode links - Direct problem solving")

def create_secrets_template():
    """Create a secrets template file"""
    template = """# Streamlit Cloud Secrets Template
# Copy this to your Streamlit Cloud dashboard → Settings → Secrets

# GitHub Configuration
GITHUB_TOKEN = "your_github_token_here"
GITHUB_REPO = "your-username/dsa-notes"

# Google Drive Configuration (Optional)
GDRIVE_CREDENTIALS = '''
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
}
'''
GDRIVE_FOLDER_ID = "your_google_drive_folder_id"

# NotebookLM Configuration (Optional)
NOTEBOOKLM_WEBHOOK_URL = "your_notebooklm_webhook_url"
NOTEBOOKLM_API_KEY = "your_notebooklm_api_key"

# AI Configuration
GROQ_API_KEY = "your_groq_api_key"
OPENROUTER_API_KEY = "your_openrouter_api_key"
"""
    
    with open("streamlit_secrets_template.toml", "w") as f:
        f.write(template)
    
    print("\n📄 Created: streamlit_secrets_template.toml")
    print("Copy this template to your Streamlit Cloud secrets!")

def main():
    """Main setup function"""
    print_header()
    
    # Check environment
    is_cloud = check_streamlit_cloud()
    
    # Setup guides
    github_setup()
    google_drive_setup()
    notebooklm_setup()
    mobile_access_guide()
    
    # Create template
    create_secrets_template()
    
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("Next steps:")
    print("1. Follow the setup guides above")
    print("2. Add secrets to Streamlit Cloud")
    print("3. Deploy your app to Streamlit Cloud")
    print("4. Access on mobile - no terminal login needed!")
    
    print("\n📚 Additional Resources:")
    print("- MOBILE_AUTHENTICATION_GUIDE.md - Detailed setup instructions")
    print("- streamlit_secrets_template.toml - Secrets template")
    print("- FINAL_COMPLETE_SYSTEM.md - Complete system overview")

if __name__ == "__main__":
    main() 
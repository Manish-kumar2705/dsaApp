#!/usr/bin/env python3
"""
DSA Mastery System Setup Script
Helps users set up the system quickly
"""

import os
import sys
import subprocess
from pathlib import Path

def create_env_file():
    """Create .env file with default configuration"""
    env_content = """# DSA Mastery System Configuration
# Copy this file to .env and fill in your values

# AI Configuration
USE_GROQ=true
GROQ_API_KEY=your_groq_api_key_here
OPENROUTER_API_KEY=your_openrouter_key_here

# Paths
OBSIDIAN_VAULT=~/Documents/Obsidian/DSA

# Anki Settings
ANKI_CONNECT_URL=http://localhost:8765
ANKI_DECK=DSA::Patterns

# UI Settings
THEME_COLOR=#4B8BBE
SECONDARY_COLOR=#FF6B6B
SUCCESS_COLOR=#4CAF50
WARNING_COLOR=#FF9800

# Code Editor Settings
DEFAULT_LANGUAGE=java
ENABLE_SYNTAX_HIGHLIGHTING=true

# Study Settings
DAILY_GOAL=3
REVIEW_INTERVAL_DAYS=7
SPACED_REPETITION_ENABLED=true

# Export Settings
DEFAULT_EXPORT_FORMAT=markdown
"""
    
    if not Path('.env').exists():
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with default configuration")
        print("📝 Please edit .env file and add your API keys")
    else:
        print("ℹ️  .env file already exists")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--user"], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    return True

def check_system():
    """Check if system is ready to run"""
    print("🔍 Checking system...")
    
    # Check if required files exist
    required_files = ['neetcode_150.json', 'dsa_system.py', 'ai_client.py']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    # Check if .env exists
    if not Path('.env').exists():
        print("⚠️  .env file not found. Run setup to create it.")
    
    print("✅ System check completed")
    return True

def main():
    """Main setup function"""
    print("🚀 DSA Mastery System Setup")
    print("=" * 50)
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    if install_dependencies():
        print("\n✅ Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Edit .env file and add your API keys")
        print("2. Run: streamlit run ui.py")
        print("3. Open browser at: http://localhost:8501")
        print("\n🎯 Get API keys from:")
        print("   - Groq: https://console.groq.com/")
        print("   - OpenRouter: https://openrouter.ai/")
    else:
        print("\n❌ Setup failed. Please check the errors above.")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
DSA Mastery System Startup Script
Checks configuration and provides setup guidance
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'streamlit', 'requests', 'python-dotenv', 'matplotlib',
        'plotly', 'pandas', 'pygments', 'streamlit-ace', 
        'streamlit-option-menu', 'streamlit-extras'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def check_configuration():
    """Check if configuration is set up properly"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ Configuration file (.env) not found")
        print("\n📝 Create a .env file with the following content:")
        print("""
# AI Configuration
USE_GROQ=true
GROQ_API_KEY=your_groq_api_key_here
OPENROUTER_API_KEY=your_openrouter_key_here

# Paths
OBSIDIAN_VAULT=~/Documents/Obsidian/DSA

# UI Settings
THEME_COLOR=#4B8BBE
SECONDARY_COLOR=#FF6B6B

# Study Settings
DAILY_GOAL=3
REVIEW_INTERVAL_DAYS=7
        """)
        return False
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check for required API keys
    groq_key = os.getenv('GROQ_API_KEY')
    openrouter_key = os.getenv('OPENROUTER_API_KEY')
    
    if not groq_key or groq_key == 'your_groq_api_key_here':
        if not openrouter_key or openrouter_key == 'your_openrouter_key_here':
            print("❌ No API keys configured")
            print("\n🔑 You need to set up at least one AI API key:")
            print("   1. Get a Groq API key from: https://console.groq.com/")
            print("   2. Or get an OpenRouter API key from: https://openrouter.ai/")
            print("   3. Add the key to your .env file")
            return False
    
    print("✅ Configuration looks good")
    return True

def check_data_files():
    """Check if required data files exist"""
    required_files = ['neetcode_150.json']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required data files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n📥 Please ensure all data files are present")
        return False
    
    print("✅ All data files are present")
    return True

def main():
    """Main startup function"""
    print("🚀 DSA Mastery System - Startup Check")
    print("=" * 50)
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    if not check_dependencies():
        return 1
    
    # Check configuration
    print("\n⚙️  Checking configuration...")
    if not check_configuration():
        return 1
    
    # Check data files
    print("\n📁 Checking data files...")
    if not check_data_files():
        return 1
    
    print("\n✅ All checks passed! Starting DSA Mastery System...")
    print("\n🌐 The application will open in your browser at: http://localhost:8501")
    print("📖 Press Ctrl+C to stop the application")
    print("=" * 50)
    
    # Start the Streamlit application
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "ui.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 DSA Mastery System stopped")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 
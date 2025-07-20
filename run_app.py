#!/usr/bin/env python3
"""
DSA Mastery System - Startup Script
Run this to start the enhanced application
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'requests', 
        'python-dotenv',
        'pandas',
        'plotly'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing packages:", missing_packages)
        print("💡 Installing missing packages...")
        for package in missing_packages:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '--user'])
        print("✅ All packages installed!")
    else:
        print("✅ All required packages are installed!")

def check_env_file():
    """Check if .env file exists and has API keys"""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("💡 Creating .env file template...")
        
        env_content = """# DSA Mastery System Configuration

# AI API Configuration
USE_GROQ=true
GROQ_API_KEY=your_groq_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Obsidian Configuration
OBSIDIAN_VAULT_PATH=your_obsidian_vault_path_here

# Anki Configuration
ANKI_CONNECT_URL=http://localhost:8765
ANKI_DECK_NAME=DSA Mastery
ANKI_MODEL_NAME=Basic

# Study Configuration
DAILY_GOAL=3
REVIEW_INTERVAL_DAYS=7
SPACED_REPETITION_ENABLED=true

# Export Settings
DEFAULT_EXPORT_FORMAT=markdown
NOTEBOOKLM_EXPORT_PATH=./exports
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ .env file created!")
        print("🔧 Please edit .env file and add your API keys:")
        print("   - Get Groq API key from: https://console.groq.com/")
        print("   - Get OpenRouter API key from: https://openrouter.ai/")
        return False
    else:
        print("✅ .env file found!")
        return True

def main():
    print("🚀 DSA Mastery System - Startup")
    print("=" * 50)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    check_dependencies()
    
    # Check environment
    print("\n🔍 Checking environment...")
    env_ok = check_env_file()
    
    print("\n" + "=" * 50)
    print("🎯 Starting DSA Mastery System...")
    print("📱 The app will open in your browser")
    print("🔗 Local URL: http://localhost:8501")
    print("🌐 Network URL: http://192.168.1.70:8501")
    print("\n💡 Tips:")
    print("   - Use '💻 Solve Problems' to practice with AI guidance")
    print("   - Click '🔍 Analyze Solution' to get AI feedback")
    print("   - Click '📚 Explain Code' for detailed explanations")
    print("   - Use '📚 Problem Browser' to find specific problems")
    print("\n🛑 Press Ctrl+C to stop the app")
    print("=" * 50)
    
    try:
        # Start the enhanced UI
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'ui_enhanced.py'])
    except KeyboardInterrupt:
        print("\n👋 App stopped. Thanks for using DSA Mastery System!")
    except Exception as e:
        print(f"\n❌ Error starting app: {e}")
        print("💡 Try running: streamlit run ui_enhanced.py")

if __name__ == "__main__":
    main() 
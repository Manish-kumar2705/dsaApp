#!/usr/bin/env python3
"""
DSA Mastery System - Status Check
This script checks if all components are working correctly.
"""

import os
import json
import sys

def check_files():
    """Check if all required files exist"""
    print("🔍 Checking required files...")
    
    required_files = [
        "ui_simple.py",
        "dsa_system.py", 
        "config.py",
        "ai_client.py",
        "anki_manager.py",
        "neetcode_150.json"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    return len(missing_files) == 0

def check_imports():
    """Check if all imports work"""
    print("\n🔍 Checking imports...")
    
    try:
        import streamlit
        print(f"✅ streamlit {streamlit.__version__}")
    except ImportError as e:
        print(f"❌ streamlit - {e}")
        return False
    
    try:
        import pandas as pd
        print(f"✅ pandas {pd.__version__}")
    except ImportError as e:
        print(f"❌ pandas - {e}")
        return False
    
    try:
        import plotly
        print(f"✅ plotly {plotly.__version__}")
    except ImportError as e:
        print(f"❌ plotly - {e}")
        return False
    
    try:
        from config import THEME_COLOR, SECONDARY_COLOR, PROGRESS_FILE, NEETCODE_FILE
        print("✅ config.py")
    except ImportError as e:
        print(f"❌ config.py - {e}")
        return False
    
    try:
        from dsa_system import DSAMasterySystem
        print("✅ dsa_system.py")
    except ImportError as e:
        print(f"❌ dsa_system.py - {e}")
        return False
    
    try:
        from ai_client import call_ai_api
        print("✅ ai_client.py")
    except ImportError as e:
        print(f"❌ ai_client.py - {e}")
        return False
    
    try:
        from anki_manager import create_flashcards
        print("✅ anki_manager.py")
    except ImportError as e:
        print(f"❌ anki_manager.py - {e}")
        return False
    
    return True

def check_data():
    """Check if data files are valid"""
    print("\n🔍 Checking data files...")
    
    try:
        with open("neetcode_150.json", "r") as f:
            data = json.load(f)
        print(f"✅ neetcode_150.json ({len(data)} problems)")
    except Exception as e:
        print(f"❌ neetcode_150.json - {e}")
        return False
    
    # Check if progress file exists or can be created
    try:
        from dsa_system import DSAMasterySystem
        system = DSAMasterySystem()
        print("✅ DSAMasterySystem initialized successfully")
    except Exception as e:
        print(f"❌ DSAMasterySystem - {e}")
        return False
    
    return True

def check_ui():
    """Check if UI can be imported"""
    print("\n🔍 Checking UI...")
    
    try:
        # Try to import the UI components
        import streamlit as st
        print("✅ Streamlit UI components")
    except Exception as e:
        print(f"❌ UI components - {e}")
        return False
    
    return True

def main():
    print("🚀 DSA Mastery System - Status Check")
    print("=" * 50)
    
    all_good = True
    
    # Check files
    if not check_files():
        all_good = False
    
    # Check imports
    if not check_imports():
        all_good = False
    
    # Check data
    if not check_data():
        all_good = False
    
    # Check UI
    if not check_ui():
        all_good = False
    
    print("\n" + "=" * 50)
    
    if all_good:
        print("🎉 All checks passed! Your DSA Mastery System is ready to run.")
        print("\n🚀 To start the application:")
        print("   streamlit run ui_simple.py")
        print("\n🌐 The app will be available at: http://localhost:8501")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\n🔧 Common fixes:")
        print("   1. Install missing packages: pip install streamlit pandas plotly")
        print("   2. Check file permissions")
        print("   3. Ensure all files are in the correct directory")
    
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
#!/usr/bin/env python3
"""
DSA Mastery System - Startup Script
This script starts the Streamlit application with error handling.
"""

import subprocess
import sys
import os

def main():
    print("🚀 Starting DSA Mastery System...")
    print("=" * 50)
    
    # Check if required files exist
    required_files = ["ui_simple.py", "dsa_system.py", "config.py", "neetcode_150.json"]
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please ensure all files are in the current directory.")
        return
    
    print("✅ All required files found!")
    
    # Try to run the application
    try:
        print("🌐 Starting Streamlit server...")
        print("📱 The app will open in your browser automatically")
        print("🔗 If it doesn't open, go to: http://localhost:8501")
        print("=" * 50)
        
        # Run streamlit
        result = subprocess.run([
            sys.executable, "-m", "streamlit", "run", "ui_simple.py",
            "--server.port", "8501",
            "--server.headless", "false"
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting application: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure Streamlit is installed: pip install streamlit")
        print("2. Check if port 8501 is available")
        print("3. Try running: streamlit run ui_simple.py")
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("\n🔧 Try running manually:")
        print("streamlit run ui_simple.py")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Simple test to verify environment and API keys
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    try:
        import streamlit as st
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment variable loading"""
    print("\n🔍 Testing environment variables...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        groq_key = os.getenv('GROQ_API_KEY', '')
        openrouter_key = os.getenv('OPENROUTER_API_KEY', '')
        
        print(f"GROQ_API_KEY: {'✅ Set' if groq_key else '❌ Not set'}")
        print(f"OPENROUTER_API_KEY: {'✅ Set' if openrouter_key else '❌ Not set'}")
        
        if groq_key or openrouter_key:
            print("🎉 Environment variables loaded successfully!")
            return True
        else:
            print("⚠️ No API keys found in environment")
            return False
            
    except Exception as e:
        print(f"❌ Environment test failed: {e}")
        return False

def test_ai_client():
    """Test AI client functionality"""
    print("\n🔍 Testing AI client...")
    
    try:
        from ai_client import call_ai_api
        
        # Test with a simple prompt
        response = call_ai_api("What is 2 + 2? Answer with just the number.")
        
        if response and response.strip():
            print("✅ AI client test successful")
            print(f"Response: {response[:100]}...")
            return True
        else:
            print("❌ AI client returned empty response")
            return False
            
    except Exception as e:
        print(f"❌ AI client test failed: {e}")
        return False

def main():
    print("🚀 DSA Mastery System - Environment Test")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test environment
    env_ok = test_environment()
    
    # Test AI client
    ai_ok = test_ai_client()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"Imports: {'✅' if imports_ok else '❌'}")
    print(f"Environment: {'✅' if env_ok else '❌'}")
    print(f"AI Client: {'✅' if ai_ok else '❌'}")
    
    if imports_ok and env_ok and ai_ok:
        print("\n🎉 All tests passed! Your environment is ready.")
        print("You can now run: streamlit run ui_simple.py")
    else:
        print("\n🔧 Some tests failed. Check the errors above.")
        
        if not imports_ok:
            print("💡 Try: pip install -r requirements.txt --user")
        if not env_ok:
            print("💡 Check your .env file and API keys")
        if not ai_ok:
            print("💡 Verify your API keys are valid")

if __name__ == "__main__":
    main() 
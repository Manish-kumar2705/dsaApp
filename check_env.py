#!/usr/bin/env python3
"""
Simple environment check script
"""

import os

def check_env():
    print("🔍 Environment Check")
    print("=" * 40)
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
        with open('.env', 'r') as f:
            content = f.read()
            print(f"📄 .env file size: {len(content)} characters")
            if 'GROQ_API_KEY' in content:
                print("✅ GROQ_API_KEY found in .env file")
            else:
                print("❌ GROQ_API_KEY not found in .env file")
    else:
        print("❌ .env file NOT found")
        print("💡 Create a .env file with your API keys")
    
    # Check environment variables
    print("\n🔑 Environment Variables:")
    groq_key = os.getenv('GROQ_API_KEY', '')
    openrouter_key = os.getenv('OPENROUTER_API_KEY', '')
    use_groq = os.getenv('USE_GROQ', 'true')
    
    print(f"USE_GROQ: {use_groq}")
    print(f"GROQ_API_KEY: {'✅ Set' if groq_key else '❌ Not set'}")
    print(f"OPENROUTER_API_KEY: {'✅ Set' if openrouter_key else '❌ Not set'}")
    
    if groq_key:
        print(f"   Length: {len(groq_key)} characters")
        print(f"   Starts with: {groq_key[:10]}...")
    
    if openrouter_key:
        print(f"   Length: {len(openrouter_key)} characters")
        print(f"   Starts with: {openrouter_key[:10]}...")
    
    # Summary
    print("\n📊 Summary:")
    if groq_key or openrouter_key:
        print("✅ API keys are configured!")
        print("🎉 Your .env file is working correctly")
    else:
        print("❌ No API keys found")
        print("🔧 You need to:")
        print("   1. Create a .env file")
        print("   2. Add your API keys")
        print("   3. Restart the application")

if __name__ == "__main__":
    check_env() 
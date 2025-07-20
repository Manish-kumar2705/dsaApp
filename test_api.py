#!/usr/bin/env python3
"""
Test script to check if API keys are working properly
"""

import os
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        pass  # Fallback if dotenv is not available
from ai_client import call_ai_api, call_groq_api, call_openrouter_api

def test_env_loading():
    """Test if environment variables are loaded correctly"""
    print("🔍 Testing environment variable loading...")
    
    # Load .env file
    load_dotenv()
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("⚠️ .env file not found")
    
    # Check API keys
    groq_key = os.getenv("GROQ_API_KEY", "")
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
    use_groq = os.getenv("USE_GROQ", "true").lower() == "true"
    
    print(f"USE_GROQ: {use_groq}")
    print(f"GROQ_API_KEY: {'✅ Set' if groq_key else '❌ Not set'}")
    print(f"OPENROUTER_API_KEY: {'✅ Set' if openrouter_key else '❌ Not set'}")
    
    if groq_key:
        print(f"Groq key length: {len(groq_key)} characters")
        print(f"Groq key starts with: {groq_key[:10]}...")
    
    if openrouter_key:
        print(f"OpenRouter key length: {len(openrouter_key)} characters")
        print(f"OpenRouter key starts with: {openrouter_key[:10]}...")
    
    return groq_key, openrouter_key, use_groq

def test_simple_prompt():
    """Test with a simple prompt"""
    print("\n🧪 Testing simple prompt...")
    
    simple_prompt = "What is 2 + 2? Answer with just the number."
    
    try:
        response = call_ai_api(simple_prompt)
        print(f"Response: {response}")
        if response and response.strip():
            print("✅ Simple prompt test successful")
            return True
        else:
            print("❌ Simple prompt returned empty response")
            return False
    except Exception as e:
        print(f"❌ Simple prompt test failed: {e}")
        return False

def test_analysis_prompt():
    """Test with an analysis prompt that should return JSON"""
    print("\n🧪 Testing analysis prompt...")
    
    analysis_prompt = """
    Problem: Two Sum
    Description: Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
    
    User's Solution:
    def twoSum(nums, target):
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []
    
    Tasks:
    1. Check if solution is correct (return boolean)
    2. If incorrect, provide fixed optimal solution
    3. Add detailed inline comments
    4. Explain approach and complexity
    5. Compare with brute force solution
    6. Highlight 2 common mistakes
    7. Create 3 flashcards (Q;A format)
    
    Return JSON format:
    {
        "correct": bool,
        "fixed_code": str,
        "annotated_code": str,
        "approach_summary": str,
        "complexity": str,
        "brute_force": str,
        "mistakes": [str],
        "flashcards": [str]
    }
    """
    
    try:
        response = call_ai_api(analysis_prompt)
        print(f"Response length: {len(response)} characters")
        print(f"Response preview: {response[:200]}...")
        
        # Try to parse as JSON
        try:
            import json
            parsed = json.loads(response)
            print("✅ Analysis prompt returned valid JSON")
            print(f"JSON keys: {list(parsed.keys())}")
            return True
        except json.JSONDecodeError as e:
            print(f"❌ Analysis prompt returned invalid JSON: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Analysis prompt test failed: {e}")
        return False

def test_direct_api_calls():
    """Test direct API calls"""
    print("\n🧪 Testing direct API calls...")
    
    groq_key, openrouter_key, use_groq = test_env_loading()
    
    test_prompt = "What is the time complexity of binary search?"
    
    if use_groq and groq_key:
        print("\n📡 Testing Groq API directly...")
        try:
            response = call_groq_api(test_prompt)
            print(f"Groq response: {response[:100]}...")
        except Exception as e:
            print(f"❌ Groq API test failed: {e}")
    
    if openrouter_key:
        print("\n📡 Testing OpenRouter API directly...")
        try:
            response = call_openrouter_api(test_prompt)
            print(f"OpenRouter response: {response[:100]}...")
        except Exception as e:
            print(f"❌ OpenRouter API test failed: {e}")

def main():
    print("🚀 API Testing Script")
    print("=" * 50)
    
    # Test environment loading
    groq_key, openrouter_key, use_groq = test_env_loading()
    
    # Test simple prompt
    simple_success = test_simple_prompt()
    
    # Test analysis prompt
    analysis_success = test_analysis_prompt()
    
    # Test direct API calls
    test_direct_api_calls()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"Environment loading: {'✅' if groq_key or openrouter_key else '❌'}")
    print(f"Simple prompt test: {'✅' if simple_success else '❌'}")
    print(f"Analysis prompt test: {'✅' if analysis_success else '❌'}")
    
    if not (groq_key or openrouter_key):
        print("\n🔧 To fix API issues:")
        print("1. Create a .env file in your project directory")
        print("2. Add your API keys:")
        print("   GROQ_API_KEY=your_groq_api_key_here")
        print("   OPENROUTER_API_KEY=your_openrouter_key_here")
        print("3. Restart the application")
    
    if groq_key or openrouter_key:
        print("\n✅ API keys are configured!")
        print("If tests are still failing, check:")
        print("1. API key validity")
        print("2. Internet connection")
        print("3. API service status")

if __name__ == "__main__":
    main() 
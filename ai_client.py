import requests
import json
import time
import os
import hashlib
from config import USE_GROQ, GROQ_API_KEY, OPENROUTER_API_KEY

CACHE_FILE = "ai_cache.json"

def _get_cache():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)

def _prompt_hash(prompt):
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()

def call_ai_api(prompt: str, model: str = None, max_retries=3):
    """Unified AI interface with automatic failover and retries, now with JSON cache"""
    cache = _get_cache()
    key = _prompt_hash(prompt)
    if key in cache:
        return cache[key]
    
    # Check if API keys are configured
    if not GROQ_API_KEY and not OPENROUTER_API_KEY:
        print("⚠️ No API keys found. Using fallback response.")
        return get_fallback_response(prompt)
    
    for attempt in range(max_retries):
        try:
            if USE_GROQ and GROQ_API_KEY:
                print(f"🤖 Using Groq API (attempt {attempt + 1})")
                response = call_groq_api(prompt, model)
                if response and response.strip():
                    cache[key] = response
                    _save_cache(cache)
                    return response
                else:
                    print(f"⚠️ Groq API returned empty response (attempt {attempt + 1})")
            elif OPENROUTER_API_KEY:
                print(f"🤖 Using OpenRouter API (attempt {attempt + 1})")
                response = call_openrouter_api(prompt, model)
                if response and response.strip():
                    cache[key] = response
                    _save_cache(cache)
                    return response
                else:
                    print(f"⚠️ OpenRouter API returned empty response (attempt {attempt + 1})")
            else:
                print("⚠️ No valid API configuration found. Using fallback response.")
                return get_fallback_response(prompt)
        except Exception as e:
            print(f"❌ AI Error (attempt {attempt+1}): {e}")
            time.sleep(2)  # Wait before retrying
            if attempt == max_retries - 1:
                print("⚠️ All API attempts failed. Using fallback response.")
                return get_fallback_response(prompt)
    
    # If we get here, return fallback
    return get_fallback_response(prompt)

def get_fallback_response(prompt: str):
    """Return a fallback response when AI APIs are not available"""
    if "analyze" in prompt.lower() and "solution" in prompt.lower():
        # Return a structured JSON response for solution analysis
        return json.dumps({
            "correct": False,
            "fixed_code": "# Your optimized solution will appear here\n# Set up API keys for AI analysis",
            "annotated_code": "# Your solution with comments will appear here\n# Set up API keys for detailed analysis",
            "approach_summary": "AI analysis requires API key setup",
            "complexity": "Time: O(n), Space: O(1) - Analysis pending",
            "brute_force": "Brute force approach analysis pending",
            "mistakes": [
                "Set up API keys for detailed mistake analysis",
                "Enable AI features for comprehensive feedback"
            ],
            "flashcards": [
                "What is the time complexity of this solution?;O(n) - Set up API for detailed analysis",
                "What pattern does this problem use?;Pattern detection pending - Enable AI features",
                "What are common mistakes in this problem?;Mistake analysis pending - Set up API keys"
            ]
        })
    elif "explain" in prompt.lower() and "code" in prompt.lower():
        return """
## Code Explanation

**Note:** AI-powered code explanation requires API key setup.

### What the code does:
[AI explanation would appear here - requires API key]

### DSA Pattern:
[Pattern detection would appear here]

### Complexity:
[Complexity analysis would appear here]

### Key Insights:
[Insights would appear here]

**To enable AI features:**
1. Get API keys from Groq (https://console.groq.com/) or OpenRouter (https://openrouter.ai/)
2. Add them to your `.env` file
3. Restart the application
        """
    else:
        return f"""
I'm here to help with DSA questions! Your question was: "{prompt[:100]}..."

**Note:** AI integration requires an API key. Please set up your API keys in the .env file to get detailed responses.

For now, here are some general DSA resources:
- **Patterns:** Sliding Window, Two Pointers, BFS, DFS, Dynamic Programming
- **Data Structures:** Arrays, Linked Lists, Trees, Graphs, Heaps
- **Algorithms:** Sorting, Searching, Recursion, Backtracking

Try solving problems in the "Solve Problems" section to practice!
        """

def call_groq_api(prompt: str, model: str = None):
    """Call Groq API"""
    if not GROQ_API_KEY:
        print("❌ No Groq API key found")
        return get_fallback_response(prompt)
    
    model = model or "llama3-70b-8192"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": model,
        "temperature": 0.3,
        "max_tokens": 4000
    }
    
    try:
        print(f"📡 Calling Groq API with model: {model}")
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            if content and content.strip():
                print("✅ Groq API call successful")
                return content
            else:
                print("⚠️ Groq API returned empty content")
                return get_fallback_response(prompt)
        else:
            print("⚠️ Groq API response missing choices")
            return get_fallback_response(prompt)
    except requests.exceptions.RequestException as e:
        print(f"❌ Groq API request failed: {e}")
        return get_fallback_response(prompt)
    except json.JSONDecodeError as e:
        print(f"❌ Groq API response not valid JSON: {e}")
        return get_fallback_response(prompt)
    except Exception as e:
        print(f"❌ Groq API unexpected error: {e}")
        return get_fallback_response(prompt)

def call_openrouter_api(prompt: str, model: str = None):
    """Call OpenRouter API (fallback)"""
    if not OPENROUTER_API_KEY:
        print("❌ No OpenRouter API key found")
        return get_fallback_response(prompt)
    
    model = model or "mistralai/mixtral-8x7b-instruct"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": model
    }
    
    try:
        print(f"📡 Calling OpenRouter API with model: {model}")
        response = requests.post(
            "https://api.openrouter.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            if content and content.strip():
                print("✅ OpenRouter API call successful")
                return content
            else:
                print("⚠️ OpenRouter API returned empty content")
                return get_fallback_response(prompt)
        else:
            print("⚠️ OpenRouter API response missing choices")
            return get_fallback_response(prompt)
    except requests.exceptions.RequestException as e:
        print(f"❌ OpenRouter API request failed: {e}")
        return get_fallback_response(prompt)
    except json.JSONDecodeError as e:
        print(f"❌ OpenRouter API response not valid JSON: {e}")
        return get_fallback_response(prompt)
    except Exception as e:
        print(f"❌ OpenRouter API unexpected error: {e}")
        return get_fallback_response(prompt)

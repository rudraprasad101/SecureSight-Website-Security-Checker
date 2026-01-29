"""
AI Helper Module
Generates AI prompts and optionally calls Gemini API to produce explanations.
If `GEMINI_API_KEY` is set in the environment (or .env), the app can request
live, step-by-step explanations from the Gemini API. Otherwise it returns a
prompt that you can paste into any AI chat service.
"""

import os
import time
import threading
import functools
from dotenv import load_dotenv

load_dotenv()

try:
    import google.genai as genai
except Exception:
    genai = None

# Simple in-process rate limiter to avoid rapid-fire calls
_last_call_lock = threading.Lock()
_last_call_time = 0.0
_MIN_CALL_INTERVAL = 0.8  # seconds between calls (adjust as needed)


def generate_ai_prompt(issue: dict) -> str:
    """
    Creates an AI prompt that explains a security issue in detail.
    This helps beginners understand what each vulnerability means.
    
    Args:
        issue: Dictionary containing security issue details
        
    Returns:
        A formatted prompt ready to copy into an AI chatbot
    """
    title = issue.get("title", "Unknown Issue")
    details = issue.get("details", "No details available")
    fix = issue.get("fix", "No fix information available")
    severity = issue.get("severity", "Unknown")
    
    # Create a comprehensive prompt for AI
    prompt = f"""
Explain this web security issue to a beginner:

Issue: {title}
Severity: {severity}
Description: {details}
Recommended Fix: {fix}

Please explain:
1. What does this mean in simple terms?
2. Why is this a security risk?
3. What could happen if not fixed?
4. Step-by-step how to fix it
5. How to verify the fix works

Keep your explanation suitable for someone learning web security for the first time.
"""
    
    return prompt.strip()


def _call_gemini_for_prompt(prompt_text: str, model: str = "gemini-2.0-flash") -> str:
    """Internal helper that calls Gemini for a given prompt string.

    This function is cached to avoid duplicate requests for the same prompt.
    """
    # Rate limiting (simple): ensure at least _MIN_CALL_INTERVAL between calls
    global _last_call_time
    with _last_call_lock:
        now = time.time()
        elapsed = now - _last_call_time
        if elapsed < _MIN_CALL_INTERVAL:
            time.sleep(_MIN_CALL_INTERVAL - elapsed)
        _last_call_time = time.time()

    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=prompt_text,
        config=genai.types.GenerateContentConfig(
            max_output_tokens=800,
            temperature=0.3,
        )
    )

    if response and hasattr(response, 'text') and response.text:
        return response.text.strip()
    elif response:
        return "Gemini API returned an empty response. Please try again."
    else:
        return "No response from Gemini API. Please check your internet connection and try again."


# Cached wrapper around the low-level call
_cached_call = functools.lru_cache(maxsize=256)(_call_gemini_for_prompt)


def generate_ai_explanation(issue: dict, model: str = "gemini-2.0-flash") -> str:
    """
    Generate an explanation for the given issue using Gemini (cached + rate-limited).
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return (
            "⚠️ Gemini API key not found. To enable live AI explanations, add \"GEMINI_API_KEY\" "
            "to your .env file."
        )

    if genai is None:
        return (
            "⚠️ The `google-genai` Python package is not installed. Install it with: `pip install google-genai`"
        )

    prompt_text = generate_ai_prompt(issue)

    try:
        return _cached_call(prompt_text, model)
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            return f"⚠️ API Quota Exceeded\n\nYour Gemini API quota has been exceeded. Please wait a few minutes before trying again, or upgrade your plan at https://ai.google.dev/pricing"
        elif "401" in error_msg or "unauthorized" in error_msg.lower():
            return f"⚠️ Authentication Error\n\nYour API key is invalid or has expired. Please check your GEMINI_API_KEY in the .env file."
        elif "403" in error_msg or "permission" in error_msg.lower():
            return f"⚠️ Permission Error\n\nYour API key doesn't have access. Make sure Gemini API is enabled in your Google Cloud Console."
        else:
            return f"⚠️ Error: {error_msg}\n\nPlease check your internet connection and API key."


def clear_ai_cache() -> bool:
    """Clear the in-process AI response cache."""
    try:
        _cached_call.cache_clear()
        return True
    except Exception:
        return False


def is_api_configured() -> tuple[bool, str]:
    """Return (configured, message) indicating API key and package status."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return False, "GEMINI_API_KEY not set"
    if genai is None:
        return False, "google-genai package not installed"
    return True, "Gemini API available"

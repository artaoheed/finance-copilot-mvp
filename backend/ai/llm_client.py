import os
import json
import time
import random
from typing import List, Dict, Any, Optional

# --- Provider SDK Imports (install the ones you need) ---
# pip install openai google-generativeai anthropic

try:
    import openai
except ImportError:
    openai = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    import anthropic
except ImportError:
    anthropic = None


# --- Configuration ---
PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # "openai", "gemini", or "claude"

# API Keys (set via environment variables)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")


# --- Helper Function: Retry Decorator ---
def with_retries(func):
    def wrapper(*args, **kwargs):
        for i in range(3):  # 3 retries
            try:
                return func(*args, **kwargs)
            except Exception as e:
                wait = 2 ** i + random.random()
                print(f"⚠️ Error: {e}. Retrying in {wait:.1f}s...")
                time.sleep(wait)
        raise RuntimeError("❌ Failed after 3 retries.")
    return wrapper


# --- Unified LLM Interface ---
class LLMClient:
    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or PROVIDER.lower()
        if self.provider == "openai" and openai:
            openai.api_key = OPENAI_API_KEY
        elif self.provider == "gemini" and genai:
            genai.configure(api_key=GEMINI_API_KEY)
        elif self.provider == "claude" and anthropic:
            self.client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        else:
            raise ValueError(f"Unsupported or improperly configured provider: {self.provider}")

    @with_retries
    def generate(self, prompt: str) -> str:
        if self.provider == "openai":
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return response.choices[0].message["content"].strip()

        elif self.provider == "gemini":
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text.strip()

        elif self.provider == "claude":
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()

        else:
            raise ValueError(f"Unknown provider: {self.provider}")


# --- High-level Function: Analyze Transactions ---
def analyze_transactions_with_llm(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Given a list of transaction dicts, call an LLM to:
    1. Identify top 3 spending categories.
    2. Suggest one actionable advice.
    3. Summarize monthly spending in 3 sentences.
    """

    prompt = f"""
You are a financial analyst. Analyze this transaction list:
{json.dumps(transactions[:100], indent=2)}

Return a JSON with this structure only:
{{
  "top_categories": [
    {{"category": "Food", "total": 1234.56}},
    ...
  ],
  "advice": "string",
  "summary": "string"
}}
    """

    llm = LLMClient()
    raw_output = llm.generate(prompt)

    try:
        # Attempt to parse JSON response from model
        start = raw_output.find("{")
        end = raw_output.rfind("}") + 1
        return json.loads(raw_output[start:end])
    except Exception as e:
        print("⚠️ Failed to parse LLM response:", e)
        return {"error": "Failed to parse response", "raw_output": raw_output}


    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful finance assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    # Extract model response
    content = response["choices"][0]["message"]["content"]

    # Attempt to parse as JSON
    import json
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # If model returned non-JSON, wrap in dict
        return {"raw_response": content}

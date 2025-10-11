import json
import asyncio
from typing import Dict, Any
from openai import AsyncOpenAI  # Changed to AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Changed to AsyncOpenAI

# Model configuration with environment variables
SMALL_MODEL = os.getenv("SMALL_MODEL", "gpt-3.5-turbo")  # Router/Chitchat
MEDIUM_MODEL = os.getenv("MEDIUM_MODEL", "gpt-4")        # Researcher
LARGE_MODEL = os.getenv("LARGE_MODEL", "gpt-4-turbo")    # Main

async def small_llm(text: str, system: str = "You are a fast, cheap intent router and casual chat bot.") -> str:
    """Use small LLM for quick tasks like routing and chitchat"""
    resp = await _client.chat.completions.create(
        model=SMALL_MODEL,
        messages=[{"role":"system","content":system},
                  {"role":"user","content":text}],
        temperature=0.2,
    )
    return resp.choices[0].message.content

async def medium_llm(text: str, system: str = "You write search queries and summarize results into bullet points.") -> str:
    """Use medium LLM for research and analysis tasks"""
    resp = await _client.chat.completions.create(
        model=MEDIUM_MODEL,
        messages=[{"role":"system","content":system},
                  {"role":"user","content":text}],
        temperature=0.3,
    )
    return resp.choices[0].message.content

async def main_llm_json(prompt: str) -> Dict[str, Any]:
    """Use large LLM for final response generation with JSON output"""
    resp = await _client.chat.completions.create(
        model=LARGE_MODEL,
        messages=[{"role":"user","content":prompt}],
        response_format={"type": "json_object"},
        temperature=0.5,
    )
    try:
        return json.loads(resp.choices[0].message.content)
    except Exception:
        return {"answer_text": resp.choices[0].message.content}
from typing import Dict, Any
from ..schemas import ContextBundle, UserProfile
from .llm import medium_llm
from .tools.web_search import web_search
from .tools.vector_db import vector_search
from .tools.flights_api import search_flights
from .tools.hotels_api import search_hotels

RESEARCHER_SYS = (
    "You are a research orchestrator for a travel assistant. "
    "Given the user input and profile, produce search queries, decide which tools to call, "
    "and return succinct bullet summaries for prompt grounding."
)

async def build_context_bundle(user_input: str, user_profile: UserProfile, intent: str) -> ContextBundle:
    """
    Build comprehensive context bundle using medium LLM for orchestration
    """
    # 1) Medium LLM suggests search strategy
    plan_prompt = f"""
[INPUT]
{user_input}

[PROFILE]
{user_profile.model_dump()}

[INTENT]
{intent}

[INSTRUCTIONS]
- Make 2-4 web search queries.
- Suggest 1-2 vector_db topics.
- Decide if flights/hotels APIs are needed based on intent and dates.
- Return JSON with keys: web_queries, vector_topics, need_flights, need_hotels.
"""
    plan_raw = await medium_llm(plan_prompt, system=RESEARCHER_SYS)
    plan = _safe_json(plan_raw, fallback={
        "web_queries": [user_input],
        "vector_topics": [],
        "need_flights": intent == "trip_generation",
        "need_hotels": intent in ("trip_generation", "trip_qa")
    })

    # 2) Parallel tool execution
    import asyncio
    tasks = [
        web_search(plan["web_queries"]),
        vector_search(plan["vector_topics"])
    ]

    if plan.get("need_flights"):
        tasks.append(search_flights(user_input, user_profile))
    if plan.get("need_hotels"):
        tasks.append(search_hotels(user_input, user_profile))

    results = await asyncio.gather(*tasks)

    web_snippets = results[0]
    vector_notes = results[1]
    idx = 2
    flights = results[idx] if plan.get("need_flights") else []
    idx += 1 if plan.get("need_flights") else 0
    hotels = results[idx] if plan.get("need_hotels") else []

    # 3) Sentiment/summary generation
    summary_prompt = f"""
Summarize web and vector findings into compact bullet points (Korean).
Focus on hotel/attraction/food sentiments and constraints.

[WEB]
{web_snippets}

[VECTOR]
{vector_notes}
"""
    sentiments_text = await medium_llm(summary_prompt)
    sentiments = {"bullets": sentiments_text}

    return ContextBundle(
        web_snippets=web_snippets,
        vector_notes=vector_notes,
        flights=flights,
        hotels=hotels,
        sentiments=sentiments
    )

def _safe_json(text: str, fallback: Dict[str, Any]) -> Dict[str, Any]:
    """Safely parse JSON with fallback"""
    try:
        import json
        return json.loads(text)
    except Exception:
        return fallback
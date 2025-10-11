from ..schemas import ContextBundle

SYSTEM_RULES = """
You are a senior travel planner. Output MUST be valid JSON with keys:
- answer_text (string, Korean)
- itinerary (array of items with day, title, activities[], est_cost?, city?) WHEN intent == trip_generation
- selected_flights (array)? WHEN flights in context exist
- selected_hotels (array)? WHEN hotels in context exist
- assumptions (array of strings)?
- warnings (array of strings)?
Keep prices in user's currency if possible.
Be concise but actionable.
"""

def build_main_prompt(user_input: str, ctx: ContextBundle, intent: str) -> str:
    """
    Build prompt for main LLM including context bundle and system rules
    """
    return f"""
[SYSTEM_RULES]
{SYSTEM_RULES}

[INTENT]
{intent}

[USER_INPUT]
{user_input}

[CONTEXT.web_snippets]
{ctx.web_snippets}

[CONTEXT.vector_notes]
{ctx.vector_notes}

[CONTEXT.flights]
{ctx.flights}

[CONTEXT.hotels]
{ctx.hotels}

[CONTEXT.sentiments]
{ctx.sentiments}

Return ONLY JSON.
"""
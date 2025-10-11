import json
from typing import Dict, Any
from ..schemas import MainModelOutput
from .llm import main_llm_json

VALIDATION_HINT = """
Your previous JSON did not match the schema. Fix it strictly.
Only return valid JSON. Do not add comments or text outside JSON.
SCHEMA summary:
- answer_text: string (required)
- itinerary: array of objects {day:int,title:str,activities:list[str],est_cost?:number,city?:str}
- selected_flights: array?
- selected_hotels: array?
- assumptions: array?
- warnings: array?
"""

async def validate_or_retry(original_prompt: str, candidate_json: Dict[str, Any], max_tries: int = 2) -> Dict[str, Any]:
    """
    Validate JSON output against schema and retry with feedback if invalid
    """
    for attempt in range(max_tries + 1):
        try:
            MainModelOutput(**candidate_json)  # pydantic validation
            return candidate_json
        except Exception as e:
            if attempt == max_tries:
                # Last attempt: return safe fallback with answer_text only
                return {
                    "answer_text": candidate_json.get(
                        "answer_text",
                        "요청을 처리하는 중 오류가 있었습니다."
                    )
                }
            fix_prompt = f"{original_prompt}\n\n[VALIDATION_ERROR]\n{str(e)}\n\n{VALIDATION_HINT}"
            candidate_json = await main_llm_json(fix_prompt)
    return candidate_json
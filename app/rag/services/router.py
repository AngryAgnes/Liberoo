from typing import Literal
from ..schemas import UserProfile
from .llm import small_llm

async def route_intent(user_input: str, profile: UserProfile) -> Literal["trip_qa", "trip_generation", "chitchat"]:
    """
    Route user input to appropriate intent using small LLM
    """
    system = (
        "You classify travel assistant intents. "
        "Return one of: trip_qa, trip_generation, chitchat. "
        "trip_qa = 여행 관련 사실/정보/비교 질문. "
        "trip_generation = 일정/루트/플랜 생성 요청. "
        "chitchat = 잡담, 비여행 대화."
        "Answer ONLY the label."
    )
    label = (await small_llm(user_input, system=system)).strip().lower()
    if label not in {"trip_qa", "trip_generation", "chitchat"}:
        label = "trip_qa"
    return label  # type: ignore
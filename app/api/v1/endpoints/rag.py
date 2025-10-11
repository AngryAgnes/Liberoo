from fastapi import APIRouter, HTTPException
from app.rag.schemas import ChatRequest, ChatResponse, UserProfile
from app.rag.services.router import route_intent
from app.rag.services.researcher import build_context_bundle
from app.rag.services.prompt import build_main_prompt
from app.rag.services.llm import main_llm_json
from app.rag.services.validator import validate_or_retry

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Main chat endpoint using 3-LLM RAG system
    """
    try:
        # 1) Router (Small LLM)
        intent = await route_intent(req.user_input, req.user_profile)

        if intent == "chitchat":
            # Handle chitchat directly with small LLM
            return ChatResponse(
                intent=intent,
                answer=f"안녕하세요! 여행 이야기를 해볼까요? 🙂 '{req.user_input}'"
            )

        # 2) Researcher (Medium LLM) - orchestrate API calls
        context_bundle = await build_context_bundle(
            user_input=req.user_input,
            user_profile=req.user_profile,
            intent=intent
        )

        # 3) Main (Large LLM) - generate structured response
        prompt = build_main_prompt(req.user_input, context_bundle, intent=intent)
        raw_json = await main_llm_json(prompt)

        # 4) Validate schema & retry if needed
        final_json = await validate_or_retry(
            original_prompt=prompt,
            candidate_json=raw_json
        )

        return ChatResponse(
            intent=intent,
            answer=final_json.get("answer_text"),
            structured=final_json
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
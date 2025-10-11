from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

Intent = Literal["trip_qa", "trip_generation", "chitchat"]

class UserProfile(BaseModel):
    home_airport: Optional[str] = None
    budget_level: Optional[Literal["low","mid","high"]] = None
    locale: Optional[str] = "ko-KR"
    currency: Optional[str] = "KRW"
    travelers: Optional[int] = 1
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class ChatRequest(BaseModel):
    user_input: str
    user_profile: UserProfile = UserProfile()

class ContextBundle(BaseModel):
    web_snippets: List[Dict[str, Any]] = []
    vector_notes: List[Dict[str, Any]] = []
    flights: List[Dict[str, Any]] = []
    hotels: List[Dict[str, Any]] = []
    sentiments: Optional[Dict[str, Any]] = None

class ItineraryItem(BaseModel):
    day: int
    title: str
    activities: List[str] = []
    est_cost: Optional[float] = None
    city: Optional[str] = None

class MainModelOutput(BaseModel):
    answer_text: str = Field(..., description="사용자에게 보여줄 자연어 요약")
    itinerary: Optional[List[ItineraryItem]] = None
    selected_flights: Optional[List[Dict[str, Any]]] = None
    selected_hotels: Optional[List[Dict[str, Any]]] = None
    assumptions: Optional[List[str]] = None
    warnings: Optional[List[str]] = None

class ChatResponse(BaseModel):
    intent: Intent
    answer: str
    structured: Optional[MainModelOutput] = None
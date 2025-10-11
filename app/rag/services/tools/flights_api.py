from typing import Dict, Any, List
import asyncio
from ...schemas import UserProfile

async def search_flights(user_input: str, profile: UserProfile) -> List[Dict[str, Any]]:
    """
    Mock flight search implementation - integrate with actual flight API
    Possible integrations: Amadeus, Duffel, Skyscanner
    """
    await asyncio.sleep(0.05)
    if not profile.start_date or not profile.end_date or not profile.home_airport:
        return []
    return [{
        "from": profile.home_airport,
        "to": "HND",
        "dates": [profile.start_date, profile.end_date],
        "price": 850000,
        "currency": profile.currency
    }]
from typing import List, Dict, Any
import asyncio

async def vector_search(topics: List[str]) -> List[Dict[str, Any]]:
    """
    Mock vector search implementation - integrate with actual vector DB
    Supported backends: FAISS (current), Pinecone, Weaviate, pgvector
    """
    await asyncio.sleep(0.02)
    return [{"topic": t, "passage": f"{t} 관련 노트 요약"} for t in topics[:3]]
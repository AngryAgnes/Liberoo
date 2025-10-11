from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from pydantic import BaseModel
from app.rag.model import RAGModel

# Initialize RAG model
rag_model = RAGModel()

router = APIRouter()

class DocumentInput(BaseModel):
    texts: List[str]
    metadatas: Optional[List[Dict]] = None

class QuestionInput(BaseModel):
    question: str
    num_contexts: Optional[int] = 4

@router.post("/add-knowledge")
async def add_knowledge(input_data: DocumentInput):
    """Add documents to the RAG knowledge base"""
    try:
        rag_model.add_knowledge(input_data.texts, input_data.metadatas)
        return {"status": "success", "message": f"Added {len(input_data.texts)} documents to knowledge base"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate")
async def generate_response(input_data: QuestionInput):
    """Generate a response using the RAG model"""
    try:
        response = await rag_model.generate_response(
            question=input_data.question,
            num_contexts=input_data.num_contexts
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save-knowledge")
async def save_knowledge(path: str):
    """Save the knowledge base to disk"""
    try:
        rag_model.save_knowledge_base(path)
        return {"status": "success", "message": f"Knowledge base saved to {path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/load-knowledge")
async def load_knowledge(path: str):
    """Load the knowledge base from disk"""
    try:
        rag_model.load_knowledge_base(path)
        return {"status": "success", "message": f"Knowledge base loaded from {path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import APIRouter
from . import users, auth, rag

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(rag.router, prefix="/rag", tags=["RAG"])

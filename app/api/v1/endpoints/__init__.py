from fastapi import APIRouter
from . import users, auth

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

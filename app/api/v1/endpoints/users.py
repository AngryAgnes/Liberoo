from typing import Annotated
from fastapi import APIRouter, Depends
from app.core.auth import get_current_active_user
from app.schemas.user import User

router = APIRouter()


@router.get("/")
async def get_users(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> dict:
    """
    Retrieve a list of users.
    Requires authentication.
    """
    return {
        "authenticated_user": current_user.username
    }


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """Get current user info."""
    return current_user

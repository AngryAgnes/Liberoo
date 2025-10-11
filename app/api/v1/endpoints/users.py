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

@router.get("/{user_id}")
async def get_user(user_id: int):
    """Retrieve a user by ID."""
    return {"user_id": user_id, "username": f"user{user_id}"}


@router.post("/")
async def create_user():
    """Create a new user."""
    return {"message": "User created"}


@router.patch("/{user_id}")
async def update_user(user_id: int):
    """Update user information."""
    return {"message": f"User {user_id} updated"}


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """Delete a user."""
    return {"message": f"User {user_id} deleted"}


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """Get current user info."""
    return current_user

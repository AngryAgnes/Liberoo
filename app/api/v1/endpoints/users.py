from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_users() -> dict:
    """
    Retrieve a list of users.
    """
    return {"message": "List of users"}

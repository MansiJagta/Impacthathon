from fastapi import APIRouter, Depends, HTTPException
from app.schemas import UserCreate, UserLogin
from app.database import user_collection
from app.auth import hash_password, verify_password, create_access_token
from app.dependencies import get_current_user, require_role

router = APIRouter()


@router.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "You are authorized", "user": current_user}

@router.get("/admin-only")
async def admin_route(user: dict = Depends(require_role("admin"))):
    return {"message": "Welcome Admin"}
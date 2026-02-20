from fastapi import APIRouter, Depends, HTTPException
from app.schemas import UserCreate, UserLogin
from app.database import user_collection
from app.auth import hash_password, verify_password, create_access_token
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/signup")
async def signup(user: UserCreate):

    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)

    user_dict = user.dict()
    user_dict["password"] = hashed_pw

    await user_collection.insert_one(user_dict)

    return {"message": "User created successfully"}

@router.post("/login")
async def login(user: UserLogin):

    db_user = await user_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": str(db_user["_id"]),
        "email": db_user["email"],
        "role": db_user.get("role", "user")
    })

    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
async def get_current_user(current_user: dict = Depends(get_current_user)):
    return {
        "user_id": current_user.get("user_id"),
        "email": current_user.get("email"),
        "role": current_user.get("role", "user")
    }

@router.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "You are authorized", "user": current_user}
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

router = APIRouter()

MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client["intelliclaim"]
users_collection = db["users"]


class SignupRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str


@router.post("/signup")
def signup(data: SignupRequest):

    existing_user = users_collection.find_one({"email": data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    users_collection.insert_one(
        {
            "name": data.name,
            "email": data.email,
            "password": data.password,  # later we hash this
            "role": data.role,
            "created_at": datetime.utcnow(),
        }
    )

    return {"message": "User created successfully"}


from app.core.security import create_access_token  # make sure this exists


class LoginRequest(BaseModel):
    email: str
    password: str
    role: str


@router.post("/login")
def login(data: LoginRequest):

    user = users_collection.find_one({"email": data.email, "role": data.role})

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token({"sub": user["email"], "role": user["role"]})

    return {"access_token": token, "token_type": "bearer"}

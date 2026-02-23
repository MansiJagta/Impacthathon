from fastapi import Depends
from fastapi.security import HTTPBearer
from app.core.security import verify_token

security = HTTPBearer()


def get_current_user(token=Depends(security)):
    return verify_token(token.credentials)

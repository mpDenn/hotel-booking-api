from schemas.auth import LoginRequest, TokenResponse
from services.security import authenticate_user, create_access_token
from fastapi import APIRouter, Depends
from database import get_db
from fastapi import HTTPException
router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def user_login(user_data: LoginRequest, db = Depends(get_db)):
    user = authenticate_user(user_data.email, user_data.password, db)

    if user is None:
        raise HTTPException(
                status_code=401, 
                detail="Incorrect email or password"
                )

    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

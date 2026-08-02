from schemas.user import UserCreate, UserResponse
from services.user import usercreate
from fastapi import APIRouter, Depends
from database import get_db
router = APIRouter()


@router.post("/users", response_model = UserResponse)
def create_user(user:UserCreate, db = Depends(get_db)):
    new_user = usercreate(user,db)

    return new_user
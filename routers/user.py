from schemas.user import UserCreate, UserResponse, UserUpdate 
from services.user import usercreate
from fastapi import APIRouter, Depends
from database import get_db
from fastapi import HTTPException
from services.user import (
    get_users, 
    get_user_by_id,
    update_user,
    delete_user
)
router = APIRouter()


@router.post("/users", response_model = UserResponse)
def create_user(user:UserCreate, db = Depends(get_db)):
    new_user = usercreate(user,db)

    return new_user

@router.get("/users", response_model = list[UserResponse])
def get_users_endpoint(db = Depends(get_db)):
    users = get_users(db)

    return users

@router.get("/user/{user_id}", response_model = UserResponse)
def get_user_endpoint(user_id: int, db = Depends(get_db)):
    user = get_user_by_id(user_id, db)

    if user is None:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
        )
    
    return user

@router.patch("/user/{user_id}", response_model=UserResponse)
def change_user_endpoint(user_id: int,user_data: UserUpdate,  db = Depends(get_db)):
    user = update_user(user_id, user_data, db)

    if user is None:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
        )

    return user

@router.delete("/user/{user_id}")
def delete_user_endpint(user_id: int, db = Depends(get_db)):
    user = delete_user(user_id, db)

    if user is None:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
        )
    return user


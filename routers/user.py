from schemas.user import UserCreate, UserResponse, UserUpdate
from services.user import create_new_user
from fastapi import APIRouter, Depends
from database import get_db
from fastapi import HTTPException
from services.security import get_current_user, get_current_admin
from services.user import (
    get_users,
    get_user_by_id,
    update_user,
    delete_user
)
router = APIRouter()


@router.post("/users", response_model = UserResponse)
def create_user(user:UserCreate, db = Depends(get_db)):
    new_user = create_new_user(user,db)

    if new_user == "email_exist":
        raise HTTPException(
            status_code=409,
            detail = "Email already exists"
        )

    return new_user

@router.get("/users", response_model = list[UserResponse])
def get_users_endpoint(current_admin = Depends(get_current_admin), db = Depends(get_db)):
    users = get_users(db)

    return users

@router.get("/me", response_model = UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user

@router.get("/user/{user_id}", response_model = UserResponse)
def get_user_endpoint(user_id: int,current_admin = Depends(get_current_admin), db = Depends(get_db)):
    user = get_user_by_id(user_id, db)

    if user is None:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
        )

    return user

@router.patch("/user/{user_id}", response_model=UserResponse)
def change_user_endpoint(
            user_id: int,
            user_data: UserUpdate,
            current_admin = Depends(get_current_admin),
            db = Depends(get_db)):

    user = update_user(user_id, user_data, db)

    if user == "name_cant_be_none":
            raise HTTPException(
                    status_code = 422,
                    detail = "Name can't be none"
                   )

    if user == "surname_cant_be_none":
                raise HTTPException(
                        status_code = 422,
                        detail = "Surname can't be none"
                       )

    if user == "email_cant_be_none":
        raise HTTPException(
                status_code = 422,
                detail = "Email can't be none"
               )

    if user == "email_exist":
        raise HTTPException(
                status_code = 409,
                detail = "Email already exists"
            )

    if user == "user_not_found":
        raise HTTPException(
                status_code = 404,
                detail = "User not found"
            )

    return user

@router.delete("/user/{user_id}", response_model=UserResponse)
def delete_user_endpoint(
        user_id: int,
        current_admin = Depends(get_current_admin),
        db = Depends(get_db)
        ):

    user = delete_user(user_id, db)

    if user == "user_none":
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
        )
    if user == "user_has_bookings":
         raise HTTPException(
            status_code = 409,
            detail = "User has existing bookings"
        )
    return user


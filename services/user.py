from schemas.user import UserCreate
from models.user import User
from services.security import hash_password
from sqlalchemy import select


def usercreate(user: UserCreate, db):

    email_check = db.execute(select(User).where(User.email == user.email)).scalars().first()
    if email_check:
        return "email_exist"
    hashed_password = hash_password(user.password)
    new_user = User(
        email = user.email,
        name = user.name,
        surname = user.surname,
        password_hash = hashed_password,
        phone = user.phone
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get_users(db):
    
    users = db.execute(select(User)).scalars().all()
    return users

def get_user_by_id(user_id, db):
    user = db.execute(
                select(User).where(User.id == user_id)
                    ).scalars().first()
    return user

def update_user(user_id, user_data, db):
    user = get_user_by_id(user_id, db)

    if user is None:
        return "User_none"
    
    data = user_data.model_dump(exclude_unset=True)

    if "name" in data and data["name"] is None:
         return "name_cant_be_none"

    if "surname" in data and data["surname"] is None:
            return "surname_cant_be_none"

    if "email" in data:
        new_email = data["email"]
        if new_email is None:
                return "email_cant_be_none"
        email_check = db.execute(select(User).where(User.email == new_email)).scalars().first()
        if email_check is not None:
            if email_check.id != user_id:
                    return "email_exist"

    password = data.pop("password", None)

    if password is not None:
        user.password_hash = hash_password(password)
        
    for field, value in data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user

def delete_user(user_id, db):
    user = get_user_by_id(user_id, db)

    if user is None:
        return "user_none"
    
    db.delete(user)
    db.commit()

    return user

from schemas.user import UserCreate
from models.user import User
from sqlalchemy import select

def usercreate(user: UserCreate, db):

    new_user = User(
        email = user.email,
        name = user.name,
        surname = user.surname,
        password = user.password
        
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


    
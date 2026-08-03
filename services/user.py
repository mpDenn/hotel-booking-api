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




    
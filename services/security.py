from passlib.context import CryptContext
from sqlalchemy import select
from models.user import User
import jwt
from datetime import datetime, timedelta, timezone
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password):
    hashed_password = pwd_context.hash(password)
    return hashed_password

def verify_password(password, hashed_password):
    verify = pwd_context.verify(password,hashed_password)

    return verify

def authenticate_user(email, password, db):

    user_find = db.execute(select(User).where(User.email == email)).scalars().first()
    if user_find is None:
        return None

    password_hash = user_find.password_hash

    user_password_check = verify_password(password, password_hash)
    if user_password_check is False:
        return None

    return user_find

def create_access_token(user_id):

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm = ALGORITHM
    )

    return token





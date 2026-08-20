from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
bearer_scheme = HTTPBearer()
from database import get_db
from passlib.context import CryptContext
from sqlalchemy import select
from models.user import User
import jwt
from fastapi import HTTPException
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

def decode_access_token(token):

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    user_payload = int(payload["sub"])

    return user_payload

def get_current_user(
                credential: HTTPAuthorizationCredentials = Depends(bearer_scheme),
                db = Depends(get_db)
                    ):
    token = credential.credentials

    try:
        user_id = decode_access_token(token)
    except (jwt.InvalidTokenError, KeyError, ValueError) as error:
        
        raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
                )       

    user = db.execute(select(User).where(User.id == user_id)).scalars().first()

    if user is None:
        raise HTTPException(
                status_code = 401,
                detail = "Invalid authentication credentials"
                )

    return user
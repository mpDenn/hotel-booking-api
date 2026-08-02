from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()
class Base(DeclarativeBase):
    pass

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()
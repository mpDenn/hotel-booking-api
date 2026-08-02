from fastapi import FastAPI
app = FastAPI()
from routers.user import router
app.include_router(router)
from database import Base, engine
from models.user import User

Base.metadata.create_all(bind=engine)
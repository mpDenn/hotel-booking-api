from fastapi import FastAPI
app = FastAPI()
from routers import user, room
app.include_router(user.router)
app.include_router(room.router)
from database import Base, engine
from models.user import User
from models.rooms import Room

Base.metadata.create_all(bind=engine)





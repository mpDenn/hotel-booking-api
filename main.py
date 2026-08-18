from fastapi import FastAPI
app = FastAPI()
from routers import user, room, booking, auth
from database import Base, engine
Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(room.router)
app.include_router(booking.router)
app.include_router(auth.router)





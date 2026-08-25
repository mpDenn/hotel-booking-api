from fastapi import FastAPI
app = FastAPI()
from routers import user, room, booking, auth


app.include_router(user.router)
app.include_router(room.router)
app.include_router(booking.router)
app.include_router(auth.router)





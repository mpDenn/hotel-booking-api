from pydantic import BaseModel
from datetime import date

class BookingCreate(BaseModel):
    user_id: int
    room_id: int
    check_in: date
    check_out: date
    guests: int

class BookingReasponse(BaseModel):
    id: int
    user_id: int
    room_id: int
    check_in: date
    check_out: date
    guests: int

class BookingPatch(BaseModel):
    check_in: date
    check_out: date

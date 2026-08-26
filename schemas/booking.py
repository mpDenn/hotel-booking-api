from pydantic import BaseModel, Field
from datetime import date

class BookingCreate(BaseModel):
    room_id: int = Field(gt=0)
    check_in: date
    check_out: date
    guests: int = Field(gt=0)

class BookingResponse(BaseModel):
    id: int
    user_id: int
    room_id: int
    check_in: date
    check_out: date
    guests: int

class BookingPatch(BaseModel):
    check_in: date
    check_out: date

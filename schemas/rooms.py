from pydantic import BaseModel
from decimal import Decimal


class RoomResponse(BaseModel):
    id: int
    number: int
    room_type: str
    price: Decimal | None = None
    base_capacity: int
    max_capacity: int

class RoomPriceUpdate(BaseModel):
    price: Decimal

class RoomCreate(BaseModel):
    number: int
    room_type: str
    price: Decimal
    base_capacity: int
    max_capacity: int





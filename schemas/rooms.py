from pydantic import BaseModel, Field
from decimal import Decimal

class RoomResponse(BaseModel):
    id: int
    number: int
    room_type: str
    price: Decimal
    base_capacity: int
    max_capacity: int

class RoomPriceUpdate(BaseModel):
    price: Decimal = Field(gt=0)

class RoomCreate(BaseModel):
    number: int
    room_type: str
    price: Decimal = Field(gt=0)
    base_capacity: int = Field(gt=0)
    max_capacity: int = Field(gt=0)





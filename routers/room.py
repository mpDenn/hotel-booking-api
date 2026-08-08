from schemas.rooms import RoomResponse, RoomPriceUpdate, RoomCreate
from services.rooms import get_rooms, get_room_id,update_room_price, create_room
from fastapi import APIRouter, Depends
from database import get_db
from fastapi import HTTPException
router = APIRouter()

@router.get("/rooms", response_model = list[RoomResponse])
def get_rooms_endpoint(db = Depends(get_db)):
    rooms = get_rooms(db)

    return rooms

@router.get("/rooms/{room_id}", response_model = RoomResponse)
def get_room_endpint(room_id: int , db = Depends(get_db)):
    room = get_room_id(room_id, db)

    if room is None:
            raise HTTPException(
                status_code = 404,
                detail = "Room not found"
            )
    return room

@router.patch("/rooms/{room_id}", response_model = RoomResponse)
def price_update_endpoint(room_id:int, room_data:RoomPriceUpdate, db = Depends(get_db)):
    room = update_room_price(room_id, room_data, db)

    if room is None:
        raise HTTPException(
                status_code = 404,
                detail = "Room not found"
                )

    return room

@router.post("/rooms", response_model = RoomResponse)
def create_room_endpoint(room_data: RoomCreate, db = Depends(get_db)):
    room = create_room(room_data, db)

    return room

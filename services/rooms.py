from models.rooms import Room
from sqlalchemy import select

def get_rooms(db):
    rooms = db.execute(select(Room)).scalars().all()
    return rooms

def get_room_id(room_id, db):
    room = db.execute(select(Room).where(Room.id == room_id)).scalars().first()
    return room

def update_room_price(room_id, room_data, db):
    room = get_room_id(room_id, db)

    if room is None:
        return "room_none"

    room.price = room_data.price

    db.commit()
    db.refresh(room)

    return room

def create_room(room_data, db):

    room = Room(
        number = room_data.number,
        room_type = room_data.room_type,
        price = room_data.price,
        base_capacity = room_data.base_capacity,
        max_capacity = room_data.max_capacity,
    )

    db.add(room)
    db.commit()
    db.refresh(room)

    return room





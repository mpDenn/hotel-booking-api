from schemas.booking import BookingReasponse, BookingCreate, BookingPatch
from models.booking import Booking
from sqlalchemy import select
from services.user import get_user_by_id
from services.rooms import get_room_id

def booking_create(booking_data: BookingCreate, db):
    user = get_user_by_id(booking_data.user_id, db)
    room = get_room_id(booking_data.room_id, db)

    if user is None:
        return None
    if room is None:
        return None

    guests_max = room.max_capacity
    check_in = booking_data.check_in
    check_out = booking_data.check_out
    guests = booking_data.guests

    if check_in >= check_out:
        return "wrong_data"

    if guests > guests_max:
        return "too_many_guests"
    
    booking_conflict = book_time_conflict(booking_data.room_id, check_in, check_out, db)

    if booking_conflict:
        return "booking_conflict"

    new_booking = Booking(
        user_id = booking_data.user_id,
        room_id = booking_data.room_id,
        check_in = booking_data.check_in,
        check_out = booking_data.check_out,
        guests = booking_data.guests,
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking

def get_user_bookings(user_id, db):

    user_bookings = db.query(Booking).filter(Booking.user_id == user_id).all()

    return user_bookings
  
def delete_booking(booking_id, db):

    booking = db.execute(select(Booking).where(Booking.id == booking_id)).scalars().first()
    if booking is None:
        return None
    
    db.delete(booking)
    db.commit()
    return booking

def time_book_patch(booking_id, check_in, check_out, db):

    db_time = db.execute(select(Booking). where(Booking.id == booking_id)).scalars().first()
    
    if db_time is None:
        return "booking_not_exist"

    if check_in >= check_out:
        return "wrong_data"
    
    room_id = db_time.room_id
    exeption_book_id = db_time.id

    conflict = book_time_conflict(room_id, check_in, check_out, db, exeption_book_id)

    if conflict:
        return "booking_conflict"

    db_time.check_in = check_in
    db_time.check_out = check_out

    

    db.commit()
    db.refresh(db_time)
    return db_time

def book_time_conflict(room_id, check_in, check_out, db, exeption_book_id = None ):

    booking = db.execute(select(Booking).where(
                                    Booking.room_id == room_id,
                                    Booking.id !=exeption_book_id,
                                    Booking.check_in < check_out,
                                    Booking.check_out > check_in,
                                    )
                                    ).scalars().first()

    if booking is None:
        return False

    return True
    
    




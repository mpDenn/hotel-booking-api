from schemas.booking import BookingReasponse, BookingCreate, BookingPatch
from models.booking import Booking

from services.user import get_user_by_id
from services.rooms import get_room_id

def has_booking_conflict(room_id, check_in, check_out, db):
    bookings = db.query(Booking).filter(Booking.room_id == room_id).all()

    for book in bookings:
        if book.check_in <= check_out:
            if book.check_out >= check_in:
                return True

    return False

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
        return None

    if guests > guests_max:
        return None
    
    booking_conflict = has_booking_conflict(booking_data.room_id, check_in, check_out, db)

    if booking_conflict:
        return None

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

def booking_patch_time(booking_id: int,booking_data: BookingPatch, db):

    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking is None:
        return None

    check_in = booking_data.check_in
    check_out = booking_data.check_out

    if check_in >= check_out:
        return None

    booking.check_in = check_in
    booking.check_out = check_out

    db.commit()
    db.refresh(booking)
    return booking
    

    
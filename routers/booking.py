from schemas.booking import BookingReasponse, BookingCreate, BookingPatch
from models.booking import Booking
from services.booking import booking_create, get_user_bookings, booking_patch_time, delete_booking
from fastapi import APIRouter, Depends
from database import get_db
from fastapi import HTTPException
router = APIRouter()

@router.post("/booking")
def create_booking_endpoint(booking_data: BookingCreate, db = Depends(get_db)):
    booking = booking_create(booking_data, db)
    
    if booking == "wrong_data":
        raise HTTPException(
                status_code = 400,
                detail ="Check-out date must be after check-in date"
                )
    if booking == "too_many_guests":
            raise HTTPException(
                status_code = 400,
                detail ="A room cannot have more than 4 guests"
                )
    if booking == "booking_conflict":
            raise HTTPException(
                status_code = 409,
                detail ="Room is already booked for these dates"
                )

    return booking

@router.get("/booking/{user_id}", response_model = list[BookingReasponse])
def get_user_bookings_endpint(user_id, db = Depends(get_db)):   

    user_bookings = get_user_bookings(user_id, db)

    return user_bookings

@router.patch("/booking/{booking_id}")
def booking_patch_time_endpoint(booking_id,booking_data: BookingPatch,db = Depends(get_db)):
    bookings = booking_patch_time(booking_id,booking_data, db)

    
    return bookings

@router.delete("/booking/{booking_id}")
def delete_booking_endpoint(booking_id, db = Depends(get_db)):
    booking = delete_booking(booking_id, db)

    if booking is None:
        raise HTTPException(
                    status_code = 404,
                    detail ="Booking not found"
                    )

    return booking


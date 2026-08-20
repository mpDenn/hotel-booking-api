from schemas.booking import BookingReasponse, BookingCreate, BookingPatch
from models.booking import Booking
from services.booking import booking_create, get_user_bookings, delete_booking, time_book_patch
from fastapi import APIRouter, Depends
from database import get_db
from fastapi import HTTPException
from services.security import get_current_user
router = APIRouter()

@router.post("/booking")
def create_booking_endpoint(booking_data: BookingCreate, 
                            db = Depends(get_db), 
                            current_user = Depends (get_current_user)
                            ):
    booking = booking_create(booking_data, db, current_user.id)
    
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
    
    if booking == "room_none":
                raise HTTPException(
                    status_code = 404,
                    detail ="Room doesn't exist"
                        )

    return booking

@router.get("/booking/me", response_model = list[BookingReasponse])
def get_my_booking_endpont(current_user = Depends(get_current_user), db = Depends(get_db)):
    user = get_user_bookings(current_user.id,db)

    return user

@router.delete("/booking/{booking_id}")
def delete_booking_endpoint(
                    booking_id, 
                    db = Depends(get_db), 
                    current_user = Depends(get_current_user) 
                    ):
    
    booking = delete_booking(booking_id, db, current_user.id)

    if booking == "booking_none":
        raise HTTPException(
                    status_code = 404,
                    detail ="Booking not found"
                    )
    if booking == "forbidden":
          raise HTTPException(
                status_code=403,
                detail="you cannot delete this booking"
          )
    
    return booking

@router.patch("/booking/{booking_id}", response_model = BookingReasponse)
def time_book_patch_endpoint(booking_id,
                             booking_data: BookingPatch, 
                             db = Depends(get_db),
                             current_user = Depends(get_current_user)
                             ):
    
    time = time_book_patch(
                    booking_id, 
                    booking_data.check_in, 
                    booking_data.check_out, 
                    db,
                    current_user.id
                    )

    if time == "forbidden":
          raise HTTPException(status_code=403, detail="You cannot modify this booking")

    if time == "booking_not_exist":
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if time == "wrong_data":
         raise HTTPException(status_code=400, detail="Check-out must be after check-in")

    if time == "booking_conflict":
         raise HTTPException(status_code=409, detail="Room is already booked for these dates")

    return time

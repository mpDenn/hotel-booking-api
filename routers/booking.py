from schemas.booking import BookingResponse, BookingCreate, BookingPatch
from services.booking import booking_create, get_user_bookings, delete_booking, patch_booking_time
from fastapi import APIRouter, Depends
from database import get_db
from fastapi import HTTPException
from services.security import get_current_user
router = APIRouter()

@router.post("/booking", response_model= BookingResponse)
def create_booking_endpoint(booking_data: BookingCreate, 
                            db = Depends(get_db), 
                            current_user = Depends (get_current_user)
                            ):
    booking = booking_create(booking_data, db, current_user.id)
    
    if booking == "booking_in_past":
        raise HTTPException(
                status_code = 400,
                detail ="Check-in date cannot be in the past"
                ) 
    
    if booking == "wrong_data":
        raise HTTPException(
                status_code = 400,
                detail ="Check-out date must be after check-in date"
                )
    
    if booking == "too_many_guests":
            raise HTTPException(
                status_code = 400,
                detail ="Number of guests exceeds room capacity"
                )
    
    if booking == "booking_conflict":
            raise HTTPException(
                status_code = 409,
                detail ="Room is already booked for these dates"
                )
    
    if booking == "room_not_found":
                raise HTTPException(
                    status_code = 404,
                    detail ="Room doesn't exist"
                        )

    return booking

@router.get("/booking/me", response_model = list[BookingResponse])
def get_my_booking_endpoint(current_user = Depends(get_current_user), db = Depends(get_db)):
    user = get_user_bookings(current_user.id,db)

    return user

@router.delete("/booking/{booking_id}")
def delete_booking_endpoint(
                    booking_id:int, 
                    db = Depends(get_db), 
                    current_user = Depends(get_current_user) 
                    ):
    
    booking = delete_booking(booking_id, db, current_user.id)

    if booking == "booking_not_found":
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

@router.patch("/booking/{booking_id}", response_model = BookingResponse)
def time_book_patch_endpoint(
                            booking_id: int,
                             booking_data: BookingPatch, 
                             db = Depends(get_db),
                             current_user = Depends(get_current_user)
                             ):
    
    time = patch_booking_time(
                    booking_id, 
                    booking_data.check_in, 
                    booking_data.check_out, 
                    db,
                    current_user.id
                    )

    if time == "check_in_past":
        raise HTTPException(
                status_code = 400,
                detail ="Check-in date cannot be in the past"
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

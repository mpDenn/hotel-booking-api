from sqlalchemy.orm import Mapped, mapped_column
from database import Base 
from datetime import date
from sqlalchemy import ForeignKey


class Booking(Base):
    __tablename__ = "Bookings"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("Rooms.id"))
    check_in: Mapped[date] = mapped_column()
    check_out: Mapped[date] = mapped_column()
    guests: Mapped[int] = mapped_column()
   
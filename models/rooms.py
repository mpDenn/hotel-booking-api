from sqlalchemy.orm import Mapped, mapped_column
from database import Base 
from sqlalchemy import Numeric
from decimal import Decimal

class Room(Base):
    __tablename__ = "Rooms"
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(unique=True)
    room_type: Mapped[str] = mapped_column()
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    base_capacity: Mapped[int] = mapped_column()
    max_capacity: Mapped[int] = mapped_column()

from sqlalchemy.orm import Mapped, mapped_column
from database import Base 

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    role: Mapped[str] = mapped_column(default="user")
    password_hash: Mapped[str] = mapped_column()

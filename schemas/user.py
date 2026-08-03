from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str | None = None
    name: str | None = None
    surname: str | None = None
    password: str | None = None

class UserResponse(BaseModel):
    id: int
    email: str | None = None
    name: str | None = None
    surname: str | None = None

class UserUpdate(BaseModel):
    email: str | None = None
    name: str | None = None
    surname: str | None = None
    password: str | None = None
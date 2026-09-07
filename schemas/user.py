from pydantic import BaseModel, EmailStr, field_validator, Field

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    surname: str
    password: str  = Field(min_length=8)
    phone: str | None = None

    @field_validator("name", "surname")
    @classmethod
    def name_surname_validation(cls,value):

        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Name and surname cannot be empty")

        return cleaned_value


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    surname: str
    phone: str | None = None

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
    surname: str | None = None
    password: str | None = Field(default=None, min_length=8)
    phone: str | None = None


    @field_validator("name", "surname")
    @classmethod
    def name_surname_validation(cls,value):

        if value is None:
            raise ValueError("Name and surname cannot be empty")

        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Name and surname cannot be empty")

        return cleaned_value

    @field_validator("password")
    @classmethod
    def password_check(cls, value):

        if value is None:
            raise ValueError("password cannot be empty")

        return value
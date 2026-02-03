import enum
from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        description="Password must be at least 8 characters long"
    )

    model_config = ConfigDict(
    json_schema_extra={
        "examples": [
            {
                "email": "jane.doe@example.com",
                "password": "a_very_strong_password",
            }
        ]
    }
)


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: int
    email: EmailStr
    role: UserRole

    model_config = ConfigDict(from_attributes=True)

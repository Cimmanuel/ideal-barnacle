"""
Pydantic models used to serialize and deserialize data are defined here.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, validator

from utils import PasswordContext

password_context = PasswordContext()


class User(BaseModel):
    id: Optional[UUID] = uuid4().hex
    name: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = datetime.utcnow()

    @validator("password")
    def hash_password(cls, value):
        return password_context.make_password(value)

    class Config:
        schema_extra = {
            "example": {
                "name": "User Fullname",
                "email": "user@example.com",
                "password": "helloworld@123",
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        alias_generator = None


class Converter(BaseModel):
    amount: float
    to_currency: str
    from_currency: str

    class Config:
        schema_extra = {
            "example": {
                "amount": 100.0,
                "to_currency": "EUR",
                "from_currency": "USD",
            }
        }


class HistoricalRates(BaseModel):
    end_date: str
    start_date: str


class Welcome(BaseModel):
    status: str = "success"
    message: str = "Welcome to Shake's Currency Converter API Assessment"

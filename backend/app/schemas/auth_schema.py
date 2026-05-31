from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.user_model import GeoLocation

class UserSignup(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    blood_group: str = Field(..., pattern="^(A|B|AB|O)[+-]$")
    role: str = Field(default="donor", pattern="^(donor|patient|hospital|admin)$")
    city: str
    phone_number: str
    # Coordinates sent as [longitude, latitude]
    coordinates: List[float] = Field(..., min_items=2, max_items=2)
    availability: bool = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class GoogleLoginRequest(BaseModel):
    token: str

class UserProfileResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    blood_group: str
    city: str
    phone_number: str
    availability: bool
    reliability_score: int
    coordinates: List[float]

    class Config:
        populate_by_name = True

class TokenResponse(BaseModel):
    accessToken: str
    refreshToken: str
    user: UserProfileResponse

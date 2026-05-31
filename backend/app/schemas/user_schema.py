from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    blood_group: Optional[str] = Field(None, pattern="^(A|B|AB|O)[+-]$")
    city: Optional[str] = None
    phone_number: Optional[str] = None
    availability: Optional[bool] = None
    coordinates: Optional[List[float]] = Field(None, min_items=2, max_items=2)
    last_donation_date: Optional[datetime] = None

class UserBriefResponse(BaseModel):
    id: str
    name: str
    blood_group: str
    role: str
    city: str
    availability: bool
    reliability_score: int
    coordinates: List[float]
    last_donation_date: Optional[datetime] = None

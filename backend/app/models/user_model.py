from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

class GeoLocation(BaseModel):
    type: str = Field(default="Point", pattern="^Point$")
    coordinates: List[float] = Field(..., min_items=2, max_items=2) # [longitude, latitude]

class UserDoc(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    email: EmailStr
    hashed_password: str
    blood_group: str
    role: str # donor, patient, hospital, admin
    city: str
    phone_number: str
    geo_location: GeoLocation
    availability: bool = True
    last_donation_date: Optional[datetime] = None
    reliability_score: int = 100
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

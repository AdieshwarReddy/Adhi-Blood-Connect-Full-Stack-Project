from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.user_model import GeoLocation

class EmergencyRequestDoc(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    patient_name: str
    blood_group: str
    units_needed: int
    urgency_level: str # low, medium, high, critical
    hospital_name: str
    hospital_contact: str
    location: GeoLocation
    status: str = Field(default="pending") # pending, active, fulfilled, cancelled
    created_by: str # User ID of the creator
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

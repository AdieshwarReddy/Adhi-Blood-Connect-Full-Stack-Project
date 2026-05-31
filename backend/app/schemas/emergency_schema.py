from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class EmergencyCreate(BaseModel):
    patient_name: str = Field(..., min_length=2, max_length=100)
    blood_group: str = Field(..., pattern="^(A|B|AB|O)[+-]$")
    units_needed: int = Field(..., gt=0)
    urgency_level: str = Field(..., pattern="^(low|medium|high|critical)$")
    hospital_name: str
    hospital_contact: str
    coordinates: List[float] = Field(..., min_items=2, max_items=2) # [longitude, latitude]

class EmergencyUpdate(BaseModel):
    patient_name: Optional[str] = None
    blood_group: Optional[str] = None
    units_needed: Optional[int] = None
    urgency_level: Optional[str] = None
    hospital_name: Optional[str] = None
    hospital_contact: Optional[str] = None
    coordinates: Optional[List[float]] = None
    status: Optional[str] = Field(None, pattern="^(pending|active|fulfilled|cancelled)$")

class EmergencyResponse(BaseModel):
    id: str
    patient_name: str
    blood_group: str
    units_needed: int
    urgency_level: str
    hospital_name: str
    hospital_contact: str
    coordinates: List[float]
    status: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True

class MatchedDonorResponse(BaseModel):
    donor_id: str
    name: str
    blood_group: str
    phone_number: str
    availability: bool
    distance_km: float
    compatibility_score: float # 0 to 100
    reliability_score: int # 0 to 100
    matching_rank_score: float # final overall rank score

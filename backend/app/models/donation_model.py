from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class DonationDoc(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    request_id: Optional[str] = None # associated emergency request
    donor_id: str
    recipient_id: Optional[str] = None # can be a hospital or patient user id
    units: int = 1
    status: str = "scheduled" # scheduled, completed, cancelled
    donation_date: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

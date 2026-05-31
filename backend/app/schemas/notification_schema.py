from datetime import datetime
from pydantic import BaseModel

class NotificationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime

    class Config:
        populate_by_name = True

class NotificationRespondRequest(BaseModel):
    request_id: str
    patient_name: str
    hospital: str


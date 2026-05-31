from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class NotificationDoc(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str # recipient ID
    title: str
    message: str
    type: str = "emergency" # emergency, alert, update, system
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

from typing import List, Optional
from pydantic import BaseModel

class ChatQuery(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    suggestions: Optional[List[str]] = None

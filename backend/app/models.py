from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Architecture(BaseModel):
    name: str
    description: str
    summary: str
    category: Optional[str] = None
    services: List[str] = []
    timestamp: datetime = Field(default_factory=datetime.utcnow)

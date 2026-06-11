from pydantic import BaseModel
from typing import Optional
class JobCreate(BaseModel):
    company: str
    title: str
    status: str
    notes: Optional[str] = None
class JobUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    
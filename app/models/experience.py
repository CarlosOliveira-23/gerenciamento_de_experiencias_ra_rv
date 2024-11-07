from pydantic import BaseModel
from typing import Optional
from datetime import date


class Experience(BaseModel):
    id: Optional[int]
    title: str
    description: Optional[str] = None
    type: str
    requirements: Optional[str] = None
    created_at: Optional[date] = date.today()

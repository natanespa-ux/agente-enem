
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Lead(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = None
    phone: str
    email: Optional[str] = None
    is_active: bool = True
    greeted: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

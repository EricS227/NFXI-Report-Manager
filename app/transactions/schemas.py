from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionCreate(BaseModel):
    type: str
    value: float

class TransactionRead(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TransactionUpdate(BaseModel):
    category: str | None = None
    value: float | None = None
    description: str | None = None
    status: str | None = None

class TransactionBase(BaseModel):
    type: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    value: Optional[float] = None

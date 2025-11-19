from sqlmodel import SQLModel, Field
from datetime import datetime, Field, Column, Integer, DateTime, String

class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    type: str = Field(nullable=False)
    category: str | None = Field(default=None)
    value: float = Field(nullable=False)
    description: str | None = Field(default=None)
    date: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="Pendente")

    created_at: datetime = Field(
        sa_column=Column(DateTime, default=datetime.utcnow)
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    )
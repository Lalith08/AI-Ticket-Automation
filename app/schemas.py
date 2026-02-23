from typing import Optional
from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)


class TicketPatch(BaseModel):
    # all optional because PATCH can update any subset
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, min_length=1)

    status: Optional[str] = Field(default=None)  # NEW / PROCESSED
    ai_summary: Optional[str] = None
    ai_priority: Optional[str] = None  # LOW/MEDIUM/HIGH
    ai_draft_reply: Optional[str] = None


class TicketOut(BaseModel):
    id: int
    title: str
    description: str
    status: str

    ai_summary: Optional[str] = None
    ai_priority: Optional[str] = None
    ai_draft_reply: Optional[str] = None

    class Config:
        from_attributes = True  # pydantic v2 compatibility with ORM objects
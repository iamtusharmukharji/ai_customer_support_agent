from typing import Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class NewSupportTicket(BaseModel):
    """Schema for creating new support ticket."""
    ticket_number : str
    customer_id : int
    order_id : int
    subject : str
    description : str
    priority : Literal['low','medium','high','urgent']
    status : Literal['open','in_progress','waiting_customer','resolved','closed']
    assigned_team : Optional[str] = ''
    created_at : datetime = Field(default_factory=datetime.now)
    resolved_at : Optional[datetime] = None

class UserChat(BaseModel):
    prompt : str
    thread_id : str
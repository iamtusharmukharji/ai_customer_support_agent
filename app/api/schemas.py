from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import uuid


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

class InitiateRefund(BaseModel):
    """Schema for creating new refund entry"""
    refund_number : str | None
    order_id : int 
    customer_id : int 
    refund_amount : float 
    reason : str 
    status : Literal['requested','approved','processing','completed','rejected'] 
    requested_at : datetime = Field(default_factory=datetime.now)

    @field_validator('refund_number')
    def vaidate_refund_number(refund_number):
        if refund_number == None:
            return f'REF-{datetime.now().year}-{uuid.uuid4().hex[:5].upper()}'

class UserChat(BaseModel):
    prompt : str
    thread_id : str
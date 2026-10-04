from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import uuid

class InitiateRefund(BaseModel):
    """Schema for creating new refund entry"""
    refund_number : str | None
    status : Literal['requested','approved','processing','completed','rejected']
    requested_at : datetime = Field(default_factory=datetime.now)

    @field_validator('refund_number')
    def vaidate_refund_number(refund_number):
        print('validator', refund_number)
        if refund_number == None:
            return f'REF-{datetime.now().year}-{uuid.uuid4().hex[:5].upper()}'

d = InitiateRefund(
    refund_number=None,
    status='processing'
)

print(d.model_dump())
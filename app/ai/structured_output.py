# app/ai/structured_output.py

from typing import Literal, Optional
from pydantic import BaseModel, Field

"""
Production Tip: Always include a reasoning field in schemas used for classification. 
Forcing the LLM to think through the query before outputting the final enum value significantly increases extraction accuracy (Chain-of-Thought effect).
"""

class IntentExtraction(BaseModel):
    """Schema for classifying customer support query intent and extracting entities."""
    
    intent: Literal["FAQ", "ORDER", "REFUND", "HUMAN", "UNKNOWN"] = Field(
        description="Primary intent of the customer inquiry."
    )
    order_number: Optional[str] = Field(
        default=None,
        description="The order reference number if mentioned (e.g., ORD-2026-10002). Format must match ORD-YYYY-XXXXX."
    )
    refund_number: Optional[str] = Field(
        default=None,
        description="The refund reference number if mentioned (e.g., REF-2026-50001)."
    )
    reasoning: str = Field(
        description="Brief step-by-step reasoning for why this intent and these entities were selected."
    )


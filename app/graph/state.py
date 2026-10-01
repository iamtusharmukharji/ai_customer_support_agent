from typing import TypedDict, Optional, Literal


class SupportState(TypedDict):

    """
    Represents the shared schema for the customer support graph execution context.
    Keep state fields strictly scoped to what nodes need to pass downstream.
    """
    
    user_message : str
    intent : Optional[str]
    order_number : Optional[str]
    refund_number : Optional[str]
    ticket_subject : Optional[str]
    ticket_priority : Optional[Literal['low', 'medium', 'high', 'urgent']]
    ticket_description : Optional[str]
    context : Optional[str]
    response : Optional[str]
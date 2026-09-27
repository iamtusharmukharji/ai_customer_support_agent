from typing import Literal
from app.graph.state import SupportState


def route_intent(
        state: SupportState
) -> Literal["faq", "order", "refund", "human", "unknown"]:

    """
    Evaluates current state and returns the path key for conditional edges.
    MUST NOT mutate state or perform business logic operations.
    """
    
    intent = state.get('intent')

    if intent == "FAQ":
        return 'faq'
    
    if intent == "ORDER":
        return 'order'
    
    if intent == "REFUND":
        return 'refund'

    if intent == "HUMAN":
        return 'human'

    return 'unknown'
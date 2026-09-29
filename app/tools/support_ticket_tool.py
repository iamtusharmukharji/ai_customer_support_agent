from langchain_core.tools import tool
from app.api.services import support_ticket_service
from app.api.schemas import NewSupportTicket

@tool
def create_new_support_ticket(ticket_data:NewSupportTicket) -> str:
    """Creates new support ticket for Human Escalation."""
    db_data = support_ticket_service.create_new_support_ticket(ticket_data)

    formatted_context = support_ticket_service.new_support_ticket_context(db_data)

    return formatted_context
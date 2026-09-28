from langchain_core.tools import tool
from app.api.services import faq_service


@tool
def fetch_faq() -> str:
    """Fetches all FAQs saved in DB and create context."""
    db_data = faq_service.get_raw_faq()

    formatted_context = faq_service.faq_data_context(db_data)

    return formatted_context
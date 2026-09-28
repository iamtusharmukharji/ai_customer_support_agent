from langchain_core.tools import tool
from typing import Literal
from app.api.services import order_service


@tool
def fetch_refund(reference_number:str, reference_type: Literal['order_number', 'refund_number']) -> str:
    """Fetches refund details as by order_number or refund_number"""
    
    if reference_type == "order_number":
        db_data = order_service.get_order_refund_details_by_order_number(reference_number)

    elif reference_type == "refund_number":
        db_data = order_service.get_order_refund_details_by_refund_number(reference_number)

    formatted_context = order_service.refund_detail_context(db_data, reference_type)

    return formatted_context
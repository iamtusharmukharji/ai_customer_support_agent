from langchain_core.tools import tool
from app.api.services import order_service


@tool
def fetch_order_details(order_number:str) -> str:
    """Fetches status and items for a specific order reference number like 'ORD-2026-10001'."""
    db_data = order_service.get_order_details(order_number=order_number)

    formatted_context = order_service.order_detail_context(db_data)

    return formatted_context

@tool
def fetch_raw_order_details(order_number:str, keys: list[str]) -> dict:
    """Fetches specific data as per keys from raw db data for order number like 'ORD-2026-10001'."""
    db_data = order_service.get_order_details(order_number=order_number)

    db_data = db_data['data']
    
        
    response = {}
    if not db_data:
        for key in keys:
            response[key] = None
    else:
        for key in keys:
            response[key] = db_data.get(key, None)
    
    return response

from app.api.database import SessionLocal
from sqlalchemy.orm import joinedload
from app.api import models
from fastapi.encoders import jsonable_encoder


def get_order_details(order_number:str) -> dict:
    db = SessionLocal()
    try:
        response = {"data":None}
        order_qry = db.query(models.Order).filter(models.Order.order_number == order_number).options(
            joinedload(models.Order.items).load_only(models.OrderItem.order_id).options(
                joinedload(models.OrderItem.product)
            )
        ).first()
        if order_qry:
            response['data'] = jsonable_encoder(order_qry)

        return response

    finally:
        db.close()


def order_detail_context(data:dict) -> str:

    data = data.get('data', None)
    
    if data == None:
        return "No order details found"
    
    order_number = data['order_number']
    status = data['order_status']
    delivery_date = data['delivered_at']
    total_price = data['subtotal']
    tracking_number = data['tracking_number']
    
    item_counter = {}
    
    for item in data['items']:
        product_name = item['product']['name']
        product_price = item['product']['price']
        if item_counter.get(product_name, False):
            item_counter[product_name][0] += 1
        else:
            item_counter[product_name] = [1, product_price]
    
    items = ''
    for prod, metadata in item_counter.items():
        items += f"{metadata[0]} X {prod} worth ₹ {metadata[1]} per Unit, "
    
    final_context = (
        f"Order {order_number} status is '{status}'. "
        f"Delivery info: {delivery_date}. "
        f"Total Amount: ₹ {total_price}. "
        f"Items: {items}. "
        f"Tracking Number: {tracking_number}."
    )

    return final_context


if __name__ == "__main__":

    test_oder_numbers = ["ORD-2026-10001", "ORD-2026-100234", None]
    for i in test_oder_numbers:
        res = get_order_details(i)

        print(order_detail_context(res))
    

from app.api.database import SessionLocal
from sqlalchemy.orm import joinedload, load_only
from app.api import models
from typing import Literal
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

def get_order_refund_details_by_order_number(order_number:str) -> dict:
    db = SessionLocal()
    try:
        response = {"data":None}
        
        order_qry = db.query(models.Order).options(load_only(
                            models.Order.order_number,
                            models.Order.payment_status, models.Order.subtotal, models.Order.total_amount,
                            models.Order.created_at, models.Order.order_status, models.Order.payment_method,
                            models.Order.shipping_fee, models.Order.tracking_number, models.Order.delivered_at
        )).filter(models.Order.order_number == order_number).options(
                joinedload(models.Order.refunds).load_only(
                    models.Refund.reason, models.Refund.requested_at, models.Refund.refund_number,
                    models.Refund.refund_amount, models.Refund.status, models.Refund.completed_at
                )
        ).first()
        

        if order_qry:
            response['data'] = jsonable_encoder(order_qry)

        return response

    finally:
        db.close()

def get_order_refund_details_by_refund_number(refund_number:str) -> dict:
    db = SessionLocal()
    try:
        response = {"data":None}

        order_qry = db.query(models.Refund).options(load_only(
                        models.Refund.reason, models.Refund.requested_at, models.Refund.refund_number,
                        models.Refund.refund_amount, models.Refund.status, models.Refund.completed_at
                        )).filter(models.Refund.refund_number == refund_number).options(
                                joinedload(models.Refund.order).load_only(
                                    models.Order.order_number,
                                    models.Order.payment_status, models.Order.subtotal, models.Order.total_amount,
                                    models.Order.created_at, models.Order.order_status, models.Order.payment_method,
                                    models.Order.shipping_fee, models.Order.tracking_number, models.Order.delivered_at
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

def refund_detail_context(data:dict, reference_type : Literal['order_number', 'refund_number']) -> str:
    data = data.get('data', None)
    
    if data == None:
        return "No refund details found"
    
    if reference_type == 'order_number':
        final_context = f"""This is a JSON data with order details and refund details in 'refunds' key which is an array of JSON as one order can have multiple refunds if one not failed which has fixed structure of : 
        {{
            'order_number': 'ORD-2026-10001',
            'payment_status': 'paid',
            'subtotal': 129998.0,
            'total_amount': 129998.0,
            'created_at': '2026-09-27T00:43:14',
            'order_status': 'delivered',
            'payment_method': 'upi',
            'shipping_fee': 0.0,
            'tracking_number': 'TRK-DL-839201',
            'delivered_at': '2026-09-17T14:30:00',
            'refunds': [
            {{
            
                'reason': 'Product damaged',
                'requested_at': '2026-09-25T09:45:00',
                'order_id': 1,
                'refund_number': 'REF-2026-50002',
                'refund_amount': 74999.0,
                'status': 'processing',
                'completed_at': None
            }}
            ]
        }}
        Data: {data}
        """

    elif reference_type == 'refund_number':
        order_detail = data["order"]
        data.pop('order')
        data.update(order_detail)
    
        final_context = f""" This is a JSON data with refund details and order details which has fixed structure of : 

        {{
            'reason': 'Order cancelled by customer',
            'requested_at': '2026-09-20T10:15:00',
            'refund_number': 'REF-2026-50001',
            'refund_amount': 6098.0,
            'status': 'completed',
            'completed_at': '2026-09-22T16:30:00',
            'payment_status': 'refunded',
            'order_number': 'ORD-2026-10004',
            'subtotal': 5999.0,
            'total_amount': 6098.0,
            'created_at': '2026-09-27T00:43:14',
            'order_status': 'cancelled',
            'payment_method': 'debit_card',
            'shipping_fee': 99.0,
            'tracking_number': None,
            'delivered_at': None
        }}

    Data: {data}

    """
    return final_context

if __name__ == "__main__":

    # test_oder_numbers = ["ORD-2026-10001", "ORD-2026-100234", None]
    # for i in test_oder_numbers:
    #     res = get_order_details(i)

    #     print(order_detail_context(res))

    test_oder_numbers = ["ORD-2026-10001", "ORD-2026-10010", "REF-2026-50001", "REF-2026-50002", "REF-2026-50003"]
    for i in test_oder_numbers:
        res = get_order_refund_details_by_order_number(i)
        print(refund_detail_context(res, 'order_number'))
    

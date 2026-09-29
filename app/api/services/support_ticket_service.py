from app.api.database import SessionLocal
from app.api.schemas import NewSupportTicket
from sqlalchemy.orm import joinedload, load_only
from app.api import models
from typing import Literal
import traceback
from fastapi.encoders import jsonable_encoder


def get_support_ticket(ticket_number:str) -> dict:
    db = SessionLocal()
    try:
        response = {"data":None}
        ticket_qry = db.query(models.SupportTicket).filter(models.SupportTicket.ticket_number == ticket_number).options(
            load_only(models.SupportTicket.ticket_number, models.SupportTicket.subject, models.SupportTicket.description,
                      models.SupportTicket.priority, models.SupportTicket.status, models.SupportTicket.assigned_team,
                      models.SupportTicket.created_at, models.SupportTicket.resolved_at)).first()
        if ticket_qry:
            response['data'] = jsonable_encoder(ticket_qry)

        return response

    finally:
        db.close()

def create_new_support_ticket(ticket_data : NewSupportTicket) -> dict:
    db = SessionLocal()
    try:
        ticket_data = ticket_data.model_dump()
        new_ticket = models.SupportTicket(**ticket_data)
        db.add(new_ticket)
        db.commit()
        return {"data":ticket_data, "message":"ticket has been created"}
    except Exception as err:
        traceback.print_exc()
        db.rollback()
        return {"data":None, "message":f"ticket not created, Error: {str(err)}"}
    finally:
        db.close()



def new_support_ticket_context(data:dict) -> str:

    ticket_data = data.get('data', None)
    if not ticket_data:
        return f"Some error occured while creating ticket, Reason: {data.get('message')}"

    final_context = f"""
    New support ticket has been created with below details 
    - Ticket Number : {ticket_data["ticket_number"]}
    - Subject : {ticket_data["subject"]}
    - Priority : {ticket_data["priority"]}
    """

    return final_context

if __name__ == "__main__":

    # test_oder_numbers = ["ORD-2026-10001", "ORD-2026-100234", None]
    # for i in test_oder_numbers:
    #     res = get_order_details(i)

    #     print(order_detail_context(res))
    print("Support Ticket Service")
    

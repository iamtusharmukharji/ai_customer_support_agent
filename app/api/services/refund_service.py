from app.api.database import SessionLocal
from sqlalchemy.orm import joinedload, load_only
from app.api import models, schemas
from typing import Literal
from fastapi.encoders import jsonable_encoder



def initiate_refund(refund_details: schemas.InitiateRefund) -> dict:
    db = SessionLocal()
    try:
        response = {"data":None}
        refund = refund_details.model_dump()
        refund = models.Refund(**refund)
        db.add(refund)
        db.commit()
        response['data'] = refund_details.refund_number
        return response
    finally:
        db.close()



from app.api.database import SessionLocal
from sqlalchemy.orm import joinedload, load_only
from app.api import models
from fastapi.encoders import jsonable_encoder


def get_raw_faq() -> dict:
    db = SessionLocal()
    try:
        response = {"data":None}
        faq_qry = db.query(models.FAQArticle).options(load_only(
            models.FAQArticle.question,
            models.FAQArticle.answer,
            models.FAQArticle.category
            )
        ).filter(models.FAQArticle.status == "active").all()
        
        if faq_qry != []:
            response['data'] = jsonable_encoder(faq_qry)

        return response

    finally:
        db.close()


def faq_data_context(data:dict) -> str:

    data = data.get('data', None)
    
    if data == None:
        return "No faq articles found"
    
    final_context = f"""Data consist of array of json where each json in an array is one FAQ Article, the structure of json is 
    {{
        'question': 'How long does standard delivery take',
        'answer': 'Standard delivery usually takes 3 to 5 business days depending on the delivery location.'
        'category': 'Shipping'
    }}

    Data : {data}
    """

    return final_context


if __name__ == "__main__":

    
    res = get_raw_faq()


    print(faq_data_context(res))
    

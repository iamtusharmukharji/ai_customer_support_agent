from fastapi import APIRouter


route = APIRouter(
    prefix="/chats",
    tags=["Chats"]
    )

@route.get('/')
async def chat(prompt : str):
    return prompt
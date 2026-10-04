from fastapi import APIRouter
from fastapi import Request
from app.api.schemas import UserChat
import time

route = APIRouter(
    prefix="/chats",
    tags=["Chats"]
    )

@route.post('/')
async def chat(
                chat_data: UserChat,
                request: Request
            ):
    config = {"configurable": {"thread_id": chat_data.thread_id}}
    graph = request.app.state.graph
    response = await graph.ainvoke({"user_message":chat_data.prompt}, config = config)
    print(response)
    if "__interrupt__" in response:
        return {"response": "Your request is being processed", "thread_id" : chat_data.thread_id}
    return {"response": response.get("response"), "thread_id" : chat_data.thread_id}

@route.get('/{thread_id}/history')
async def get_chat_history(
                thread_id: str,
                request: Request
            ):
    config = {"configurable": {"thread_id": thread_id}}
    graph = request.app.state.graph
    snapshot = await graph.aget_state(config = config)
    
    return {"response": snapshot.values, "thread_id" : thread_id}

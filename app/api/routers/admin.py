from fastapi import APIRouter, Request, HTTPException
from app.api.schemas import UserChat
from langgraph.types import Command

import time

route = APIRouter(
    prefix="/admin",
    tags=["Admin"]
    )

@route.post('/refund/decision')
async def handle_refund_approval(request: Request, thread_id: str, approved: bool, notes: str = ""):
    graph = request.app.state.graph
    config = {"configurable": {"thread_id": thread_id}}
    
    # 1. Fetch thread state to confirm an interrupt is active
    snapshot = await graph.aget_state(config)
    if not snapshot.next:
        raise HTTPException(status_code=400, detail="No active interrupt for this thread.")

    # 2. Resume graph execution with human response
    resume_payload = {
        "approved": approved,
        "notes": notes
    }
    
    # Passing Command(resume=...) sends data straight into interrupt() return value
    final_state = await graph.ainvoke(Command(resume=resume_payload), config=config)
    
    return {
        "status": "success",
        "final_context": final_state.get("context"),
        "response": final_state.get("response")
    }
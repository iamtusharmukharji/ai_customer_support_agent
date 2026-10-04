# app/graph/test_graph.py

from app.graph.graph import build_support_graph
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver

def run_tests():
    app = build_support_graph(checkpointer=MemorySaver())

    test_queries = [
        # "Where is my order ORD-2026-10001?",
        # "What is your standard return policy?"
        # "I have an issue with the received order, please help me",
        "I want refund for ORD-2026-10001, In this order I have a laptop and a smartphone out of which the laptop is damaged"
        # "What is the status of my refund REF-2026-50002?"
    ]
    config = {"configurable": {"thread_id": "th_test"}}
    resume_payload = {
            "approved": True,
            "notes": "approved for this user"
        }
    for query in test_queries:
        # print(f"\n--- Query: '{query}' ---")
        result = app.invoke({"user_message": query}, config=config)
        print("\n------------ Start ------------")
        print(f"User Message : {result.get('user_message')}")
        print(f"Extracted Intent : {result.get('intent')}")
        print(f"Order Number     : {result.get('order_number')}")
        print(f"Refund Number     : {result.get('refund_number')}")
        print(f"Refund Intent     : {result.get('refund_intent')}")
        print(f"Ticket Subject   : {result.get('ticket_subject')}")
        print(f"Ticket Description   : {result.get('ticket_description')}")
        print(f"Ticket Priority   : {result.get('ticket_priority')}")
        print(f"Final Response   : {result.get('response')}")
        print("------------ END ------------\n")
    final_state = app.invoke(Command(resume=resume_payload), config=config)
    print(final_state)
if __name__ == "__main__":
    run_tests()
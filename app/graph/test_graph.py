# app/graph/test_graph.py

from app.graph.graph import build_support_graph

def run_tests():
    app = build_support_graph()

    test_queries = [
        # "Where is my order ORD-2026-10001?",
        # "What is your standard return policy?"
        # "I have an issue with the received order, please help me",
        "My order number is ORD-2026-10001, In this order I have a laptop and a smartphone out of which the laptop is damaged"
        # "What is the status of my refund REF-2026-50002?"
    ]

    for query in test_queries:
        # print(f"\n--- Query: '{query}' ---")
        result = app.invoke({"user_message": query})
        print("\n------------ Start ------------")
        print(f"User Message : {result.get('user_message')}")
        print(f"Extracted Intent : {result.get('intent')}")
        print(f"Order Number     : {result.get('order_number')}")
        print(f"Refund Number     : {result.get('refund_number')}")
        print(f"Refund Number     : {result.get('refund_number')}")
        print(f"Ticket Subject   : {result.get('ticket_subject')}")
        print(f"Ticket Description   : {result.get('ticket_description')}")
        print(f"Ticket Priority   : {result.get('ticket_priority')}")
        print(f"Final Response   : {result.get('response')}")
        print("------------ END ------------\n")

if __name__ == "__main__":
    run_tests()
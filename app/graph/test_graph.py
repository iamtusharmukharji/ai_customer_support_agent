# app/graph/test_graph.py

from app.graph.graph import build_support_graph

def run_tests():
    app = build_support_graph()

    test_queries = [
        "Where is my order ORD-2026-10002?",
        "What is your standard return policy?",
        "My laptop arrived damaged, let me speak with a representative!",
        "What is the status of my refund REF-2026-50001?"
    ]

    for query in test_queries:
        print(f"\n--- Query: '{query}' ---")
        result = app.invoke({"user_message": query})
        print(f"Extracted Intent : {result.get('intent')}")
        print(f"Order Number     : {result.get('order_number')}")
        print(f"Graph Response   : {result.get('response')}")

if __name__ == "__main__":
    run_tests()
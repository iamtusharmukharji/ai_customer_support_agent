from langgraph.graph import StateGraph, START, END
from app.graph.state import SupportState
from app.graph.nodes import (
    classify_intent,
    handle_faq,
    handle_human,
    handle_order,
    handle_refund,
    handle_unknown,
    generate_response
)
from app.graph.edges import route_intent


def build_support_graph():

    workflow = StateGraph(SupportState)

    # Add Nodes
    workflow.add_node('classify_intent', classify_intent)
    workflow.add_node('faq', handle_faq)
    workflow.add_node('order', handle_order)
    workflow.add_node('human', handle_human)
    workflow.add_node('refund', handle_refund)
    workflow.add_node('unknown', handle_unknown)
    workflow.add_node('generate_final_response', generate_response)

    # Add fixed edges

    workflow.add_edge(START, 'classify_intent')

    # Add conditional edge

    workflow.add_conditional_edges('classify_intent', route_intent, {
            
            "faq": "faq",
            "order": "order",
            "refund": "refund",
            "human": "human",
            "unknown": "unknown",
        },
    )

    # final end nodes
    workflow.add_edge('faq', "generate_final_response")
    workflow.add_edge('order', "generate_final_response")
    workflow.add_edge('human', "generate_final_response")
    workflow.add_edge('refund',"generate_final_response")
    workflow.add_edge('unknown', "generate_final_response")
    workflow.add_edge('generate_final_response', END)

    return workflow.compile()
    
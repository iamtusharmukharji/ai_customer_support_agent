from app.graph.state import SupportState
from app.ai.llm import get_classifier_llm, get_general_llm
from app.tools import order_tool, faq_tool, refund_tool
from app.ai.structured_output import IntentExtraction
from langchain_core.messages import HumanMessage, SystemMessage


classifier_llm = get_classifier_llm()

SYSTEM_PROMPT = """
You are an intent classification and entity extraction assistant for an e-commerce platform.
Analyze the user's input and classify it into one of these intents:
- FAQ: Inquiries about general policies, returns, shipping times, or FAQs.
- ORDER: Inquiries regarding order status, delivery date, item details, or tracking.
- REFUND: Inquiries about refund status, processing times, or refund IDs.
- HUMAN: Requests to speak to a agent, representative, or complaining about damaged items/escalations.
- UNKNOWN: Inquiries that do not match any of the above or are completely ambiguous.

Extract any explicit order numbers (e.g., ORD-2026-10002) or refund numbers (e.g., REF-2026-50001).
"""

def classify_intent(state: SupportState) -> dict:

    # message = state['user_message'].lower()

    # intent = "UNKNOWN"

    # if 'orders' in message or 'order' in message:
    #     intent = 'ORDER'

    # elif 'refund' in message:
    #     intent = 'REFUND'

    # elif 'return' in message or 'policy' in message:
    #     intent = 'FAQ'

    # elif 'human' in message or 'agent' in message:
    #     intent = "HUMAN"
        

    # return {"intent":intent}

    user_message = state['user_message']

    message_array = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_message)
    ]

    result:IntentExtraction = classifier_llm.invoke(message_array)

    return {
        "intent" : result.intent,
        "order_number" : result.order_number,
        "refund_number" : result.refund_number
    }


def handle_faq(state: SupportState) -> dict:
    faq_context = faq_tool.fetch_faq.invoke({})
    return {"context": faq_context}


def handle_order(state: SupportState) -> dict:
    order_number = state.get('order_number')
    if not order_number:
        return {"context": "No order number provided in user query."}
    context_string = order_tool.fetch_order_details.invoke({'order_number':order_number})

    return {'context':context_string}
    

def handle_refund(state: SupportState) -> dict:
    order_number = state.get("order_number")
    refund_number = state.get("refund_number")

    # route tool call as per order_number or refund_number availability
    if order_number:
        context_string = refund_tool.fetch_refund.invoke({'reference_number':order_number, 'reference_type':'order_number'})
    
    elif refund_number:
        context_string = refund_tool.fetch_refund.invoke({'reference_number':refund_number, 'reference_type':'refund_number'})

    else:
        context_string = "No order number or refund reference number was provided in the query."

    return {"context": context_string}

def handle_human(state: SupportState) -> dict:
    return {"response": "Escalating to Human Support Agent..."}

def handle_unknown(state: SupportState) -> dict:
    return {"response": "Unable to determine intent. Routing to general fallback..."}

def generate_response(state: SupportState) -> dict:
    
    llm = get_general_llm()

    context = state.get("context")
    user_message = state.get("user_message")
    SYS_PROMPT = f"""You are a helpful, professional e-commerce customer support AI assistant.
        Answer the customer's query accurately using ONLY the background context provided below.
        If the context states that no order was found or an error occurred, explain that politely to the user.
        BACKGROUND CONTEXT:\n{context}"""
    
    message_array = [
            SystemMessage(content=SYS_PROMPT),
            HumanMessage(content=user_message)
        ]
    
    resposne = llm.invoke(message_array)
    # print(resposne.content)
    return {"response" : resposne.content}
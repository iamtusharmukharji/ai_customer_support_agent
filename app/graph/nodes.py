from app.graph.state import SupportState
from app.ai.llm import get_classifier_llm, get_general_llm
from app.tools import order_tool, faq_tool, refund_tool, support_ticket_tool
from app.api.services import order_service, refund_service
from app.ai.structured_output import IntentExtraction
from app.api.schemas import NewSupportTicket, InitiateRefund
from langgraph.types import interrupt
import uuid
from langchain_core.messages import HumanMessage, SystemMessage
from datetime import datetime

classifier_llm = get_classifier_llm(provider='gemini')
generic_llm = get_general_llm()
# support_ticket_llm = get_support_ticket_llm()

SYSTEM_PROMPT = """
You are an intent classification and entity extraction assistant for an e-commerce platform.
Analyze the user's input and classify it into one of these intents:
- FAQ: Inquiries about general policies, returns, shipping times, or FAQs.
- ORDER: Inquiries regarding order status, delivery date, item details, or tracking.
- REFUND: Inquiries about refund status, processing times, refund IDs or wants to initate refund against any order_number.
- HUMAN: Requests to speak to a agent, representative, or complaining about damaged items/escalations, whith order_number otherwise ask user to provide order_number with issue description.
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
    print(result.model_dump())
    return {
        "intent" : result.intent,
        "order_number" : result.order_number,
        "refund_number" : result.refund_number,
        "refund_intent" : result.refund_intent,
        "ticket_priority" : result.ticket_priority,
        "ticket_subject" : result.ticket_subject,
        "ticket_description" : result.ticket_description
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

async def handle_refund(state: SupportState) -> dict:
    order_number = state.get("order_number")
    refund_number = state.get("refund_number")
    refund_intent = state.get('refund_intent')
    context_string = ''
    # route tool call as per order_number or refund_number availability
    if order_number:

        # when user does enquiry for refund status
        if refund_intent == 'status':
            context_string = refund_tool.fetch_refund.invoke({'reference_number':order_number, 'reference_type':'order_number'})

        # when user wants to initiate refund
        elif refund_intent == 'initiate':
            order_details = order_service.get_order_refund_details_by_order_number(order_number=order_number)
            order_details = order_details.get('data')
            
            # if order_number is invalid
            if order_details == None:
            
                context_string = f"No order found for order_number = {order_number}"
            
            else:
                
                existing_refund = order_details.get('refunds')
                print("EXISTING REFUND", existing_refund)

                # when there is any existing refund data exists for an order_number
                if existing_refund:
                    
                    refund_list = existing_refund[0]
                    existing_refund_number = refund_list['refund_number']
                    existing_refund_status = refund_list['status']
                    existing_refund_amount = refund_list['refund_amount']
                    context_string = f"""
                    Refund data already exists for order {order_number}
                    - Refund Number : {existing_refund_number}
                    - Current Status : {existing_refund_status}
                    - Refund Amount : {existing_refund_amount}
                    """
                # when there is no refund data exists in table
                else:

                    # creates interrupt before creating actual entry for refund in DB
                    approval_interrupt = interrupt({
                        "action": "approve_refund_creation",
                        "order_number": order_number,
                        "customer_id": order_details.get("customer_id"),
                        "amount": order_details.get("subtotal"),
                        "reason": state.get("ticket_subject"),
                    })

                    # Handle Human Decision from resume payload
                    is_approved = approval_interrupt.get("approved", False)
                    admin_notes = approval_interrupt.get("notes", "No notes provided")

                    # when any human(admin/supervisor) approves the interrupt with approved = True
                    if is_approved:

                        refund_details = InitiateRefund(
                            refund_number = None, # Allow auto-generation of refund_number from schema's field_validator
                            order_id = order_details['id'],
                            customer_id = order_details['customer_id'],
                            refund_amount = order_details['subtotal'],
                            reason = state.get('ticket_subject'),
                            status = 'processing',
                        )

                        create_refund = refund_service.initiate_refund(refund_details)
                        context_string = f"Refund has been initiated for order {order_number}. Refund Number is {create_refund['data']}"
                    
                    # when admin/supervisor rejects the refund creation request
                    else:
                        context_string = f"Refund request for order {order_number} was REJECTED by human supervisor. Reason: {admin_notes}"

    
    elif refund_number:

        context_string = refund_tool.fetch_refund.invoke({'reference_number':refund_number, 'reference_type':'refund_number'})

    else:

        context_string = "No order number or refund reference number was provided in the query."

    return {"context": context_string}

def handle_human(state: SupportState) -> dict:
    
    order_number = state.get('order_number')
    if not order_number:
        return {"context": "order number and issue description is required to create ticket"}
    details_for_new_ticket = order_tool.fetch_raw_order_details.invoke({'order_number':order_number, 'keys' : ['id', 'customer_id']})

    # No order details found
    if details_for_new_ticket.get("id") == None:
        return {"context" : f"No order details found for order_number = {order_number}"}

    current_date = datetime.now()
    ticket_num = f"TKT-{current_date.year}-{uuid.uuid4().hex[:5].upper()}"
    
    ticket_data = NewSupportTicket(
        ticket_number = ticket_num,
        order_id = details_for_new_ticket['id'],
        customer_id = details_for_new_ticket['customer_id'],
        subject = state.get('ticket_subject'),
        description = state.get('ticket_description'),
        priority = state.get('ticket_priority'),
        status = 'open'
    )

    create_ticket_tool_call = support_ticket_tool.create_new_support_ticket.invoke({'ticket_data':ticket_data})
    return {"context": create_ticket_tool_call}

def handle_unknown(state: SupportState) -> dict:
    return {"response": "Unable to determine intent. Routing to general fallback..."}

def generate_response(state: SupportState) -> dict:
    
    context = state.get("context")
    user_message = state.get("user_message")
    SYS_PROMPT = f"""You are a helpful, professional e-commerce customer support AI assistant.
        Answer the customer's query accurately using ONLY the background context provided below.
        If the context states that no order was found or an error occurred, explain that politely to the user.
        If the context states that new ticket is created for further escalation, explain that politely to the user.
        BACKGROUND CONTEXT:\n{context}"""
    
    message_array = [
            SystemMessage(content=SYS_PROMPT),
            HumanMessage(content=user_message)
        ]
    
    resposne = generic_llm.invoke(message_array)
    # print(resposne.content)
    return {"response" : resposne.content}
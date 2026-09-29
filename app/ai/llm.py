# app/ai/llm.py

import os
# from langchain_openai import ChatOpenAI
# If using Gemini / ChatGoogleGenerativeAI:
from langchain_google_genai import ChatGoogleGenerativeAI
from app.ai.structured_output import IntentExtraction
from app.api.schemas import NewSupportTicket
from app.creds import credentials

llm_model="gemini-2.5-flash-lite"

def get_classifier_llm():
    """Returns an LLM bound with structured output enforcing IntentExtraction."""
    llm = ChatGoogleGenerativeAI(
        api_key = credentials.gemini_api_key,
        model=llm_model, # or "gpt-4o-mini"
        temperature=0.0,      # Deterministic execution for structured extraction
    )
    
    # Force the LLM to return data matching our Pydantic class
    return llm.with_structured_output(IntentExtraction)

def get_support_ticket_llm():

    """Returns an LLM bound with structured output enforcing IntentExtraction."""
    llm = ChatGoogleGenerativeAI(
        api_key = credentials.gemini_api_key,
        model=llm_model, # or "gpt-4o-mini"
        temperature=0.0,      # Deterministic execution for structured extraction
    )
    
    # Force the LLM to return data matching our Pydantic class
    return llm.with_structured_output(NewSupportTicket)

def get_general_llm():
    """Returns an general LLM """
    llm = ChatGoogleGenerativeAI(
        api_key = credentials.gemini_api_key,
        model=llm_model, # or "gpt-4o-mini"
        temperature=0.0,      # Deterministic execution for structured extraction
    )
    
    return llm


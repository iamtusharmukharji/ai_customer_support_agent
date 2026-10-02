# app/ai/llm.py

import os
from langchain_openai import ChatOpenAI
# If using Gemini / ChatGoogleGenerativeAI:
from langchain_google_genai import ChatGoogleGenerativeAI
from app.ai.structured_output import IntentExtraction
from app.api.schemas import NewSupportTicket
from app.creds import credentials
from typing import Literal

def get_classifier_llm(provider : Literal['openai', 'gemini']):
    """Returns an LLM bound with structured output enforcing IntentExtraction."""
    
    if provider == 'gemini':
        llm = ChatGoogleGenerativeAI(
            api_key = credentials.gemini_api_key,
            model=credentials.gemini_model,
            temperature=0.0,
        )
    
    elif provider == 'openai':
        llm = ChatOpenAI(
            model=credentials.openai_model,
            temperature=0,
            # max_tokens=None,
            # timeout=None,
            max_retries=2,
            api_key=credentials.openai_api_key,)
    
    else:

        raise TypeError("Invalid model provider, select between 'openai' or 'gemini'")
    
    # Force the LLM to return data matching our Pydantic class
    return llm.with_structured_output(IntentExtraction)

def get_support_ticket_llm():

    """Returns an LLM bound with structured output enforcing IntentExtraction."""
    llm = ChatGoogleGenerativeAI(
        api_key = credentials.gemini_api_key,
        model=credentials.gemini_model,
        temperature=0.0,
    )
    
    # Force the LLM to return data matching our Pydantic class
    return llm.with_structured_output(NewSupportTicket)

def get_general_llm():
    """Returns an general LLM """
    llm = ChatGoogleGenerativeAI(
        api_key = credentials.gemini_api_key,
        model=credentials.gemini_model,
        temperature=0.0,
    )
    
    return llm


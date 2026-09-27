# app/ai/llm.py

import os
# from langchain_openai import ChatOpenAI
# If using Gemini / ChatGoogleGenerativeAI:
from langchain_google_genai import ChatGoogleGenerativeAI
from app.ai.structured_output import IntentExtraction
from app.creds import credentials

def get_classifier_llm():
    """Returns an LLM bound with structured output enforcing IntentExtraction."""
    llm = ChatGoogleGenerativeAI(
        api_key = credentials.gemini_api_key,
        model="gemini-2.5-flash", # or "gpt-4o-mini"
        temperature=0.0,      # Deterministic execution for structured extraction
    )
    
    # Force the LLM to return data matching our Pydantic class
    return llm.with_structured_output(IntentExtraction)
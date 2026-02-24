# app/services/llm_service.py
from langchain_ollama import OllamaLLM

def get_llm():
    return OllamaLLM(
        model="phi3:mini",
        temperature=0.2,
        num_predict=300
    )

"""LLM configuration for the application."""

import os
from pathlib import Path

from langchain_groq import ChatGroq
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[2] / ".env")

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured in Backend/.env.")

    return ChatGroq(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        temperature=0.2,
        max_tokens=300,
        api_key=api_key,
    )


def invoke_text(llm, prompt: str) -> str:
    """Normalize chat-model responses to the text interface used by the app."""
    response = llm.invoke(prompt)
    content = getattr(response, "content", response)
    if isinstance(content, list):
        return "".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        )
    return str(content)

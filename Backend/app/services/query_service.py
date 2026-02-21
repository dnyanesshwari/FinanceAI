from app.rag.retriever import retrieve
from app.services.llm_service import get_llm
from app.services.intent_service import classify_intent
from app.services.memory_service import get_memory

from collections import defaultdict
def generate_answer(query, session_id):
    intent = classify_intent(query)
    llm = get_llm()
    memory = get_memory(session_id)


    if intent == "regulation":
        docs = retrieve(query, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])

        prompt = f"""
You are a strict financial regulation assistant.

Previous Conversation:
{memory}

Answer ONLY using the context below.
If not found, say:
"Information not available in verified sources."

Context:
{context}

Question:
{query}

Answer:
"""
        return llm.invoke(prompt)

    elif intent == "planning":
        prompt = f"""
You are a responsible financial planning assistant.

Previous Conversation:
{memory}

Provide structured guidance.
Do NOT predict stock prices.
Be clear and professional.

Question:
{query}

Answer:
"""
        return llm.invoke(prompt)

    else:
        docs = retrieve(query, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])

        prompt = f"""
Previous Conversation:
{memory}

Answer using the context below.
If unsure, say information not available.

Context:
{context}

Question:
{query}

Answer:
"""
        return llm.invoke(prompt)


from app.services.llm_service import get_llm, invoke_text
def classify_intent(query: str):
    llm = get_llm()

    prompt = f"""
You are an intent classifier for a financial AI system.

Classify the user query into ONLY one of these categories:
- regulation
- planning
- general

Return ONLY the category word. No explanation.

Query: {query}
"""

    response = invoke_text(llm, prompt).strip().lower()

    if "regulation" in response:
        return "regulation"
    elif "planning" in response:
        return "planning"
    else:
        return "general"

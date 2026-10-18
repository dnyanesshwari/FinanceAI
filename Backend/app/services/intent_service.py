import re

from app.services.llm_service import get_llm, invoke_text


def classify_intent(query: str):
    normalized = query.strip().lower()
    if re.fullmatch(r"(?:hi+|hello+|hey+|good morning|good afternoon|good evening)[!. ,]*", normalized):
        return "general"
    if re.search(r"\b(rbi|sebi|regulation|regulated|regulatory|legal|law|compliance|tax|digital lending)\b", normalized):
        return "regulation"
    if re.search(r"\b(budget|plan|planning|save|saving|savings|invest|investment|spend|emergency fund|retire|retirement|financial goal)\b", normalized):
        return "planning"

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

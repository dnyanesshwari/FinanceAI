# app/agent/tools.py
"""
Tools available to the agent.

Design note: parameter extraction and tool *selection* are done with plain
code (regex), not by asking phi3:mini to emit a structured tool call. Small
local models are unreliable at structured function-calling, so we keep that
decision deterministic and let the LLM do what it's actually good at:
synthesizing a final natural-language answer from whatever the tools/RAG
returned. This is still a genuine agent workflow — the graph in graph.py
dynamically chooses which nodes to visit per query — it's just that the
"which tool" decision is a safe, testable function instead of a model guess.
"""

import re
from typing import Optional

from app.rag.retriever import retrieve as rag_retrieve
from app.services.finance_tools import (
    calculate_emi,
    calculate_simple_interest,
    calculate_compound_interest,
)

# Registry so new calculators can be added without touching the graph
CALCULATOR_REGISTRY = {
    "emi": calculate_emi,
    "simple": calculate_simple_interest,
    "compound": calculate_compound_interest,
}

_NUM = r"[\d][\d,]*\.?\d*"


def _to_float(s: str) -> float:
    return float(s.replace(",", ""))


def extract_calculation(query: str) -> tuple[Optional[str], Optional[dict]]:
    """
    Detects whether a query is a calculator request and extracts
    (principal, rate, time). Returns (None, None) if this isn't a
    calculation query, so the graph can fall through to RAG/planning.
    """
    q = query.lower()

    if "emi" in q:
        calc_type = "emi"
    elif "compound interest" in q or "compound" in q:
        calc_type = "compound"
    elif "simple interest" in q or "interest" in q:
        calc_type = "simple"
    else:
        return None, None

    principal_match = re.search(
        rf"(?:principal|amount|loan of|₹|rs\.?)\s*({_NUM})", q
    ) or re.search(rf"({_NUM})\s*(?:rupees|rs)", q) or re.search(rf"({_NUM})", q)

    rate_match = re.search(rf"({_NUM})\s*%|\brate\s*(?:of)?\s*({_NUM})", q)
    time_match = re.search(rf"({_NUM})\s*(?:years?|yrs?)", q)

    if not (principal_match and rate_match and time_match):
        # Looks like a calc question but we can't confidently parse numbers —
        # let it fall through to the LLM, which will ask a clarifying question.
        return None, None

    rate_str = next(g for g in rate_match.groups() if g)

    params = {
        "principal": _to_float(principal_match.group(1)),
        "rate": _to_float(rate_str),
        "time": _to_float(time_match.group(1)),
    }
    return calc_type, params


_REGULATION_PATTERN = re.compile(
    r"\b(rbi|sebi|regulat\w*|legal\w*|complian\w*|permitted|allowed|licens\w*|"
    r"lawful|is this .*(legal|allowed))\b"
)


def needs_regulation_context(query: str) -> bool:
    """
    Deterministic check: does this query also ask about the legal/regulatory
    side of things (e.g. "...and is this loan type regulated by RBI?")?

    This is what lets the graph chain calculator -> retrieve for a single
    query instead of only ever picking one tool.
    """
    return bool(_REGULATION_PATTERN.search(query.lower()))


def run_calculator(calc_type: str, params: dict) -> dict:
    fn = CALCULATOR_REGISTRY[calc_type]
    result = fn(params["principal"], params["rate"], params["time"])
    return {"calc_type": calc_type, "params": params, "result": result}


def retrieve_context(query: str, k: int = 3) -> str:
    docs = rag_retrieve(query, k=k)
    return "\n\n".join(doc.page_content for doc in docs)
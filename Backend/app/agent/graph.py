# app/agent/graph.py
"""
The agent workflow.

    START
      |
      v
 analyze_query --(pure calculation)--------> calculator ---------------+
      |                                           |                     |
      | (no calc detected)                        | (also asks about   |
      v                                           |  RBI/legal/etc)     v
  classify_intent                                  v                synthesize --> END
      |                                        retrieve                  ^
      +--(regulation/general)--> retrieve --------+                      |
      |                                                                  |
      +--(planning)------------------------------------------------------+

Every node reads/writes the shared AgentState (see state.py). Two things
make this a genuine multi-step agent rather than a single-branch router:

1. `analyze_query` deterministically detects BOTH a calculation request AND
   whether the same query also asks about the regulatory/legal side (e.g.
   "EMI for 5L at 8% for 5 years, and is this loan type regulated by RBI?").
   When both are present, the graph visits calculator -> retrieve -> synthesize
   in sequence for a single query, instead of only ever answering one half.
2. `synthesize` combines whichever pieces of state got populated (tool
   result, RAG context, or neither for planning) into one coherent answer.
"""

from langgraph.graph import END, StateGraph

from app.agent.state import AgentState
from app.agent.tools import (
    extract_calculation,
    needs_regulation_context,
    retrieve_context,
    run_calculator,
)
from app.services.intent_service import classify_intent
from app.services.llm_service import get_llm, invoke_text

_llm = get_llm()


# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------

def analyze_query_node(state: AgentState) -> AgentState:
    calc_type, params = extract_calculation(state["query"])
    needs_reg = needs_regulation_context(state["query"])
    return {
        **state,
        "calc_type": calc_type,
        "calc_params": params,
        "needs_regulation": needs_reg,
    }


def calculator_node(state: AgentState) -> AgentState:
    result = run_calculator(state["calc_type"], state["calc_params"])
    used = state.get("used_tool")
    return {
        **state,
        "tool_result": result,
        "used_tool": f"{used}+calculator" if used else "calculator",
    }


def classify_intent_node(state: AgentState) -> AgentState:
    intent = classify_intent(state["query"])
    return {**state, "intent": intent}


def retrieve_node(state: AgentState) -> AgentState:
    context = retrieve_context(state["query"], k=3)
    used = state.get("used_tool")
    return {
        **state,
        "context": context,
        "used_tool": f"{used}+rag" if used else "rag",
    }


def synthesize_node(state: AgentState) -> AgentState:
    memory = state.get("memory", "")
    query = state["query"]

    tool_result = state.get("tool_result")
    context = state.get("context")

    if tool_result and context:
        # Chained path: a calculation AND regulatory context both apply.
        r = tool_result
        prompt = f"""
You are a financial assistant. A calculation has already been performed by a
verified tool, and relevant regulatory context has been retrieved. Do not
redo the math - explain the result, then answer the regulatory part using
ONLY the context given. If the context doesn't cover it, say so.

Previous Conversation:
{memory}

Calculation type: {r['calc_type']}
Inputs: {r['params']}
Result: {r['result']}

Regulatory Context:
{context}

Question:
{query}

Answer both parts of the question clearly, in separate short sections.
"""
    elif tool_result:
        r = tool_result
        prompt = f"""
You are a financial calculator assistant. A calculation has already been
performed by a verified tool - do not redo the math, just explain it clearly.

Previous Conversation:
{memory}

Calculation type: {r['calc_type']}
Inputs: {r['params']}
Result: {r['result']}

Question:
{query}

Explain the result to the user in plain language, referencing the inputs.
"""
    elif state.get("intent") == "regulation":
        prompt = f"""
You are a strict financial regulation assistant.

Previous Conversation:
{memory}

Answer ONLY using the context below.
If not found, say:
"Information not available in verified sources."

Context:
{context or ''}

Question:
{query}

Answer:
"""
    elif state.get("intent") == "planning":
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
    else:
        prompt = f"""
Previous Conversation:
{memory}

Answer using the context below.
If unsure, say information not available.

Context:
{context or ''}

Question:
{query}

Answer:
"""

    answer = invoke_text(_llm, prompt)
    used = state.get("used_tool") or state.get("intent")
    return {**state, "final_answer": answer, "used_tool": used}


# ---------------------------------------------------------------------------
# Conditional edges
# ---------------------------------------------------------------------------

def route_after_analyze(state: AgentState) -> str:
    return "calculator" if state.get("calc_type") else "classify_intent"


def route_after_calculator(state: AgentState) -> str:
    # Chain into retrieval too if the same query also asked about the
    # regulatory/legal side of the calculation.
    return "retrieve" if state.get("needs_regulation") else "synthesize"


def route_after_classify(state: AgentState) -> str:
    return "synthesize" if state.get("intent") == "planning" else "retrieve"


# ---------------------------------------------------------------------------
# Build graph
# ---------------------------------------------------------------------------

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("analyze_query", analyze_query_node)
    graph.add_node("calculator", calculator_node)
    graph.add_node("classify_intent", classify_intent_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("synthesize", synthesize_node)

    graph.set_entry_point("analyze_query")

    graph.add_conditional_edges(
        "analyze_query",
        route_after_analyze,
        {"calculator": "calculator", "classify_intent": "classify_intent"},
    )
    graph.add_conditional_edges(
        "calculator",
        route_after_calculator,
        {"retrieve": "retrieve", "synthesize": "synthesize"},
    )
    graph.add_conditional_edges(
        "classify_intent",
        route_after_classify,
        {"retrieve": "retrieve", "synthesize": "synthesize"},
    )

    graph.add_edge("retrieve", "synthesize")
    graph.add_edge("synthesize", END)

    return graph.compile()


# Compiled once at import time - reused across requests
agent_graph = build_graph()

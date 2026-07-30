# app/agent/state.py
"""
Shared state that flows through every node of the LangGraph agent.

Keeping this as a single TypedDict (rather than passing loose args between
functions, like the old query_service.py did) is what makes this an actual
graph-based agent: every node reads from and writes to the same state object,
so you can log/inspect/replay the full reasoning trace for any query.
"""

from typing import Optional, TypedDict


class AgentState(TypedDict, total=False):
    # ---- input ----
    query: str
    username: str          # used as the memory/session key
    memory: str            # past conversation, injected once at the start

    # ---- routing ----
    intent: Optional[str]          # "regulation" | "planning" | "general"
    calc_type: Optional[str]       # "emi" | "simple" | "compound" | None
    calc_params: Optional[dict]    # {"principal": ..., "rate": ..., "time": ...}
    needs_regulation: bool         # True if query also asks about legal/regulatory side

    # ---- tool / retrieval outputs ----
    context: Optional[str]         # concatenated RAG context
    tool_result: Optional[dict]    # raw calculator output
    used_tool: Optional[str]       # name of the node that produced the answer, for logging

    # ---- output ----
    final_answer: str
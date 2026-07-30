from app.agent.graph import agent_graph
from app.services.memory_service import get_memory


def generate_answer(query: str, session_id: str):
    """
    Entry point used by main.py. Unchanged signature/return type, so nothing
    else in the app needs to change - but internally this now runs the
    LangGraph agent (see app/agent/graph.py) instead of a hardcoded
    if/elif prompt chain.
    """
    state = {
        "query": query,
        "username": session_id,
        "memory": get_memory(session_id),
    }

    result = agent_graph.invoke(state)
    return result["final_answer"]


def generate_answer_debug(query: str, session_id: str) -> dict:
    """
    Same as generate_answer, but returns the full agent state so you can
    inspect which path was taken (calculator vs RAG vs planning) - useful
    for debugging and for demoing the agent in interviews.
    """
    state = {
        "query": query,
        "username": session_id,
        "memory": get_memory(session_id),
    }
    return agent_graph.invoke(state)

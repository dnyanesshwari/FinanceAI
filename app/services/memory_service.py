from collections import defaultdict

# store chats per user
chat_memory = defaultdict(list)

def add_to_memory(username: str, query: str, response: str):
    chat_memory[username].append({"query": query, "response": response})

def get_user_history(username: str):
    return chat_memory.get(username, [])

def clear_session_memory(username: str):
    chat_memory[username] = []

def get_memory(username: str) -> str:
    """
    Return the conversation history for `username` as a single string
    suitable for inclusion in an LLM prompt.
    """
    history = chat_memory.get(username, [])
    return "\n".join(
        f"User: {entry['query']}\nAssistant: {entry['response']}"
        for entry in history
    )
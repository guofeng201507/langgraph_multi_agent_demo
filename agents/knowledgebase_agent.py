from llm_router import summarize


def knowledgebase_agent(query: str) -> str:
    prompt = f"""
    You are a knowledge base assistant. Answer the user's question using the internal company FAQ.
    If the answer is unknown, say so clearly.

    User Query: {query}
    """
    return summarize(prompt)

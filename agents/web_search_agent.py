from langsmith import traceable
from llm_router import summarize  # your LLM wrapper
from mcp.client import call_mcp


@traceable(name="web_search_agent")
def web_search_agent(state):
    query = state.get("coordinator_response", {}).get("query") or state.get("user_input", "")
    history = state.get("chat_history", [])

    raw_result = call_mcp(
        task="web_search",
        input_data={"query": query},
        history=history,
        agent_name="web_search_agent"
    )

    print(f"Search resdult is : {raw_result}")

    if not raw_result or "Error" in raw_result:
        response = raw_result
    else:
        prompt = f"""
            You are a helpful AI assistant. Summarize the web search result for the user query below in 3 sentences.

            Query: "{query}"

            Raw Result: "{raw_result}"

            Summary:
            """
        try:
            response = summarize(prompt)
        except Exception as e:
            response = f"Search result fetched, but summarization failed: {str(e)}"

    return {
        **state,
        "agent_outputs": {
            **state.get("agent_outputs", {}),
            "web_search_agent": response
        }
    }

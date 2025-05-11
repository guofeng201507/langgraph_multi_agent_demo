from langsmith import traceable
from llm_router import summarize  # your LLM wrapper
from langchain_community.tools import DuckDuckGoSearchResults


@traceable(name="web_search_agent")
def web_search_agent(state):
    query = state.get("coordinator_response", {}).get("query", "") or state.get("user_input", "")
    history = state.get("chat_history", [])

    search_type = classify_search_type_with_llm(query)

    tool = DuckDuckGoSearchResults()

    if search_type == "news":
        # DuckDuckGo's 'news' not directly supported in tool, so just refine query
        result = tool.run(f"{query} site:news")
    else:
        result = tool.run(query)

    return {
        **state,
        "agent_outputs": {
            **state.get("agent_outputs", {}),
            "duckduckgo_search_agent": result
        }
    }


def classify_search_type_with_llm(query: str) -> str:
    prompt = f"""
You are an intent classifier for a DuckDuckGo search agent.

Classify this query as:
- "news" → if the user wants current or recent events.
- "general" → otherwise.

Query: "{query}"

Return only one word: "news" or "general".
"""
    try:
        result = summarize(prompt, expect_json=False).strip().lower()
        return result if result in {"news", "general"} else "general"
    except Exception:
        return "general"

from llm_router import summarize


def merge_agent(state):
    outputs = state.get("agent_outputs", {})
    query = state.get("coordinator_response", {}).get("query", "")
    if not outputs:
        print("\nℹ️ No output from sub-agents.")
        return state

    merged_context = "\n".join([
        f"[{agent}]\n{resp}" for agent, resp in outputs.items()
    ])

    prompt = f"""
You are a customer service summarizer.

User's request: "{query}"

Agent outputs:
{merged_context}

Please summarize all the relevant findings in a clear and concise reply to the user.

Be short, helpful, and accurate. Respond as customer support would.

Your reply:
"""

    try:
        user_facing_reply = summarize(prompt)
    except Exception:
        user_facing_reply = "Your request has been processed. Please check individual results above."

    print("\n📦 Final Merged Response to User:")
    print("----------------------------------")
    print(user_facing_reply)
    print("----------------------------------")

    return {
        **state,
        "final_response": user_facing_reply
    }

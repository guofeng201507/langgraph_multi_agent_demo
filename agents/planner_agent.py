from llm_router import summarize


def planner_agent(state):
    """
    The planner decides which agent to call next based on:
    - user input
    - current outputs
    - previous agents called
    """
    print("------Planner Agent is triggered---------")
    user_input = state.get("user_input", "")
    context = state.get("agent_outputs", {})
    history = state.get("agent_call_history", [])
    chat = "\n".join(state.get("chat_history", [])[-3:])

    query = state.get("coordinator_response", {}).get("query", user_input)

    valid_agents = ["billing_agent", "order_status_agent", "user_profile_agent",
                    "coingecko_trending_agent"]

    prompt = f"""
        You are an AI planner in a multi-agent system.
        
        Here is the recent conversation:
        {chat}
        
        user's request is: "{query}"
        
        You have already called the following agents (in order): {history}
        
        Current agent outputs: {context}
        
        Choose the next agent to call from: {valid_agents}
        
        Avoid calling the same agent more than once. If all required info is gathered, return "merge".
        
        Respond with:
        {{
          "next_agent": "agent_name or merge"
        }}
        """

    # print(f"Planner_agent lastest prompt → {prompt}")
    try:
        result = summarize(prompt, expect_json=True)
        next_agent = result.get("next_agent", "merge")

        # 防止无限循环
        if history.count(next_agent) >= 2 and next_agent != "merge":
            print(f"⚠️ Detected too many calls to {next_agent}, forcing merge.")
            next_agent = "merge"

        # 更新历史
        history.append(next_agent)

        print(f"🤖 planner_agent decided next → {next_agent}")
        return {
            "next_agent": next_agent,
            "agent_call_history": history
        }

    except Exception as e:
        print("❌ planner_agent failed:", str(e))
        return {
            "next_agent": "merge",
            "agent_call_history": history + ["merge"]
        }

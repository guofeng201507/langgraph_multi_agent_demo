from mcp.client import call_mcp


def exchange_list_agent(state):
    query = state.get("coordinator_response", {}).get("query", "")

    history = state.get("chat_history", [])

    response = call_mcp(
        task="get_exchange_list",
        history=history,
        input_data= {},
        agent_name="exchange_list_agent"
    )

    print(f"----MCP exchange list --- is {response}")
    formatted_response = f": {response}"

    return {
        **state,
        "agent_outputs": {
            **state.get("agent_outputs", {}),
            "exchange_list_agent": formatted_response
        }
    }

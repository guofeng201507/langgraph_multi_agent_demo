def user_profile_agent(state):

    query = state.get("coordinator_response", {}).get("query", "")
    response = (
        "👤 User Profile:\n"
        "- Name: John Doe\n"
        "- Account Tier: Gold\n"
        "- Joined: August 12, 2021"
    )

    # state["agent_outputs"] = state.get("agent_outputs", {})
    # state["agent_outputs"]["user_profile_agent"] = response
    # return state

    outputs = state.get("agent_outputs", {})
    outputs["user_profile_agent"] = "...response..."
    return {"agent_outputs": outputs}
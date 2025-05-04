def user_profile_agent(state):

    query = state.get("coordinator_response", {}).get("query", "")
    response = (
        "👤 User Profile:\n"
        "- Name: John Doe\n"
        "- Account Tier: Gold\n"
        "- Joined: August 12, 2021"
    )

    return {
        "agent_outputs": {
            "user_profile_agent": response
        }
    }
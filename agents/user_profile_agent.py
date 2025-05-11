from mcp.client import call_mcp
from langsmith import traceable


@traceable(name="user_profile_agent")
def user_profile_agent(state):
    # query = state.get("coordinator_response", {}).get("query", "")
    # response = (
    #     "👤 User Profile:\n"
    #     "- Name: John Doe\n"
    #     "- Account Tier: Gold\n"
    #     "- Joined: August 12, 2021"
    # )
    #
    # return {
    #     "agent_outputs": {
    #         "user_profile_agent": response
    #     }
    # }

    query = state.get("coordinator_response", {}).get("query", "")
    user_id = state.get("user_id")
    history = state.get("chat_history", [])

    response = call_mcp(
        task="get_user_profile",
        input_data={"user_id": user_id},
        history=history,
        agent_name="user_profile_agent"
    )

    formatted_response = f"👤 User Profile:\n{response}"

    return {
        **state,
        "agent_outputs": {
            **state.get("agent_outputs", {}),
            "user_profile_agent": formatted_response
        }
    }

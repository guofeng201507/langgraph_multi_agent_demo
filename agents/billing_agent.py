from llm_router import summarize


def billing_agent(state):
    """
    Simulated billing agent that responds to billing-related queries.

    This agent reads the cleaned query from coordinator_response["query"],
    and writes its result only to `agent_outputs["billing_agent"]`.

    LangGraph expects isolated updates to avoid state conflicts.
    """

    query = state.get("coordinator_response", {}).get("query", "")

    # You can plug real billing API logic here
    response = (
        "📄 Billing Summary:\n"
        "- Last payment: $42.50 on March 29, 2025\n"
        "- Current balance: $0.00\n"
        "- Next invoice due: None"
    )

    return {
        "agent_outputs": {
            "billing_agent": response
        }
    }

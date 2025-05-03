def order_status_agent(state):
    query = state.get("coordinator_response", {}).get("query", "")

    response = (
        "📦 Order Status:\n"
        "- Order #ORD123456\n"
        "- Item: Bluetooth Headphones\n"
        "- Status: Shipped\n"
        "- Estimated Delivery: May 5, 2025"
    )

    return {
        "agent_outputs": {
            "order_status_agent": response
        }
    }

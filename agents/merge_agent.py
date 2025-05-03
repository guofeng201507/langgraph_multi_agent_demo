def merge_agent(state):
    outputs = state.get("agent_outputs", {})
    if not outputs:
        print("\nℹ️ No output from sub-agents.")
        return state

    merged_response = "\n".join([
        f"🧠 [{agent}]\n{resp}" for agent, resp in outputs.items()
    ])

    print("\n📦 Final Merged Response to User:")
    print("----------------------------------")
    print(merged_response)
    print("----------------------------------")

    return state

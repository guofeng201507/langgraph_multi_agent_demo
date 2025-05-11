from graph_planner import graph
from copy import deepcopy

test_inputs = [
    # "asdfghjkl 12345 !!!", #SPAM
    # "What are your business hours?", #"KNOWLEDGEBASE"
    # "I think my billing info is outdated and my order hasn’t arrived.", #"MULTI_API"
    # "what is the current trending items in crypto market?", #"MULTI_API":
    "give me a list of most popular crypto exchanges"
]

def print_section(title):
    print("\n" + "="*40)
    print(f"{title}")
    print("="*40)

for user_input in test_inputs:
    # print_section(f"🧪 Testing Intent: {label}")
    state = {
        "user_input": user_input,
        "coordinator_response": {},
        "agent_outputs": {},
        "agent_call_history": [],
        "next_agent": "planner"
    }

    final_state = graph.invoke(deepcopy(state))

    print("User Input:", user_input)
    print("Intent:", final_state["coordinator_response"].get("intent", "N/A"))

    print("\nAgent Call History:")
    for step in final_state["agent_call_history"]:
        print("→", step)

    print("\nAgent Outputs:")
    for agent, response in final_state["agent_outputs"].items():
        print(f"\n🧠 [{agent}]:\n{response}")

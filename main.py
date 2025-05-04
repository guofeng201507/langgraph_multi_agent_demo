from graph_planner import graph
from copy import deepcopy

state = {
    "chat_history": [],
    "agent_outputs": {},
    "coordinator_response": {},
    "agent_call_history": [],
    "next_agent": "planner"
}

print("🧠 Welcome to Smart Customer Support. Type 'exit' to quit.\n")


def run():
    while True:
        user_input = input("👤 You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting. Goodbye!")
            break

        # 注入用户输入
        state["user_input"] = user_input
        state["chat_history"].append(user_input)

        # 执行图
        result = graph.invoke(deepcopy(state))
        state.update(result)  # 累积状态，支持多轮

        # 输出当前轮结果
        print("🧾 Intent:", result["coordinator_response"].get("intent", "N/A"))
        print("\n📜 Agent Call History:")
        for step in result["agent_call_history"]:
            print("→", step)

        print("\n🤖 Agent Outputs:")
        for agent, response in result["agent_outputs"].items():
            print(f"\n🧠 [{agent}]:\n{response}")
        print("-" * 50)

        print(state["chat_history"])

if __name__ == "__main__":
    run()

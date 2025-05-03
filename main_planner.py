
from graph_planner import graph
from copy import deepcopy

# 用户输入示例：混合多个潜在子任务
user_input = "My billing looks wrong and my order status may be outdated."

# 初始状态注入（第一次只有 user_input 和 coordinator_response）
state = {
    "user_input": user_input,
    "coordinator_response": {
        "query": user_input  # 简化模拟，无需 coordinator_agent 分类
    },
    "agent_outputs": {},
    "agent_call_history": [],
    "next_agent": "planner"  # graph 的入口
}

def print_section(title):
    print("\n" + "="*30)
    print(f"{title}")
    print("="*30)

# 执行多轮 Graph 推理链
final_state = graph.invoke(deepcopy(state))

# 打印结果
print("\n🧾 Agent Call History:")
for step in final_state["agent_call_history"]:
    print("→", step)

print("\n📦 Aggregated Agent Outputs:")
for agent, response in final_state["agent_outputs"].items():
    print(f"\n🧠 [{agent}]:\n{response}")

from langgraph.graph import StateGraph
"""
This is simple SOP based multi-agent

"""

def merge_dicts(a: dict, b: dict) -> dict:
    return {**a, **b}


from typing import TypedDict, Annotated
from agents import (
    coordinator_agent,
    knowledgebase_agent,
    billing_agent,
    order_status_agent,
    user_profile_agent,
    merge_agent
)


# 定义状态结构
class GraphState(TypedDict):
    user_input: str
    coordinator_response: dict
    agent_outputs: Annotated[dict, merge_dicts]


# Agent 名称与函数映射
AGENT_MAP = {
    "billing_agent": billing_agent.billing_agent,
    "order_status_agent": order_status_agent.order_status_agent,
    "user_profile_agent": user_profile_agent.user_profile_agent,
}

# 初始化图构建器
builder = StateGraph(state_schema=GraphState)

# 注册核心节点
builder.add_node("coordinator", coordinator_agent.coordinator_agent)
builder.add_node("knowledgebase", knowledgebase_agent.knowledgebase_agent)
builder.add_node("merge", merge_agent.merge_agent)

# 注册所有 multi_api agents
for name, func in AGENT_MAP.items():
    builder.add_node(name, func)

# 设置入口点
builder.set_entry_point("coordinator")


# 分支路由逻辑
def router(state: GraphState) -> str | list[str]:
    intent = state["coordinator_response"].get("intent", "")
    actions = state["coordinator_response"].get("actions", [])

    if intent == "SPAM":
        print("\n🛑 Detected SPAM:\n", state["coordinator_response"].get("final_response"))
        return "merge"
    elif intent == "KNOWLEDGEBASE":
        return "knowledgebase"
    elif intent == "MULTI_API":
        return actions
    else:
        return "merge"


# 添加条件跳转
builder.add_conditional_edges("coordinator", router)

# 每个子 Agent 返回 merge
builder.add_edge("knowledgebase", "merge")
for agent_name in AGENT_MAP.keys():
    builder.add_edge(agent_name, "merge")

# 设置终点
builder.set_finish_point("merge")

# 编译图
graph = builder.compile()

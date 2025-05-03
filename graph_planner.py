from langgraph.graph import StateGraph
from typing import TypedDict, Annotated

from agents import (
    planner_agent,
    billing_agent,
    user_profile_agent,
    # address_agent,
    order_status_agent,
    merge_agent,
)


# 多轮合并函数
def merge_dicts(a: dict, b: dict) -> dict:
    return {**a, **b}


def merge_lists(a: list, b: list) -> list:
    return a + b


class PlannerGraphState(TypedDict):
    user_input: str
    coordinator_response: dict
    agent_outputs: Annotated[dict, merge_dicts]
    agent_call_history: Annotated[list[str], merge_lists]
    next_agent: str  # 每一轮由 planner_agent 设置


AGENT_MAP = {
    "billing_agent": billing_agent.billing_agent,
    "user_profile_agent": user_profile_agent.user_profile_agent,
    "order_status_agent": order_status_agent.order_status_agent,
}

builder = StateGraph(state_schema=PlannerGraphState)

# 注册核心 agent
builder.add_node("planner", planner_agent.planner_agent)
for name, func in AGENT_MAP.items():
    builder.add_node(name, func)
builder.add_node("merge", merge_agent.merge_agent)

# 设置入口点为 planner（每轮都重新判断下一步）
builder.set_entry_point("planner")


# planner 根据 context 决策下一 agent
def router(state: PlannerGraphState):
    return state.get("next_agent", "merge")


builder.add_conditional_edges("planner", router)

# 每个业务 agent 执行后 → 回到 planner（循环）
for name in AGENT_MAP.keys():
    builder.add_edge(name, "planner")

# 设置终点
builder.set_finish_point("merge")

graph = builder.compile()

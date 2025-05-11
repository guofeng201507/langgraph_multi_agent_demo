from langgraph.graph import StateGraph
from typing import TypedDict, Annotated

from agents import (
    coordinator_agent,
    knowledgebase_agent,
    merge_agent,
    planner_agent,
    billing_agent,
    user_profile_agent,
    order_status_agent,
    coingecko_trending_agent,
    exchange_list_agent
)


# 合并器函数
def merge_dicts(a: dict, b: dict) -> dict:
    return {**a, **b}


def merge_lists(a: list, b: list) -> list:
    return a + b


class GraphState(TypedDict):
    user_input: str
    chat_history: Annotated[list[str], merge_lists]
    coordinator_response: dict
    agent_outputs: Annotated[dict, merge_dicts]
    agent_call_history: Annotated[list[str], merge_lists]
    next_agent: str  # only used in planner flow


builder = StateGraph(state_schema=GraphState)

# 注册所有必要节点
builder.add_node("coordinator", coordinator_agent.coordinator_agent)
builder.add_node("knowledgebase", knowledgebase_agent.knowledgebase_agent)
builder.add_node("merge", merge_agent.merge_agent)
builder.add_node("planner", planner_agent.planner_agent)

# 注册业务 agent（由 planner 控制）
builder.add_node("billing_agent", billing_agent.billing_agent)
builder.add_node("user_profile_agent", user_profile_agent.user_profile_agent)
builder.add_node("order_status_agent", order_status_agent.order_status_agent)
builder.add_node("coingecko_trending_agent", coingecko_trending_agent.coingecko_trending_agent)
builder.add_node("exchange_list_agent", exchange_list_agent.exchange_list_agent)

# 入口：先执行 coordinator
builder.set_entry_point("coordinator")


# 总入口路由逻辑：根据 intent 决定后续路径
def coordinator_router(state: GraphState):
    intent = state["coordinator_response"].get("intent", "")
    if intent == "SPAM":
        print("🛑 Detected SPAM — skipping to merge.")
        return "merge"
    elif intent == "KNOWLEDGEBASE":
        return "knowledgebase"
    elif intent == "MULTI_API":
        return "planner"
    else:
        return "merge"


builder.add_conditional_edges("coordinator", coordinator_router)

# 单 agent 流程 → merge
builder.add_edge("knowledgebase", "merge")


# planner 多轮调用 → 动态判断下一跳
def planner_router(state: GraphState):
    return state.get("next_agent", "merge")


builder.add_conditional_edges("planner", planner_router)

# 每个 planner 控制的 agent 都回到 planner
for agent_name in ["billing_agent", "user_profile_agent", "order_status_agent", "coingecko_trending_agent",
                   "exchange_list_agent"]:
    builder.add_edge(agent_name, "planner")

# 终点
builder.set_finish_point("merge")

graph = builder.compile()

#visualize graph
# print(graph.get_graph().draw_mermaid())
# copy output and paste here: https://mermaid.live/
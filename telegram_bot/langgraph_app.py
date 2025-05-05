# langgraph_app.py
from graph_planner import graph
from copy import deepcopy

state = {
    "chat_history": [],
    "agent_outputs": {},
    "coordinator_response": {},
    "agent_call_history": [],
    "next_agent": "planner"
}

def extract_final_response(langgraph_output):
    """
    从 LangGraph 返回的 JSON 中抽取 final_response 字段的值。
    如果字段不存在或结构异常，返回默认提示。
    """
    try:
        return langgraph_output.get("coordinator_response", {}).get("final_response", "对不起，我没能理解你的请求。")
    except Exception:
        return "对不起，我没能理解你的请求。"


def process_user_message(user_input):
    """
    调用 LangGraph app 的接口。
    输入: 用户消息文本
    输出: LangGraph agent 的回复
    """
    # 根据你的 LangGraph 接口结构进行调整

    # 注入用户输入
    state["user_input"] = user_input
    state["chat_history"].append(user_input)

    # 执行图
    response = graph.invoke(deepcopy(state))
    state.update(response)  # 累积状态，支持多轮

    return extract_final_response(response)

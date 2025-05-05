# client.py

import requests


def call_mcp(task, input_data, history, agent_name):
    payload = {
        "task": task,
        "input": input_data,
        "history": history,
        "meta": {"agent_name": agent_name}
    }
    try:
        response = requests.post("http://localhost:8000/mcp", json=payload)
        response.raise_for_status()
        return response.json().get("response", "未返回响应。")
    except Exception as e:
        print(f"调用 MCP 失败：{e}")
        return "服务暂时不可用。"

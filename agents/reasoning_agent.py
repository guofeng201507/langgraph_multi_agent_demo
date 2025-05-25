import json
import requests
from llm_router import summarize
from langsmith import traceable

# 读取服务目录
with open("../service_catalog.json", "r") as f:
    SERVICE_CATALOG = json.load(f)

MCP_ENDPOINT = "http://localhost:8000/mcp"


@traceable(name="reasoning_agent")
def reasoning_agent(state):
    print(f""""State information is {state}""")
    user_input = state.get("user_input", "")
    chat_history = state.get("chat_history", [])
    context = state.get("agent_outputs", {})
    service_history = state.get("service_call_history", [])

    catalog_summary = "\n".join([
        f"- {name}: {meta['description']}" for name, meta in SERVICE_CATALOG.items()
    ])

    prompt = f"""
You are an intelligent AI assistant in a customer service system.

Your goal is to reason step-by-step what information is needed to answer the user's question.

You are given a catalog of available services:

{catalog_summary}

User input: "{user_input}"

So far you have called: {service_history}

Based on current conversation, choose the next service to call (or say "none" if ready to reply).

Reply in JSON format:
{{
  "service_to_call": "service_name or none",
  "params": {{...}}  // keys from 'inputs' field of service
}}
"""

    try:
        plan = summarize(prompt, expect_json=True)
        service = plan.get("service_to_call", "none")

        print(f"""Service to call  {service} """)
        if service == "none":
            return {
                **state,
                "next_agent": "merge"  # 推动流程到merge agent
            }

        # 构造 MCP payload
        payload = {
            "task": service,
            "input": plan.get("params", {}),
            "history": chat_history,
            "meta": {"agent_name": "reasoning_agent"}
        }

        response = requests.post(MCP_ENDPOINT, json=payload).json().get("response", {})

        return {
            **state,
            "agent_outputs": {
                **state.get("agent_outputs", {}),
                f"reasoning_agent::{service}": response
            },
            "service_call_history": service_history + [service],
            "next_agent": "reasoning_agent"  # 可继续由自己接管
        }

    except Exception as e:
        print("❌ reasoning_agent error:", str(e))
        return {
            **state,
            "agent_outputs": {
                **state.get("agent_outputs", {}),
                "reasoning_agent::error": "Failed to process."
            },
            "next_agent": "merge"
        }

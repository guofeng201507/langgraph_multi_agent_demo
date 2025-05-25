import json
from agents.reasoning_agent import reasoning_agent

# 假设你已经在 llm_router.summarize 中 mock 或实际调用了 OpenAI/GPT
# 如果你需要 mock summarize，请在 llm_router 中加一个 test 模式判断

def run_test_case(test_case):
    print("=" * 60)
    print(f"🧪 Test: {test_case['title']}")
    state = {
        "user_input": test_case["user_input"],
        "chat_history": test_case.get("chat_history", []),
        "agent_outputs": {},
        "service_call_history": []
    }

    updated_state = reasoning_agent(state)

    print("🔁 Next Agent:", updated_state.get("next_agent"))
    print("📤 Service Called:", updated_state.get("service_call_history"))
    print("📦 Agent Outputs:")
    for k, v in updated_state.get("agent_outputs", {}).items():
        print(f"  {k}: {v}")
    print("=" * 60 + "\n\n")


if __name__ == "__main__":
    # 🧾 准备测试用例
    test_cases = [
        {
            "title": "查询客户资料",
            "user_input": "Can you show me my account details?",
        },
        {
            "title": "订单状态查询",
            "user_input": "What's the status of my order 123456?",
            "chat_history": ["Hi", "I placed an order last week", "order 123456"]
        },
        {
            "title": "退款政策提问",
            "user_input": "What is the refund policy for product ABC123?",
        },
        {
            "title": "新建支持工单",
            "user_input": "I'm having trouble with logging in. Please help me.",
        },
        {
            "title": "获取加密趋势",
            "user_input": "Show me latest crypto market trends.",
        }
    ]

    for case in test_cases:
        run_test_case(case)

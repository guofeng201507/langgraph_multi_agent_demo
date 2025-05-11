from llm_router import summarize
from langsmith import traceable


@traceable(name="knowledgebase_agent")
def knowledgebase_agent(state):
    """
    Hybrid knowledgebase agent:
    - For general knowledge, use LLM to answer
    - For customer support topics, use internal knowledgebase (mock)
    """

    query = state.get("coordinator_response", {}).get("query", "").lower()

    # 判断是否属于客服支持领域
    support_keywords = ["refund", "delivery", "support", "invoice", "billing", "shipping", "order"]

    if any(keyword in query for keyword in support_keywords):
        # 内部知识库模拟响应（可接 API 或向量检索）
        if "refund" in query:
            answer = "💰 Our refund policy allows returns within 14 days of purchase. Contact support to initiate."
        elif "delivery" in query:
            answer = "📦 Deliveries typically arrive in 2–5 business days. Delays may occur during holidays."
        elif "support" in query:
            answer = "🧑‍💻 You can reach our support team via chat or email (support@example.com)."
        else:
            answer = "📘 For customer-related topics, please check internal policies or support portal."
    else:
        # 非客服问题，使用 LLM 回答（调用 summarize() 接 openai/qwen/deepseek）
        print("Not related with domain knowledge, using LLM own knowledge")
        prompt = f"You are a helpful AI assistant. Please answer the following question clearly:\n\nQ: {query}"
        try:
            answer = summarize(prompt, expect_json=False)["answer"]  # LLM 返回格式应为 {"answer": "..."}
        except:
            answer = "⚠️ Sorry, I couldn't generate a response. Please rephrase your question."

    return {
        "agent_outputs": {
            "knowledgebase_agent": answer
        }
    }

import os
from llm_router import summarize
from dotenv import load_dotenv
import json

load_dotenv()

from langsmith import traceable


@traceable(name="coordinator_agent")
def coordinator_agent(state):
    user_input = state["user_input"]
    chat_history = state.get("chat_history", [])
    context = "\n".join(chat_history[-3:])  # 最多参考最近三轮对话

    print("------coordinator_agent is triggered---------")

    valid_agents = ["billing_agent", "order_status_agent", "user_profile_agent",
                    "coingecko_trending_agent", "exchange_list_agent", "web_search_agent"]

    system_prompt = f"""
    You are the Coordinator Agent in a multi-agent customer service system in crypto exchange. Your role is to analyze the user's input and determine the correct routing and orchestration strategy.
    
    Your process:
    
    1. Classify the user's input into one of the following categories:
       - SPAM: Irrelevant, nonsensical, or abusive message.   
       - KNOWLEDGEBASE: Can be answered directly using static knowledge such as company FAQs, documentations or LLM built-in knowledge .
       - MULTI_API: Requires data aggregation from 2 or more APIs or functions or need to do web search.
    
    2. Take action based on the classification:
       - If SPAM: Respond with "Your message doesn't seem related to customer service. Please clarify."
       - If KNOWLEDGEBASE: Forward to the KnowledgebaseAgent.
       - If MULTI_API: Identify relevant API or function agents such as {valid_agents}

    
    Respond with a valid JSON only, no explanation or commentary. Format:
    {{
      "intent": "SPAM|KNOWLEDGEBASE|MULTI_API",
      "actions": ["agent1", "agent2"],
      "query": "Cleaned or refined user query",
      "final_response": "If SPAM, provide user-facing response here."
    }}

    """
    #       (e.g., user_profile_agent, order_status_agent, billing_agent, exchange_list_agent, coingecko_trending_agent) and query them. Then summarize all results into a single coherent user-facing message.
    prompt = f"{system_prompt}\n\nUse the chat history and current input to determine how to route the request.\n\nChat history:{context}\n\nCurrent Input: {user_input}\n\n"

    try:
        result = summarize(prompt)
        print("🧾 Coordinator Agent (LLM) Output:", result)
    except json.JSONDecodeError:
        result = {
            "intent": "SPAM",
            "actions": [],
            "query": "",
            "final_response": "Sorry, I couldn't understand your request. Could you please rephrase it?"
        }

    return {
        "coordinator_response": result
    }

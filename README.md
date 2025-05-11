
# 🧠 LangGraph Multi-Agent Customer Support System

A modular, multi-agent customer service system built with [LangGraph](https://github.com/langchain-ai/langgraph).  
It supports LLM-driven task routing, knowledgebase lookup, multi-API aggregation, and response synthesis.

---

## 🚀 Features

- 🤖 **LLM-Powered Coordinator**: Classifies input into `SPAM`, `KNOWLEDGEBASE`, or `MULTI_API`
- 🔍 **Knowledgebase Agent**: Handles FAQ queries (extendable to vector search)
- 🔗 **API Agents**: Simulated agents for billing, order status, and user profile
- 🔄 **Dynamic Routing**: Automatically orchestrates relevant agents
- 🧩 **Pluggable LLMs**: Supports `OpenAI`, `Qwen`, `DeepSeek` (via `llm_router.py`)
- 🧠 **Final Merge Agent**: Aggregates multi-agent outputs into a user-friendly response

---

## 📁 Project Structure

```
langgraph_multi_agent_demo/
│
├── main.py                      # Entry script to run the graph
├── graph.py                     # LangGraph workflow with dynamic routing
├── llm_router.py                # Unified LLM interface (OpenAI / Qwen / DeepSeek)
├── .env                         # Local API secrets (DO NOT COMMIT)
├── .env.example                 # Sample config file
│
├── agents/
│   ├── coordinator_agent.py     # Prompt-based intent classification
│   ├── knowledgebase_agent.py   # Static / LLM knowledge agent
│   ├── billing_agent.py         # Simulated billing info agent
│   ├── order_status_agent.py    # Simulated order status agent
│   ├── user_profile_agent.py    # Simulated user profile agent
│   └── merge_agent.py           # Final response aggregation
```

---

## 📦 Installation

```bash
git clone https://github.com/your-org/langgraph-multi-agent-demo.git
cd langgraph-multi_agent_demo
pip install -r requirements.txt
```

---

## 🔐 Environment Setup

1. Copy `.env.example` and fill in your keys:
```bash
cp .env.example .env
```

2. Example `.env` for OpenAI:
```env
MODEL_PROVIDER=openai
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4
OPENAI_API_BASE=https://api.openai.com/v1
```

---

## 🧪 Run the Demo

```bash
python main.py
```

Sample prompt inside `main.py`:
```python
user_input = "Can you check my billing and order status?"
```

Sample output:
```
📦 Final Merged Response to User:
----------------------------------
🧠 [billing_agent]
📄 Billing Summary:
- Last payment: $42.50 on March 29, 2025
- Current balance: $0.00
- Next invoice due: None

🧠 [order_status_agent]
📦 Order Status:
- Order #ORD123456
- Item: Bluetooth Headphones
- Status: Shipped
- Estimated Delivery: May 5, 2025
----------------------------------
```
```

langgraph_multi_agent_demo\mcp>uvicorn server:app --host 0.0.0.0 --port 8000 

INFO:     Started server process [6072]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:64483 - "POST /mcp HTTP/1.1" 200 OK


```
---

## 🧠 Future Improvements

- ✅ Integrate real APIs (CRM, ERP, database)
- ✅ Replace `knowledgebase_agent` with vector search (e.g. FAISS + LlamaIndex)
- ✅ Add Gradio / Streamlit frontend
- ✅ Deploy as a FastAPI or LangServe service
- ✅ Add chat memory with LangGraph state
- ✅ Add https://smith.langchain.com/

---

## 📄 License

MIT License – free to use, modify, and contribute.

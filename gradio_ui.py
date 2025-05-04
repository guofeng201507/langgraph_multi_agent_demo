import gradio as gr
from graph_planner import graph
from copy import deepcopy

# 初始化状态
def init_state():
    return {
        "chat_history": [],
        "agent_outputs": {},
        "coordinator_response": {},
        "agent_call_history": [],
        "next_agent": "planner",
        "chatbot_history": []
    }

# 单轮对话处理函数
def chat_fn(user_input, chat_state):
    chat_state["user_input"] = user_input
    chat_state["chat_history"].append(user_input)

    result = graph.invoke(deepcopy(chat_state))
    chat_state.update(result)

    reply = result.get("final_response", "(No response)")
    chat_state["chatbot_history"].append((user_input, reply))

    return chat_state, chat_state["chatbot_history"]

# 构建 Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🤖 Smart Customer Service Chatbot")

    chatbot = gr.Chatbot()
    txt = gr.Textbox(placeholder="Type your request (e.g., billing, shipping)...")
    state = gr.State(init_state())

    def submit(user_input, state_data):
        state_data, updated_history = chat_fn(user_input, state_data)
        return state_data, updated_history, ""

    txt.submit(submit, inputs=[txt, state], outputs=[state, chatbot, txt])

# 启动服务
if __name__ == "__main__":
    demo.launch()

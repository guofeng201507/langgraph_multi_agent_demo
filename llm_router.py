import os
from openai import OpenAI
from dotenv import load_dotenv

import json

load_dotenv()

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")


# ========== 统一 LLM 路由入口 ==========
def summarize(prompt: str, expect_json: bool = True) -> dict:
    """
    LLM wrapper that supports two modes:
    - expect_json=True: return parsed JSON object
    - expect_json=False: return raw answer in {"answer": "..."}
    """
    try:
        if MODEL_PROVIDER == "openai":
            return summarize_response_openai(prompt, expect_json)
        elif MODEL_PROVIDER == "qwen":
            return summarize_response_qwen(prompt, expect_json)
        elif MODEL_PROVIDER == "deepseek":
            return summarize_response_deepseek(prompt, expect_json)
        else:
            raise ValueError(f"Unknown MODEL_PROVIDER: {MODEL_PROVIDER}")
    except Exception as e:
        print("⚠️ summarize() failed:", str(e))

        # Fallback values
        if expect_json:
            return {
                "intent": "SPAM",
                "actions": [],
                "query": "",
                "final_response": "Sorry, I couldn't understand your request. Please rephrase it."
            }
        else:
            return {
                "answer": "⚠️ Sorry, I couldn't generate an answer right now. Please try again later."
            }


# ========== OpenAI ==========
def summarize_response_openai(prompt: str, expect_json: bool = True) -> dict:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    )

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    if expect_json:
        messages[0]["content"] += " Respond in valid JSON only."

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        messages=messages,
        temperature=0.3
    )

    # content = response.choices[0].message.content

    content = response.choices[0].message.content.strip()

    # 尝试提取 JSON 块
    if expect_json:
        import json, re
        try:
            match = re.search(r"{.*}", content, re.DOTALL)
            if match:
                return json.loads(match.group())
            else:
                raise ValueError("No JSON found in LLM output.")
        except Exception as e:
            print("❌ JSON parse failed. Raw content:", content)
            raise e
    else:
        return {"answer": content}
    # return json.loads(content)


# ========== Qwen（阿里） ==========
def summarize_response_qwen(prompt: str) -> dict:
    # Replace with actual SDK/API call
    raise NotImplementedError("Qwen support not implemented yet.")


# ========== DeepSeek ==========
def summarize_response_deepseek(prompt: str) -> dict:
    # Replace with actual SDK/API call
    raise NotImplementedError("DeepSeek support not implemented yet.")

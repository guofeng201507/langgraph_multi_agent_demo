import os
from openai import OpenAI
from dotenv import load_dotenv

import json

load_dotenv()

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")


# ========== 统一 LLM 路由入口 ==========
def summarize(prompt: str) -> dict:
    if MODEL_PROVIDER == "openai":
        return summarize_response_openai(prompt)
    elif MODEL_PROVIDER == "qwen":
        return summarize_response_qwen(prompt)
    elif MODEL_PROVIDER == "deepseek":
        return summarize_response_deepseek(prompt)
    else:
        raise ValueError(f"Unknown MODEL_PROVIDER: {MODEL_PROVIDER}")


# ========== OpenAI ==========
def summarize_response_openai(prompt: str) -> dict:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    )

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        messages=[
            {"role": "system", "content": "You are a smart assistant. Reply in JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    # content = response.choices[0].message.content

    content = response.choices[0].message.content.strip()

    # 尝试提取 JSON 块
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

    # return json.loads(content)


# ========== Qwen（阿里） ==========
def summarize_response_qwen(prompt: str) -> dict:
    # Replace with actual SDK/API call
    raise NotImplementedError("Qwen support not implemented yet.")


# ========== DeepSeek ==========
def summarize_response_deepseek(prompt: str) -> dict:
    # Replace with actual SDK/API call
    raise NotImplementedError("DeepSeek support not implemented yet.")

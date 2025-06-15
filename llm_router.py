import os
from openai import OpenAI
from dotenv import load_dotenv
import json, re
import requests

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
        elif MODEL_PROVIDER == "local":
            return summarize_response_ollama(prompt, expect_json)
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


def extract_json(content: str, expect_json: bool = True):
    if expect_json:
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

    model = os.getenv("OPENAI_MODEL", "gpt-4o")
    print(f"LLM model used: {model}")
    content = response.choices[0].message.content.strip()

    return extract_json(content, expect_json)


# ========== Qwen（阿里） ==========
def summarize_response_qwen(prompt: str, expect_json: bool = True) -> dict:
    client = OpenAI(
        api_key=os.getenv("QWEN_API_KEY"),
        base_url=os.getenv("QWEN_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    )

    try:
        response = client.chat.completions.create(
            model="qwen-plus",  # Or use "qwen-max", "qwen-turbo", etc. based on your plan
            messages=[
                {"role": "system", "content": "You are a helpful customer service summarizer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        content = response.choices[0].message.content.strip()

        print(f"-------QWEN Summary------------- ")
        print(content)
        return extract_json(content, expect_json)

    except Exception as e:
        print(f"❌ Qwen summarization failed: {e}")
        return {"summary": "Sorry, we couldn't summarize your request at this time."}


# ========== DeepSeek ==========
def summarize_response_deepseek(prompt: str) -> dict:
    # Replace with actual SDK/API call
    raise NotImplementedError("DeepSeek support not implemented yet.")


def summarize_response_ollama(prompt: str, expect_json: bool = True) -> dict:
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen3:8b",
                "messages": [
                    {"role": "system", "content": "You are a helpful customer service summarizer. /no_think"},
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            },
            timeout=30
        )

        response.raise_for_status()
        content = response.json()["message"]["content"].strip()

        print("-------QWEN (Local) Summary-------------")
        print(content)

        return extract_json(content, expect_json)

    except Exception as e:
        print(f"❌ Local Qwen summarization failed: {e}")
        return {"summary": "Sorry, we couldn't summarize your request at this time."}

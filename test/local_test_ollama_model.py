import csv
import requests
import json

OLLAMA_URL = 'http://localhost:11434/api/chat'  # Ollama 默认接口

OLLAMA_URL_gen = 'http://localhost:11434/api/generate'

# 自定义设置
MODEL = 'qwen2.5:7b-instruct'  # 改成你本地的模型名
SYSTEM_PROMPT_FILE = "OKX_Invite_Support_Prompt full-1.1.txt"
TEMPERATURE = 0

# 输入输出文件路径
INPUT_CSV = 'input_rag_1.1.csv'
OUTPUT_CSV = 'output.csv'


# 读取 system prompt
def load_system_prompt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read().strip()


def query_ollama(user_input, system_prompt):
    payload = {
        "model": MODEL,
        "temperature": TEMPERATURE,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post(OLLAMA_URL, json=payload, stream=False)
    response.raise_for_status()

    # 即便你设置了 stream=False，Ollama 实际还是以流式逐行返回了多个 JSON 对象，每行一个 {"message": {...}, "done": false}，最后没有合并为一个 JSON。
    full_response = ""
    for line in response.text.strip().splitlines():
        try:
            data = json.loads(line)
            full_response += data.get("message", {}).get("content", "")
        except json.JSONDecodeError as e:
            continue  # 忽略异常行
    return full_response

    # result = response.json()
    # print(result)
    # return result.get("message", {}).get("content", "")


def main():
    system_prompt = load_system_prompt(SYSTEM_PROMPT_FILE)

    with open(INPUT_CSV, newline='', encoding='utf-8') as infile, \
            open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        writer.writerow(['input', 'output'])  # Header

        for row in reader:
            input_text = row[0]
            try:
                output_text = query_ollama(input_text, system_prompt)
                # print(output_text)
            except Exception as e:
                output_text = f"Error: {str(e)}"
            writer.writerow([input_text, output_text])


if __name__ == '__main__':
    main()

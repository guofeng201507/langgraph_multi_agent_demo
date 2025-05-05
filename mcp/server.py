from fastapi import FastAPI, Request, HTTPException
import asyncio
import requests
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()  # 加载 .env 文件


@app.post("/mcp")
async def mcp_endpoint(request: Request):
    data = await request.json()
    task = data.get("task")
    input_data = data.get("input", {})
    user_id = input_data.get("user_id", "unknown")

    # 🎯 模拟权限不足
    if input_data.get("simulate") == "forbidden":
        raise HTTPException(status_code=403, detail="Permission denied.")

    # 🎯 模拟内部错误
    if input_data.get("simulate") == "error":
        raise Exception("Internal MCP error.")

    # 🎯 模拟超时
    if input_data.get("simulate") == "timeout":
        await asyncio.sleep(10)  # 客户端应设置超时为小于 10s
        return {"response": "This should not be returned (timeout)."}

    # ✅ 正常任务模拟
    if task == "get_exchange_list":
        try:
            url = "https://api.coingecko.com/api/v3/exchanges"

            api_key = os.getenv("COINGECKO_DEMO_API_KEY")
            headers = {
                "accept": "application/json",
                "x-cg-demo-api-key": api_key
            }

            resp = requests.get(url, headers=headers, timeout=5)
            data = resp.json()

            # 可选择缩减返回内容
            exchanges = [
                f"- {ex['name']} (Rank: {ex['trust_score_rank']}, "
                f"Since: {ex.get('year_established', 'N/A')}, "
                f"Country: {ex.get('country', 'N/A')}, "
                f"24h BTC Volume: {ex.get('trade_volume_24h_btc', 'N/A'):.2f})"
                for ex in data[:15]
            ]
            return {
                "response": "🌐 Top Exchanges:\n" + "\n".join(exchanges)
            }

        except Exception as e:
            print(f"❌ 外部API错误: {e}")
            return {"response": "⚠️ Unable to fetch exchange list at this time."}

    # 其他 mock 数据
    elif task == "get_user_profile":
        return {
            "response": (
                "- Name: John Doe\n"
                "- Account Tier: Gold\n"
                "- Joined: August 12, 2021"
            )
        }

    elif task == "get_account_summary":
        return {
            "response": (
                "- Balance: $0.00\n"
                "- Last Payment: $42.50 on March 29, 2025\n"
                "- Next Invoice: None"
            )
        }

    elif task == "get_loyalty_status":
        return {
            "response": (
                "- Loyalty Points: 4,230\n"
                "- Tier Progress: 85% toward Platinum\n"
                "- Rewards Available: 3 vouchers"
            )
        }

    elif task == "get_recent_activity":
        return {
            "response": (
                "- 2025-04-25: Login from Singapore\n"
                "- 2025-04-20: Payment made\n"
                "- 2025-04-12: Updated mailing address"
            )
        }

    # ❌ 未识别任务
    return {"response": f"❓ MCP: Task '{task}' not recognized."}

import requests
import os
from dotenv import load_dotenv
from llm_router import summarize

load_dotenv()

"""
This endpoint allows you query trending search coins, NFTs and categories on CoinGecko in the last 24 hours

The endpoint currently supports:
Top 15 trending coins (sorted by the most popular user searches)
Top 7 trending NFTs (sorted by the highest percentage change in floor prices)
Top 5 trending categories (sorted by the most popular user searches)

"""

from langsmith import traceable

@traceable(name="coingecko_trending_agent")
def coingecko_trending_agent(state):
    query = state.get("coordinator_response", {}).get("query", "")

    url = "https://api.coingecko.com/api/v3/search/trending"
    api_key = os.getenv("COINGECKO_DEMO_API_KEY")

    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": api_key
    }

    try:
        print("🔥 Top trending search coins, NFTs and categories on CoinGecko in the last 24 hours", )

        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        data = res.json()

        prompt = f"""
        You are a crypto market analyzer. 

        This is the latest crypto market info "{data}"

        Please summarize all the relevant findings in a clear and concise reply to the user.

        Be short, helpful, and accurate. Respond as customer support would.

        Respond with a valid JSON only, no explanation or commentary. Format:
        {{
          "summary": "summarized content"
        }}
        
        """

        try:
            summary = summarize(prompt)
        except Exception:
            summary = "Not able to get data insight from coingecko API"

        response = {
            "message": "🔥 Top trending search coins, NFTs and categories on CoinGecko in the last 24 hours",
            "raw": summary
        }

        return {
            "agent_outputs": {
                "coingecko_trending_agent": response
            }
        }

    except Exception as e:
        print("❌ coingecko_trending_agent failed:", str(e))
        return {
            "agent_outputs": {
                "coingecko_trending_agent": {
                    "message": "Failed to retrieve trending coins from CoinGecko.",
                    "error": str(e)
                }
            }
        }

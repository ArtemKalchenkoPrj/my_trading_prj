from dotenv import load_dotenv
from langchain_core.documents import Document
import os

from tavily import TavilyClient

from my_trading_prj.state import GraphState

load_dotenv()

include_domains = [
    "investing.com",
    "coindesk.com",
    "cointelegraph.com",
    "reuters.com",
    "bloomberg.com",
    "binance.com"
]

def web_search(state: GraphState):
    coin = state['coin']
    existing_news = state.get("news")

    client = TavilyClient(os.getenv("TAVILY_API_KEY"))
    results = client.search(
        query=f"{coin} price impact news",
        include_answer="basic",
        max_results=3,
        start_date="2025-12-20",
        include_domains=include_domains
    )['results']

    documents = [
        Document(
            page_content=r["content"],
            metadata={
                "source": r.get("url"),
                "title": r.get("title"),
                "coin": coin,
            }
        )
        for r in results
    ]

    news = documents if existing_news is None else existing_news + documents

    return {
        "news": news
    }

if __name__ == "__main__":
    res = web_search(state={"coin": "BITCOIN", "news": None})
    print()
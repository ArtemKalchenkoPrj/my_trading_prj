from typing import Any, Dict

from dotenv import load_dotenv
from langchain_core.messages import Document
from langchain_tavily import TavilySearch

from my_trading_prj.state import GraphState, NewsItem

web_search_tool = TavilySearch(max_results=3)

include_domains = [
    "investing.com",
    "coindesk.com",
    "cointelegraph.com",
    "reuters.com",
    "bloomberg.com",
    "binance.com"
]

def web_search(GraphState):
    coin = GraphState.coin

    tavily_results = web_search_tool.invoke(
        {"query": f"{coin} breaking news",
         "include_domains": include_domains,
         "timeRange": "day"}
    )["results"]

    joined_tavily_result = "\n".join(
        [tavily_result["content"] for tavily_result in tavily_results]
    )
    web_results = Document(page_content=joined_tavily_result)

    news_item = NewsItem()
    news_item.content = web_results


    if news:= GraphState.news:
        news.append(NewsItem())

    return {}
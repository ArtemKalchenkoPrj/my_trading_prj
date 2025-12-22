from langchain_core.prompts import ChatPromptTemplate
from typing import Literal

from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from my_trading_prj.consts import *


class Route(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["news", "indicators"] = Field(
        ...,
        description="What the agent should do next"
    )

llm = ChatOllama(model=MODEL_TYPE,temperature=0,format='json')
structured_llm_router = llm.bind_tools([Route], tool_choice="any")


system = """
You are an expert trading agent.
Your task is to decide what information is missing to make a trading decision.

Rules:
- Choose 'news' if recent or impactful events may influence price.
- Choose 'indicators' if technical confirmation is needed.

Never choose randomly.
Do NOT repeat the same datasource if it was already used in the previous step,
unless new information is clearly required.

Also provide a short reason for your decision values.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human",
         """
         State summary:
         - News available: {has_news}
         - Indicators available: {has_indicators}

         Goal: Predict {coin} price in {timeframe}h.
         """
         ),
    ]
)
parser = RunnableLambda(lambda x: x.content_blocks[1]['args'])
routing_chain = prompt | structured_llm_router | parser

if __name__ == "__main__":
    res = routing_chain.invoke({"coin": "BTC-USD", "timeframe": 1,'has_indicators':False,'has_news':False})
    print(res)
    print("")
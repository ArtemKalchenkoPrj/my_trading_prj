from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from typing import Literal
from my_trading_prj.consts import *

class IndicatorType(BaseModel):
    """Route a user to most relevant indicators and says what size of window in needed"""

    name: Literal['volatility','trend'] = Field(
        ...,
        description='Indicator of what kind of indicator is needed',
    )
    window: int = Field(
        ...,
        description='Indicator of how many hours to look back',
        ge=3,
        le=20,
    )
    question_to_DB: str = Field(
        ...,
        description='The information that might be useful about chosen metric',
    )

llm = ChatOllama(model=MODEL_TYPE, temperature=0)
structured_llm_router = llm.bind_tools([IndicatorType], tool_choice="any")

system = """
You are an expert trading agent.
Your task is to decide what indicator is missing to make a trading decision.
And set window size - the amount of hours hor using it in the indicator functions.

Rules:
- Choose 'volatility' if think that user should check volatility of market.
- Choose 'trend' if information about current trend of price is needed.

Never choose randomly.
Do NOT repeat the same indicator if it was already used in the previous step,
unless new information is clearly required.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human",
         """
         State summary:
         - Coin: {coin}
         - Indicators have been used: {has_indicators} with windows {windows}:
         - Price prediction is needed in {timeframe} hours

         My goal:
         Using the available information choose what kind of indicators do I need

         What should the agent do next?
         Also provide a short reason for your chosen next move. And some query for searching relevant docs
         about metrics in data base. Data base contains information about simple moving average, exponential moving average, 
         bollinger bands and keltner channel
         """
         ),
    ]
)
parser = RunnableLambda(lambda x: x.content_blocks[1]['args'])
indicator_choose_chain = prompt | structured_llm_router | parser
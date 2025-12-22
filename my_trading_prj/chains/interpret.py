from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from my_trading_prj.consts import *


class Confidence(BaseModel):
    """Confidence of model about final move"""
    sell:float = Field (
        ...,
        ge=0.1, le=0.7,
        description="Confidence that user should sell coin",
    )
    buy:float = Field (
        ...,
        ge=0.1, le=0.7,
        description="Confidence that user should buy coin",
    )
    hold:float = Field (
        ...,
        ge=0.1, le=0.7,
        description="Confidence that user should hold coin",
    )

system = """You are an expert crypto trading assistant.
    Analyze the provided news, technical indicators, and background knowledge. 
    Return confidence values for BUY, SELL, and HOLD decisions.
    
    Rules:
    - Each confidence must be between 0.1 and 0.7
    - Sum of all confidences must be <= 1.0
    - Exactly one action must have confidence >= 0.5
    
    Also provide a short reason for your chosen confidence values."""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", """Coin: {coin}
     "Current balance: {current_balance}
     "Timeframe (hours): {timeframe}
     "News:\n{news}
     "Indicators: {indicators}
     "Background context:\n{DBcontext}
     """),
    ]
)
llm = ChatOllama(model=MODEL_TYPE,temperature=0)
structured_llm_confidence = llm.bind_tools([Confidence], tool_choice="any")

parser = RunnableLambda(lambda x: x.content_blocks[1]['args'])
interpretation_chain = prompt | structured_llm_confidence | parser


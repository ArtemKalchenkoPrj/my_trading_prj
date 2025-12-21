from langchain_core.prompts import ChatPromptTemplate
from typing import Literal
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

class Route(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["news", "indicators"] = Field(
        description="What the agent should do next"
    )
    reason: str = Field(
        description="Why this datasource was chosen"
    )

llm = ChatOllama(model="gpt-oss:20b",temperature=0)
structured_llm_router = llm.with_structured_output(Route)

system = """
You are an expert trading agent.
Your task is to decide what information is missing to make a trading decision.

Rules:
- Choose 'news' if recent or impactful events may influence price.
- Choose 'indicators' if technical confirmation is needed.

Never choose randomly.
Do NOT repeat the same datasource if it was already used in the previous step,
unless new information is clearly required.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human",
            """
Context:
- Asset: {coin}
- Timeframe: {timeframe}

State summary:
- News available: {has_news}
- Indicators available: {has_indicators}

User goal:
{question}

What should the agent do next?
"""
        ),
    ]
)
generation_chain = prompt | structured_llm_router
from typing import List, TypedDict, Literal
from langchain_core.documents import Document

class IndicatorSignal(TypedDict):
    """Indicator of the signal

    Attributes:
        name: name of the signal
        window: the amount of days for calculation
        value: value of the signal for last 10 hours
    """
    name: str
    window: int
    value: List[float]

class ActionConfidence(TypedDict):
    """Model confidence about last move of user

    Attributes:
        buy: confidence that price will fall
        sell: confidence that price will rise
        hold: confidence that price will be the same
    """
    buy: float
    sell: float
    hold: float

class IndicatorChoice(TypedDict):
    """The most relevant indicator at the moment

    Attributes:
        window: the amount of days for calculation
        name: name of the indicator type
    """

    window: int
    name: Literal["trend","volatility"]

class GraphState(TypedDict):
    """
    Represents the state of a graph state.

    Attributes:
        confidence: confidence in the next move
        news: relevant news
        indicators: relevant indicators
        DBcontext: relevant DB context
        coin: coin name
        timeframe: hours before final decision
        current_balance: amount of current balance
        last_price: price of the coin for previous 10 hours
        next_datasource: what datasource will be used next
    """
    window: int
    confidence: ActionConfidence
    news: List[Document]
    indicators: List[IndicatorSignal]
    DBcontext: List[str]
    coin: str
    timeframe: int
    current_balance: float
    last_price: IndicatorSignal
    next_indicator: IndicatorChoice
    next_datasource: Literal['news','indicators']
    question_to_DB: str
from typing import List, TypedDict

class NewsItem(TypedDict):
    content: str
    sentiment: float  # [-1, 1]

class IndicatorSignal(TypedDict):
    name: str
    timeframe: str
    value: float
    signal: str  # bullish / bearish / neutral

class ActionConfidence(TypedDict):
    buy: float
    sell: float
    hold: float

class GraphState(TypedDict):
    """
    Represents the state of a graph state.

    Attributes:
        confidence: confidence in the next move
        question: user provided question
        generation: generation by LLM
        news: relevant news
        indicators: relevant indicators
        DBcontext: relevant DB context
        coin: coin name
        timeframe: time before final decision, like 1h, 1d
    """
    confidence: ActionConfidence
    question: str
    generation: str
    news: List[NewsItem]
    indicators: List[IndicatorSignal]
    DBcontext: List[str]
    coin: str
    timeframe: str
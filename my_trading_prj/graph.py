from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import END, StateGraph
from my_trading_prj.consts import *

from my_trading_prj.nodes import (
    retrieve,
    choose_indicator,
    interpret,
    web_search,
    routing_node,
    calculate_trend,
    calculate_volatility)

from my_trading_prj.state import GraphState

def choose_next_indicator(state: GraphState):

    if state['next_indicator']['name'] == 'volatility':
        return VOLATILITY
    else:
        return TREND


def choose_next_datasource(state: GraphState):
    if state['next_datasource'] == "news":
        return NEWS_SIGNAL
    else:
        return GET_NEXT_INDICATOR

def is_max_confidence(state: GraphState):
    confidence = state['confidence']

    if any(v >= 1 for v in confidence.values()):
        return END
    else:
        return GET_NEXT_DATA_SOURCE

workflow = StateGraph(GraphState)

workflow.add_node(DB_CONTEXT,retrieve)
workflow.add_node(GET_NEXT_INDICATOR, choose_indicator)
workflow.add_node(INTERPRETER,interpret)
workflow.add_node(NEWS_SIGNAL,web_search)
workflow.add_node(GET_NEXT_DATA_SOURCE, routing_node)
workflow.add_node(TREND,calculate_trend)
workflow.add_node(VOLATILITY,calculate_volatility)

workflow.add_conditional_edges(
    GET_NEXT_DATA_SOURCE,
    choose_next_datasource,
    {
        NEWS_SIGNAL: NEWS_SIGNAL,
        GET_NEXT_INDICATOR: GET_NEXT_INDICATOR,
    }
)

workflow.add_conditional_edges(
    GET_NEXT_INDICATOR,
    choose_next_indicator,
    {
        VOLATILITY: VOLATILITY,
        TREND: TREND,
    }
)

workflow.add_conditional_edges(
    INTERPRETER,
    is_max_confidence,
    {
        GET_NEXT_DATA_SOURCE: GET_NEXT_DATA_SOURCE,
        END:END
    }
)

workflow.add_edge(
    GET_NEXT_INDICATOR, DB_CONTEXT,
)
workflow.add_edge(
    NEWS_SIGNAL, INTERPRETER,
)
workflow.add_edge(
    DB_CONTEXT, INTERPRETER,
)
workflow.add_edge(
    VOLATILITY, INTERPRETER,
)
workflow.add_edge(
    TREND, INTERPRETER,
)

workflow.set_entry_point(GET_NEXT_DATA_SOURCE)

app = workflow.compile()
app.get_graph().draw_mermaid_png(output_file_path="flow.png")
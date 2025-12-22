from my_trading_prj.chains.route import routing_chain
from my_trading_prj.state import GraphState


def routing_node(state: GraphState):
    if news:=state.get('news'):
        has_news = [n.metadata['title'] for n in news] #solve?
    else:
        has_news = False

    if state.get('indicators'):
        has_indicators = [i.get("name") for i in state['indicators']]
    else:
        has_indicators = False

    route = routing_chain.invoke(
        {
            "coin": state["coin"],
            "timeframe": state["timeframe"],
            "has_news": has_news,
            "has_indicators": has_indicators
        }
    )
    next_datasource = route['datasource']
    return {
        'next_datasource': next_datasource
    }

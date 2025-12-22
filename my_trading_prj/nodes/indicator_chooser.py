from my_trading_prj.chains.choose_indicator import indicator_choose_chain
from my_trading_prj.state import GraphState, IndicatorChoice

def choose_indicator(state: GraphState):
    if indicators := state.get('indicators'):
        has_indicators = [i.get("name") for i in indicators]
    else:
        has_indicators = False

    if indicators := state.get('indicators'):
        windows = [i.get("window") for i in indicators]
    else:
        windows = False

    next_indicator_predict = indicator_choose_chain.invoke({
        "coin": state["coin"],
        "timeframe": state["timeframe"],
        "news": state.get("news", "Not provided"),
        "indicators": state.get("indicators", "Not provided"),
        "has_indicators": has_indicators,
        "windows": windows
    })

    name = next_indicator_predict.get("name")
    window = next_indicator_predict.get("window")
    question = next_indicator_predict.get("question_to_DB")

    next_indicator = IndicatorChoice(
        name=name,
        window=window
    )
    return {"next_indicator":next_indicator,"question_to_DB":question}



from my_trading_prj.chains.interpret import interpretation_chain
from my_trading_prj.state import GraphState, ActionConfidence

def interpret(state: GraphState):

    new_conf = interpretation_chain.invoke(
        {
            "coin": state["coin"],
            "timeframe": state["timeframe"],
            "news": state.get("news","Not provided"),
            "indicators": state.get("indicators","Not provided"),
            "DBcontext":state.get("DBcontext","Not provided"),
            "current_balance": state.get("current_balance"),
        }
    )

    old_conf = state.get('confidence',{'buy':0,'sell':0,"hold":0})
    old_buy = old_conf['buy']
    old_sell = old_conf['sell']
    old_hold = old_conf['hold']

    new_buy = old_buy + new_conf['buy']
    new_sell = old_sell + new_conf['sell']
    new_hold = old_hold + new_conf['hold']

    result_confidence = ActionConfidence(
        buy=new_buy,sell=new_sell,hold=new_hold
    )
    return {"confidence":result_confidence}
from my_trading_prj.state import GraphState
from my_trading_prj.push_to_DB import retriever

def retrieve(state: GraphState):
    question = state["question_to_DB"]

    documents = retriever.invoke(question)

    return {"DBcontext": documents}
from typing import Dict, TypedDict
from langgraph.graph import StateGraph


class AgentState(TypedDict):
    question: str
    answer: str
    dialogue: str


def evaluate_node(state: AgentState) -> AgentState:
    """Simple node that evaluates user's answer"""

    state["evaluation"] = "evaluation"

    return state


graph = StateGraph(AgentState)

graph.add_node("evaluate", evaluate_node)

graph.set_entry_point("evaluate")
graph.set_finish_point("evaluate")

app = graph.compile()

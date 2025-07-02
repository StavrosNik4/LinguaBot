import random
from typing import Dict, TypedDict
from langgraph.graph import StateGraph

# Questions to ask
questions = [
    "Question 1: What's your name?",
    "Question 2: How old are you?",
    "Question 3: What's your favorite game?",
    "Question 4: Why do you like it?",
    "Question 5: Any final thoughts?"
]


class AgentState(TypedDict):
    question: str


def question_node(state: AgentState) -> AgentState:
    """Simple node that creates the question for the user"""

    state['question'] = questions[random.randint(0, 4)]

    return state


graph = StateGraph(AgentState)

graph.add_node("question", question_node)

graph.set_entry_point("question")
graph.set_finish_point("question")

app = graph.compile()

# result = app.invoke({}).get("question")

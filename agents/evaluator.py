from typing import Dict, TypedDict

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from dotenv import load_dotenv

load_dotenv()

llm_evaluator = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

evaluator_prompt = PromptTemplate.from_template(
    """You are an evaluator for Italian reading comprehension questions. You will receive the dialogue 
Read this Italian dialogue (with {topic} topic):
{dialogue}

then read the question of that it was given to the user: {question}

and finally read the user's answer: {answer}

The evaluation must:
- Be short.
- Be in English, but you can use Italian from the dialogue to demonstrate.
- Congratulate the user if the answer was correct and give them a 10/10 mark.
- Explain what the user did wrong, if they did.
- Have a mark between 0 and 10.

If the user's answer was not related to the dialogue material, then you have to give them a 0/10 mark and inform them.

IMPORTANT: that does not mean that the user must give the exact answer from the text. 
They can answer correctly with other use of words. Be aware of that before rejecting their answer.

Evaluation:"""
)


class AgentState(TypedDict):
    question: str
    topic: str
    answer: str
    dialogue: str
    evaluation: str


def evaluate_node(state: AgentState) -> AgentState:
    """Simple node that evaluates user's answer"""

    # state["evaluation"] = "evaluation"
    state["evaluation"] = llm_evaluator.invoke(evaluator_prompt.format(
                        dialogue=state["dialogue"],
                        topic=state["topic"],
                        question=state["question"],
                        answer=state["answer"])).content

    return state


graph = StateGraph(AgentState)

graph.add_node("evaluate", evaluate_node)

graph.set_entry_point("evaluate")
graph.set_finish_point("evaluate")

app = graph.compile()

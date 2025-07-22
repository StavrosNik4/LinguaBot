import random
from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph

load_dotenv()

# === LLM for dialogues generation ===
llm_generator = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
llm_questioner = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

# === Prompt Template ===
generation_prompt = PromptTemplate.from_template(
    """You are a dialogue generator for Italian reading material intended for reading comprehension tests.
You must create a medium size dialogue between 2 or more characters. You must only provide the dialogue,
not the characters or the topic, but you must specify who is talking by giving their name before their lines. Also, do 
not only produce default dialogues like 2 people meeting each other, there must be a topic. 

The dialogue must:
- Be in Italian only
- Be suitable for A1 level learners
- not have empty lines
- have 2 or more characters
- have this topic: {topic}

Dialogue:"""
)

topics = [
    "sports",
    "films",
    "every day life",
    "corporate",
    "at the restaurant",
    "shopping",
    "at the airport",
    "travel and holidays",
    "weather",
    "school and education",
    "at the doctor's",
    "family",
    "friends meeting",
    "hobbies",
    "ordering food",
    "making plans",
    "asking for directions",
    "public transport",
    "introducing oneself",
    "talking about the weekend",
    "daily routine",
    "going to the cinema",
    "describing your house",
    "talking about jobs",
    "at the supermarket"
]

question_prompt = PromptTemplate.from_template(
    """You are an examiner for Italian reading comprehension tests. 
Read this Italian dialogue (with {topic} topic) and create one comprehension question in Italian:
{dialogue}

The question must:
- Be in Italian only
- Not be a riddle or tricky question
- Be directly answerable from the dialogue
- Be suitable for A1 level learners

Question:"""
)


class AgentState(TypedDict):
    dialogue: str
    question: str
    topic: str


def dialogue_generation_node(state: AgentState) -> AgentState:
    """Node that creates a dialogue"""

    topic_index = random.randint(0, len(topics))
    topic = topics[topic_index]
    generated = llm_generator.invoke(generation_prompt.format(topic=topic)).content

    state["dialogue"] = generated.strip()
    state["topic"] = topic

    return state


def question_node(state: AgentState) -> AgentState:
    """Node that creates a question using relevant dialogue chunks from the retriever"""

    prompt = question_prompt.format(dialogue=state["dialogue"], topic=state["topic"])
    generated = llm_questioner.invoke(prompt).content

    state["question"] = generated.strip()
    return state


# === Graph construction ===
graph = StateGraph(AgentState)
graph.add_node("dialogue_gen", dialogue_generation_node)
graph.add_node("question_node", question_node)
graph.set_entry_point("dialogue_gen")
graph.add_edge("dialogue_gen", "question_node")
graph.set_finish_point("question_node")

app = graph.compile()

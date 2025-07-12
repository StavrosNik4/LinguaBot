import random
from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph

from tools.file_processing import save_multiple_dialogues_to_pdf

load_dotenv()

file_path = "../../dialogues/A1.pdf"

# === LLM for dialogues generation ===
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

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


class AgentState(TypedDict):
    dialogue: str
    topic: str


def dialogue_generation_node(state: AgentState) -> AgentState:
    """Node that creates a dialogue"""

    topic_index = random.randint(0, len(topics))
    topic = topics[topic_index]
    generated = llm.invoke(generation_prompt.format(topic=topic)).content

    state["dialogue"] = generated.strip()
    state["topic"] = topic

    return state


# === Graph construction ===
graph = StateGraph(AgentState)
graph.add_node("dialogue_gen", dialogue_generation_node)
graph.set_entry_point("dialogue_gen")
graph.set_finish_point("dialogue_gen")

app = graph.compile()

# === Loop N times to create N dialogues ===

all_dialogues = []
all_topics = []

for i in range(0, 5):
    result = app.invoke({})
    result_dialogue = result["dialogue"]
    result_topic = result["topic"]
    all_dialogues.append(result_dialogue)
    all_topics.append(result_topic)

# === Call the function to save the dialogue ===
save_multiple_dialogues_to_pdf(all_dialogues, all_topics, filename=file_path)

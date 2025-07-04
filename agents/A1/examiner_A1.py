import random
from typing import TypedDict

from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langgraph.graph import StateGraph

from tools.file_processing import chunk_by_dialogue

load_dotenv()

file_path = "../dialogues/A1.txt"

dialogue_chunks = chunk_by_dialogue(file_path)

docs = [Document(page_content=chunk) for chunk in dialogue_chunks]

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(docs, embedding_model)
retriever = vectorstore.as_retriever()

# === LLM for question generation ===
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# === Prompt Template ===
question_prompt = PromptTemplate.from_template(
    """You are an examiner for Italian reading comprehension tests. 
Read this Italian dialogue and create one comprehension question in Italian:
{dialogue}

The question must:
- Be in Italian only
- Not be a riddle or tricky question
- Be directly answerable from the dialogue
- Be suitable for A1 level learners

Question:"""
)


class AgentState(TypedDict):
    question: str


def question_node(state: AgentState) -> AgentState:
    """Simple node that creates a question for the user using the retriever of the Italian dialogues file"""

    chosen = random.choice(dialogue_chunks)

    prompt = question_prompt.format(dialogue=chosen)
    generated = llm.predict(prompt)

    # Save generated question
    state["question"] = generated.strip()

    return state


# === Graph construction ===
graph = StateGraph(AgentState)
graph.add_node("question", question_node)
graph.set_entry_point("question")
graph.set_finish_point("question")

app = graph.compile()

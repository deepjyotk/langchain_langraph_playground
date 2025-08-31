from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("placeholder", "{history}"),
    ("human", "{question}"),
])

# Base chain
chain = prompt | llm

# Memory store
history_store = {}

def get_history(session_id: str):
    if session_id not in history_store:
        history_store[session_id] = InMemoryChatMessageHistory()
    return history_store[session_id]

# Wrap with memory
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="question",
    history_messages_key="history",
)

session_id = "abc123"

# Interactions
resp1 = chain_with_memory.invoke(
    {"question": "Hello, who are you?"},
    config={"configurable": {"session_id": session_id}}
)
print(resp1.content)

resp2 = chain_with_memory.invoke(
    {"question": "Do you remember me?"},
    config={"configurable": {"session_id": session_id}}
)
print(resp2.content)

# 👀 Print conversation history
print("\n--- Conversation History ---")
for msg in get_history(session_id).messages:
    role = "User" if msg.type == "human" else "Assistant"
    print(f"{role}: {msg.content}")

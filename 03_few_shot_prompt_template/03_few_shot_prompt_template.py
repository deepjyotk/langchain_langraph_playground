from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate
)
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


# --------------------------
# 1. Base LLM
# --------------------------
llm = ChatOpenAI(model="gpt-4o-mini")

# --------------------------
# 2. Example QA pairs (for few-shot)
# --------------------------
examples = [
    {"question": "What is polymorphism in OOP?", "answer": "It allows objects of different classes to be treated through the same interface."},
    {"question": "What is encapsulation?", "answer": "It is bundling of data with the methods that operate on that data, restricting direct access."}
]

# --------------------------
# 3. Few-shot template
# --------------------------
example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{question}"),
    ("ai", "{answer}")
])
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples
)

# --------------------------
# 4. Main prompt with memory injection + few-shot
# --------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a study assistant. Explain concepts clearly with examples."),
    few_shot_prompt,                  # inject few-shot examples
    ("placeholder", "{history}"),     # memory slot
    ("human", "{question}")           # new user question
])

# --------------------------
# 5. Runnable with memory
# --------------------------
history_store = {}

def get_history(session_id: str):
    if session_id not in history_store:
        history_store[session_id] = InMemoryChatMessageHistory()
    return history_store[session_id]

chain = RunnableWithMessageHistory(
    prompt | llm,
    get_history,
    input_messages_key="question",
    history_messages_key="history",
)

# --------------------------
# 6. Run interactions
# --------------------------
session_id = "student1"

resp1 = chain.invoke({"question": "Can you explain inheritance in OOP?"},
                     config={"configurable": {"session_id": session_id}})
print("Answer 1:", resp1.content)

resp2 = chain.invoke({"question": "And how is it different from composition?"},
                     config={"configurable": {"session_id": session_id}})
print("Answer 2:", resp2.content)

# Print conversation history
print("\n--- Conversation History ---")
for msg in get_history(session_id).messages:
    role = "User" if msg.type == "human" else "Assistant"
    print(f"{role}: {msg.content}")

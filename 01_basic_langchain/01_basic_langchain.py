from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os


load_dotenv()


openai_api_key = os.getenv("OPENAI_API_KEY")

# 1. Model
llm = ChatOpenAI(model="gpt-4o-mini")

# 2. Prompt
prompt = ChatPromptTemplate.from_template(
    "You are a helpful assistant. Answer the question:\n{question}"
)

# 3. Runnable pipeline (Prompt → LLM)
chain = prompt | llm

# 4. Call it
resp = chain.invoke({"question": "What is LangChain?"})
print(resp.content)

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# --------------------------
# 1. Base LLM
# --------------------------
llm = ChatOpenAI(model="gpt-4o-mini")

# --------------------------
# 2. First chain → explain concept
# --------------------------
explain_prompt = ChatPromptTemplate.from_template(
    "Explain the concept of {topic} for a computer science student."
)
explain_chain = explain_prompt | llm | StrOutputParser()

# --------------------------
# 3. First chain → extract keywords
# --------------------------
keywords_prompt = ChatPromptTemplate.from_template(
    "List 3-5 important keywords related to {topic}, comma-separated."
)
keywords_chain = keywords_prompt | llm | StrOutputParser()

# --------------------------
# 4. Combine explanation + keywords into dict
# --------------------------
two_output_chain = RunnableLambda(
    lambda x: {
        "explanation": explain_chain.invoke(x),
        "keywords": keywords_chain.invoke(x)
    }
)

# --------------------------
# 5. Downstream chain consumes both keys
# --------------------------
quiz_prompt = ChatPromptTemplate.from_template(
    "Here is the explanation:\n{explanation}\n\n"
    "Important keywords: {keywords}\n\n"
    "Now create a multiple-choice quiz with 4 options. Highlight the correct one."
)
quiz_chain = quiz_prompt | llm | StrOutputParser()

# --------------------------
# 6. Full pipeline
# --------------------------
full_chain = two_output_chain | quiz_chain

# --------------------------
# 7. Run
# --------------------------
if __name__ == "__main__":
    topic = "polymorphism"

    # First, run two_output_chain to get dict
    # intermediate = two_output_chain.invoke({"topic": topic})

    # # Preview what quiz_prompt will look like
    # preview_messages = quiz_prompt.format_messages(**intermediate)

    # print("=== Final Prompt Sent to LLM ===")
    # for msg in preview_messages:
    #     print(f"{msg.type.upper()}: {msg.content}")
    #     print("-----")

    # Now run full chain
    result = full_chain.invoke({"topic": topic})

    print(f"\n=== Quiz on {topic} ===")
    print(result)

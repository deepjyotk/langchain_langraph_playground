# LangChain and LangGraph Playground

This repository contains examples demonstrating key concepts in LangChain and LangGraph.

## Examples

### Basic LangChain (`01_basic_langchain.py`)
Demonstrates the fundamental LangChain concept of creating a simple chain using a prompt template and LLM to process a single question.

### Memory Injection (`02_runnable_with_memory_injection.py`)
Shows how to implement conversation memory in LangChain using `RunnableWithMessageHistory` to maintain context across multiple interactions.

## Setup

1. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_key_here
```

2. Install dependencies using `uv`:
```bash
uv pip install langchain langchain-openai python-dotenv
```

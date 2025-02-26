from langchain_openai.llms import OpenAI

# Set up Cohere API key
import os
os.environ["OPENAI_API_KEY"] = f"OpenAI_API_KEY"

# Initialize LLM
llm = OpenAI(temperature=0)

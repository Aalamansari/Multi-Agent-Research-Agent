from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# main model/llm
llm = ChatOpenAI(model="gpt-6-luna", reasoning_effort="none", temperature=0)
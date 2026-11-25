from src.utils.nodes import create_analysts
from src.utils.states import GenerateAnalystsState
from langgraph.graph import START, END, StateGraph
from dotenv import load_dotenv

load_dotenv()

# create the graph
builder = StateGraph(GenerateAnalystsState)

# add the create_analysts nodes
builder.add_node("create_analysts", create_analysts)

# adding the edges
builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", END)

graph = builder.compile()
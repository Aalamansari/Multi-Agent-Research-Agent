from src.utils.nodes import create_analysts, human_feedback
from src.utils.states import GenerateAnalystsState
from langgraph.graph import START, END, StateGraph
from dotenv import load_dotenv
from src.utils.edges import should_continue

load_dotenv()

# create the graph
builder = StateGraph(GenerateAnalystsState)

# add the create_analysts nodes
builder.add_node("create_analysts", create_analysts)
builder.add_node("human_feedback", human_feedback)

# adding the edges
builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", "human_feedback")
builder.add_conditional_edges("human_feedback", should_continue)

graph = builder.compile()
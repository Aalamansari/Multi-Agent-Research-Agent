from dotenv import load_dotenv
from src.utils.states import GenerateAnalystsState, InterviewState
from src.utils.models import llm
from src.utils.objects import Perspectives, Analyst, SearchQuery
from src.utils.prompts import analyst_instructions, question_instructions, search_instructions
from langchain.messages import SystemMessage, HumanMessage
from langgraph.types import interrupt
from langchain_tavily import TavilySearch

load_dotenv()

#nodes

# create analyst node
def create_analysts(state: GenerateAnalystsState):
    """Create analysts"""

    topic = state["topic"]
    max_analysts = state["max_analysts"]
    human_analyst_feedback = state.get("human_analyst_feedback")

    # enforcing structured output
    structured_llm = llm.with_structured_output(Perspectives)

    # system_message
    system_message = analyst_instructions.format(topic = topic, 
                                                 human_analyst_feedback = human_analyst_feedback,
                                                 max_analysts = max_analysts
                                                )

    # generate analysts
    result = structured_llm.invoke([SystemMessage(content=system_message)] +
                                    [HumanMessage(content="Please generate the set of analysts.")])

    assert isinstance(result, Perspectives)
    return {"analysts": result.analysts}

# human feedback node
def human_feedback(state: GenerateAnalystsState):
    """this is where the human gives feedback about the analysts given"""

    feedback = interrupt({
        "question": "Are these analysts okay for you?",
        "analysts": [
            analyst.model_dump() if hasattr(analyst, "model_dump") else analyst 
                for analyst in state.get("analysts", [])
        ],
        "instructions": "Return feedback to regenerate analysts "
        "or return empty/perfect/continue/okay to approve and continue the graph"
    })

    if feedback is None:
        return {"human_analyst_feedback": None}

    if isinstance(feedback, str):
        feedback = feedback.strip()
   
        if feedback == "":
            return {"human_analyst_feedback": None}

        if feedback.lower() in {"perfect", "okay", "continue", "yes"}:
            return {"human_analyst_feedback": None} 

        return {"human_analyst_feedback": feedback}

    return {"human_analyst_feedback": None}

# question node
def generate_question(state: InterviewState):
    """node to generate questions"""

    # get state analyst
    analyst = state["analyst"]
    if isinstance(analyst, dict):
        analyst = Analyst.model_validate(analyst)

    messages = state["messages"]

    # generate question
    system_message = question_instructions.format(goals=analyst.persona)

    question = llm.invoke([SystemMessage(content=system_message)] + messages)

    return {"messages": [question]}

def search_web(state: InterviewState):
    """Retrieve documents from the web"""

    # search query
    structured_llm = llm.with_structured_output(SearchQuery)

    # search instruction
    search_instruction_system_message = SystemMessage(content=search_instructions)
    tavily_search = TavilySearch(max_results = 3)

    search_query = structured_llm.invoke([search_instruction_system_message] + state["messages"])

    # search the web
    data = tavily_search.invoke({
        "query": search_instruction_system_message
    })

    search_docs = data.get("results", data)

    # format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]}
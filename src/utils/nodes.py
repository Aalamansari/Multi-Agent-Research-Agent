from dotenv import load_dotenv
from src.utils.states import GenerateAnalystsState
from src.utils.models import llm
from src.utils.objects import Perspectives
from src.utils.prompts import analyst_instructions
from langchain.messages import SystemMessage, HumanMessage

load_dotenv()

#nodes
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
                                     [HumanMessage(content="Please generate the set of analysts.")]
                                    )

    assert isinstance(result, Perspectives)
    return {
        "analysts": result.analysts
    }
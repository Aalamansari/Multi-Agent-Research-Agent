from typing_extensions import TypedDict, NotRequired, Annotated
from typing import Optional, List
from src.utils.objects import Analyst
from langgraph.graph import MessagesState
import operator

class GenerateAnalystsState(TypedDict):
    topic: str # research topic
    max_analysts: int # number of analysts
    human_analyst_feedback: NotRequired[Optional[str]]
    analysts: NotRequired[List[Analyst]] # list of all our analysts

class InterviewState(MessagesState):
    max_num_turns: int # number of turns of questions
    context: Annotated[list, operator.add]
    analyst: Analyst # my analyst
    interview: str # interview transcript
    section: list # final key we duplicate in outer state for Send() api

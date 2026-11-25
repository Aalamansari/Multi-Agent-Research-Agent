from typing_extensions import TypedDict, NotRequired
from typing import Optional, List
from src.utils.objects import Analyst

class GenerateAnalystsState(TypedDict):
    topic: str # research topic
    max_analysts: int # number of analysts
    human_analyst_feedback: NotRequired[Optional[str]]
    analysts: NotRequired[List[Analyst]] # list of all our analysts
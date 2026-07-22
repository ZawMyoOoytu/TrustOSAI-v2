from pydantic import BaseModel
from typing import List



class DecisionReasoning(BaseModel):

    execution_id:int

    decision:str

    reasoning:List[str]

    actions:List[str]

    confidence:float
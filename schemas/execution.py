from datetime import datetime

from typing import Optional, Any


from pydantic import BaseModel





class ExecuteRequest(BaseModel):

    task:str





class ExecutionResponse(BaseModel):


    execution_id:int


    task:str


    agent:Optional[str]


    trust_score:float


    risk_score:float


    conflict_score:float


    decision:str


    result:Optional[str]


    quality_score:float


    latency_ms:float


    created_at:datetime



    class Config:

        from_attributes=True
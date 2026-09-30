from pydantic import BaseModel



class ExecutionResponse(BaseModel):

    id: int

    task: str

    agent: str

    trust_score: float

    risk_score: float

    governance_result: str


    class Config:

        from_attributes = True
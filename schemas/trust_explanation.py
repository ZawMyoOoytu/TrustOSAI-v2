from pydantic import BaseModel
from typing import List


class TrustFactor(BaseModel):
    name: str
    score: float
    weight: float
    contribution: float
    description: str



class TrustExplanation(BaseModel):
    execution_id: int
    final_score: float
    level: str
    factors: List[TrustFactor]
    recommendation: str
from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict
)





# =====================================================
# CREATE MEMORY
# =====================================================


class MemoryCreate(BaseModel):


    agent_id:int


    execution_id:int | None = None


    memory_type:str = "EXECUTION"


    content:str


    importance_score:float = 0.5






# =====================================================
# MEMORY RESPONSE
# =====================================================


class MemoryResponse(BaseModel):


    id:int


    agent_id:int


    execution_id:int | None


    memory_type:str


    content:str


    importance_score:float


    access_count:int


    created_at:datetime


    updated_at:datetime



    model_config = ConfigDict(

        from_attributes=True

    )
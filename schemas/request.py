from pydantic import BaseModel



class ExecutionRequest(BaseModel):

    task: str
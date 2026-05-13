from pydantic import BaseModel, Field


class WorkflowRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=200)
    audience: str = Field(default="通用用户", max_length=200)
    goal: str = Field(default="提升转化", max_length=200)


class WorkflowResponse(BaseModel):
    task_id: int
    status: str
    result: dict

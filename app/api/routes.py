from fastapi import APIRouter, HTTPException

from app.core.db import create_task, get_task, list_tasks, update_task
from app.schemas import WorkflowRequest, WorkflowResponse
from app.workflows.marketing import MarketingWorkflow

router = APIRouter()
workflow = MarketingWorkflow()


@router.post("/api/run", response_model=WorkflowResponse)
async def run_workflow(payload: WorkflowRequest):
    task_id = create_task(payload.topic, payload.audience, payload.goal)
    try:
        result = await workflow.execute(payload.topic, payload.audience, payload.goal)
        update_task(task_id, "done", result)
        return WorkflowResponse(task_id=task_id, status="done", result=result)
    except Exception as exc:
        update_task(task_id, "failed", {"error": str(exc)})
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tasks")
def get_tasks():
    return {"items": list_tasks()}


@router.get("/api/tasks/{task_id}")
def get_task_detail(task_id: int):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

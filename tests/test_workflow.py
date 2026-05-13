import asyncio

from app.workflows.marketing import MarketingWorkflow


def test_workflow_executes():
    async def _run():
        wf = MarketingWorkflow()
        result = await wf.execute("新品发布", "开发者", "提升预约")
        assert result["topic"] == "新品发布"
        assert "planner" in result["agents"]
        assert "report" in result["agents"]

    asyncio.run(_run())

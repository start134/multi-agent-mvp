from __future__ import annotations

from dataclasses import asdict

from app.agents.planner import PlannerAgent
from app.agents.content import ContentAgent
from app.agents.review import ReviewAgent
from app.agents.data import DataAgent
from app.agents.report import ReportAgent


class MarketingWorkflow:
    def __init__(self) -> None:
        self.planner = PlannerAgent()
        self.content = ContentAgent()
        self.review = ReviewAgent()
        self.data = DataAgent()
        self.report = ReportAgent()

    async def execute(self, topic: str, audience: str, goal: str) -> dict:
        planner_out = await self.planner.run(
            f"主题：{topic}\n受众：{audience}\n目标：{goal}\n请输出 5 步执行计划。"
        )
        content_out = await self.content.run(
            f"根据以下计划生成可用于运营发布的内容：\n{planner_out.output}"
        )
        review_out = await self.review.run(
            f"请审查以下内容的质量、风险和可改进点：\n{content_out.output}"
        )
        data_out = await self.data.run(
            f"请给出基于该项目的核心运营指标建议：\n主题：{topic}\n目标：{goal}"
        )
        report_out = await self.report.run(
            "请把下面的信息整理成一份简洁的运营汇总报告：\n"
            f"【计划】\n{planner_out.output}\n\n"
            f"【内容】\n{content_out.output}\n\n"
            f"【审核】\n{review_out.output}\n\n"
            f"【数据】\n{data_out.output}"
        )
        return {
            "topic": topic,
            "audience": audience,
            "goal": goal,
            "agents": {
                "planner": asdict(planner_out),
                "content": asdict(content_out),
                "review": asdict(review_out),
                "data": asdict(data_out),
                "report": asdict(report_out),
            },
        }

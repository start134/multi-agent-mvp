from app.agents.base import BaseAgent


class ReportAgent(BaseAgent):
    name = "ReportAgent"
    system_prompt = "You are the Report Agent for a multi-agent automation system."

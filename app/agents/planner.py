from app.agents.base import BaseAgent


class PlannerAgent(BaseAgent):
    name = "PlannerAgent"
    system_prompt = "You are the Planner Agent for a multi-agent automation system."

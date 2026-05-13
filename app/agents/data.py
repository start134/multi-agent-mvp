from app.agents.base import BaseAgent


class DataAgent(BaseAgent):
    name = "DataAgent"
    system_prompt = "You are the Data Agent for a multi-agent automation system."

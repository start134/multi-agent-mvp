from app.agents.base import BaseAgent


class ContentAgent(BaseAgent):
    name = "ContentAgent"
    system_prompt = "You are the Content Agent for a multi-agent automation system."

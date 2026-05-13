from app.agents.base import BaseAgent


class ReviewAgent(BaseAgent):
    name = "ReviewAgent"
    system_prompt = "You are the Review Agent for a multi-agent automation system."

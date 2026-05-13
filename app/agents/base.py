from __future__ import annotations

from dataclasses import dataclass
from app.core.llm import get_llm


@dataclass
class AgentOutput:
    agent: str
    mode: str
    output: str


class BaseAgent:
    name = "BaseAgent"
    system_prompt = "You are a helpful agent."

    def __init__(self) -> None:
        self.llm = get_llm()

    async def run(self, user_prompt: str) -> AgentOutput:
        result = await self.llm.generate(self.system_prompt, user_prompt)
        return AgentOutput(agent=self.name, mode=result.mode, output=result.text)

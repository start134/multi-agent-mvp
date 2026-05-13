from __future__ import annotations

import re
from dataclasses import dataclass

from app.core.config import settings

try:
    from openai import AsyncOpenAI
except Exception:  # pragma: no cover
    AsyncOpenAI = None


@dataclass
class LLMResult:
    text: str
    mode: str


class MockLLM:
    async def generate(self, system: str, user: str) -> LLMResult:
        topic = self._extract_topic(user)
        low = system.lower()
        if "planner" in low:
            text = (
                f"1. 明确 {topic} 的目标与受众\n"
                f"2. 设计核心信息与内容结构\n"
                f"3. 制定渠道投放与执行节奏\n"
                f"4. 安排审核与优化反馈\n"
                f"5. 输出日报和复盘结论"
            )
        elif "content" in low:
            text = (
                f"【标题】{topic} 的高转化运营文案\n"
                f"【正文】围绕 {topic} 输出卖点、场景、行动号召。\n"
                f"【CTA】立即查看详情 / 预约体验 / 联系我们"
            )
        elif "review" in low:
            text = (
                "内容整体可用，建议补充：\n"
                "- 更明确的目标用户画像\n"
                "- 加入可量化指标\n"
                "- CTA 再具体一些"
            )
        elif "data" in low:
            text = (
                "建议关注以下指标：\n"
                "- 曝光率\n"
                "- 点击率\n"
                "- 转化率\n"
                "- 留资成本\n"
                "- 次日留存"
            )
        else:
            text = (
                f"该项目围绕 {topic} 构建了一个多 Agent 协同工作流，"
                "能够完成规划、生成、审核、分析与报告汇总。"
            )
        return LLMResult(text=text, mode="mock")

    def _extract_topic(self, text: str) -> str:
        m = re.search(r"主题[:：]\s*(.+)", text)
        if m:
            return m.group(1).strip()
        m = re.search(r"为\s*(.+?)\s*制定", text)
        if m:
            return m.group(1).strip()
        return "运营任务"


class OpenAILLM:
    def __init__(self) -> None:
        if AsyncOpenAI is None:
            raise RuntimeError("openai package is not available")
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    async def generate(self, system: str, user: str) -> LLMResult:
        resp = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.5,
        )
        text = resp.choices[0].message.content or ""
        return LLMResult(text=text.strip(), mode="openai")


def get_llm():
    try:
        return OpenAILLM()
    except Exception:
        return MockLLM()

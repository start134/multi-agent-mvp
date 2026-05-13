# Multi-Agent Automation MVP

一个可以直接放到 GitHub 的多 Agent 协同运营自动化系统 MVP。

## 功能

- Planner Agent：拆解任务
- Content Agent：生成运营内容
- Review Agent：审查风险与质量
- Data Agent：给出数据分析与指标建议
- Report Agent：汇总成可展示的运营报告
- FastAPI 后端
- SQLite 持久化
- 简单 Web Dashboard
- OpenAI 可选接入，未配置时自动进入 mock 模式

## 本地运行

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

打开浏览器访问：

- http://127.0.0.1:8000

## API

### 运行工作流

`POST /api/run`

示例：

```bash
curl -X POST "http://127.0.0.1:8000/api/run" \
  -H "Content-Type: application/json" \
  -d '{"topic":"新品上线推广","audience":"独立开发者","goal":"提升预约转化"}'
```

### 查询任务列表

`GET /api/tasks`

### 查询单个任务

`GET /api/tasks/{task_id}`

## OpenAI 模式

如果在 `.env` 中填写了 `OPENAI_API_KEY`，系统会自动调用 OpenAI。  
如果没有填写，系统会使用内置 mock 生成器，仍然可以完整运行和演示。

## 适合写进简历的描述

> 我搭建了一个多 Agent 协同运营自动化 MVP，包含任务规划、内容生成、质量审核、数据分析与报告汇总等 Agent，通过 FastAPI 提供统一接口，并使用 SQLite 进行任务持久化。系统支持 OpenAI 在线推理和离线 mock 两种模式，已形成可直接部署演示的端到端工作流。

## 目录

```text
app/
  api/
  agents/
  core/
  workflows/
templates/
static/
tests/
```

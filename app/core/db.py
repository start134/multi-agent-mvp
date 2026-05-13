import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.core.config import settings

def _sqlite_path() -> Path:
    db_url = settings.database_url
    if db_url.startswith("sqlite:///"):
        return Path(db_url.replace("sqlite:///", "", 1))
    return Path("./data/agent_mvp.db")

DB_PATH = _sqlite_path()
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                audience TEXT,
                goal TEXT,
                status TEXT NOT NULL,
                result_json TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()

def create_task(topic: str, audience: str, goal: str) -> int:
    created_at = datetime.now(timezone.utc).isoformat()
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO tasks (topic, audience, goal, status, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (topic, audience, goal, "running", created_at),
        )
        conn.commit()
        return int(cur.lastrowid)

def update_task(task_id: int, status: str, result: dict[str, Any] | None = None) -> None:
    payload = json.dumps(result, ensure_ascii=False) if result is not None else None
    with get_conn() as conn:
        conn.execute(
            "UPDATE tasks SET status = ?, result_json = ? WHERE id = ?",
            (status, payload, task_id),
        )
        conn.commit()

def list_tasks() -> list[dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, topic, audience, goal, status, result_json, created_at FROM tasks ORDER BY id DESC"
        ).fetchall()
    return [dict(row) for row in rows]

def get_task(task_id: int) -> dict[str, Any] | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, topic, audience, goal, status, result_json, created_at FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()
    return dict(row) if row else None

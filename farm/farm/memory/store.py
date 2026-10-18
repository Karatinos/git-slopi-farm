"""SQLite-backed data layer.

The blueprint's reference stack is Postgres + Redis + MinIO + pgvector, but it
also says explicitly: do not over-engineer at small scale. SQLite closes every
role for a single-host farm and keeps the whole thing to one file, while the
DAO surface below is written so a Postgres backend can drop in later without
touching callers.

WAL mode is enabled so the parallel ensemble workers can read/write
concurrently without locking each other out.
"""
from __future__ import annotations

import json
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from ..config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id            TEXT PRIMARY KEY,
    name          TEXT NOT NULL,
    category      TEXT NOT NULL,
    path          TEXT NOT NULL,
    points        INTEGER DEFAULT 100,
    difficulty    TEXT DEFAULT 'unknown',
    p_solve       REAL DEFAULT 0.5,
    flag_format   TEXT DEFAULT '',
    description   TEXT DEFAULT '',
    status        TEXT DEFAULT 'new',       -- new|triaged|solving|solved|failed
    created_at    REAL
);

-- Gold answers are kept in a SEPARATE table and are NEVER handed to an agent.
CREATE TABLE IF NOT EXISTS gold_flags (
    task_id       TEXT,
    flag          TEXT,
    source        TEXT,                     -- e.g. 'writeup:...'
    PRIMARY KEY (task_id, flag)
);

CREATE TABLE IF NOT EXISTS attempts (
    id            TEXT PRIMARY KEY,
    task_id       TEXT NOT NULL,
    trace_id      TEXT,
    strategy      TEXT,                     -- temperature/angle label
    tier_path     TEXT,                     -- e.g. 'flash' or 'flash->pro'
    steps         INTEGER DEFAULT 0,
    tokens        INTEGER DEFAULT 0,
    cost_usd      REAL DEFAULT 0.0,
    outcome       TEXT,                     -- solved|failed|stalled|killed|error
    flag          TEXT,
    started_at    REAL,
    ended_at      REAL
);

-- Blackboard: shared, reusable findings across parallel attempts of a task.
CREATE TABLE IF NOT EXISTS findings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id       TEXT NOT NULL,
    kind          TEXT,                     -- artifact|hypothesis|credential|partial_flag|note
    content       TEXT,
    author        TEXT,
    ts            REAL
);

-- Negative memory: dead ends, so the swarm does not repeat them.
CREATE TABLE IF NOT EXISTS negative_memory (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id       TEXT NOT NULL,
    approach      TEXT,
    reason        TEXT,
    ts            REAL
);

-- Solution bank (RAG): reusable templates mined from successful trajectories.
CREATE TABLE IF NOT EXISTS solutions (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id       TEXT,
    category      TEXT,
    title         TEXT,
    summary       TEXT,
    template      TEXT,
    vector        TEXT,                     -- JSON list[float]
    ts            REAL
);

CREATE TABLE IF NOT EXISTS runs (
    id            TEXT PRIMARY KEY,
    label         TEXT,
    provider      TEXT,
    started_at    REAL,
    ended_at      REAL,
    summary       TEXT                      -- JSON metrics blob
);

CREATE INDEX IF NOT EXISTS ix_findings_task ON findings(task_id);
CREATE INDEX IF NOT EXISTS ix_attempts_task ON attempts(task_id);
CREATE INDEX IF NOT EXISTS ix_solutions_cat ON solutions(category);
"""


class Store:
    def __init__(self, path: Path = DB_PATH):
        self.path = Path(path)
        self._local = threading.local()
        with self._conn() as c:
            c.executescript(SCHEMA)

    def _conn(self) -> sqlite3.Connection:
        conn = getattr(self._local, "conn", None)
        if conn is None:
            conn = sqlite3.connect(self.path, timeout=30, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA busy_timeout=30000;")
            conn.execute("PRAGMA foreign_keys=ON;")
            self._local.conn = conn
        return conn

    # -- generic helpers --------------------------------------------------- #
    def execute(self, sql: str, params: Iterable = ()) -> sqlite3.Cursor:
        c = self._conn()
        cur = c.execute(sql, tuple(params))
        c.commit()
        return cur

    def query(self, sql: str, params: Iterable = ()) -> List[sqlite3.Row]:
        return self._conn().execute(sql, tuple(params)).fetchall()

    def query_one(self, sql: str, params: Iterable = ()) -> Optional[sqlite3.Row]:
        return self._conn().execute(sql, tuple(params)).fetchone()

    # -- tasks ------------------------------------------------------------- #
    def upsert_task(self, task: Dict[str, Any]) -> None:
        cols = ["id", "name", "category", "path", "points", "difficulty",
                "p_solve", "flag_format", "description", "status", "created_at"]
        task = {**task}
        task.setdefault("created_at", time.time())
        task.setdefault("status", "new")
        placeholders = ",".join("?" for _ in cols)
        updates = ",".join(f"{c}=excluded.{c}" for c in cols if c != "id")
        self.execute(
            f"INSERT INTO tasks ({','.join(cols)}) VALUES ({placeholders}) "
            f"ON CONFLICT(id) DO UPDATE SET {updates}",
            [task.get(c) for c in cols],
        )

    def set_task_status(self, task_id: str, status: str) -> None:
        self.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))

    def update_task_triage(self, task_id: str, category: str, difficulty: str,
                           p_solve: float) -> None:
        self.execute(
            "UPDATE tasks SET category=?, difficulty=?, p_solve=?, status='triaged' "
            "WHERE id=?", (category, difficulty, p_solve, task_id))

    def get_task(self, task_id: str) -> Optional[sqlite3.Row]:
        return self.query_one("SELECT * FROM tasks WHERE id=?", (task_id,))

    def list_tasks(self, status: Optional[str] = None) -> List[sqlite3.Row]:
        if status:
            return self.query("SELECT * FROM tasks WHERE status=? ORDER BY category, name",
                              (status,))
        return self.query("SELECT * FROM tasks ORDER BY category, name")

    # -- gold flags (evaluation only) ------------------------------------- #
    def add_gold_flag(self, task_id: str, flag: str, source: str = "") -> None:
        self.execute(
            "INSERT OR IGNORE INTO gold_flags (task_id, flag, source) VALUES (?,?,?)",
            (task_id, flag, source))

    def gold_flags(self, task_id: str) -> List[str]:
        return [r["flag"] for r in
                self.query("SELECT flag FROM gold_flags WHERE task_id=?", (task_id,))]

    # -- attempts ---------------------------------------------------------- #
    def record_attempt(self, a: Dict[str, Any]) -> None:
        cols = ["id", "task_id", "trace_id", "strategy", "tier_path", "steps",
                "tokens", "cost_usd", "outcome", "flag", "started_at", "ended_at"]
        placeholders = ",".join("?" for _ in cols)
        self.execute(
            f"INSERT OR REPLACE INTO attempts ({','.join(cols)}) VALUES ({placeholders})",
            [a.get(c) for c in cols])

    def attempts_for(self, task_id: str) -> List[sqlite3.Row]:
        return self.query("SELECT * FROM attempts WHERE task_id=? ORDER BY started_at",
                          (task_id,))

    # -- runs -------------------------------------------------------------- #
    def record_run(self, run_id: str, label: str, provider: str,
                   started_at: float, ended_at: float, summary: dict) -> None:
        self.execute(
            "INSERT OR REPLACE INTO runs (id,label,provider,started_at,ended_at,summary) "
            "VALUES (?,?,?,?,?,?)",
            (run_id, label, provider, started_at, ended_at,
             json.dumps(summary, ensure_ascii=False)))

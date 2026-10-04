import sqlite3
import datetime
from pathlib import Path

DB_PATH = Path("history.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            cpu REAL NOT NULL,
            ram REAL NOT NULL,
            disk REAL NOT NULL
        )"""
    )
    conn.commit()
    conn.close()


def insert_record(cpu: float, ram: float, disk: float):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO history (timestamp, cpu, ram, disk) VALUES (?, ?, ?, ?)",
        (datetime.datetime.now().isoformat(), cpu, ram, disk),
    )
    conn.commit()
    conn.close()


def fetch_history(limit: int = None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if limit:
        cur.execute("SELECT timestamp, cpu, ram, disk FROM history ORDER BY id DESC LIMIT ?", (limit,))
    else:
        cur.execute("SELECT timestamp, cpu, ram, disk FROM history ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    return rows

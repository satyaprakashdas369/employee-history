import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "employee_history.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_id TEXT UNIQUE NOT NULL,
            role_id TEXT NOT NULL,
            role_title TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            city TEXT NOT NULL,
            linkedin TEXT,
            highest_qualification TEXT NOT NULL,
            institution TEXT NOT NULL,
            graduation_year TEXT NOT NULL,
            education_details TEXT,
            experience TEXT,
            skills TEXT,
            projects TEXT,
            career_goals TEXT,
            availability TEXT,
            resume_filename TEXT NOT NULL,
            resume_path TEXT NOT NULL,
            consent INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()


def save_application(data):
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    with get_connection() as conn:
        conn.execute(f"INSERT INTO applications ({columns}) VALUES ({placeholders})", tuple(data.values()))
        conn.commit()


def list_applications():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM applications ORDER BY id DESC").fetchall()


def get_application(applicant_id):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM applications WHERE applicant_id = ?", (applicant_id,)).fetchone()

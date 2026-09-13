import json
import os
import sys

from core.models import Habit, Log

# Resolve data directory relative to this file's location
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(_BASE_DIR, "data")
HABITS_FILE = os.path.join(DATA_DIR, "habits.json")
LOGS_FILE = os.path.join(DATA_DIR, "logs.json")


def _ensure_data_dir():
    """Create data/ directory and empty JSON files if they don't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    for filepath in (HABITS_FILE, LOGS_FILE):
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                json.dump([], f)


def _read_json(filepath: str) -> list:
    """Read and return a JSON list from a file. Returns [] if file is empty."""
    _ensure_data_dir()
    try:
        with open(filepath, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        print(
            f"Error: Could not parse {filepath}. The file may be corrupted.",
            file=sys.stderr,
        )
        sys.exit(1)


def _write_json(filepath: str, data: list):
    """Write a list as pretty-printed JSON to a file."""
    _ensure_data_dir()
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


# ── Habits ────────────────────────────────────────────────────────────────────

def load_habits() -> list[Habit]:
    """Load all habits from habits.json."""
    raw = _read_json(HABITS_FILE)
    return [Habit.from_dict(item) for item in raw]


def save_habits(habits: list[Habit]):
    """Save the full habits list to habits.json."""
    _write_json(HABITS_FILE, [h.to_dict() for h in habits])


# ── Logs ──────────────────────────────────────────────────────────────────────

def load_logs() -> list[Log]:
    """Load all logs from logs.json."""
    raw = _read_json(LOGS_FILE)
    return [Log.from_dict(item) for item in raw]


def save_logs(logs: list[Log]):
    """Save the full logs list to logs.json."""
    _write_json(LOGS_FILE, [l.to_dict() for l in logs])


def get_log(habit_id: str, date: str) -> Log | None:
    """Return the log entry for a specific habit and date, or None if not found."""
    logs = load_logs()
    for log in logs:
        if log.habit_id == habit_id and log.date == date:
            return log
    return None


def add_log(log: Log):
    """Append a new log entry and save to logs.json."""
    logs = load_logs()
    logs.append(log)
    save_logs(logs)

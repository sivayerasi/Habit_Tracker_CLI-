from core.storage import load_habits, load_logs
from utils.display import print_streak_table


def run():
    """View streaks for all habits."""
    habits = load_habits()
    logs = load_logs()
    print_streak_table(habits, logs)

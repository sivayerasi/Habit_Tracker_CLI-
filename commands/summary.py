from core.storage import load_habits, load_logs
from utils.display import print_weekly_summary


def run():
    """Show the weekly summary."""
    habits = load_habits()
    logs = load_logs()
    print_weekly_summary(habits, logs)

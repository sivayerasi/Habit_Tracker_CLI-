from core.storage import load_habits, load_logs
from utils.date_utils import today
from utils.display import print_status_table


def run():
    """Show today's status for all habits."""
    habits = load_habits()
    logs = load_logs()
    print_status_table(habits, logs, today())

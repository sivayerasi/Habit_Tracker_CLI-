from core.storage import load_habits, load_logs
from utils.date_utils import last_n_days
from utils.display import print_history_table


def run(name: str, last: int = 30):
    """Show day-wise history for a specific habit."""
    habits = load_habits()

    if not habits:
        print("No habits yet. Use 'habit add' to create one.")
        return

    # Find habit by name (case-insensitive)
    habit = None
    for h in habits:
        if h.name.lower() == name.lower():
            habit = h
            break

    if not habit:
        print(f"Error: Habit \"{name}\" not found.")
        print("\nAvailable habits:")
        for i, h in enumerate(habits, start=1):
            print(f"  [{i}] {h.name}")
        return

    logs = load_logs()
    dates = last_n_days(last)

    print(f"\n  Showing last {last} days for: {habit.name}")
    print_history_table(habit, dates, logs)

from core.models import Log
from core.storage import load_habits, load_logs, get_log, add_log, save_logs
from utils.date_utils import today, parse_date, is_future_date
from utils.display import print_habit_list


def _find_habit_by_name(habits, name):
    """Find a habit by exact or case-insensitive name match."""
    for h in habits:
        if h.name.lower() == name.lower():
            return h
    return None


def _log_single(habit, date_str: str, status: str):
    """Log a single habit if not already logged. Returns True if logged."""
    existing = get_log(habit.id, date_str)
    if existing:
        print(f"⚠️  \"{habit.name}\" already logged for {date_str} ({existing.status}) — skipped.")
        return False

    add_log(Log(habit_id=habit.id, date=date_str, status=status))
    action = "logged" if status == "done" else "marked as skipped"
    print(f"✅ \"{habit.name}\" {action} for {date_str}.")
    return True


def run(name: str = None, log_all: bool = False, date_str: str = None, skip: bool = False):
    """Log one or all habits as done or skipped."""
    habits = load_habits()

    if not habits:
        print("No habits yet. Use 'habit add' to create one.")
        return

    # Resolve and validate date
    if date_str:
        try:
            date_str = parse_date(date_str)
        except ValueError as e:
            print(f"Error: {e}")
            return
        if is_future_date(date_str):
            print("Error: Cannot log for a future date.")
            return
    else:
        date_str = today()

    status = "skipped" if skip else "done"

    # ── Log all habits ─────────────────────────────────────────────────────────
    if log_all:
        try:
            confirm = input(
                f"Log all {len(habits)} habits as {status} for {date_str}? (y/n): "
            ).strip().lower()
        except EOFError:
            confirm = "n"

        if confirm != "y":
            print("Cancelled.")
            return

        logged = 0
        skipped = 0
        for habit in habits:
            if _log_single(habit, date_str, status):
                logged += 1
            else:
                skipped += 1

        print(f"\n  {logged} habit(s) logged, {skipped} skipped (already logged).")
        return

    # ── Log by name passed directly ────────────────────────────────────────────
    if name:
        habit = _find_habit_by_name(habits, name)
        if not habit:
            print(f"Error: Habit \"{name}\" not found.")
            print("\nAvailable habits:")
            print_habit_list(habits)
            return
        _log_single(habit, date_str, status)
        return

    # ── Interactive picker ─────────────────────────────────────────────────────
    print_habit_list(habits)

    try:
        choice = input("Enter habit number, name, or 'all': ").strip()
    except EOFError:
        print("Cancelled.")
        return

    if choice.lower() == "all":
        # Delegate to log-all flow
        run(log_all=True, date_str=date_str, skip=skip)
        return

    # Try as number
    try:
        index = int(choice) - 1
        if index < 0 or index >= len(habits):
            print(f"Invalid selection. Please enter a number between 1 and {len(habits)}.")
            return
        habit = habits[index]
    except ValueError:
        # Try as name
        habit = _find_habit_by_name(habits, choice)
        if not habit:
            print(f"Error: Habit \"{choice}\" not found.")
            return

    _log_single(habit, date_str, status)

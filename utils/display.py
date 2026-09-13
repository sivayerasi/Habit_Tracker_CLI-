from core.models import Habit, Log
from core.streak_engine import get_current_streak, get_longest_streak
from utils.date_utils import today, last_n_days, get_day_name

# ── Status symbols ─────────────────────────────────────────────────────────────
DONE    = "✅"
MISSED  = "❌"
SKIPPED = "⏭️ "
PENDING = "⏳"

# ── Helpers ───────────────────────────────────────────────────────────────────

def _separator(width: int = 50) -> str:
    return "─" * width


def _status_symbol(status: str | None) -> str:
    if status == "done":
        return DONE
    if status == "skipped":
        return SKIPPED
    if status == "pending":
        return PENDING
    return MISSED


def _build_log_map(logs: list[Log]) -> dict[tuple, str]:
    """Build a {(habit_id, date): status} lookup map."""
    return {(log.habit_id, log.date): log.status for log in logs}


# ── Print functions ───────────────────────────────────────────────────────────

def print_habit_list(habits: list[Habit]):
    """Print a numbered list of all habits."""
    if not habits:
        print("No habits yet. Use 'habit add' to create one.")
        return

    print(_separator())
    print(f"  {'#':<4} {'Name':<25} {'Description'}")
    print(_separator())
    for i, habit in enumerate(habits, start=1):
        desc = habit.description if habit.description else "—"
        print(f"  [{i}]  {habit.name:<25} {desc}")
    print(_separator())


def print_status_table(habits: list[Habit], logs: list[Log], date: str = None):
    """Print today's status for all habits."""
    if date is None:
        date = today()

    log_map = _build_log_map(logs)

    print(f"\n  Today — {date}")
    print(_separator())
    print(f"  {'#':<4} {'Habit':<25} Status")
    print(_separator())

    if not habits:
        print("  No habits yet. Use 'habit add' to create one.")
    else:
        for i, habit in enumerate(habits, start=1):
            status = log_map.get((habit.id, date))
            if status == "done":
                label = f"{DONE}  Done"
            elif status == "skipped":
                label = f"{SKIPPED} Skipped"
            else:
                label = f"{PENDING}  Pending"
            print(f"  [{i}]  {habit.name:<25} {label}")

    print(_separator())
    print()


def print_history_table(habit: Habit, dates: list[str], logs: list[Log]):
    """Print a day-wise history table for a single habit (newest first)."""
    log_map = {log.date: log.status for log in logs if log.habit_id == habit.id}

    print(f"\n  History for: {habit.name}")
    print(_separator())
    print(f"  {'Date':<15} {'Day':<6} Status")
    print(_separator())

    for date_str in reversed(dates):
        status = log_map.get(date_str)
        day   = get_day_name(date_str)
        if status == "done":
            label = f"{DONE}  Done"
        elif status == "skipped":
            label = f"{SKIPPED} Skipped"
        else:
            label = f"{MISSED}  Missed"
        print(f"  {date_str:<15} {day:<6} {label}")

    print(_separator())
    print()


def print_streak_table(habits: list[Habit], logs: list[Log]):
    """Print current and longest streak for each habit."""
    if not habits:
        print("No habits yet. Use 'habit add' to create one.")
        return

    print(f"\n  {'Habit':<25} {'Current Streak':<18} Longest Streak")
    print(_separator(60))

    for habit in habits:
        current = get_current_streak(habit.id, logs)
        longest = get_longest_streak(habit.id, logs)

        cur_label = f"{current} day{'s' if current != 1 else ''}"
        lng_label = f"{longest} day{'s' if longest != 1 else ''}"

        # Highlight streaks > 7 days
        streak_flag = " 🔥" if current > 7 else ""
        print(f"  {habit.name:<25} {cur_label:<18} {lng_label}{streak_flag}")

    print(_separator(60))
    print()


def print_weekly_summary(habits: list[Habit], logs: list[Log]):
    """Print a 7-day completion grid with rates, best and worst day."""
    if not habits:
        print("No habits yet. Use 'habit add' to create one.")
        return

    dates = last_n_days(7)
    day_names = [get_day_name(d) for d in dates]
    log_map = _build_log_map(logs)

    # Header
    day_col_width = 5
    habit_col_width = 22
    header_days = "  ".join(f"{d:<{day_col_width}}" for d in day_names)
    print(f"\n  Weekly Summary  ({dates[0]}  →  {dates[-1]})")
    print(_separator(70))
    print(f"  {'Habit':<{habit_col_width}}  {header_days}  Rate")
    print(_separator(70))

    day_totals = [0] * 7  # completions per day column

    for habit in habits:
        row_symbols = []
        done_count = 0

        for col, date_str in enumerate(dates):
            status = log_map.get((habit.id, date_str))
            if status == "done":
                row_symbols.append(DONE)
                done_count += 1
                day_totals[col] += 1
            elif status == "skipped":
                row_symbols.append("⏭️ ")
            else:
                row_symbols.append(MISSED)

        rate = int((done_count / 7) * 100)
        row_str = "  ".join(f"{s:<{day_col_width}}" for s in row_symbols)
        print(f"  {habit.name:<{habit_col_width}}  {row_str}  {rate}%")

    print(_separator(70))

    # Best / worst day
    max_total = max(day_totals)
    min_total = min(day_totals)
    best_days  = [day_names[i] for i, v in enumerate(day_totals) if v == max_total]
    worst_days = [day_names[i] for i, v in enumerate(day_totals) if v == min_total]

    print(f"\n  Best day:  {', '.join(best_days)}   |   Worst day: {', '.join(worst_days)}")
    print()

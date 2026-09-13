from datetime import date, datetime, timedelta

from core.models import Log

DATE_FORMAT = "%Y-%m-%d"


def _to_date(date_str: str) -> date:
    return datetime.strptime(date_str, DATE_FORMAT).date()


def _build_log_map(habit_id: str, logs: list[Log]) -> dict[str, str]:
    """
    Build a {date_str: status} map for a specific habit.
    Only includes 'done' and 'skipped' entries (missed = not present).
    """
    return {
        log.date: log.status
        for log in logs
        if log.habit_id == habit_id
    }


def get_current_streak(habit_id: str, logs: list[Log]) -> int:
    """
    Return the current streak (consecutive 'done' days going back from today).

    Rules:
    - Count consecutive 'done' days walking backwards from today
    - 'skipped' days are transparent — they neither count nor break the streak
    - First 'missed' day (no entry) stops the streak
    - If today is not logged yet, start checking from yesterday
    """
    log_map = _build_log_map(habit_id, logs)
    if not log_map:
        return 0

    streak = 0
    current = date.today()

    # If today has no entry yet, start from yesterday so pending today
    # doesn't immediately break an active streak
    if current.strftime(DATE_FORMAT) not in log_map:
        current -= timedelta(days=1)

    while True:
        date_str = current.strftime(DATE_FORMAT)
        status = log_map.get(date_str)

        if status == "done":
            streak += 1
        elif status == "skipped":
            pass  # transparent — keep walking back
        else:
            # missed or no record before habit existed
            break

        current -= timedelta(days=1)

    return streak


def get_longest_streak(habit_id: str, logs: list[Log]) -> int:
    """
    Return the longest streak ever recorded for a habit.

    Rules:
    - Scan all logged dates in chronological order
    - Count consecutive 'done' days (skipped days are transparent)
    - Track the maximum run seen
    """
    log_map = _build_log_map(habit_id, logs)
    if not log_map:
        return 0

    # Get all dates with any entry, sorted oldest to newest
    all_dates = sorted(log_map.keys())
    if not all_dates:
        return 0

    # Walk day by day from first log date to today
    start = _to_date(all_dates[0])
    end = date.today()

    longest = 0
    current_run = 0
    current = start

    while current <= end:
        date_str = current.strftime(DATE_FORMAT)
        status = log_map.get(date_str)

        if status == "done":
            current_run += 1
            longest = max(longest, current_run)
        elif status == "skipped":
            pass  # transparent — don't reset run
        else:
            # missed — reset current run
            current_run = 0

        current += timedelta(days=1)

    return longest

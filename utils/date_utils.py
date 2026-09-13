from datetime import date, datetime, timedelta


DATE_FORMAT = "%Y-%m-%d"


def today() -> str:
    """Return today's date as a YYYY-MM-DD string."""
    return date.today().strftime(DATE_FORMAT)


def parse_date(s: str) -> str:
    """
    Validate and return a date string in YYYY-MM-DD format.
    Raises ValueError if the format is invalid.
    """
    try:
        datetime.strptime(s, DATE_FORMAT)
        return s
    except ValueError:
        raise ValueError(f"Invalid date format '{s}'. Expected YYYY-MM-DD (e.g. 2026-09-13).")


def date_range(start: str, end: str) -> list[str]:
    """
    Return a list of date strings from start to end (inclusive),
    ordered from oldest to newest.
    """
    start_dt = datetime.strptime(start, DATE_FORMAT).date()
    end_dt = datetime.strptime(end, DATE_FORMAT).date()

    if start_dt > end_dt:
        return []

    dates = []
    current = start_dt
    while current <= end_dt:
        dates.append(current.strftime(DATE_FORMAT))
        current += timedelta(days=1)
    return dates


def last_n_days(n: int) -> list[str]:
    """
    Return a list of the last N date strings including today,
    ordered from oldest to newest.
    """
    end_dt = date.today()
    start_dt = end_dt - timedelta(days=n - 1)
    dates = []
    current = start_dt
    while current <= end_dt:
        dates.append(current.strftime(DATE_FORMAT))
        current += timedelta(days=1)
    return dates


def is_future_date(date_str: str) -> bool:
    """Return True if the given date string is in the future."""
    return datetime.strptime(date_str, DATE_FORMAT).date() > date.today()


def get_day_name(date_str: str) -> str:
    """Return the abbreviated weekday name for a date string (e.g. 'Mon')."""
    return datetime.strptime(date_str, DATE_FORMAT).strftime("%a")

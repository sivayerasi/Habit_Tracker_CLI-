# Habit Tracker CLI — Design Document

---

## 1. Project Structure

```
Habit Tracker/
├── habit.py               # Entry point — parses CLI arguments and routes commands
├── commands/
│   ├── __init__.py
│   ├── add.py             # habit add
│   ├── delete.py          # habit delete
│   ├── edit.py            # habit edit
│   ├── list.py            # habit list
│   ├── log.py             # habit log
│   ├── status.py          # habit status
│   ├── streak.py          # habit streak
│   ├── summary.py         # habit summary
│   └── history.py         # habit history
├── core/
│   ├── __init__.py
│   ├── storage.py         # Read/write habits.json and logs.json
│   ├── models.py          # Habit and Log data classes
│   └── streak_engine.py   # Streak calculation logic
├── utils/
│   ├── __init__.py
│   ├── display.py         # Terminal output formatting helpers
│   └── date_utils.py      # Date parsing and range helpers
├── data/
│   ├── habits.json        # Persisted habit definitions
│   └── logs.json          # Persisted daily log entries
├── requirements.md
└── design.md
```

---

## 2. Data Models

### Habit
Represents a single tracked habit.

```python
@dataclass
class Habit:
    id: str           # UUID (auto-generated)
    name: str         # Habit name e.g. "Drink Water"
    description: str  # Optional description, default ""
    created_at: str   # ISO date string e.g. "2026-09-01"
```

### Log
Represents a single day's entry for a habit.

```python
@dataclass
class Log:
    habit_id: str   # References Habit.id
    date: str       # ISO date string e.g. "2026-09-13"
    status: str     # "done" | "skipped"
```

If no Log entry exists for a habit on a given date, that date is treated as **missed**.

---

## 3. JSON Storage Schema

### `data/habits.json`
```json
[
  {
    "id": "a1b2c3d4",
    "name": "Drink Water",
    "description": "Drink 8 glasses of water",
    "created_at": "2026-09-01"
  },
  {
    "id": "e5f6g7h8",
    "name": "Exercise",
    "description": "",
    "created_at": "2026-09-01"
  }
]
```

### `data/logs.json`
```json
[
  { "habit_id": "a1b2c3d4", "date": "2026-09-13", "status": "done" },
  { "habit_id": "a1b2c3d4", "date": "2026-09-12", "status": "done" },
  { "habit_id": "a1b2c3d4", "date": "2026-09-10", "status": "skipped" },
  { "habit_id": "e5f6g7h8", "date": "2026-09-13", "status": "done" }
]
```

---

## 4. Module Responsibilities

### `habit.py` — Entry Point
- Uses `argparse` to define all subcommands and flags
- Maps each subcommand to its handler in `commands/`
- Initialises storage (creates `data/` and empty JSON files if they don't exist)

### `core/storage.py` — Storage Layer
- `load_habits() -> list[Habit]` — reads and parses `habits.json`
- `save_habits(habits: list[Habit])` — writes habits back to `habits.json`
- `load_logs() -> list[Log]` — reads and parses `logs.json`
- `save_logs(logs: list[Log])` — writes logs back to `logs.json`
- `get_log(habit_id, date) -> Log | None` — fetch a single log entry
- `add_log(log: Log)` — append a log entry and save

### `core/models.py` — Data Classes
- Defines `Habit` and `Log` as Python `dataclasses`
- Provides `to_dict()` and `from_dict()` methods for JSON serialisation

### `core/streak_engine.py` — Streak Logic
- `get_current_streak(habit_id, logs) -> int`
  - Walk backwards from today
  - Count consecutive `done` days
  - Stop at first `missed` day (skip over `skipped` days)
- `get_longest_streak(habit_id, logs) -> int`
  - Scan entire log history
  - Track max consecutive `done` run (ignoring `skipped`)

### `utils/display.py` — Output Formatting
- `print_habit_list(habits)` — numbered list of habits
- `print_status_table(habits, logs, date)` — today's status table
- `print_history_table(habit, logs)` — day-wise history table
- `print_streak_table(habits, logs)` — streak overview table
- `print_weekly_summary(habits, logs)` — weekly grid with completion rates
- Centralised emoji/symbol constants: `DONE = "✅"`, `MISSED = "❌"`, `SKIPPED = "⏭️ "`, `PENDING = "⏳"`

### `utils/date_utils.py` — Date Helpers
- `today() -> str` — returns today as `YYYY-MM-DD`
- `date_range(start, end) -> list[str]` — list of date strings between two dates
- `last_n_days(n) -> list[str]` — last N days including today
- `parse_date(s) -> str` — validates and parses a date string input

---

## 5. Command Flows

### `habit add "Drink Water" -d "8 glasses"`
1. Parse name and optional description from args
2. Check if a habit with the same name already exists → warn and exit if so
3. Generate a new UUID for the habit
4. Append to `habits.json`
5. Print confirmation

### `habit delete`
1. Load and display numbered habit list
2. Prompt: `Enter habit number to delete:`
3. Remove habit from `habits.json`
4. Remove all logs for that habit from `logs.json`
5. Print confirmation

### `habit edit`
1. Load and display numbered habit list
2. Prompt: `Enter habit number to edit:`
3. Show current name and description
4. Prompt for new name (press Enter to keep current)
5. Prompt for new description (press Enter to keep current)
6. Save updated habit
7. Print confirmation

### `habit list`
1. Load all habits
2. Print numbered table with name, description, and created date

### `habit log` (interactive)
1. Load and display all habits with index numbers
2. Prompt: `Enter habit number, name, or 'all':`
3. If a specific habit is selected:
   - Check if already logged today → warn and skip if so
   - Append `done` log entry for today
   - Print confirmation
4. If `all` is entered → same as `habit log --all`

### `habit log --all`
1. Load all habits
2. Confirm: `Log all N habits as done for YYYY-MM-DD? (y/n):`
3. For each habit:
   - If already logged today → print warning and skip
   - Else → append `done` log entry
4. Print summary of how many were logged vs skipped

### `habit log "Drink Water" --date 2026-09-12`
1. Validate the provided date (cannot be in the future)
2. Check if already logged for that date → warn and exit if so
3. Append log entry with the given date
4. Print confirmation

### `habit log "Drink Water" --skip`
1. Check if already logged today → warn and exit if so
2. Append `skipped` log entry for today
3. Print confirmation

### `habit status`
1. Load all habits and today's logs
2. Print table: habit name + status (Done / Skipped / Pending)

### `habit streak`
1. Load all habits and all logs
2. For each habit, compute current streak and longest streak via `streak_engine`
3. Print streak table

### `habit summary`
1. Compute date range for last 7 days
2. Load all habits and logs within that range
3. For each habit, build a 7-column row (Mon–Sun) with status symbols
4. Calculate completion rate per habit
5. Calculate total completions per day → find best and worst day
6. Print summary table

### `habit history "Drink Water" --last 30`
1. Find the habit by name
2. Compute date range for last N days (default 30)
3. For each date in range, look up log status (done / skipped / missed)
4. Print day-wise table newest first

---

## 6. Argument Parser Structure (`argparse`)

```
habit
├── add       <name> [-d <description>]
├── delete
├── edit
├── list
├── log       [name] [--all] [--date YYYY-MM-DD] [--skip]
├── status
├── streak
├── summary
└── history   <name> [--last N]
```

---

## 7. Error Handling

| Scenario                                      | Behaviour                                      |
|-----------------------------------------------|------------------------------------------------|
| No habits exist yet                           | Print friendly message, suggest `habit add`    |
| Habit name not found                          | Print error with list of existing habits       |
| Already logged today                          | Print warning, skip silently (no crash)        |
| Future date passed to `--date`                | Print error, reject the entry                  |
| Invalid date format                           | Print error with expected format               |
| Duplicate habit name on `add`                 | Print warning, do not add duplicate            |
| Empty `habits.json` or `logs.json`            | Treat as empty list, do not crash              |
| Corrupted JSON file                           | Print error and exit with a clear message      |

---

## 8. Output Conventions

- All tables use plain ASCII separators (`─`) for compatibility
- Emoji status symbols used for readability:
  - `✅` Done
  - `❌` Missed
  - `⏭️` Skipped
  - `⏳` Pending (not yet logged today)
- Dates always displayed as `YYYY-MM-DD`
- Confirmation prompts always `(y/n)` defaulting to `n`
- All output goes to `stdout`; errors go to `stderr`

---

## 9. File Initialisation

On every run, `habit.py` checks:
- If `data/` directory does not exist → create it
- If `data/habits.json` does not exist → create with empty list `[]`
- If `data/logs.json` does not exist → create with empty list `[]`

This ensures a clean first-run experience with no manual setup.

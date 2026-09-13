# Habit Tracker CLI — Task List

## Overview
Tasks are grouped by phase and ordered by dependency.
Each task references the relevant module from `design.md`.

**Status legend:** `[ ]` To Do — `[x]` Done — `[-]` In Progress

---

## Phase 1 — Project Setup

- [ ] **TASK-01** Create the project folder structure
  - Create `commands/`, `core/`, `utils/`, `data/` directories
  - Create all `__init__.py` files
  - Create empty placeholder files: `habit.py`, all `commands/*.py`, all `core/*.py`, all `utils/*.py`

- [ ] **TASK-02** Create empty JSON data files
  - Create `data/habits.json` with content `[]`
  - Create `data/logs.json` with content `[]`

---

## Phase 2 — Core Layer

- [ ] **TASK-03** Implement `core/models.py` — Data Classes
  - Define `Habit` dataclass with fields: `id`, `name`, `description`, `created_at`
  - Define `Log` dataclass with fields: `habit_id`, `date`, `status`
  - Implement `to_dict()` on both classes for JSON serialisation
  - Implement `from_dict()` class methods on both classes for deserialisation
  - Validate `status` field — must be `"done"` or `"skipped"`

- [ ] **TASK-04** Implement `core/storage.py` — Storage Layer
  - Implement `load_habits() -> list[Habit]`
  - Implement `save_habits(habits: list[Habit])`
  - Implement `load_logs() -> list[Log]`
  - Implement `save_logs(logs: list[Log])`
  - Implement `get_log(habit_id, date) -> Log | None`
  - Implement `add_log(log: Log)` — append and save
  - Handle missing or empty JSON files gracefully (return empty list)
  - Handle corrupted JSON — print error to stderr and exit

- [ ] **TASK-05** Implement `utils/date_utils.py` — Date Helpers
  - Implement `today() -> str` — returns `YYYY-MM-DD`
  - Implement `date_range(start: str, end: str) -> list[str]`
  - Implement `last_n_days(n: int) -> list[str]` — includes today
  - Implement `parse_date(s: str) -> str` — validates format, raises ValueError on bad input

- [ ] **TASK-06** Implement `core/streak_engine.py` — Streak Logic
  - Implement `get_current_streak(habit_id: str, logs: list[Log]) -> int`
    - Walk backwards from today
    - Count consecutive `done` days
    - `skipped` days are transparent (neither count nor break streak)
    - Stop at first `missed` day
  - Implement `get_longest_streak(habit_id: str, logs: list[Log]) -> int`
    - Scan entire log history
    - Track max consecutive `done` run
    - `skipped` days are transparent

- [ ] **TASK-07** Implement `utils/display.py` — Output Formatting
  - Define emoji constants: `DONE`, `MISSED`, `SKIPPED`, `PENDING`
  - Implement `print_habit_list(habits: list[Habit])` — numbered list
  - Implement `print_status_table(habits, logs, date)` — today's status
  - Implement `print_history_table(habit, dates, logs)` — day-wise history
  - Implement `print_streak_table(habits, logs)` — streak overview
  - Implement `print_weekly_summary(habits, logs)` — 7-day grid with rates

---

## Phase 3 — Entry Point & Argument Parser

- [ ] **TASK-08** Implement `habit.py` — Entry Point
  - Set up `argparse` with all subcommands:
    - `add <name> [-d <description>]`
    - `delete`
    - `edit`
    - `list`
    - `log [name] [--all] [--date YYYY-MM-DD] [--skip]`
    - `status`
    - `streak`
    - `summary`
    - `history <name> [--last N]`
  - Auto-initialise `data/` directory and JSON files if they don't exist
  - Route each subcommand to its handler in `commands/`
  - Print help if no subcommand is provided

---

## Phase 4 — Commands

- [ ] **TASK-09** Implement `commands/add.py`
  - Accept `name` (required) and `description` (optional, default `""`)
  - Check for duplicate habit name → warn and exit if found
  - Generate UUID for new habit
  - Save to `habits.json`
  - Print: `✅ Habit "Drink Water" added.`

- [ ] **TASK-10** Implement `commands/list.py`
  - Load all habits
  - If none exist → print: `No habits yet. Use 'habit add' to create one.`
  - Print numbered table: index, name, description, created date

- [ ] **TASK-11** Implement `commands/delete.py`
  - Load and display numbered habit list
  - Prompt: `Enter habit number to delete:`
  - Validate input is a valid number in range
  - Confirm: `Delete "Drink Water"? (y/n):`
  - Remove habit from `habits.json`
  - Remove all associated logs from `logs.json`
  - Print: `🗑️  Habit "Drink Water" deleted.`

- [ ] **TASK-12** Implement `commands/edit.py`
  - Load and display numbered habit list
  - Prompt: `Enter habit number to edit:`
  - Show current name and description
  - Prompt for new name (Enter to keep current)
  - Prompt for new description (Enter to keep current)
  - Save updated habit
  - Print: `✏️  Habit updated.`

- [ ] **TASK-13** Implement `commands/log.py`
  - **Interactive mode** (no args):
    - Display numbered habit list
    - Prompt: `Enter habit number, name, or 'all':`
    - If valid habit selected → log as `done` for today
    - If `all` typed → delegate to log-all flow
  - **`--all` flag**:
    - Confirm: `Log all N habits as done for YYYY-MM-DD? (y/n):`
    - Loop through all habits, skip already-logged ones with warning
    - Print summary: `3 habits logged, 1 skipped (already done)`
  - **`--date YYYY-MM-DD`**:
    - Validate date is not in the future
    - Check not already logged for that date
    - Log for the given date
  - **`--skip` flag**:
    - Log status as `skipped` instead of `done`
  - If already logged today → print warning and skip without error

- [ ] **TASK-14** Implement `commands/status.py`
  - Load all habits and today's logs
  - If no habits → suggest `habit add`
  - Print table with today's date as header
  - Each row: index, habit name, status (`✅ Done` / `⏭️ Skipped` / `⏳ Pending`)

- [ ] **TASK-15** Implement `commands/streak.py`
  - Load all habits and all logs
  - For each habit compute current streak and longest streak via `streak_engine`
  - Print streak table: habit name, current streak, longest streak
  - Highlight habits with streak > 7 days

- [ ] **TASK-16** Implement `commands/summary.py`
  - Compute last 7 days date range
  - Load all habits and logs in that range
  - Build weekly grid: one row per habit, columns = Mon–Sun
  - Calculate completion rate per habit (done days / 7)
  - Calculate per-day totals → identify best and worst day
  - Print formatted summary table
  - Print: `Best day: Monday | Worst day: Wednesday`

- [ ] **TASK-17** Implement `commands/history.py`
  - Accept `name` (required) and `--last N` (optional, default 30)
  - Find habit by name → error if not found, show available habits
  - Compute date range for last N days
  - For each date: look up log status (`done` / `skipped` / `missed`)
  - Print day-wise table newest first
  - Print: `Showing last 30 days for: Drink Water`

---

## Phase 5 — Error Handling & Edge Cases

- [ ] **TASK-18** Add input validation across all commands
  - Invalid habit number input → `Invalid selection. Please enter a number.`
  - Habit name not found → `Habit "X" not found.` + show list
  - Future date on `--date` → `Cannot log for a future date.`
  - Invalid date format → `Invalid date format. Use YYYY-MM-DD.`
  - Already logged today → `⚠️  Already logged today — skipped.`
  - Duplicate habit name on add → `⚠️  A habit named "X" already exists.`

- [ ] **TASK-19** Handle empty state gracefully
  - `habit list` with no habits → friendly message
  - `habit log` with no habits → friendly message
  - `habit status` with no habits → friendly message
  - `habit streak` with no habits → friendly message
  - `habit summary` with no habits → friendly message
  - `habit history` with no logs yet → show all dates as `❌ Missed`

---

## Phase 6 — Testing

- [ ] **TASK-20** Test `core/models.py`
  - `to_dict()` and `from_dict()` round-trip
  - Invalid status value handling

- [ ] **TASK-21** Test `core/storage.py`
  - Load from missing file → returns empty list
  - Save and reload round-trip
  - `get_log()` returns correct entry or None
  - `add_log()` appends correctly

- [ ] **TASK-22** Test `utils/date_utils.py`
  - `today()` returns correct format
  - `date_range()` returns inclusive range
  - `last_n_days()` includes today and correct count
  - `parse_date()` rejects invalid formats

- [ ] **TASK-23** Test `core/streak_engine.py`
  - Current streak with all `done` days
  - Current streak resets on `missed` day
  - `skipped` days are transparent
  - Longest streak is tracked across history
  - Empty log history → streak = 0

- [ ] **TASK-24** Integration test — full command flows
  - Add → List → Log → Status → Streak → Summary → History → Delete
  - Log `--all` with mix of already-logged and pending habits
  - Log `--skip` then verify streak is not broken
  - Log `--date` for a past date then verify history

---

## Phase 7 — Final Polish

- [ ] **TASK-25** Add `--help` text to all commands and flags
  - Each subcommand should have a clear description
  - Each flag should have a usage example in its help text

- [ ] **TASK-26** Update `README.md`
  - Installation instructions (Python version required)
  - Usage examples for all commands
  - Sample output screenshots/text
  - Project structure overview

---

## Task Summary

| Phase | Tasks        | Count |
|-------|--------------|-------|
| 1     | Project Setup | 2    |
| 2     | Core Layer    | 5    |
| 3     | Entry Point   | 1    |
| 4     | Commands      | 9    |
| 5     | Error Handling| 2    |
| 6     | Testing       | 5    |
| 7     | Final Polish  | 2    |
| **Total** |           | **26** |

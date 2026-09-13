# Habit Tracker CLI

A lightweight Command Line Interface (CLI) habit tracker built with Python.
Track your daily habits, view streaks, and get weekly summaries — all from your terminal.

---

## Requirements

- Python 3.10 or higher
- No third-party packages — uses Python standard library only

---

## Installation

```bash
# Clone or download the project
cd "Habit Tracker"

# Run directly
python3 habit.py <command>
```

Optionally make it executable and add an alias:

```bash
chmod +x habit.py
alias habit="python3 /path/to/Habit\ Tracker/habit.py"
```

---

## Project Structure

```
Habit Tracker/
├── habit.py               # Entry point
├── commands/              # One file per CLI command
│   ├── add.py
│   ├── delete.py
│   ├── edit.py
│   ├── list.py
│   ├── log.py
│   ├── status.py
│   ├── streak.py
│   ├── summary.py
│   └── history.py
├── core/                  # Business logic
│   ├── models.py          # Habit and Log data classes
│   ├── storage.py         # JSON read/write layer
│   └── streak_engine.py   # Streak calculation logic
├── utils/                 # Helpers
│   ├── display.py         # Terminal output formatters
│   └── date_utils.py      # Date parsing and range helpers
├── data/                  # Auto-created on first run
│   ├── habits.json
│   └── logs.json
├── requirements.md
├── design.md
└── tasks.md
```

---

## Commands

### Add a habit
```bash
python3 habit.py add "Drink Water"
python3 habit.py add "Drink Water" -d "8 glasses a day"
```

### List all habits
```bash
python3 habit.py list
```
```
──────────────────────────────────────────────────
  #    Name                      Description
──────────────────────────────────────────────────
  [1]  Drink Water               8 glasses a day
  [2]  Exercise                  30 mins
  [3]  Read 30 mins              —
──────────────────────────────────────────────────
```

### Log a habit
```bash
# Interactive picker — shows all habits, pick by number or name
python3 habit.py log

# Log all habits at once
python3 habit.py log --all

# Log a specific habit by name
python3 habit.py log "Drink Water"

# Log for a past date
python3 habit.py log "Drink Water" --date 2026-09-12

# Mark a habit as skipped
python3 habit.py log "Drink Water" --skip
```

Interactive log example:
```
──────────────────────────────────────────────────
  #    Name                      Description
──────────────────────────────────────────────────
  [1]  Drink Water               8 glasses a day
  [2]  Exercise                  30 mins
  [3]  Read 30 mins              —
──────────────────────────────────────────────────
Enter habit number, name, or 'all': 1
✅ "Drink Water" logged for 2026-09-13.
```

### Today's status
```bash
python3 habit.py status
```
```
  Today — 2026-09-13
──────────────────────────────────────────────────
  #    Habit                     Status
──────────────────────────────────────────────────
  [1]  Drink Water               ✅  Done
  [2]  Exercise                  ⏭️  Skipped
  [3]  Read 30 mins              ⏳  Pending
──────────────────────────────────────────────────
```

### View streaks
```bash
python3 habit.py streak
```
```
  Habit                     Current Streak     Longest Streak
────────────────────────────────────────────────────────────
  Drink Water               5 days             12 days
  Exercise                  2 days             7 days
  Read 30 mins              30 days            30 days 🔥
────────────────────────────────────────────────────────────
```

### Weekly summary
```bash
python3 habit.py summary
```
```
  Weekly Summary  (2026-09-07  →  2026-09-13)
──────────────────────────────────────────────────────────────────────
  Habit                   Mon    Tue    Wed    Thu    Fri    Sat    Sun    Rate
──────────────────────────────────────────────────────────────────────
  Drink Water             ✅      ✅      ❌      ✅      ✅      ✅      ✅      86%
  Exercise                ✅      ❌      ❌      ✅      ✅      ❌      ✅      57%
  Read 30 mins            ✅      ✅      ✅      ✅      ✅      ✅      ✅      100%
──────────────────────────────────────────────────────────────────────

  Best day:  Mon   |   Worst day: Wed
```

### View history
```bash
# Last 30 days (default)
python3 habit.py history "Drink Water"

# Last N days
python3 habit.py history "Drink Water" --last 7
```
```
  Showing last 7 days for: Drink Water

  History for: Drink Water
──────────────────────────────────────────────────
  Date            Day    Status
──────────────────────────────────────────────────
  2026-09-13      Sun    ✅  Done
  2026-09-12      Sat    ✅  Done
  2026-09-11      Fri    ⏭️  Skipped
  2026-09-10      Thu    ✅  Done
  2026-09-09      Wed    ❌  Missed
  2026-09-08      Tue    ✅  Done
  2026-09-07      Mon    ✅  Done
──────────────────────────────────────────────────
```

### Edit a habit
```bash
python3 habit.py edit
# Shows numbered list, pick by number, then update name/description interactively
```

### Delete a habit
```bash
python3 habit.py delete
# Shows numbered list, pick by number, confirms before deleting
```

---

## Streak Rules

- **Done** days count toward and build the streak
- **Skipped** days are transparent — they neither build nor break the streak
- **Missed** days (no entry) reset the streak to 0
- Streaks of more than 7 days are highlighted with 🔥

---

## Data Storage

All data is stored locally as JSON files in the `data/` directory:

- `data/habits.json` — habit definitions
- `data/logs.json` — daily log entries

Both files are human-readable and can be manually edited if needed.
The `data/` directory and files are created automatically on first run.

---

## Help

```bash
python3 habit.py --help
python3 habit.py <command> --help
```

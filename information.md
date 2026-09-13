# Habit Tracker CLI — Project Information

> A simple guide to understand the whole project.
> Written in plain words so anyone can follow along.

---

## 1. What Does This Project Do?

This is a **Command Line Interface (CLI) app** written in Python.

It helps you:
- Add habits you want to track (like "Drink Water" or "Exercise")
- Mark them as done or skipped every day
- See your streaks (how many days in a row you completed a habit)
- View a weekly summary of your progress
- See the full history of any habit day by day

You use it by typing commands in the terminal. No buttons, no website — just your keyboard and the terminal.

---

## 2. How Does the User Interact With It?

The user types a command like this:

```
python3 habit.py add "Drink Water"
python3 habit.py log
python3 habit.py status
```

Every command starts with `python3 habit.py` followed by what you want to do.

---

## 3. Big Picture — How the App Works

```
┌─────────────────────────────────────────────────────────────┐
│                        USER (Terminal)                       │
│                                                             │
│         python3 habit.py log "Drink Water"                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      habit.py  (Entry Point)                 │
│                                                             │
│   Reads the command → decides which handler to call         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    commands/  (9 files)                      │
│                                                             │
│   add.py   delete.py   edit.py   list.py   log.py           │
│   status.py   streak.py   summary.py   history.py           │
│                                                             │
│   Each file handles ONE specific command                     │
└────────────┬──────────────────────────┬─────────────────────┘
             │                          │
             ▼                          ▼
┌────────────────────────┐   ┌────────────────────────────────┐
│    core/  (Logic)       │   │    utils/  (Helpers)            │
│                        │   │                                │
│  models.py             │   │  display.py                    │
│  → Habit & Log objects  │   │  → Prints tables to terminal   │
│                        │   │                                │
│  storage.py            │   │  date_utils.py                 │
│  → Read/write JSON      │   │  → Date calculations           │
│                        │   │                                │
│  streak_engine.py      │   └────────────────────────────────┘
│  → Streak calculations  │
└────────────┬───────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                      data/  (Storage)                        │
│                                                             │
│   habits.json          logs.json                            │
│   (list of habits)     (daily log entries)                  │
└─────────────────────────────────────────────────────────────┘
```

**In simple words:**
1. You type a command
2. `habit.py` reads it and calls the right command file
3. The command file uses `core/` to read/write data and do calculations
4. The result is printed to your terminal using `utils/display.py`

---

## 4. Folder Structure — What Each File Does

```
Habit Tracker/
│
├── habit.py                ← START HERE. Reads your command and routes it.
│
├── commands/               ← One file per command. Each does one job.
│   ├── add.py              ← Add a new habit
│   ├── delete.py           ← Delete a habit
│   ├── edit.py             ← Edit a habit's name or description
│   ├── list.py             ← Show all habits
│   ├── log.py              ← Mark a habit as done or skipped
│   ├── status.py           ← Show today's progress
│   ├── streak.py           ← Show streaks
│   ├── summary.py          ← Show weekly summary
│   └── history.py          ← Show day-by-day history
│
├── core/                   ← The brain of the app. Pure logic, no printing.
│   ├── models.py           ← Blueprints for Habit and Log objects
│   ├── storage.py          ← Reads and writes the JSON files
│   └── streak_engine.py    ← Calculates current and longest streaks
│
├── utils/                  ← Helper tools used across the app
│   ├── display.py          ← All the pretty table printing
│   └── date_utils.py       ← Date helpers (today, ranges, day names)
│
├── data/                   ← Where all your data lives
│   ├── habits.json         ← Your habits stored as JSON
│   └── logs.json           ← Your daily logs stored as JSON
│
└── tests/                  ← Automated tests to verify everything works
    ├── test_models.py
    ├── test_storage.py
    ├── test_date_utils.py
    ├── test_streak_engine.py
    └── test_integration.py
```

---

## 5. The Two Data Files Explained

All data is saved locally on your computer as plain text JSON files.
No internet, no database — just two simple files.

### habits.json — stores your habit list

```json
[
  {
    "id": "a1b2c3d4",
    "name": "Drink Water",
    "description": "8 glasses a day",
    "created_at": "2026-09-13"
  },
  {
    "id": "e5f6g7h8",
    "name": "Exercise",
    "description": "30 mins",
    "created_at": "2026-09-13"
  }
]
```

Think of it as a list of cards. Each card has an ID, name, description, and the date it was created.

---

### logs.json — stores what you did each day

```json
[
  { "habit_id": "a1b2c3d4", "date": "2026-09-13", "status": "done"    },
  { "habit_id": "a1b2c3d4", "date": "2026-09-12", "status": "skipped" },
  { "habit_id": "e5f6g7h8", "date": "2026-09-13", "status": "done"    }
]
```

Every time you log a habit, one new row is added here.
Each row says: "For this habit, on this date, the status was done/skipped."
If a date has no row at all → it is treated as **missed**.

---

### Relationship Between the Two Files

```
habits.json                    logs.json
────────────────               ──────────────────────────────
id: "a1b2c3d4"   ──────────►  habit_id: "a1b2c3d4"
name: "Drink Water"            date: "2026-09-13"
                               status: "done"

                    ──────────►  habit_id: "a1b2c3d4"
                               date: "2026-09-12"
                               status: "skipped"
```

The `habit_id` in logs.json links back to the `id` in habits.json.
This is how the app knows which log belongs to which habit.

---

## 6. The Three Status Types

| Status    | Symbol | Meaning                               | Breaks Streak? |
|-----------|--------|---------------------------------------|----------------|
| `done`    | ✅      | You completed the habit               | No — builds it |
| `skipped` | ⏭️      | You chose to skip (valid reason)      | No — ignored   |
| `missed`  | ❌      | No entry found for that day           | Yes — resets   |

---

## 7. How Streaks Work — Step by Step

A streak counts how many days IN A ROW you completed a habit.

**Example:**

```
Day        Status     Streak Count
─────────────────────────────────
Mon        ✅ Done    1
Tue        ✅ Done    2
Wed        ⏭️ Skipped  2  ← skipped = transparent, streak keeps going
Thu        ✅ Done    3
Fri        ❌ Missed  0  ← missed = streak RESETS to 0
Sat        ✅ Done    1
Sun        ✅ Done    2  ← current streak = 2
```

The streak engine walks backwards from today one day at a time:
- Sees `done` → adds 1
- Sees `skipped` → ignores it, keeps walking
- Sees `missed` (no entry) → stops

---

## 8. How a Command Works — Full Flow Example

**Command:** `python3 habit.py log "Drink Water"`

```
Step 1 — habit.py reads the command
         └── sees "log" and "Drink Water"
         └── calls commands/log.py → run(name="Drink Water")

Step 2 — commands/log.py takes over
         └── calls storage.load_habits() to get all habits
         └── finds "Drink Water" in the list
         └── calls storage.get_log(habit_id, today)
             └── checks: already logged today?
                 YES → print warning, stop
                 NO  → continue

Step 3 — create a new Log entry
         └── Log(habit_id="a1b2c3d4", date="2026-09-13", status="done")
         └── calls storage.add_log(log)
             └── loads logs.json
             └── appends the new entry
             └── saves logs.json back to disk

Step 4 — print confirmation
         └── ✅ "Drink Water" logged for 2026-09-13.
```

---

## 9. All Available Commands

| Command                                      | What it does                              |
|----------------------------------------------|-------------------------------------------|
| `habit add "Name"`                           | Add a new habit                           |
| `habit add "Name" -d "description"`          | Add with a description                    |
| `habit list`                                 | Show all habits                           |
| `habit log`                                  | Interactive — pick a habit and log it     |
| `habit log "Name"`                           | Log a specific habit as done              |
| `habit log --all`                            | Log all habits as done at once            |
| `habit log "Name" --skip`                    | Mark a habit as skipped                   |
| `habit log "Name" --date 2026-09-12`         | Log for a past date                       |
| `habit status`                               | See today's done / skipped / pending      |
| `habit streak`                               | See current and longest streaks           |
| `habit summary`                              | 7-day grid with completion rates          |
| `habit history "Name"`                       | Day-by-day history (last 30 days)         |
| `habit history "Name" --last 60`             | Day-by-day history (last N days)          |
| `habit edit`                                 | Edit a habit's name or description        |
| `habit delete`                               | Delete a habit and all its logs           |

---

## 10. The Three Layers of the App

Think of the app as three separate layers, each with a clear job:

```
┌──────────────────────────────────────────────┐
│           PRESENTATION LAYER                  │
│                                              │
│   commands/   +   utils/display.py           │
│                                              │
│   Handles user input and prints output.      │
│   Does NOT touch files directly.             │
└─────────────────────┬────────────────────────┘
                      │ calls
                      ▼
┌──────────────────────────────────────────────┐
│             BUSINESS LOGIC LAYER              │
│                                              │
│   core/streak_engine.py                      │
│   core/models.py                             │
│   utils/date_utils.py                        │
│                                              │
│   Calculates streaks, validates data,        │
│   defines what a Habit and Log look like.    │
│   Does NOT know about files or printing.     │
└─────────────────────┬────────────────────────┘
                      │ calls
                      ▼
┌──────────────────────────────────────────────┐
│               STORAGE LAYER                   │
│                                              │
│   core/storage.py                            │
│                                              │
│   Only job: read and write JSON files.       │
│   Does NOT calculate anything.               │
└──────────────────────────────────────────────┘
```

This separation makes the code clean, easy to test, and easy to change.
For example: if you wanted to switch from JSON to a database later,
you only need to change `storage.py` — nothing else.

---

## 11. The Test Suite

The project has **81 automated tests** across 5 files.
You run them all with one command:

```bash
python3 -m unittest discover -s tests -v
```

| Test File               | What it tests                                 |
|-------------------------|-----------------------------------------------|
| `test_models.py`        | Habit and Log objects, serialisation          |
| `test_storage.py`       | Reading and writing JSON files                |
| `test_date_utils.py`    | Date formatting, ranges, future date checks   |
| `test_streak_engine.py` | Streak counting, skipped logic, edge cases    |
| `test_integration.py`   | Full command flows end to end                 |

---

## 12. Key Python Concepts Used

| Concept           | Where Used                  | Simple Explanation                                  |
|-------------------|-----------------------------|-----------------------------------------------------|
| `dataclass`       | `core/models.py`            | A clean way to define a data object like a template |
| `argparse`        | `habit.py`                  | Reads and understands command line arguments        |
| `json` module     | `core/storage.py`           | Reads and writes .json files                        |
| `datetime` module | `utils/date_utils.py`       | Works with dates — today, ranges, day names         |
| `unittest`        | `tests/`                    | Python's built-in testing framework                 |
| `from_dict`       | `core/models.py`            | Converts a JSON dictionary into a Python object     |
| `to_dict`         | `core/models.py`            | Converts a Python object back into a dictionary     |

---

## 13. What Happens on First Run?

The app is smart enough to set itself up automatically:

```
First time you run any command
        │
        ▼
Does data/ folder exist?
   NO  → creates it
   YES → continues

Does data/habits.json exist?
   NO  → creates it with []
   YES → continues

Does data/logs.json exist?
   NO  → creates it with []
   YES → continues
```

You never need to manually create any files or folders.

---

## 14. Summary in One Paragraph

The Habit Tracker CLI is a Python terminal app that lets you track daily habits.
It saves all data in two JSON files on your computer — one for habits, one for daily logs.
When you run a command, `habit.py` reads it and calls the right command file.
The command file uses the storage layer to read data, the streak engine to calculate streaks,
and the display helper to print a clean table in the terminal.
The app has 81 tests that verify every part works correctly.
It uses zero third-party packages — only Python's built-in standard library.

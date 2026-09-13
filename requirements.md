# Habit Tracker CLI — Requirements

## Tech Stack
- Language: Python
- Storage: JSON (local flat files, no external database)
- No third-party dependencies (standard library only)

---

## Data Storage (JSON)

Two JSON files stored locally:

### `habits.json`
Stores all habit definitions.
```json
[
  {
    "id": "1",
    "name": "Drink Water",
    "description": "Drink 8 glasses of water",
    "created_at": "2026-09-01"
  }
]
```

### `logs.json`
Stores day-wise log entries per habit.
```json
[
  {
    "habit_id": "1",
    "date": "2026-09-13",
    "status": "done"
  },
  {
    "habit_id": "1",
    "date": "2026-09-12",
    "status": "skipped"
  }
]
```

Status values: `done`, `skipped`
If no entry exists for a date, it is treated as `missed`.

---

## Functional Requirements

### 1. Habit Management

- **Add** a new habit with a name and optional description
- **Delete** a habit — show numbered list, user picks by number
- **Edit** a habit name or description
- **List** all habits with their IDs and descriptions

### 2. Daily Logging

- Running `habit log` displays all current habits with index numbers
- User selects a habit by number or name
- Habit is marked as `done` for today
- Option to type `all` or use `--all` flag to log every habit at once
- Confirm before logging all:
  ```
  Log all 4 habits as done for 2026-09-13? (y/n):
  ```
- If a habit is already logged for today, skip it with a warning instead of erroring
- Support logging for a past date using `--date YYYY-MM-DD`
- Support marking a habit as `skipped` using `--skip` flag

### 3. Streaks

- **Current streak**: consecutive days a habit has been marked `done`
- **Longest streak**: highest streak ever recorded for a habit
- Streak resets if a day is `missed` (no entry)
- `skipped` days do not break or count toward a streak
- Display streak info per habit

### 4. History (Day-wise)

- Show a day-by-day log for a specific habit
- Each row shows the date and status

```
History for: Drink Water
─────────────────────────────
Date          Status
2026-09-13    ✅ Done
2026-09-12    ✅ Done
2026-09-11    ❌ Missed
2026-09-10    ⏭️  Skipped
```

- Default: show last 30 days
- Support `--last N` to show last N days

### 5. Weekly Summary

- Show completion rate for each habit over the past 7 days
- Show how many habits were completed each day of the week
- Highlight best day (most completions) and worst day (fewest completions)

```
Weekly Summary (2026-09-07 to 2026-09-13)
──────────────────────────────────────────
Habit             Mon  Tue  Wed  Thu  Fri  Sat  Sun  Rate
Drink Water        ✅   ✅   ❌   ✅   ✅   ✅   ✅   86%
Exercise           ✅   ❌   ❌   ✅   ✅   ❌   ✅   57%
Read 30 mins       ✅   ✅   ✅   ✅   ✅   ✅   ✅  100%

Best day: Monday | Worst day: Wednesday
```

### 6. Status (Today)

- Show all habits and their status for today
- Clearly mark which are done, skipped, or not yet logged

```
Today — 2026-09-13
──────────────────
[1] Drink Water     ✅ Done
[2] Exercise        ⏳ Pending
[3] Read 30 mins    ⏭️  Skipped
```

---

## CLI Commands

```
habit add "Drink Water"                        # Add a new habit
habit add "Drink Water" -d "8 glasses a day"   # Add with description
habit delete                                   # Interactive delete (pick by number)
habit edit                                     # Interactive edit (pick by number)
habit list                                     # List all habits

habit log                                      # Interactive log (shows habits, pick one)
habit log --all                                # Log all habits as done for today
habit log "Drink Water" --date 2026-09-12      # Log for a past date
habit log "Drink Water" --skip                 # Mark as skipped for today

habit status                                   # Today's status for all habits
habit streak                                   # View streaks for all habits
habit summary                                  # Weekly summary
habit history "Drink Water"                    # Day-wise history (last 30 days)
habit history "Drink Water" --last 60          # Day-wise history (last N days)
```

---

## Non-Functional Requirements

- All data stored locally in JSON files — no internet required
- Works fully offline
- No third-party packages — Python standard library only
- Fast startup time
- Human-readable terminal output
- Data persists between sessions
- JSON files are human-readable and can be manually edited if needed

---

## Out of Scope (for now)

- Reminders or push notifications
- Sync across devices or cloud backup
- GUI or web interface
- Habit categories or tags
- User accounts or authentication

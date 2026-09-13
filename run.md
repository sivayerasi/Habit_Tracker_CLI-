# How to Run the Habit Tracker CLI

Simple step-by-step guide for Windows, Mac, and Linux.

---

## Step 1 — Make Sure Python is Installed

You need **Python 3.10 or higher**.

### Check if Python is already installed

**Mac / Linux** — open Terminal and type:
```bash
python3 --version
```

**Windows** — open Command Prompt or PowerShell and type:
```bash
python --version
```

You should see something like:
```
Python 3.11.4
```

If you see an error or a version below 3.10, install Python first.

### Install Python (if needed)

| OS      | How to install                                                   |
|---------|------------------------------------------------------------------|
| Windows | Download from https://www.python.org/downloads/ and run the installer. During install, **check the box that says "Add Python to PATH"** |
| Mac     | Download from https://www.python.org/downloads/ or run `brew install python3` if you have Homebrew |
| Linux   | Run `sudo apt install python3` (Ubuntu/Debian) or `sudo dnf install python3` (Fedora) |

---

## Step 2 — Download the Project

If you have the project as a ZIP file:
1. Unzip it to a folder on your computer
2. Remember where you saved it (e.g. `Desktop/Habit Tracker`)

If you are cloning from Git:
```bash
git clone <repo-url>
```

---

## Step 3 — Open a Terminal / Command Prompt

| OS      | How to open                                                        |
|---------|--------------------------------------------------------------------|
| Windows | Press `Win + R`, type `cmd`, press Enter — OR search "Command Prompt" in Start menu |
| Mac     | Press `Cmd + Space`, type `Terminal`, press Enter                  |
| Linux   | Press `Ctrl + Alt + T` — OR search "Terminal" in your apps         |

---

## Step 4 — Go to the Project Folder

Type this command (replace the path with where you saved the project):

**Mac / Linux:**
```bash
cd ~/Desktop/Habit\ Tracker
```

**Windows:**
```cmd
cd C:\Users\YourName\Desktop\Habit Tracker
```

Confirm you are in the right folder:

**Mac / Linux:**
```bash
ls
```

**Windows:**
```cmd
dir
```

You should see files like `habit.py`, `commands/`, `core/`, etc.

---

## Step 5 — Run Your First Command

**Mac / Linux:**
```bash
python3 habit.py --help
```

**Windows:**
```cmd
python habit.py --help
```

You should see:
```
usage: habit [-h] {add,delete,edit,list,log,status,streak,summary,history} ...

A lightweight CLI habit tracker.
...
```

If you see this — everything is working! 🎉

---

## Step 6 — Try It Out (Quick Start)

Run these commands one by one to see the app in action.

> Use `python3` on Mac/Linux and `python` on Windows.

### Add some habits
```bash
python3 habit.py add "Drink Water" -d "8 glasses a day"
python3 habit.py add "Exercise" -d "30 mins"
python3 habit.py add "Read 30 mins"
```

### List your habits
```bash
python3 habit.py list
```

### Log a habit as done
```bash
python3 habit.py log "Drink Water"
```

### Log interactively (pick from a list)
```bash
python3 habit.py log
```

### Mark a habit as skipped
```bash
python3 habit.py log "Exercise" --skip
```

### See today's status
```bash
python3 habit.py status
```

### View your streaks
```bash
python3 habit.py streak
```

### View weekly summary
```bash
python3 habit.py summary
```

### View history for a habit
```bash
python3 habit.py history "Drink Water"
python3 habit.py history "Drink Water" --last 7
```

### Edit a habit
```bash
python3 habit.py edit
```

### Delete a habit
```bash
python3 habit.py delete
```

---

## Optional — Create a Shortcut (so you can just type `habit`)

Instead of typing `python3 habit.py` every time, you can set up a shortcut.

### Mac / Linux

Open your terminal config file:

**Mac (zsh):**
```bash
nano ~/.zshrc
```

**Linux (bash):**
```bash
nano ~/.bashrc
```

Add this line at the bottom (replace the path with your actual path):
```bash
alias habit="python3 /Users/YourName/Desktop/Habit\ Tracker/habit.py"
```

Save the file (`Ctrl + X`, then `Y`, then `Enter`), then run:
```bash
source ~/.zshrc   # Mac
source ~/.bashrc  # Linux
```

Now you can just type:
```bash
habit add "Drink Water"
habit status
habit log
```

---

### Windows (PowerShell)

Open PowerShell and run:
```powershell
notepad $PROFILE
```

If it asks to create the file, click Yes. Add this line:
```powershell
function habit { python C:\Users\YourName\Desktop\Habit Tracker\habit.py $args }
```

Save and close. Restart PowerShell. Now you can type:
```powershell
habit add "Drink Water"
habit status
```

---

## Run the Tests

To verify everything is working correctly:

**Mac / Linux:**
```bash
python3 -m unittest discover -s tests -v
```

**Windows:**
```cmd
python -m unittest discover -s tests -v
```

You should see:
```
Ran 81 tests in 0.041s

OK
```

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `python3: command not found` | Python not installed | Install Python from python.org |
| `No module named ...` | Wrong folder | Make sure you are inside the `Habit Tracker` folder |
| `SyntaxError` | Python version too old | Upgrade to Python 3.10 or higher |
| `Permission denied` | File not executable | Run with `python3 habit.py` not `./habit.py` |
| `FileNotFoundError: habit.py` | Wrong directory | Run `cd` to go into the project folder first |

---

## Data Location

All your habit data is saved here inside the project folder:

```
Habit Tracker/
└── data/
    ├── habits.json    ← your habits
    └── logs.json      ← your daily logs
```

These files are created automatically the first time you run any command.
You can open them in any text editor to view or manually edit your data.

from core.storage import load_habits, save_habits, load_logs, save_logs
from utils.display import print_habit_list


def run():
    """Interactively delete a habit."""
    habits = load_habits()

    if not habits:
        print("No habits yet. Use 'habit add' to create one.")
        return

    print_habit_list(habits)

    try:
        choice = input("Enter habit number to delete: ").strip()
        index = int(choice) - 1
    except (ValueError, EOFError):
        print("Invalid input. Please enter a number.")
        return

    if index < 0 or index >= len(habits):
        print(f"Invalid selection. Please enter a number between 1 and {len(habits)}.")
        return

    habit = habits[index]

    try:
        confirm = input(f"Delete \"{habit.name}\"? (y/n): ").strip().lower()
    except EOFError:
        confirm = "n"

    if confirm != "y":
        print("Cancelled.")
        return

    # Remove habit
    habits.pop(index)
    save_habits(habits)

    # Remove all associated logs
    logs = load_logs()
    logs = [log for log in logs if log.habit_id != habit.id]
    save_logs(logs)

    print(f"🗑️  Habit \"{habit.name}\" deleted.")

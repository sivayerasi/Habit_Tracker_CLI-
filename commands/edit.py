from core.storage import load_habits, save_habits
from utils.display import print_habit_list


def run():
    """Interactively edit a habit's name or description."""
    habits = load_habits()

    if not habits:
        print("No habits yet. Use 'habit add' to create one.")
        return

    print_habit_list(habits)

    try:
        choice = input("Enter habit number to edit: ").strip()
        index = int(choice) - 1
    except (ValueError, EOFError):
        print("Invalid input. Please enter a number.")
        return

    if index < 0 or index >= len(habits):
        print(f"Invalid selection. Please enter a number between 1 and {len(habits)}.")
        return

    habit = habits[index]

    print(f"\n  Editing: {habit.name}")
    print(f"  Current name:        {habit.name}")
    print(f"  Current description: {habit.description or '—'}")
    print("  (Press Enter to keep current value)\n")

    try:
        new_name = input(f"  New name [{habit.name}]: ").strip()
        new_desc = input(f"  New description [{habit.description or '—'}]: ").strip()
    except EOFError:
        print("Cancelled.")
        return

    # Check for duplicate name if name is being changed
    if new_name and new_name.lower() != habit.name.lower():
        for other in habits:
            if other.id != habit.id and other.name.lower() == new_name.lower():
                print(f"⚠️  A habit named \"{other.name}\" already exists.")
                return

    if new_name:
        habit.name = new_name
    if new_desc:
        habit.description = new_desc

    save_habits(habits)
    print(f"\n✏️  Habit updated.")
    print(f"   Name:        {habit.name}")
    print(f"   Description: {habit.description or '—'}")

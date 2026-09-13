import uuid

from core.models import Habit
from core.storage import load_habits, save_habits
from utils.date_utils import today


def run(name: str, description: str = ""):
    """Add a new habit."""
    name = name.strip()
    description = description.strip()

    if not name:
        print("Error: Habit name cannot be empty.", flush=True)
        return

    habits = load_habits()

    # Duplicate check (case-insensitive)
    for habit in habits:
        if habit.name.lower() == name.lower():
            print(f"⚠️  A habit named \"{habit.name}\" already exists.")
            return

    new_habit = Habit(
        id=uuid.uuid4().hex[:8],
        name=name,
        description=description,
        created_at=today(),
    )

    habits.append(new_habit)
    save_habits(habits)

    print(f"✅ Habit \"{new_habit.name}\" added.")
    if description:
        print(f"   Description: {description}")

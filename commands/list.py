from core.storage import load_habits
from utils.display import print_habit_list


def run():
    """List all habits."""
    habits = load_habits()
    print_habit_list(habits)

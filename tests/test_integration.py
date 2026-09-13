"""TASK-24 — Integration tests for full command flows."""
import os
import tempfile
import unittest
from datetime import date, timedelta
from unittest.mock import patch

from core import storage
from core.storage import save_habits, save_logs, load_habits, load_logs


def yesterday():
    return (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")


def today():
    return date.today().strftime("%Y-%m-%d")


class IntegrationTestBase(unittest.TestCase):
    """Base class that redirects storage to a temp directory."""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.habits_file = os.path.join(self.tmp_dir, "habits.json")
        self.logs_file   = os.path.join(self.tmp_dir, "logs.json")

        self._patches = [
            patch.object(storage, "DATA_DIR",    self.tmp_dir),
            patch.object(storage, "HABITS_FILE", self.habits_file),
            patch.object(storage, "LOGS_FILE",   self.logs_file),
        ]
        for p in self._patches:
            p.start()

    def tearDown(self):
        for p in self._patches:
            p.stop()


class TestAddFlow(IntegrationTestBase):

    def test_add_habit(self):
        from commands.add import run as add
        add("Drink Water", "8 glasses")
        habits = load_habits()
        self.assertEqual(len(habits), 1)
        self.assertEqual(habits[0].name, "Drink Water")
        self.assertEqual(habits[0].description, "8 glasses")

    def test_add_duplicate_rejected(self):
        from commands.add import run as add
        add("Drink Water")
        add("Drink Water")  # duplicate
        self.assertEqual(len(load_habits()), 1)

    def test_add_case_insensitive_duplicate(self):
        from commands.add import run as add
        add("Drink Water")
        add("drink water")
        self.assertEqual(len(load_habits()), 1)

    def test_add_empty_name_rejected(self):
        from commands.add import run as add
        add("")
        self.assertEqual(len(load_habits()), 0)


class TestLogFlow(IntegrationTestBase):

    def setUp(self):
        super().setUp()
        from commands.add import run as add
        add("Drink Water")
        add("Exercise")

    def test_log_by_name_done(self):
        from commands.log import run as log
        log(name="Drink Water")
        logs = load_logs()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].status, "done")

    def test_log_by_name_skip(self):
        from commands.log import run as log
        log(name="Exercise", skip=True)
        logs = load_logs()
        self.assertEqual(logs[0].status, "skipped")

    def test_duplicate_log_skipped(self):
        from commands.log import run as log
        log(name="Drink Water")
        log(name="Drink Water")  # second log should be skipped
        self.assertEqual(len(load_logs()), 1)

    def test_log_past_date(self):
        from commands.log import run as log
        log(name="Drink Water", date_str=yesterday())
        logs = load_logs()
        self.assertEqual(logs[0].date, yesterday())

    def test_log_future_date_rejected(self):
        from commands.log import run as log
        log(name="Drink Water", date_str="2099-01-01")
        self.assertEqual(len(load_logs()), 0)

    def test_log_invalid_date_rejected(self):
        from commands.log import run as log
        log(name="Drink Water", date_str="not-a-date")
        self.assertEqual(len(load_logs()), 0)

    def test_log_all(self):
        from commands.log import run as log
        with patch("builtins.input", return_value="y"):
            log(log_all=True)
        logs = load_logs()
        self.assertEqual(len(logs), 2)
        self.assertTrue(all(l.status == "done" for l in logs))

    def test_log_all_skips_already_logged(self):
        from commands.log import run as log
        log(name="Drink Water")  # pre-log one
        with patch("builtins.input", return_value="y"):
            log(log_all=True)
        logs = load_logs()
        # Should still be 2 total (one was pre-logged, one new)
        self.assertEqual(len(logs), 2)

    def test_log_unknown_habit(self):
        from commands.log import run as log
        log(name="Unknown")
        self.assertEqual(len(load_logs()), 0)


class TestDeleteFlow(IntegrationTestBase):

    def test_delete_removes_habit_and_logs(self):
        from commands.add import run as add
        from commands.log import run as log
        from commands.delete import run as delete

        add("Drink Water")
        log(name="Drink Water")

        self.assertEqual(len(load_habits()), 1)
        self.assertEqual(len(load_logs()), 1)

        with patch("builtins.input", side_effect=["1", "y"]):
            delete()

        self.assertEqual(len(load_habits()), 0)
        self.assertEqual(len(load_logs()), 0)

    def test_delete_cancelled(self):
        from commands.add import run as add
        from commands.delete import run as delete

        add("Drink Water")
        with patch("builtins.input", side_effect=["1", "n"]):
            delete()

        self.assertEqual(len(load_habits()), 1)


class TestEditFlow(IntegrationTestBase):

    def test_edit_name(self):
        from commands.add import run as add
        from commands.edit import run as edit

        add("Old Name")
        with patch("builtins.input", side_effect=["1", "New Name", ""]):
            edit()

        habits = load_habits()
        self.assertEqual(habits[0].name, "New Name")

    def test_edit_description(self):
        from commands.add import run as add
        from commands.edit import run as edit

        add("Drink Water", "old desc")
        with patch("builtins.input", side_effect=["1", "", "new desc"]):
            edit()

        habits = load_habits()
        self.assertEqual(habits[0].description, "new desc")

    def test_edit_keep_current_on_empty_input(self):
        from commands.add import run as add
        from commands.edit import run as edit

        add("Drink Water", "8 glasses")
        with patch("builtins.input", side_effect=["1", "", ""]):
            edit()

        habits = load_habits()
        self.assertEqual(habits[0].name, "Drink Water")
        self.assertEqual(habits[0].description, "8 glasses")


class TestStreakFlow(IntegrationTestBase):

    def test_streak_skip_does_not_break(self):
        from commands.add import run as add
        from commands.log import run as log
        from core.storage import load_habits, load_logs
        from core.streak_engine import get_current_streak

        add("Drink Water")
        habit = load_habits()[0]

        log(name="Drink Water")                     # today: done
        log(name="Drink Water", skip=True,
            date_str=yesterday())                   # yesterday: skipped

        logs = load_logs()
        streak = get_current_streak(habit.id, logs)
        self.assertEqual(streak, 1)  # skipped yesterday, done today → streak = 1


class TestHistoryFlow(IntegrationTestBase):

    def test_history_unknown_habit(self):
        """Should not crash on unknown habit."""
        from commands.history import run as history
        # Just verify no exception is raised
        history("Unknown", last=7)

    def test_history_shows_missed_for_empty_logs(self):
        from commands.add import run as add
        from core.storage import load_habits, load_logs
        from utils.date_utils import last_n_days

        add("Drink Water")
        habit = load_habits()[0]
        logs = load_logs()
        dates = last_n_days(7)

        log_map = {l.date: l.status for l in logs if l.habit_id == habit.id}
        for d in dates:
            self.assertIsNone(log_map.get(d))  # all should be missed


if __name__ == "__main__":
    unittest.main()

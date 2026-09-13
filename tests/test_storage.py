"""TASK-21 — Tests for core/storage.py"""
import json
import os
import tempfile
import unittest
from unittest.mock import patch

from core.models import Habit, Log
from core import storage


class TestStorage(unittest.TestCase):

    def setUp(self):
        """Redirect storage to a temp directory for each test."""
        self.tmp_dir = tempfile.mkdtemp()
        self.habits_file = os.path.join(self.tmp_dir, "habits.json")
        self.logs_file = os.path.join(self.tmp_dir, "logs.json")

        # Patch the module-level constants
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

    # ── Habits ────────────────────────────────────────────────────────────────

    def test_load_habits_missing_file(self):
        result = storage.load_habits()
        self.assertEqual(result, [])

    def test_load_habits_empty_file(self):
        with open(self.habits_file, "w") as f:
            f.write("[]")
        result = storage.load_habits()
        self.assertEqual(result, [])

    def test_save_and_load_habits(self):
        h = Habit(id="h1", name="Drink Water", description="8 glasses", created_at="2026-09-13")
        storage.save_habits([h])
        loaded = storage.load_habits()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].name, "Drink Water")
        self.assertEqual(loaded[0].id, "h1")

    def test_save_habits_multiple(self):
        habits = [
            Habit(id="h1", name="Drink Water", description="", created_at="2026-09-13"),
            Habit(id="h2", name="Exercise",    description="", created_at="2026-09-13"),
        ]
        storage.save_habits(habits)
        loaded = storage.load_habits()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[1].name, "Exercise")

    def test_save_habits_overwrites(self):
        storage.save_habits([Habit(id="h1", name="Old", description="", created_at="")])
        storage.save_habits([Habit(id="h2", name="New", description="", created_at="")])
        loaded = storage.load_habits()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].name, "New")

    # ── Logs ──────────────────────────────────────────────────────────────────

    def test_load_logs_missing_file(self):
        result = storage.load_logs()
        self.assertEqual(result, [])

    def test_load_logs_empty_file(self):
        with open(self.logs_file, "w") as f:
            f.write("[]")
        result = storage.load_logs()
        self.assertEqual(result, [])

    def test_add_log_and_load(self):
        log = Log(habit_id="h1", date="2026-09-13", status="done")
        storage.add_log(log)
        loaded = storage.load_logs()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].status, "done")

    def test_add_log_appends(self):
        storage.add_log(Log(habit_id="h1", date="2026-09-12", status="done"))
        storage.add_log(Log(habit_id="h1", date="2026-09-13", status="skipped"))
        loaded = storage.load_logs()
        self.assertEqual(len(loaded), 2)

    def test_get_log_found(self):
        storage.add_log(Log(habit_id="h1", date="2026-09-13", status="done"))
        result = storage.get_log("h1", "2026-09-13")
        self.assertIsNotNone(result)
        self.assertEqual(result.status, "done")

    def test_get_log_not_found(self):
        result = storage.get_log("h1", "2026-09-01")
        self.assertIsNone(result)

    def test_get_log_wrong_habit(self):
        storage.add_log(Log(habit_id="h1", date="2026-09-13", status="done"))
        result = storage.get_log("h2", "2026-09-13")
        self.assertIsNone(result)

    def test_save_and_load_logs_round_trip(self):
        logs = [
            Log(habit_id="h1", date="2026-09-13", status="done"),
            Log(habit_id="h1", date="2026-09-12", status="skipped"),
        ]
        storage.save_logs(logs)
        loaded = storage.load_logs()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].status, "done")
        self.assertEqual(loaded[1].status, "skipped")


if __name__ == "__main__":
    unittest.main()

"""TASK-20 — Tests for core/models.py"""
import unittest
from core.models import Habit, Log


class TestHabit(unittest.TestCase):

    def _make_habit(self):
        return Habit(
            id="abc123",
            name="Drink Water",
            description="8 glasses",
            created_at="2026-09-13",
        )

    def test_to_dict(self):
        h = self._make_habit()
        d = h.to_dict()
        self.assertEqual(d["id"], "abc123")
        self.assertEqual(d["name"], "Drink Water")
        self.assertEqual(d["description"], "8 glasses")
        self.assertEqual(d["created_at"], "2026-09-13")

    def test_from_dict(self):
        data = {
            "id": "abc123",
            "name": "Drink Water",
            "description": "8 glasses",
            "created_at": "2026-09-13",
        }
        h = Habit.from_dict(data)
        self.assertEqual(h.id, "abc123")
        self.assertEqual(h.name, "Drink Water")
        self.assertEqual(h.description, "8 glasses")
        self.assertEqual(h.created_at, "2026-09-13")

    def test_round_trip(self):
        h = self._make_habit()
        self.assertEqual(h, Habit.from_dict(h.to_dict()))

    def test_default_description(self):
        h = Habit.from_dict({"id": "x", "name": "Test"})
        self.assertEqual(h.description, "")

    def test_default_created_at(self):
        h = Habit.from_dict({"id": "x", "name": "Test"})
        self.assertEqual(h.created_at, "")


class TestLog(unittest.TestCase):

    def _make_log(self, status="done"):
        return Log(habit_id="abc123", date="2026-09-13", status=status)

    def test_to_dict(self):
        l = self._make_log()
        d = l.to_dict()
        self.assertEqual(d["habit_id"], "abc123")
        self.assertEqual(d["date"], "2026-09-13")
        self.assertEqual(d["status"], "done")

    def test_from_dict(self):
        data = {"habit_id": "abc123", "date": "2026-09-13", "status": "skipped"}
        l = Log.from_dict(data)
        self.assertEqual(l.habit_id, "abc123")
        self.assertEqual(l.date, "2026-09-13")
        self.assertEqual(l.status, "skipped")

    def test_round_trip_done(self):
        l = self._make_log("done")
        self.assertEqual(l, Log.from_dict(l.to_dict()))

    def test_round_trip_skipped(self):
        l = self._make_log("skipped")
        self.assertEqual(l, Log.from_dict(l.to_dict()))

    def test_invalid_status_raises(self):
        with self.assertRaises(ValueError):
            Log(habit_id="x", date="2026-09-13", status="invalid")

    def test_invalid_status_message(self):
        try:
            Log(habit_id="x", date="2026-09-13", status="missed")
        except ValueError as e:
            self.assertIn("missed", str(e))


if __name__ == "__main__":
    unittest.main()

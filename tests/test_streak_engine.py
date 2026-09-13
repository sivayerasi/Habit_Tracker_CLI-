"""TASK-23 — Tests for core/streak_engine.py"""
import unittest
from datetime import date, timedelta
from core.models import Log
from core.streak_engine import get_current_streak, get_longest_streak

HID = "habit01"


def make_log(days_ago: int, status: str) -> Log:
    d = (date.today() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    return Log(habit_id=HID, date=d, status=status)


class TestCurrentStreak(unittest.TestCase):

    def test_empty_logs(self):
        self.assertEqual(get_current_streak(HID, []), 0)

    def test_single_done_today(self):
        logs = [make_log(0, "done")]
        self.assertEqual(get_current_streak(HID, logs), 1)

    def test_consecutive_done_days(self):
        logs = [make_log(i, "done") for i in range(5)]
        self.assertEqual(get_current_streak(HID, logs), 5)

    def test_missed_day_resets_streak(self):
        # Done today and yesterday, missed 2 days ago, done 3 days ago
        logs = [
            make_log(0, "done"),
            make_log(1, "done"),
            # day 2 missed
            make_log(3, "done"),
        ]
        self.assertEqual(get_current_streak(HID, logs), 2)

    def test_skipped_day_is_transparent(self):
        logs = [
            make_log(0, "done"),
            make_log(1, "skipped"),
            make_log(2, "done"),
        ]
        self.assertEqual(get_current_streak(HID, logs), 2)

    def test_multiple_skipped_days_transparent(self):
        logs = [
            make_log(0, "done"),
            make_log(1, "skipped"),
            make_log(2, "skipped"),
            make_log(3, "done"),
        ]
        self.assertEqual(get_current_streak(HID, logs), 2)

    def test_today_not_logged_counts_from_yesterday(self):
        logs = [make_log(1, "done"), make_log(2, "done")]
        self.assertEqual(get_current_streak(HID, logs), 2)

    def test_only_skipped_today(self):
        logs = [make_log(0, "skipped")]
        self.assertEqual(get_current_streak(HID, logs), 0)

    def test_wrong_habit_id_ignored(self):
        logs = [Log(habit_id="other", date=date.today().strftime("%Y-%m-%d"), status="done")]
        self.assertEqual(get_current_streak(HID, logs), 0)


class TestLongestStreak(unittest.TestCase):

    def test_empty_logs(self):
        self.assertEqual(get_longest_streak(HID, []), 0)

    def test_all_done(self):
        logs = [make_log(i, "done") for i in range(7)]
        self.assertEqual(get_longest_streak(HID, logs), 7)

    def test_longest_across_a_break(self):
        logs = [
            make_log(10, "done"),
            make_log(9,  "done"),
            make_log(8,  "done"),
            # day 7 missed
            make_log(6,  "done"),
            make_log(5,  "done"),
        ]
        self.assertEqual(get_longest_streak(HID, logs), 3)

    def test_skipped_transparent_in_longest(self):
        logs = [
            make_log(5, "done"),
            make_log(4, "skipped"),
            make_log(3, "done"),
            make_log(2, "done"),
        ]
        self.assertEqual(get_longest_streak(HID, logs), 3)

    def test_longest_is_max_of_all_runs(self):
        # Run of 2, then break, then run of 4
        logs = [
            make_log(10, "done"),
            make_log(9,  "done"),
            # break
            make_log(6,  "done"),
            make_log(5,  "done"),
            make_log(4,  "done"),
            make_log(3,  "done"),
        ]
        self.assertEqual(get_longest_streak(HID, logs), 4)

    def test_single_done(self):
        logs = [make_log(0, "done")]
        self.assertEqual(get_longest_streak(HID, logs), 1)

    def test_only_skipped(self):
        logs = [make_log(i, "skipped") for i in range(5)]
        self.assertEqual(get_longest_streak(HID, logs), 0)


if __name__ == "__main__":
    unittest.main()

"""TASK-22 — Tests for utils/date_utils.py"""
import unittest
from datetime import date
from utils.date_utils import today, parse_date, date_range, last_n_days, is_future_date, get_day_name


class TestToday(unittest.TestCase):

    def test_format(self):
        t = today()
        self.assertEqual(len(t), 10)
        self.assertEqual(t[4], "-")
        self.assertEqual(t[7], "-")

    def test_matches_date(self):
        self.assertEqual(today(), date.today().strftime("%Y-%m-%d"))


class TestParseDate(unittest.TestCase):

    def test_valid_date(self):
        self.assertEqual(parse_date("2026-09-13"), "2026-09-13")

    def test_invalid_format_dmy(self):
        with self.assertRaises(ValueError):
            parse_date("13-09-2026")

    def test_invalid_format_slash(self):
        with self.assertRaises(ValueError):
            parse_date("2026/09/13")

    def test_invalid_nonsense(self):
        with self.assertRaises(ValueError):
            parse_date("not-a-date")

    def test_error_message_contains_input(self):
        try:
            parse_date("bad-input")
        except ValueError as e:
            self.assertIn("bad-input", str(e))


class TestDateRange(unittest.TestCase):

    def test_single_day(self):
        self.assertEqual(date_range("2026-09-13", "2026-09-13"), ["2026-09-13"])

    def test_multiple_days(self):
        result = date_range("2026-09-10", "2026-09-13")
        self.assertEqual(result, ["2026-09-10", "2026-09-11", "2026-09-12", "2026-09-13"])

    def test_start_after_end_returns_empty(self):
        self.assertEqual(date_range("2026-09-13", "2026-09-10"), [])

    def test_order_is_oldest_first(self):
        result = date_range("2026-09-01", "2026-09-03")
        self.assertEqual(result[0], "2026-09-01")
        self.assertEqual(result[-1], "2026-09-03")


class TestLastNDays(unittest.TestCase):

    def test_count(self):
        self.assertEqual(len(last_n_days(7)), 7)
        self.assertEqual(len(last_n_days(30)), 30)
        self.assertEqual(len(last_n_days(1)), 1)

    def test_ends_with_today(self):
        self.assertEqual(last_n_days(7)[-1], today())

    def test_order_oldest_first(self):
        days = last_n_days(3)
        self.assertLess(days[0], days[1])
        self.assertLess(days[1], days[2])


class TestIsFutureDate(unittest.TestCase):

    def test_future_is_true(self):
        self.assertTrue(is_future_date("2099-01-01"))

    def test_past_is_false(self):
        self.assertFalse(is_future_date("2020-01-01"))

    def test_today_is_not_future(self):
        self.assertFalse(is_future_date(today()))


class TestGetDayName(unittest.TestCase):

    def test_known_sunday(self):
        self.assertEqual(get_day_name("2026-09-13"), "Sun")

    def test_known_monday(self):
        self.assertEqual(get_day_name("2026-09-07"), "Mon")

    def test_known_saturday(self):
        self.assertEqual(get_day_name("2026-09-12"), "Sat")


if __name__ == "__main__":
    unittest.main()

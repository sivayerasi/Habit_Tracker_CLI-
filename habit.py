#!/usr/bin/env python3
"""
Habit Tracker CLI — Entry Point
Usage: python habit.py <command> [options]
"""

import argparse
import os
import json
import sys


def init_data_files():
    """Create data/ directory and empty JSON files if they don't exist."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    for filename in ("habits.json", "logs.json"):
        filepath = os.path.join(data_dir, filename)
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                json.dump([], f)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="habit",
        description="A lightweight CLI habit tracker.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
commands:
  add       Add a new habit
  delete    Delete an existing habit
  edit      Edit a habit name or description
  list      List all habits
  log       Log a habit as done (or skipped)
  status    Show today's habit status
  streak    View streaks for all habits
  summary   Show weekly summary
  history   View day-wise history for a habit

examples:
  habit add "Drink Water" -d "8 glasses a day"
  habit log
  habit log --all
  habit log "Drink Water" --date 2026-09-12
  habit log "Drink Water" --skip
  habit status
  habit streak
  habit summary
  habit history "Drink Water"
  habit history "Drink Water" --last 60
        """,
    )

    subparsers = parser.add_subparsers(dest="command")

    # ── add ───────────────────────────────────────────────────────────────────
    add_parser = subparsers.add_parser(
        "add",
        help="Add a new habit",
        description="Add a new habit to track.",
    )
    add_parser.add_argument(
        "name",
        help='Name of the habit (e.g. "Drink Water")',
    )
    add_parser.add_argument(
        "-d", "--description",
        default="",
        help="Optional description for the habit",
    )

    # ── delete ────────────────────────────────────────────────────────────────
    subparsers.add_parser(
        "delete",
        help="Delete an existing habit",
        description="Interactively select and delete a habit.",
    )

    # ── edit ──────────────────────────────────────────────────────────────────
    subparsers.add_parser(
        "edit",
        help="Edit a habit name or description",
        description="Interactively select and edit a habit.",
    )

    # ── list ──────────────────────────────────────────────────────────────────
    subparsers.add_parser(
        "list",
        help="List all habits",
        description="Display all tracked habits.",
    )

    # ── log ───────────────────────────────────────────────────────────────────
    log_parser = subparsers.add_parser(
        "log",
        help="Log a habit as done (or skipped)",
        description="Mark a habit as done or skipped for today (or a specific date).",
    )
    log_parser.add_argument(
        "name",
        nargs="?",
        default=None,
        help="Name of the habit to log (optional — interactive picker shown if omitted)",
    )
    log_parser.add_argument(
        "--all",
        action="store_true",
        dest="log_all",
        help="Log all habits as done at once",
    )
    log_parser.add_argument(
        "--date",
        default=None,
        metavar="YYYY-MM-DD",
        help="Log for a specific past date instead of today",
    )
    log_parser.add_argument(
        "--skip",
        action="store_true",
        help="Mark the habit as skipped instead of done",
    )

    # ── status ────────────────────────────────────────────────────────────────
    subparsers.add_parser(
        "status",
        help="Show today's habit status",
        description="Display completion status for all habits today.",
    )

    # ── streak ────────────────────────────────────────────────────────────────
    subparsers.add_parser(
        "streak",
        help="View streaks for all habits",
        description="Show current and longest streaks for every habit.",
    )

    # ── summary ───────────────────────────────────────────────────────────────
    subparsers.add_parser(
        "summary",
        help="Show weekly summary",
        description="Display a 7-day completion grid with rates and best/worst days.",
    )

    # ── history ───────────────────────────────────────────────────────────────
    history_parser = subparsers.add_parser(
        "history",
        help="View day-wise history for a habit",
        description="Show a day-by-day log history for a specific habit.",
    )
    history_parser.add_argument(
        "name",
        help="Name of the habit",
    )
    history_parser.add_argument(
        "--last",
        type=int,
        default=30,
        metavar="N",
        help="Number of days to show (default: 30)",
    )

    return parser


def main():
    init_data_files()

    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    # ── Route to command handlers ─────────────────────────────────────────────
    if args.command == "add":
        from commands.add import run
        run(args.name, args.description)

    elif args.command == "delete":
        from commands.delete import run
        run()

    elif args.command == "edit":
        from commands.edit import run
        run()

    elif args.command == "list":
        from commands.list import run
        run()

    elif args.command == "log":
        from commands.log import run
        run(
            name=args.name,
            log_all=args.log_all,
            date_str=args.date,
            skip=args.skip,
        )

    elif args.command == "status":
        from commands.status import run
        run()

    elif args.command == "streak":
        from commands.streak import run
        run()

    elif args.command == "summary":
        from commands.summary import run
        run()

    elif args.command == "history":
        from commands.history import run
        run(args.name, args.last)


if __name__ == "__main__":
    main()

"""Deliberately incomplete calendars must fail their dbt data checks."""

import json
import os
import subprocess
import sys
from pathlib import Path

import psycopg

ROOT = Path(__file__).resolve().parents[1]


def check_fails(test_name):
    result = subprocess.run(
        [
            str(Path(sys.executable).parent / "dbt"),
            "test",
            "--profiles-dir",
            ".",
            "--select",
            test_name,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    run = json.loads((ROOT / "target/run_results.json").read_text())
    check = next(r for r in run["results"] if r["unique_id"].endswith("." + test_name))
    assert check["status"] == "fail"
    assert check["failures"] == 1


def test_missing_month_is_rejected():
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        conn.execute("DELETE FROM raw.calendar WHERE month = '2024-02-01'")
    try:
        check_fails("calendar_complete")
    finally:
        with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
            conn.execute("INSERT INTO raw.calendar VALUES ('2024-02-01')")


def test_calendar_starting_after_signup_is_rejected():
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        conn.execute("DELETE FROM raw.calendar WHERE month = '2024-01-01'")
    try:
        check_fails("calendar_covers_history")
    finally:
        with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
            conn.execute("INSERT INTO raw.calendar VALUES ('2024-01-01')")

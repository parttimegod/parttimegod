"""Deterministic synthetic subscriptions; no claims of real business outcomes."""

from __future__ import annotations

import argparse
import os
import random
from datetime import date
from decimal import Decimal
from pathlib import Path

import psycopg

ROOT = Path(__file__).resolve().parents[1]


def month(offset: int) -> date:
    return date(2024 + offset // 12, offset % 12 + 1, 1)


def generate(customers: int, seed: int = 42):
    rng = random.Random(seed)
    people, periods = [], []
    for cid in range(1, customers + 1):
        people.append(
            (
                cid,
                rng.choice(["small_business", "mid_market"]),
                rng.choice(["TR", "GB", "DE", "US"]),
            )
        )
        start = rng.randrange(0, 7)
        price = Decimal(rng.choice(["29", "99", "299"]))
        change = rng.randrange(start + 1, 18)
        behavior = rng.choice(["retain", "upgrade", "downgrade", "churn", "return"])
        sid = f"sub-{cid}"
        if behavior == "retain":
            periods.append((f"{cid}-0", cid, sid, month(start), None, price))
        else:
            periods.append((f"{cid}-0", cid, sid, month(start), month(change), price))
            if behavior == "upgrade":
                periods.append((f"{cid}-1", cid, sid, month(change), None, price * 2))
            elif behavior == "downgrade":
                periods.append((f"{cid}-1", cid, sid, month(change), None, price / 2))
            elif behavior == "return":
                periods.append((f"{cid}-1", cid, sid, month(change + 2), None, price))
    return people, periods, [(month(i),) for i in range(24)]


def fixture():
    people = [(i, "small_business", "TR") for i in range(1, 6)]
    periods = [
        ("A1", 1, "A", month(0), month(2), 100),
        ("A2", 1, "A", month(2), None, 150),
        ("B1", 2, "B", month(1), month(3), 80),
        ("C1", 3, "C", month(0), month(1), 50),
        ("C2", 3, "C", month(2), month(4), 70),
        ("D1", 4, "D", month(0), month(1), 120),
        ("D2", 4, "D", month(1), None, 90),
        ("E1", 5, "E", month(2), None, 40),
    ]
    return people, periods, [(month(i),) for i in range(5)]


def load(dsn: str, rows, source: str, reset: bool = False):
    people, periods, calendar = rows
    # Schema, batch and audit share one transaction. Failure rolls all back.
    with psycopg.connect(dsn) as conn, conn.cursor() as cur:
        cur.execute((ROOT / "sql/001_raw.sql").read_text())
        if reset:
            # Only this project's raw schema, explicitly requested for demo switching.
            cur.execute(
                "TRUNCATE raw.load_run, raw.subscription_period, "
                "raw.customer, raw.calendar RESTART IDENTITY CASCADE"
            )
        cur.executemany(
            "INSERT INTO raw.customer VALUES (%s,%s,%s) "
            "ON CONFLICT(customer_id) DO UPDATE SET "
            "segment=excluded.segment,country=excluded.country",
            people,
        )
        cur.executemany(
            "INSERT INTO raw.subscription_period VALUES (%s,%s,%s,%s,%s,%s) "
            "ON CONFLICT(period_id) DO UPDATE SET "
            "customer_id=excluded.customer_id, "
            "subscription_id=excluded.subscription_id, "
            "valid_from=excluded.valid_from,valid_to=excluded.valid_to, "
            "monthly_price=excluded.monthly_price",
            periods,
        )
        cur.executemany(
            "INSERT INTO raw.calendar VALUES (%s) ON CONFLICT(month) DO NOTHING",
            calendar,
        )
        cur.execute(
            "INSERT INTO raw.load_run(source,customer_count,period_count) "
            "VALUES (%s,%s,%s)",
            (source, len(people), len(periods)),
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--customers", type=int, default=10000)
    parser.add_argument("--fixture", action="store_true")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear only project raw tables before loading demo data",
    )
    args = parser.parse_args()
    if args.customers < 1:
        parser.error("--customers must be positive")
    load(
        os.environ["DATABASE_URL"],
        fixture() if args.fixture else generate(args.customers),
        "hand_checked_fixture" if args.fixture else "synthetic_seed_42",
        args.reset,
    )
    print("Demo source loaded; reruns upsert natural keys and record each load.")

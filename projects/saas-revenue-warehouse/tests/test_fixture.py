"""Independent, hand-calculated expectations, checked against built dbt marts."""

import os
from decimal import Decimal

import psycopg


def test_monthly_totals():
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        rows = conn.execute(
            "SELECT mrr FROM analytics.mart_monthly_revenue ORDER BY month"
        ).fetchall()
    assert [r[0] for r in rows] == [270, 270, 430, 350, 280]


def test_february_movement_and_nrr():
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        row = conn.execute(
            "SELECT new_mrr, churn_mrr, contraction_mrr, "
            "reactivation_mrr, net_revenue_retention "
            "FROM analytics.mart_monthly_revenue "
            "WHERE month = '2024-02-01'"
        ).fetchone()
    assert row[:4] == (80, 50, 30, 0)
    assert abs(row[4] - Decimal(190) / Decimal(270)) < Decimal("0.000000001")


def test_reactivation_is_not_new_revenue():
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        row = conn.execute(
            "SELECT new_mrr, reactivation_mrr, expansion_mrr "
            "FROM analytics.mart_monthly_revenue "
            "WHERE month = '2024-03-01'"
        ).fetchone()
    assert row == (40, 70, 50)


def test_returning_customer_and_unobserved_future():
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        rows = conn.execute(
            "SELECT months_since_signup, retained_customers, cohort_size "
            "FROM analytics.mart_cohort_retention "
            "WHERE cohort_month = '2024-01-01' ORDER BY month"
        ).fetchall()
    assert rows == [(0, 3, 3), (1, 2, 3), (2, 3, 3), (3, 3, 3), (4, 2, 3)]


def test_reruns_do_not_duplicate_source_rows():
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        counts = conn.execute(
            "SELECT (SELECT count(*) FROM raw.customer), "
            "(SELECT count(*) FROM raw.subscription_period), "
            "(SELECT count(*) FROM raw.load_run)"
        ).fetchone()
    # CI deliberately imports the same fixture twice before building.
    assert counts == (5, 8, 2)

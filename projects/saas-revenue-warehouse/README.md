# SaaS Revenue Warehouse

PostgreSQL + dbt models that explain **why recurring revenue changed**,
not just display a total. Python loads reproducible synthetic subscription
data; SQL models calculate customer movements, revenue retention, and
paid-customer cohorts.

**Portfolio project. All customers, prices, and business results are
synthetic. No production deployment or commercial outcome is claimed.**

## Business questions

- Did MRR grow through acquisition, upgrades, or returning customers?
- How much recurring revenue did existing customers retain?
- Which signup cohorts remain paying after one, three, or twelve months?
- Can the revenue changes reconcile exactly to the reported total?

## Run locally

Requirements: Python 3.12 and Docker Compose.

```bash
docker compose up -d --wait
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL='postgresql://warehouse:local_demo_only@127.0.0.1:5432/warehouse'
python scripts/load_demo.py --customers 10000
dbt build --profiles-dir .
dbt docs generate --profiles-dir .
dbt docs serve --profiles-dir .
```

On Windows PowerShell activate `.venv\Scripts\Activate.ps1` and set
`$env:DATABASE_URL` instead of `export`. Connection settings in
`profiles.yml` can be overridden with standard `PGHOST`, `PGPORT`,
`PGUSER`, `PGPASSWORD`, and `PGDATABASE` variables.

The default generator produces 10,000 customers, 24 observed months, and
240,000 customer-month rows. Its seed is fixed at 42. Re-running the
same load upserts natural keys and adds an audit record; it does not
duplicate subscriptions. Use `--reset` when switching demo sizes or
switching between fixture and generated data: additive upserts do not
delete records omitted from a later source batch.

## Model design

| Model | Grain | Purpose |
|---|---|---|
| `raw.customer` | Customer | Segment and country |
| `raw.subscription_period` | Subscription price period | Effective price intervals |
| `raw.calendar` | Observed month | Explicit as-of boundary |
| `int_customer_month` | Customer × month | Complete spine and previous-month MRR |
| `fct_mrr_movements` | Customer × month | New, return, expansion, contraction, churn |
| `mart_monthly_revenue` | Month | MRR bridge, NRR and churn rates |
| `mart_cohort_retention` | Signup cohort × month | Paying-customer retention |

All joins from customers to subscriptions are aggregated at customer-month
grain before metrics are calculated. Multiple subscriptions can contribute
to one customer's MRR without duplicating that customer in the cohort.

## Metric contract

- **MRR** is the USD subscription run rate on the first day of the month.
  It is not cash received, invoiced revenue, or accounting recognition.
- Subscription periods are **`[valid_from, valid_to)`**. An end date equal
  to the snapshot date means inactive. Prices use exact `NUMERIC` values.
- Sources are month-aligned. A data test rejects mid-month periods; daily
  billing and proration are outside this version's scope.
- **New MRR** is a customer's first paid month. A previously inactive
  customer returning later is **reactivation**, not a second acquisition.
- **NRR** is `(opening MRR + expansion - contraction - churn) / opening MRR`.
  New and returning customers are excluded because they contributed no
  opening revenue. An empty opening denominator yields `NULL`.
- **Cohort retention** divides paying customers by the cohort's starting
  size. Returning customers count again; this is not continuous survival.
- The calendar contains observed months only. An observed inactive month
  is zero; a future, unobserved month is absent.

The SQL identity is checked on every dbt build:

```text
closing MRR = opening MRR + new + reactivation + expansion - contraction - churn
```

## Correctness evidence

There are 20 dbt data tests: keys, nulls, relationships, period alignment,
non-overlapping intervals, customer-month uniqueness, retention bounds,
and exact MRR reconciliation. Five Python integration checks compare
built marts with independent hand-calculated expectations:

```bash
python scripts/load_demo.py --fixture --reset
python scripts/load_demo.py --fixture
dbt build --profiles-dir .
pytest tests/test_fixture.py -q
```

| Fixture month | MRR (USD) | Explanation |
|---|---:|---|
| January | 270 | Three new customers |
| February | 270 | +80 new, -50 churn, -30 contraction |
| March | 430 | +40 new, +70 reactivation, +50 expansion |
| April | 350 | -80 churn |
| May | 280 | -70 churn |

The GitHub Actions workflow tests both PostgreSQL 16 and 17, first on the
hand-checked fixture and then on 10,000 synthetic customers. See
[validation notes](docs/VALIDATION.md) for what has actually run.

## Explore with SQL

```sql
SELECT month, mrr, new_mrr, expansion_mrr, churn_mrr,
       round(100 * net_revenue_retention, 2) AS nrr_percent
FROM analytics.mart_monthly_revenue
ORDER BY month;

SELECT cohort_month, months_since_signup,
       round(100 * retention_rate, 2) AS paid_retention_percent
FROM analytics.mart_cohort_retention
WHERE months_since_signup IN (1, 3, 12)
ORDER BY cohort_month, months_since_signup;
```

This is deliberately a small, complete analytics pipeline. It does not
claim streaming ingestion, incremental dbt materialization, orchestration
with Airflow, production-scale benchmarks, refunds, annual billing,
foreign-exchange conversion, or accounting-grade revenue recognition.

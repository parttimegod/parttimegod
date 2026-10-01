# SaaS Revenue Warehouse

Subscription revenue models in PostgreSQL and dbt, with a Python loader
for sample data. The main outputs are monthly recurring revenue (MRR),
revenue retention and paying-customer cohorts.

A total can hide what happened underneath it. In the small fixture, MRR
stays at $270 in February: an $80 new customer offsets $50 of cancellations
and a $30 downgrade. The revenue bridge keeps those changes separate.

All data is synthetic. The default generator creates 10,000 customers
over January 2024–December 2025; the smaller fixture can be checked by hand.

## Run

You need Python 3.12 and Docker Compose.

```bash
docker compose up -d --wait
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL='postgresql://warehouse:local_demo_only@127.0.0.1:5432/warehouse'
python scripts/load_demo.py --customers 10000
dbt build --profiles-dir .
```

On PowerShell, activate `.venv\Scripts\Activate.ps1` and assign the
connection string to `$env:DATABASE_URL`. dbt connection settings are in
`profiles.yml`; override them with `PGHOST`, `PGPORT`, `PGUSER`,
`PGPASSWORD` and `PGDATABASE` for another local database.

The loader upserts the same customer and period IDs on a rerun. It adds
one `raw.load_run` record per load. Use `--reset` when changing the
sample size or switching to the fixture: upserts do not remove rows that
are missing from a later batch.

## Tables and models

| Relation | One row per | Use |
|---|---|---|
| `raw.customer` | Customer | Segment and country |
| `raw.subscription_period` | Subscription price period | Price and effective dates |
| `raw.calendar` | Observed month | Reporting range |
| `int_customer_month` | Customer and month | Total MRR and previous-month value |
| `fct_mrr_movements` | Customer and month | Revenue change by cause |
| `mart_monthly_revenue` | Month | Revenue bridge, NRR and churn |
| `mart_cohort_retention` | Signup cohort and month | Paying-customer retention |

`stg_periods` exposes the source columns and groups the period checks.
The marts are rebuilt as tables; the staging and customer-month models
are views. The larger demo produces 240,000 customer-month rows.

## Definitions

MRR is the subscription run rate on the first day of each month, in USD.
A price period includes its start date and excludes its end date.
Amounts use `NUMERIC`. Periods must begin and end at month boundaries.

Movements are classified per **customer**, after adding together that
customer's subscriptions. A first paid month is new revenue. Returning
after an inactive month is reactivation. A higher or lower amount for a
previously paying customer is expansion or contraction.

Net revenue retention (NRR) follows customers who paid in the previous
month:

```text
(opening MRR + expansion - contraction - churn) / opening MRR
```

New and returning customers do not contribute opening revenue. The first
month's NRR is `NULL` because its denominator is zero.

A cohort is the month of a customer's first subscription. Retention is
the share of that cohort paying in a later observed month. A customer
who returns counts again, so retention can rise. Future months have no
rows; observed inactive months have zero revenue.

More on the calendar and join decisions: [model notes](docs/DESIGN.md).

## Check the small example

```bash
python scripts/load_demo.py --fixture --reset
python scripts/load_demo.py --fixture
dbt build --profiles-dir .
pytest tests -q
```

| Month in 2024 | MRR | Change |
|---|---:|---|
| January | 270 | Three new customers |
| February | 270 | +80 new, -50 churn, -30 contraction |
| March | 430 | +40 new, +70 return, +50 expansion |
| April | 350 | -80 churn |
| May | 280 | -70 churn |

The fixture has five customers and six subscriptions. Customer A has
two subscriptions, C cancels and returns, and D downgrades. Integration
tests compare the marts with the values above. The calendar tests also
remove a month and trim the beginning of the calendar to verify that
dbt rejects both inputs.

dbt checks keys, relationships, valid periods, calendar coverage and the
revenue identity:

```text
closing MRR = opening + new + reactivation + expansion - contraction - churn
```

CI runs the fixture and the larger generated dataset on PostgreSQL 16
and 17. See [test runs](docs/VALIDATION.md).

## Query the results

```sql
SELECT month, mrr, new_mrr, expansion_mrr, churn_mrr,
       round(100 * net_revenue_retention, 2) AS nrr_percent
FROM analytics.mart_monthly_revenue
ORDER BY month;
```

This version assumes month-aligned prices in one currency. It does not
handle mid-month proration, annual billing, refunds or currency conversion.

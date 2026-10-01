# Test runs

The workflow runs on PostgreSQL 16 and 17. It imports the small fixture
twice, builds the models, checks the expected results, then rebuilds on
10,000 generated customers.

| Check | What it catches |
|---|---|
| dbt data tests | Keys, relationships, overlapping periods, missing calendar months and revenue reconciliation |
| Fixture integration tests | New vs returning revenue, downgrades, multiple subscriptions, cohort counts and duplicate imports |
| Calendar rejection tests | Gaps or a reporting range that starts after the first subscription |

The original version passed on both PostgreSQL versions in
[run 36841731070](https://github.com/parttimegod/parttimegod/actions/runs/36841731070).
The generated movement table had 240,000 rows.

For the latest revision, use the repository's
[Actions page](https://github.com/parttimegod/parttimegod/actions/workflows/warehouse.yml).
The workflow lives at the repository root because this project currently
sits under `projects/`. The copy inside this directory is for running
it as a separate repository.

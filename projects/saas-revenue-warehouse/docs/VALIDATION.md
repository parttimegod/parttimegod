# Validation

2026-10-01: local execution used PGlite (PostgreSQL compiled to WASM)
because native PostgreSQL could not start in the workspace. dbt 1.12.5
and dbt-postgres 1.11.0 built all five models; all 20 dbt tests passed
on the hand-checked fixture and on the 10,000-customer synthetic load.
All five fixture integration checks passed. The synthetic materialization
contained 240,000 customer-month records.

The local wire adapter disabled psycopg prepared statements to accommodate
PGlite's shared backend. This adapter is not part of the application.
These checks support SQL/model correctness, not native PostgreSQL
concurrency, production behavior or comparable performance measurements.

The included workflow runs the same fixture and synthetic checks on
native PostgreSQL 16 and 17. Consult its run status for that separate
verification; workflow configuration alone is not a passed result.

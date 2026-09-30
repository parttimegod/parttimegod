# EVDS data tools: retrieval, provenance, and time-series checks

## Problem and value

An AI client working with economic time series needs to find real series codes, retrieve observations, and report what a calculation means. Returning a plausible correlation without the transformation, lag, or stationarity context can mislead the user.

`evds-mcp` connects MCP clients to the Central Bank of Türkiye's EVDS database. Its optional PostgreSQL layer adds local history and fetch provenance.

This is an open-source portfolio project. It is not evidence of a production data platform or a causal-inference result.

## Implemented components

| Component | Behavior | Evidence |
| --- | --- | --- |
| MCP interface | Series discovery, retrieval, summaries, stationarity tests, relationship analysis | [server.py](https://github.com/parttimegod/evds-mcp/blob/6ca94d4aa43ee299d9e9eaaef2b37dc5fa143700/src/evds_mcp/server.py) |
| Statistical analysis | ADF checks, transformations, lag profiles, and applicable Engle-Granger tests | [analysis.py](https://github.com/parttimegod/evds-mcp/blob/6ca94d4aa43ee299d9e9eaaef2b37dc5fa143700/src/evds_mcp/analysis.py) |
| Relational storage | Series metadata, observations, and an audit row per fetch | [sema.sql](https://github.com/parttimegod/evds-mcp/blob/6ca94d4aa43ee299d9e9eaaef2b37dc5fa143700/src/evds_mcp/sema.sql) |
| Idempotent writes | Upsert keyed by series code and observation date | [depo.py](https://github.com/parttimegod/evds-mcp/blob/6ca94d4aa43ee299d9e9eaaef2b37dc5fa143700/src/evds_mcp/depo.py) |
| Calendar-aware lag | Build expected periods, left-join observations, then apply LAG | `takvim_gecikmeli_oku` in the same file |
| Database integration tests | Execute storage behavior against a disposable PostgreSQL 16 service | [Draft PR #1](https://github.com/parttimegod/evds-mcp/pull/1) |

## A design decision worth explaining

Suppose monthly observations are stored for January and March, with February absent. `LAG(value, 1)` over those rows gives January as March's previous value. That is the previous stored row, two months earlier.

The calendar-aware query generates the monthly grid and left-joins observations. February becomes a row with NULL. A one-period lag for March now refers to February, preserving the intended calendar meaning.

The implementation deliberately rejects calendar grids for business-day, weekly, and semimonthly frequencies when their calendars are not established. Row-based lag remains a separate operation with documented semantics.

See [data-quality SQL](https://github.com/parttimegod/evds-mcp/blob/6ca94d4aa43ee299d9e9eaaef2b37dc5fa143700/examples/sql/veri_kalitesi.sql) and [two-series comparison](https://github.com/parttimegod/evds-mcp/blob/6ca94d4aa43ee299d9e9eaaef2b37dc5fa143700/examples/sql/iki_seri_karsilastirma.sql).

## Evidence snapshot

Reviewed on **30 September 2026** at PR head `6ca94d4aa43ee299d9e9eaaef2b37dc5fa143700`.

[CI run](https://github.com/parttimegod/evds-mcp/actions/runs/36498651461):

- `postgres`: **15 passed, 106 deselected**, against PostgreSQL 16.
- `test`: **105 passed, 16 deselected**; Ruff passed.

The database tests cover upsert behavior, NULL handling, fetch audit rows, decimal preservation, and row-based versus calendar-based lag. See [test_depo.py](https://github.com/parttimegod/evds-mcp/blob/6ca94d4aa43ee299d9e9eaaef2b37dc5fa143700/tests/test_depo.py).

The counts are separate job results. They do not measure production load, live-API reliability, or performance at scale.

## Run the existing checks

```bash
git clone --branch codex/postgres-integration-ci-20260929 https://github.com/parttimegod/evds-mcp.git
cd evds-mcp
uv sync --extra depo
uv run pytest -q
```

For the database tests, provide a **disposable local PostgreSQL database**:

```bash
EVDS_TEST_DATABASE_URL='postgresql://postgres:postgres@127.0.0.1:5432/evds' uv run --extra depo pytest -m depo -q
```

The CI workflow provisions its own PostgreSQL 16 service; the local command above does not start a database. Offline and database tests do not require a live EVDS key. Actual EVDS retrieval does require an API key.

## Limits

Statistical warnings and transformations support interpretation; they do not establish causality. Automatic differencing is not a substitute for reviewing the series and analysis.

The database layer is optional library functionality. It is not automatically a cache used by every MCP request, and it is not a warehouse, scheduled pipeline, or dbt/Airflow deployment. Live API behavior and production-scale performance are separate from the tests reported here.

## What this project demonstrates

External-data integration, MCP interfaces, relational modeling, repeatable database writes, provenance, and statistical reasoning tied to code.

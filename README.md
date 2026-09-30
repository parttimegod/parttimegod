# Emirhan Bahçacı

**Python · Backend APIs · Document Automation · AI Tool Integration**

I build Python tools for document and economic-data workflows, with explicit validation, testable failure paths, and documented limits.

I am an econometrics student and court clerk based in Antalya, Türkiye. That background gives me firsthand exposure to document-heavy processes and a reason to question plausible-looking data results.

I am seeking remote Python backend and AI integration roles from Türkiye (UTC+3).

## Selected projects

### [Turkish document masking](https://github.com/parttimegod/kvkk-maskeleme)

A Python library and CLI for masking supported identifiers in Turkish text. The optional local-model layer handles names and addresses separately.

The [REST API draft](https://github.com/parttimegod/kvkk-maskeleme/pull/1) adds FastAPI input validation, a body limit checked before JSON parsing, generic errors that do not echo the submitted document, and a response that omits the restore mapping.

**Evidence:** its current PR CI run recorded **257 passing cases**, with 1 skipped and 7 expected failures. These are synthetic tests, not accuracy measurements on customer documents. The HTTP demo uses the pattern layer; names and addresses can remain, and every result requires human review.

[Case study](docs/document-masking.md) · [Two-minute demo](https://github.com/parttimegod/kvkk-maskeleme/blob/e8aa4faf4e5bf2ea793145631bc113053d3dae0e/API.md) · [CI run](https://github.com/parttimegod/kvkk-maskeleme/actions/runs/36709958631)

### [EVDS data tools for AI clients](https://github.com/parttimegod/evds-mcp)

An MCP server that lets AI clients discover, retrieve, and analyse Central Bank of Türkiye time series. Relationship analysis includes stationarity checks, transformations, lag analysis, and explicit warnings.

The optional PostgreSQL layer stores series metadata, observations, and fetch provenance. Calendar-aware lag queries distinguish a missing period from the previous stored row.

**Evidence:** the [PostgreSQL CI draft](https://github.com/parttimegod/evds-mcp/pull/1) runs **15 passing integration tests** against PostgreSQL 16; its separate offline job recorded 105 passing cases.

[Case study](docs/evds-data-tools.md) · [SQL examples](https://github.com/parttimegod/evds-mcp/tree/main/examples/sql) · [CI run](https://github.com/parttimegod/evds-mcp/actions/runs/36498651461)

## Technologies used in these repositories

Python, FastAPI, Pydantic, REST, MCP, pytest, GitHub Actions, PostgreSQL, and local-model integration.

The API adapter and PostgreSQL CI additions linked above are draft PRs, separate from each project's default branch. The case studies describe portfolio work and its tested scope.

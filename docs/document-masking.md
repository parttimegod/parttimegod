# Turkish document masking: a bounded REST interface

## Problem and value

Document-processing workflows can expose identifiers through the document itself, a restore mapping, or an error message. A reusable masking component needs a clear contract so another application can integrate it and understand what still requires review.

`kvkk-maskeleme` provides a library and CLI for Turkish text. Its HTTP adapter demonstrates how to expose the deterministic component through a small, local REST interface.

This is an open-source portfolio project with synthetic demo input. It is not a customer deployment or a claim of legal compliance.

## Interface and implementation

`POST /mask` accepts a JSON object with one nonblank Unicode string, `text`. It returns masked text, occurrence counts, category flags, and `manual_review_required: true`.

| Decision | Reason | Evidence |
| --- | --- | --- |
| Check actual body bytes before JSON parsing | A missing or inaccurate Content-Length must not bypass the accepted payload limit | `RequestBodyLimitMiddleware` in [api.py](https://github.com/parttimegod/kvkk-maskeleme/blob/e8aa4faf4e5bf2ea793145631bc113053d3dae0e/src/kvkk_maskeleme/api.py) |
| Separate 100,000-character text limit and 1 MiB body limit | Text characters and encoded JSON bytes are different quantities | `MaskRequest` and middleware in the same file |
| Return a generic validation error | Framework validation details can echo submitted input | `invalid_request` in the same file |
| Omit the restore mapping | The mapping contains original identifiers and is not needed by this HTTP contract | `MaskResponse` and `mask` in the same file |
| Require human review in every result | The endpoint only exposes the deterministic layer | `manual_review_required=True` in the same file |
| Keep model inference and storage outside this endpoint | A text-in/result-out demo does not need persistent state or inference | `mask` calls the existing library without a model provider |

The library uses patterns, applicable check digits, and context labels. It rescans masked output with its detector. That verification shares the detector's blind spots; it does not prove that all identifying information has been removed.

## Evidence snapshot

Reviewed on **30 September 2026** at PR head `e8aa4faf4e5bf2ea793145631bc113053d3dae0e`.

- [Draft PR #1](https://github.com/parttimegod/kvkk-maskeleme/pull/1): HTTP adapter, input boundaries, demo, and interview explanation.
- [CI run](https://github.com/parttimegod/kvkk-maskeleme/actions/runs/36709958631), job `test`: **257 passed, 1 skipped, 7 expected failures**; Ruff passed.
- [API tests](https://github.com/parttimegod/kvkk-maskeleme/blob/e8aa4faf4e5bf2ea793145631bc113053d3dae0e/tests/test_api.py) cover responses, supported formats, false positives, and verification errors.
- [Boundary tests](https://github.com/parttimegod/kvkk-maskeleme/blob/e8aa4faf4e5bf2ea793145631bc113053d3dae0e/tests/test_api_limits.py) cover actual and streamed body sizes, Unicode, independent requests, and tested file-writing behavior.

Test-case counts are not code-coverage percentages, field accuracy, or evidence of customer adoption. The skipped and expected-failure cases remain separate from the passing count.

## Reproduce the demo

The HTTP adapter is currently in the draft branch. Check out that branch before running its command:

```bash
git clone --branch codex/local-mask-api-20260928 https://github.com/parttimegod/kvkk-maskeleme.git
cd kvkk-maskeleme
uv run --locked --extra api uvicorn kvkk_maskeleme.api:app --host 127.0.0.1 --port 8000 --no-access-log
```

In another terminal:

```bash
curl -sS http://127.0.0.1:8000/mask \
  -H 'Content-Type: application/json' \
  -d '{"text":"Sağlık raporu için telefon: 0532 000 00 00; e-posta: kisi@example.test"}'
```

The phone and email are replaced by placeholders. The health context remains in the text and is flagged. Open [API.md](https://github.com/parttimegod/kvkk-maskeleme/blob/e8aa4faf4e5bf2ea793145631bc113053d3dae0e/API.md) for the expected JSON and two-minute demonstration.

## Scope

The HTTP demo does not expose the optional local-model layer. Names, addresses, institutions, unsupported formats, and identifying context can remain. Local-model recall figures in the project README do not describe this endpoint.

The documented command binds an unauthenticated demo to localhost. Accepted-payload limits and tested error paths are useful engineering controls, not a complete deployment-security guarantee.

## What this project demonstrates

A defined API contract, input validation before processing, careful error responses, automated verification, and a clear boundary between implemented behavior and remaining work.

---
id: F-CORE-003
title: Multiple weather providers with fallback
status: in-progress
owner: b0rgcube
created: 2026-06-15
last-updated: 2026-06-16
linked-story: "#3"
risk: medium
---

# Feature: Multiple weather providers with fallback

## Behaviour

`weatherbot show <city>` consults a chain of weather providers. The CLI tries providers in order; the first to return a `Reading` wins. If a provider raises a network error, returns a non-2xx response, or times out (3s), the CLI falls back to the next provider in the chain. The default chain is `RealProvider, MockProvider`; users can override via `WEATHERBOT_PROVIDERS` env var.

Failed provider calls are logged at WARNING with provider name + error class, so an on-call user can grep their terminal history.

## Scenarios

### SC-003-01 — Happy path: primary provider succeeds
- **Given** `WEATHERBOT_PROVIDERS=real,mock` and `RealProvider` returns a Reading
- **When** `weatherbot show Copenhagen` runs
- **Then** the result is the `RealProvider`'s reading; `MockProvider` is not called

### SC-003-02 — Fallback: primary fails, secondary succeeds
- **Given** `RealProvider` raises a network timeout
- **When** `weatherbot show Copenhagen` runs
- **Then** `MockProvider` is called and its reading is returned; the failure is logged

### SC-003-03 — All providers fail
- **Given** every provider in the chain raises an error
- **When** `weatherbot show Copenhagen` runs
- **Then** the CLI exits non-zero with a clear "no provider could fetch this city" message

### SC-003-04 — Provider timeout enforced
- **Given** `RealProvider` would hang indefinitely
- **When** `weatherbot show` is invoked
- **Then** the call times out after 3 seconds and falls back to the next provider

### SC-003-05 — Custom provider order honoured
- **Given** `WEATHERBOT_PROVIDERS=mock,real`
- **When** `weatherbot show Copenhagen` runs
- **Then** `MockProvider` is tried first; `RealProvider` only on its failure

### SC-003-06 — Unknown city handling *(open question — see below)*
- **Given** `RealProvider` is asked for a city that doesn't exist in its database
- **When** the call returns
- **Then** *(behaviour TBD — see Open Questions)*

## Out of Scope

- Caching (use F-CORE-002).
- Multiple API-key-required providers.
- Geographic provider routing.
- Retry of the same provider before falling back (we go straight to the next provider on error).

## Glossary

- **Provider chain**: the ordered list of providers `WEATHERBOT_PROVIDERS` resolves to.
- **Fallback**: trying the next provider after the current one fails or times out.
- **Provider error**: any exception raised by a provider's `fetch()`, including `requests.RequestException` and explicit `ProviderError`.

## Open Questions

| Question | Owner | Due | Status |
|----------|-------|-----|--------|
| What does `RealProvider` return for an unknown city? open-meteo seems to return 200 with empty results. Is "unknown city" a fallback trigger or a successful "no data"? | b0rgcube | 2026-06-18 | OPEN — see in-flight PR review |
| Should we cache the provider failures (negative cache) to avoid retry storms? | b0rgcube | — | parking until F-CORE-003 ships and we have data |

## Engineering Questions

- Is 3s the right timeout? Open-meteo p99 latency unknown to us.
- For testing: should we mock at the `requests` layer or define a `FakeRealProvider`? Current draft uses the latter.

## Non-Functional Requirements

- **Performance**: provider chain returns the *first* result within `(timeout × N) + ~10ms` worst case. Default chain length is 2; default timeout 3s; worst case ~6s.
- **Scale**: same as F-CORE-002.
- **Availability**: chain must degrade gracefully — no single-provider outage breaks the CLI.

## Dependencies

- **Related specs**: F-CORE-001, F-CORE-002
- **Code modules**: `src/weatherbot/providers.py` (extended with `RealProvider`), new `src/weatherbot/chain.py`

## Revision History

| Rev | Date       | Author    | Change |
|-----|------------|-----------|--------|
| 1   | 2026-06-15 | b0rgcube  | Initial draft |
| 2   | 2026-06-16 | b0rgcube  | Added SC-003-06 placeholder for unknown-city question raised in PR review |

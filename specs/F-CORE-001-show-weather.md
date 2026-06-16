---
id: F-CORE-001
title: Show weather for a city
status: implemented
owner: b0rgcube
created: 2026-06-10
last-updated: 2026-06-12
linked-story: "#1"
risk: low
---

# Feature: Show weather for a city

## Behaviour

A user invokes `weatherbot show <city>` from a terminal. The CLI fetches a current weather reading for the city via a configured provider and prints a one-line summary: city, temperature in Celsius, and a short text description (e.g. "clear", "rainy"). The exit code is `0` on success and non-zero on any failure.

The first version uses a `MockProvider` that returns deterministic results without network access — the demo's point is the workflow, not the actual weather data. A real-API provider arrives in F-CORE-003.

## Scenarios

### SC-001-01 — Happy path: show weather for a known city
- **Given** the user has installed `weatherbot`
- **When** they run `weatherbot show Copenhagen`
- **Then** stdout contains "Copenhagen", a temperature in `°C`, and a description; exit code is `0`

### SC-001-02 — Deterministic mock provider
- **Given** the mock provider is in use
- **When** `show` is called twice in a row with the same city
- **Then** the output is byte-identical between calls

### SC-001-03 — Failure case: empty city argument
- **Given** the user runs `weatherbot show ""`
- **When** the command executes
- **Then** the command writes an error message to stderr and exits non-zero

### SC-001-04 — Failure case: whitespace-only city
- **Given** the user runs `weatherbot show "   "`
- **When** the command executes
- **Then** treated the same as empty: error to stderr, non-zero exit

## Out of Scope

- Real network calls to a weather API (deferred to F-CORE-003).
- Caching of results across invocations (covered by F-CORE-002).
- Pretty-printed / coloured output (separate F-UX-005 — backlog only).
- Multi-city batch lookups.

## Glossary

- **Reading**: a point-in-time `(city, temperature_c, description)` tuple returned by a provider.
- **Provider**: anything that implements the `WeatherProvider` protocol.
- **MockProvider**: deterministic mock used by default in v0.1.

## Open Questions

| Question | Owner | Due | Status |
|----------|-------|-----|--------|
| Should we support Fahrenheit later? | b0rgcube | — | resolved — not in v0.1; revisit if user demand |

## Engineering Questions

- Where does provider configuration come from in v0.1? (Resolved during refinement: hardcoded MockProvider; envvar-based selection in F-CORE-003.)
- What's the error contract? (Resolved: ValueError → stderr + exit code 2.)

## Non-Functional Requirements

- **Performance**: command completes in <50ms with the mock provider.
- **Scale**: single-user CLI; no concurrency considerations for v0.1.
- **Availability**: mock provider has no external dependencies; never fails for a non-empty city.

## Dependencies

- **Related specs**: F-CORE-002 (caching), F-CORE-003 (real provider with fallback)
- **ADRs**: none
- **Code modules**: `src/weatherbot/cli.py`, `src/weatherbot/providers.py`, `tests/test_show_sc_001.py`

## Revision History

| Rev | Date       | Author    | Change |
|-----|------------|-----------|--------|
| 1   | 2026-06-10 | b0rgcube  | Initial draft |
| 2   | 2026-06-12 | b0rgcube  | Added SC-001-04 (whitespace) after adversary pass; status → implemented |

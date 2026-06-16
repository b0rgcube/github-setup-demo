---
id: F-CORE-002
title: Cache weather readings for 10 minutes
status: implemented
owner: b0rgcube
created: 2026-06-12
last-updated: 2026-06-14
linked-story: "#2"
risk: low
---

# Feature: Cache weather readings

## Behaviour

When a user runs `weatherbot show <city>`, the result is cached locally on disk. A subsequent `show` for the same city within the cache TTL returns the cached `Reading` instead of calling the provider again. The default TTL is 10 minutes; it can be overridden via the `WEATHERBOT_CACHE_TTL_SECONDS` env var.

The cache is a simple file at `~/.cache/weatherbot/cache.json`. Entries expire by wall-clock UTC time. A `weatherbot cache clear` command empties the cache.

## Scenarios

### SC-002-01 — Happy path: second call within TTL hits cache
- **Given** a fresh cache; user has run `weatherbot show Copenhagen` at t=0
- **When** the user runs `weatherbot show Copenhagen` at t=120 (within TTL=600)
- **Then** the second call returns the same `Reading` without calling the provider

### SC-002-02 — Cache expires at TTL boundary
- **Given** a cached reading at t=0 with TTL=600
- **When** the user runs `weatherbot show Copenhagen` at t=601
- **Then** the cache miss triggers a fresh provider call; the new reading is cached

### SC-002-03 — Cache survives across invocations
- **Given** the user ran `weatherbot show Copenhagen`, then exited the process
- **When** the user runs `weatherbot show Copenhagen` again in a new process within TTL
- **Then** the second call hits the cache (proves disk-backed, not in-memory only)

### SC-002-04 — Cache uses UTC; immune to local-time DST shifts
- **Given** the system clock crosses a DST boundary while a cache entry is alive
- **When** TTL math is applied
- **Then** the entry expires at the correct wall-clock moment regardless of local-time discontinuity

### SC-002-05 — `cache clear` empties the cache
- **Given** the cache contains entries
- **When** the user runs `weatherbot cache clear`
- **Then** the cache file is removed (or emptied) and subsequent calls miss

### SC-002-06 — Cache file gracefully handles corruption
- **Given** the cache file exists but is malformed JSON
- **When** the user runs `weatherbot show <city>`
- **Then** the corrupted cache is silently discarded and the call proceeds to the provider; a fresh entry is written

## Out of Scope

- Cache eviction (size or count limits) — for now, unbounded.
- Per-city TTL overrides.
- Distributed / shared cache (single-user CLI).

## Glossary

- **Cache hit**: a `show` call that finds a non-expired entry for the requested city.
- **Cache miss**: no entry, or entry expired — provider is called.
- **TTL**: time-to-live, in seconds. Default 600.

## Open Questions

| Question | Owner | Due | Status |
|----------|-------|-----|--------|
| 10-min default — is that right? | b0rgcube | — | open; revisit after first user feedback |

## Engineering Questions

- Where does the cache file live? (Resolved: `~/.cache/weatherbot/cache.json`, falling back to `$XDG_CACHE_HOME` if set.)
- What if the cache directory is not writable? (Graceful degradation: log a warning, skip caching, still return live results.)

## Non-Functional Requirements

- **Performance**: cache hit < 5ms; cache miss adds <10ms over provider latency.
- **Scale**: ~10k cities trivial; performance degradation only above 100k entries.
- **Availability**: cache failure must not break the CLI — degrade to no-cache mode.

## Dependencies

- **Related specs**: F-CORE-001 (the fetch path being cached)
- **Code modules**: `src/weatherbot/cache.py`, `src/weatherbot/cli.py`, `tests/test_cache_sc_002.py`

## Revision History

| Rev | Date       | Author    | Change |
|-----|------------|-----------|--------|
| 1   | 2026-06-12 | b0rgcube  | Initial draft |
| 2   | 2026-06-14 | b0rgcube  | Added SC-002-04 (DST) and SC-002-06 (corruption) after adversary pass |

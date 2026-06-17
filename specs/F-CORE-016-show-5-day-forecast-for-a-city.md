---
id: F-CORE-016
title: Show 5-day forecast for a city
status: draft
owner: b0rgcube
created: 2026-06-17
last-updated: 2026-06-17
linked-story: "#16"
risk: low
---

# Feature: Show 5-day forecast for a city

> **Auto-generated stub** by the spec-pr-from-story workflow.
> Edit this file in this PR to flesh out the spec, then mark the PR
> ready for review. The story body is reproduced below for context.

## Behaviour

*(Plain English. Present tense. What the feature does — not how.)*

TODO: describe the behaviour.

## Scenarios

### SC-016-01 — Happy path: ...
- **Given** ...
- **When** ...
- **Then** ...

### SC-016-02 — Edge case: ...
- **Given** ...
- **When** ...
- **Then** ...

### SC-016-03 — Failure case: ...
- **Given** ...
- **When** ...
- **Then** ...

## Out of Scope

*(What this feature does NOT do. Be specific.)*

- TODO

## Glossary

*(Domain terms used above.)*

- **<Term>**: <definition>

## Open Questions

| Question | Owner | Due | Status |
|----------|-------|-----|--------|
| TODO | | | open |

## Engineering Questions

*(Questions for engineering. Never feasibility verdicts.)*

- TODO

## Non-Functional Requirements

- **Performance**: TODO
- **Scale**: TODO
- **Availability**: TODO

## Dependencies

- **Related specs**: TODO
- **Code modules**: TODO

## Revision History

| Rev | Date | Author | Change |
|-----|------|--------|--------|
| 1   | 2026-06-17 | github-actions[bot] | Auto-generated stub from issue #16 |

---

## Source story (auto-copied from issue #16)

*Title:* [Story] Show 5-day forecast for a city

*Body:*

```
## User story
As a CLI user, I want to run `weatherbot forecast <city>` and see a 5-day forecast (one row per day), so that I can plan ahead without checking each day separately.

## Acceptance criteria
- `weatherbot forecast Copenhagen` prints 5 rows, one per upcoming day
- Each row has date, high/low temperature, and a description
- Empty/whitespace city → clear error and non-zero exit (matches F-CORE-001 behaviour)
- Forecast is cached with the same TTL as F-CORE-002

## Out of scope
- Hourly forecasts (separate story)
- Configurable forecast length (default 5; not parametrised in v1)
- Pretty-print/colors (F-UX-005)

## Code touched
- backend

## Notes
- Filed to test the spec-pr-from-story workflow. Expect a draft spec PR within ~30s of filing.
```

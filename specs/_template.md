<!--
  Copy this file to specs/F-{AREA}-{NNN}-{slug}.md when starting a new spec.
  See docs/WORKFLOW.md § "Spec" for when a spec is required vs. when the issue's
  acceptance criteria suffice.
-->

---
id: F-{AREA}-{NNN}                # AREA: CCS / VAL / INGEST / PLATFORM (NovoScribe) — extend per project
title: <feature name>
status: draft                     # draft | approved | in-progress | implemented | deprecated
owner: <PO or tech lead>
created: <YYYY-MM-DD>
last-updated: <YYYY-MM-DD>
linked-story: <#NNN>
risk: low                         # low | medium | high  (see docs/GXP_UPGRADE_PATH.md if regulated)
---

# Feature: <name>

## Behaviour

Plain English. Present tense. What the feature does — not how. Avoid implementation detail; that lives in code, not here.

## Scenarios

Each scenario has a stable id (`SC-{NNN}-{NN}`) that tests will reference. **Do not renumber existing scenario ids** once the spec is approved — tests bind to them.

### SC-{NNN}-01 — Happy path: <name>
- **Given** <starting state, in plain language>
- **When** <user action or system trigger>
- **Then** <expected outcome>

### SC-{NNN}-02 — Edge case: <name>
- **Given** ...
- **When** ...
- **Then** ...

### SC-{NNN}-03 — Failure case: <name>
- **Given** ...
- **When** ...
- **Then** ...

## Out of Scope

Explicit. What this feature does NOT do. Save downstream rework by being specific.

## Glossary

Domain terms used above. Definitions exist *here* so they don't drift across rewrites.

- **<Term>**: <definition>

## Open Questions

Pending decisions before development can finish. Each with an owner and a date.

| Question | Owner | Due | Status |
|----------|-------|-----|--------|
| <question> | <name> | <YYYY-MM-DD> | open / resolved |

## Engineering Questions

Things engineering will weigh in on during refinement. **Questions, not feasibility verdicts.** The team that knows the real constraints isn't represented here yet.

- <question>
- <question>

## Non-Functional Requirements

The non-functional requirements — most often skipped, most often the cause of late-stage rework. Even "TBD" is more useful than blank.

- **Performance**: <e.g. p95 < 200 ms>
- **Scale**: <e.g. ~10k snippets, ~100 rotations/min>
- **Retention**: <e.g. all prior versions kept for 30 days>
- **Availability**: <e.g. degrade gracefully if X is down>
- **Regulatory**: <leave blank unless concrete; do not assume GxP applies until confirmed>

## Dependencies

- **Related specs**: <F-IDs>
- **ADRs**: <ADR-NNN if any>
- **Code modules**: <paths the feature lives in or touches>

## Revision History

| Rev | Date | Author | Change |
|-----|------|--------|--------|
| 1   | <YYYY-MM-DD> | <name> | Initial draft |

---

> **This is a contract.** Tests reference scenario ids; reviewers verify the implementation matches the Behaviour. If the spec changes after `approved`, increment the revision and update the history — don't rewrite silently.

---
date: 2026-06-13
incident: Cache TTL stuck for 1 hour after EU DST transition
severity: P0
duration: ~1 hour (user-impact window after DST spring-forward)
related: bug #7, hotfix PR #13
---

# What happened

After the EU spring-forward DST transition on 2026-03-29 at 02:00 UTC (which is 03:00 local in CET), users running `weatherbot show` saw 1-hour-stale cache entries for any city they'd queried in the previous 10 minutes. Affected users in Europe got cloudy data when conditions had visibly changed; one user reported it via the team channel.

# Timeline

```
2026-03-29 01:30 UTC  — Pre-DST. weatherbot v0.2.0 deployed for ~3 days.
                        Users querying cities; cache populated normally.

2026-03-29 02:00 UTC  — EU DST transition (clocks jump 02:00 → 03:00 local).

2026-03-29 02:01 UTC  — First post-DST query. Cache entry from 01:50 UTC
                        (10 min ago wall-clock) appears to be 1h 10min ago
                        in the local-time arithmetic. So entries from up to
                        1h ago are still being served as "fresh".

2026-03-29 02:30 UTC  — A user pings the team channel: "weather is wrong,
                        showing me 30 min stale data."

2026-03-29 02:35 UTC  — Tech lead (b0rgcube) acknowledges; investigation begins.

2026-03-29 02:55 UTC  — Root cause identified: `cache._now_utc()` was actually
                        `datetime.now()` (naive local time) at the time of the
                        regression. The function name was correct; the
                        implementation was not.

2026-03-29 03:05 UTC  — Hotfix PR #13 opened. Branch from main, single-line
                        fix to use `datetime.now(timezone.utc)`.

2026-03-29 03:15 UTC  — PR reviewed (self, with explicit acknowledgement that
                        in real adoption this would have a second pair of
                        eyes). Tests added. CI green.

2026-03-29 03:25 UTC  — Merged. v0.2.1 tagged. Deploy started.

2026-03-29 03:40 UTC  — Production fully rolled. Cache wall-clock arithmetic
                        is UTC throughout. User confirms fix.
```

Total user-impact window: ~1h 40min from DST transition to fix in production. Customer escalation: 1 user reported.

# Root cause

The `_now_utc()` function in `cache.py` was originally written as:

```python
def _now_utc():
    return datetime.now().timestamp()
```

The name said "UTC" but the implementation used naive `datetime.now()`, which uses the system local timezone. On a system in CET, `.timestamp()` of a naive datetime is interpreted as local time, then converted to a UTC epoch — adding an hour offset that drifts at DST transitions.

The bug shipped because:
1. The unit tests for SC-002-01/02/03 ran in a single time window — none crossed a DST boundary, so the naive datetime worked.
2. SC-002-04 (DST immunity) was added to the spec only *after* the F-CORE-002 PR was merged — see PR #11 review thread. The test for SC-002-04 was implemented but the CI didn't catch the regression because the test suite doesn't simulate clock changes.

# What worked

- **The bug was caught by a real user, not a runtime crash.** Pages weren't going off; users were just getting stale data. That's the expected failure mode — degraded behaviour, not outage.
- **Cache module's "fail soft" design** meant the degraded cache didn't crash the CLI. Stale data is bad; a crash on every query would be worse.
- **Clear scenario-ID convention** made the spec issue searchable. SC-002-04 was already in the spec from rev 2; the *test* covering it had a bug (used naive datetime), not the spec.
- **Hotfix path** worked as designed. From bug-report to fix-in-prod: 1h 5min.

# What didn't work

- **The SC-002-04 test was a tautology:** it asserted `cached_at_utc > 0`, which any datetime call would satisfy. The test passed on a buggy implementation. *This is the most important finding.*
- **The CI doesn't simulate clock changes.** No test suite frame-of-reference travels across a DST boundary; this class of bug is invisible at PR time. Adding clock-frozen-at-DST tests would have caught this.
- **The function name lied.** `_now_utc()` returned a non-UTC value. Names that lie are a recurring source of bugs; the reviewer (self) didn't notice the mismatch.

# Lessons / actions

- [x] Action 1 — **Fix the bug** (PR #13). DONE.
- [x] Action 2 — **Strengthen the SC-002-04 test** to actually exercise the DST behaviour, not just assert a positive timestamp. Test now uses `freezegun` to assert behaviour across a simulated DST transition. (owner: b0rgcube; landed in PR #13)
- [ ] Action 3 — **Add a "names that lie" review checklist item.** When a function name asserts a property (`_now_utc`, `is_valid`, `safe_cast`), the reviewer must verify the implementation matches the assertion. (owner: b0rgcube; due 2026-06-30; tracked: not yet a separate issue, will file)
- [ ] Action 4 — **Audit other places that use `datetime.now()`** in the codebase. (owner: b0rgcube; due 2026-06-25; tracked: filing follow-up issue)
- [ ] Action 5 — **Consider adding `freezegun` to the test deps** as a standard tool, not just for cache tests. Many time-sensitive bugs follow this pattern. (owner: b0rgcube; due next sprint; tracked: filing follow-up issue)

# What this incident did NOT teach us

A few things to be honest about:
- We didn't learn that "DST is hard." We knew that. The lesson is about *test design*, not about timezones.
- We didn't learn that we need QA. The bug shipped despite the test claiming to cover SC-002-04. Adding a QA function wouldn't have caught it; reviewing tests for *what they actually assert* would have.
- This isn't a process failure of the github-setup workflow itself. The PR template was filled in correctly; the spec was cited; the test was written and ran green. The *test was insufficient* — a design failure, not a process failure. The action items above strengthen the design.

The incident is closed once Actions 3, 4, and 5 are in flight.

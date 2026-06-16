# Hotfix and bugs

How bugs get reported, triaged, and fixed. How a 3am-production-down hotfix bypasses the normal flow safely. What happens after the fire is out.

---

## Bug intake

Bugs come from three places:

1. **The team itself**, finding a defect in their own code (most common).
2. **Internal stakeholders** (sales, support, ops) reporting customer-impact issues.
3. **Production monitoring / on-call** when something fails outside what the team noticed.

All three file the same way: a GitHub Issue using the `bug` template.

### The bug issue template

The `bug.yml` template (in `templates/.github/ISSUE_TEMPLATE/`) requires:

```
Title:                <one-line description, customer-facing impact if any>
Severity:             P0 / P1 / P2 / P3
Stack:                backend / frontend / worker / infra / other
Linked spec:          F-{AREA}-{NNN} (if violated; "no spec / unknown" otherwise)
Repro steps:          1. … 2. … 3. …
Expected behaviour:   <what should have happened>
Actual behaviour:     <what did happen>
Environment:          prod / staging / dev / local
First seen:           <date or commit if known>
Logs / screenshots:   <attachments>
```

Reporters who can't fill all of these in (e.g. a non-technical stakeholder) get help from the dev who picks it up. The PO doesn't have to do this — they triage; devs investigate.

### Severity guide for bugs

| Severity | Definition | Response |
|---|---|---|
| `P0 — now` | Production broken; users impacted; data corruption; security incident | Drop everything; fix path = hotfix (see below) |
| `P1 — this sprint` | User-facing defect; degraded experience; spec violated | Goes into current sprint; not hotfixed |
| `P2 — next sprint` | Internal-facing defect; minor user-facing issue; deviates from intent without breaking | Next sprint commitment |
| `P3 — someday` | Cosmetic; rare edge case; theoretical issue | Backlog; may be closed if it stays P3 indefinitely |

The PO sets bug severity. Tech lead may suggest re-prioritization with rationale; PO decides.

---

## Triage cadence for bugs

- **P0:** within hours of report. Hotfix path triggered immediately.
- **P1 / P2:** during normal weekly triage (see `BACKLOG_AND_PRIORITIZATION.md`). Same column flow as stories.
- **P3:** logged, ignored unless they accumulate evidence. The `stale-issues` workflow surfaces them quarterly.

A bug filed on Friday afternoon with `P0` severity wakes someone up. Use it accordingly. False `P0`s erode the team's trust in the signal; under-marking a real `P0` causes preventable harm.

---

## Normal bug fix path

For `P1`, `P2`, `P3` bugs — the workflow is identical to a regular story.

1. Bug issue is filed and triaged.
2. PO sets priority; bug enters the same `Backlog → Triaged → Ready` flow as stories.
3. Refinement: dev investigates; the issue body is updated with root cause + fix sketch before being marked `Ready`.
4. Sprint planning (or kanban pull) picks it up.
5. Standard branch + PR + review + merge cycle.
6. **Definition of Done is the same.** The PR template is the same. CI is the same.

### One difference: spec follow-up

When a bug is fixed, ask: *did this bug indicate a missing spec scenario?*

- **Often yes.** A bug usually means there was an edge case the spec didn't cover, or the spec was wrong about what should happen.
- **The fix-PR adds the missing scenario** to the spec, plus a test marker for it.
- **The spec gets an entry in its Revision History** noting the new scenario was added because of bug #NNN.

The bug-fix is then visible in the spec's revision trail — you can search the spec history and see "this scenario was added because we hit it in production."

If the spec genuinely didn't need an update (the bug was a clear violation of an existing scenario, just due to a coding error), the spec doesn't change. But ask the question every time.

---

## Hotfix path — for P0 only

Production is broken; users are impacted; the on-call has been paged. The normal flow is too slow.

### When the hotfix path is justified

All three must be true:

- **Production is materially impacted.** Not "could be impacted"; not "looks degraded." Actual user impact, or customer-side error, or data integrity at risk.
- **Waiting hours-to-days for the normal flow makes the impact worse.** A P0 that can wait until tomorrow morning's PR review is a P1.
- **The fix is small and well-understood.** A hotfix that requires architectural rework is a sign the patch isn't actually fast — a clean revert (see below) might be the real hotfix.

If any of these isn't true, use the normal flow. The hotfix path has a deferred-obligation cost; don't pay it unnecessarily.

### The path

```
                        Production broken
                              │
                              ▼
                  ┌───────────────────────┐
                  │   On-call assesses    │
                  │   - revert possible?  │
                  │   - small fix possible?│
                  └───────────┬───────────┘
                              │
                              ├──────────────────┐
                              ▼                  ▼
                       ┌──────────────┐   ┌──────────────┐
                       │   REVERT     │   │   HOTFIX     │
                       │   (preferred) │   │   (small fix)│
                       └──────┬───────┘   └──────┬───────┘
                              │                  │
                              └─────────┬────────┘
                                        ▼
                            ┌────────────────────────┐
                            │ Branch from main:      │
                            │ hotfix/<short-slug>    │
                            └────────────┬───────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ PR with [hotfix] tag,  │
                            │ links to incident      │
                            └────────────┬───────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Fast-track review:     │
                            │ ANY available IC       │
                            │ approves; tech lead    │
                            │ informed in parallel   │
                            └────────────┬───────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Merge to main; deploy  │
                            └────────────┬───────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Verify in production   │
                            └────────────┬───────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ MANDATORY follow-up    │
                            │ within 24h (see below) │
                            └────────────────────────┘
```

### Revert is preferred

If the bug was introduced by a recent merge, **revert that merge first**. A revert is faster, safer, and easier to reason about than a forward-fix.

```bash
git revert <bad-merge-commit-sha>
git push origin hotfix/revert-<short-slug>
```

Open the revert PR with `[hotfix-revert]` in the title. Same fast-track review; merge; deploy.

The forward-fix-as-real-story is then filed as a follow-up `P1` issue. The revert buys you time to fix it correctly.

### Hotfix PR template

The PR template auto-populates a hotfix-specific block when the title starts with `[hotfix]`:

```
## HOTFIX
- [ ] Linked incident: #NNN (or external incident reference)
- [ ] Linked story / bug issue: #NNN
- [ ] Smallest viable change confirmed (no scope creep)
- [ ] Tested locally (output pasted)
- [ ] Risk of this change: <one paragraph>
- [ ] Rollback plan: <one sentence>
- [ ] **Follow-up issue filed for full DoD compliance:** #NNN
```

The full Definition of Done checklist is **deferred**, not waived. The follow-up issue (next section) is mandatory.

### Fast-track review

- **Any IC** can review and approve a hotfix PR. CODEOWNERS still routes for visibility, but the rule "wait for the routed reviewer" is suspended.
- **Tech lead is informed in parallel** (Slack/Teams ping, not blocking). Tech lead can ask for additional review later but doesn't gate the merge.
- **Two-person rule still holds**: someone other than the author approves. A solo merge bypasses the only safety net the team has.

### Mandatory follow-up within 24 hours

Within 24 hours of the hotfix merging, the author files a follow-up issue and PR:

- The follow-up PR brings the hotfix into full Definition of Done compliance:
  - Tests added (regression test for the bug; adversarial tests for the area).
  - Spec updated with the missing scenario.
  - Operator pass: any logging or metrics that should have caught this earlier.
  - Documentation updated if needed.
- The follow-up PR is normal-flow: full template, full CI, regular review.

If the follow-up isn't filed within 24h, **the team has a process violation**. Tech lead surfaces it at the next daily / standup. Three violations in a quarter = retro topic about whether the hotfix path is being abused.

---

## Post-mortem for P0 incidents

After every `P0` (whether it required a hotfix or just a same-day fix), within one week:

### The post-mortem doc

Lives at `docs/postmortems/<YYYY-MM-DD>-<short-slug>.md`. Template:

```
---
date: YYYY-MM-DD
incident: <short title>
severity: P0
duration: <minutes / hours>
related: bug #NNN, hotfix PR #NNN, follow-up PR #NNN
---

# What happened
Short narrative, no jargon.

# Timeline
HH:MM — <event>
HH:MM — <event>
…

# Root cause
The actual cause. Not the symptom.

# What worked
What about our process / tools / monitoring did its job.

# What didn't work
What slowed us down or made it worse.

# Lessons / actions
- [ ] Action 1 (owner: name; due: date; tracked: #NNN)
- [ ] Action 2
…
```

### Post-mortem culture

- **No blame.** Name systems, processes, tools. Avoid naming individuals as the cause.
- **Honest about what didn't work.** "Our monitoring didn't catch this" is more useful than "we should have noticed sooner."
- **Actions have owners and dates.** A post-mortem with "we should..." actions is a wishlist, not a learning loop.
- **Open by default.** All team members can read. Stakeholders may be invited to read for major incidents.

### Post-mortem cadence

- Major P0 (≥1 hour customer impact, OR data integrity affected, OR security incident): full post-mortem within 1 week.
- Minor P0 (transient, contained, no customer impact): one-pager in the post-mortem folder; no formal review.
- Recurring pattern (3 minor P0s of similar shape in a quarter): elevate to full post-mortem on the *pattern*, not any one incident.

---

## Tracking and visibility

The PO sees all bug counts on the Project board. A weekly digest can be set up via Actions if the team wants quantitative pulse.

For the team's own use:

- `P0` incidents per quarter (target: small, declining)
- Time-to-triage for new bugs (target: ≤1 day for P1)
- Time-to-fix for P1 bugs (target: within current sprint)
- Hotfix follow-up filed within 24h (target: 100%)

These metrics are for the team's retro, not for management dashboards. Don't let them become performance metrics.

---

## What this doc explicitly leaves to the team

- **On-call rotation mechanics.** Who's on-call, how rotation works, what tools alert them. Different teams have different setups; this is your team's decision.
- **Specific incident-management tooling.** PagerDuty, Opsgenie, internal tooling — this doc doesn't prescribe.
- **Customer communication.** Status pages, customer emails, public incident reports — these are product / comms decisions outside the engineering team's process.
- **External SLA commitments.** If you have customer SLAs, those override this doc's `P0` definition. (P0 in this doc is "production materially impacted"; SLA-defined P0 may be tighter.)

The bug intake, triage, hotfix, and post-mortem patterns are this doc's contribution. Everything else is yours.

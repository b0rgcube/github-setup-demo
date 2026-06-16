# Definition of Done

**This is the most important doc in the setup. Read it carefully.**

the demo team has no QA function. The Definition of Done is what compensates. If the dev didn't tick all of these, the story is not done — no matter what the assignee feels, no matter what the dashboard says.

This is non-negotiable. The PR template enforces every item with a required checkbox. The CI's PR-template lint refuses to merge if any required checkbox is unticked.

---

## The required checklist

Every PR. Every time. No exceptions.

```
[ ] Linked story issue (#NNN) — closes via "Closes #NNN" syntax
[ ] Linked spec (specs/F-{AREA}-{NNN}-*.md) if non-trivial — or "no spec required: {one-line reason}"
[ ] All acceptance criteria from the story have matching tests
[ ] Each spec scenario (SC-{NNN}-{NN}) has at least one test marker referencing it
[ ] Adversarial pass done by author — see ADVERSARY CHECKLIST below
[ ] Tests run locally; output pasted in PR description (or CI run linked)
[ ] No new lint warnings
[ ] No new TODO without owner+date
[ ] Operator pass — see OPERATOR CHECKLIST below
[ ] Out-of-scope items NOT silently expanded
[ ] Documentation/README updated if user-facing or onboarding-relevant
[ ] Reviewer can verify with: <exact command(s)>
```

The CI lint reads the PR body for these checkboxes. **An unticked required checkbox blocks merge.**

---

## Adversary checklist (sub-list under "Adversarial pass done by author")

The dev attacks their own code before opening the PR. This is the single most load-bearing piece of the no-QA compensation. The reviewer is in adversary stance later, but the *first* adversary is the author.

```
[ ] Boundary inputs tested: empty, single, max size, off-by-one
[ ] Contract violations tested: wrong type, None where value expected, malformed shape
[ ] Failure modes tested: external service down, timeout, partial result
[ ] Concurrency considered: two writers, stale read, ordering — tested if applicable;
    explicit "deferred to integration tests" finding if not unit-testable
[ ] Spec failure-case scenarios (SC-* failure cases) all have negative-path tests
[ ] If new failure modes were discovered during this work, they are added to the
    spec (in a follow-up commit on the spec file or a follow-up spec PR)
```

If the dev legitimately can't test something at the unit level, name it. "SC-042-08 (concurrent rotation under load) requires integration testing — filed as follow-up #NNN" is a valid line. Silent omission is not.

See `REVIEW_AS_ADVERSARY.md` for the reviewer's adversary pass that comes after.

---

## Operator checklist (sub-list under "Operator pass")

Code that ships gets paged on. the demo team runs production workers, ingestion pipelines, and a customer-facing API; almost every story touches code that will run on someone's pager schedule.

```
[ ] Every log line in changed code names the relevant entity:
    - Request id, user id, resource id, batch id — whatever applies
    - "validation failed" alone is a bug; "validation failed: customer_id missing,
      request_id=abc-123, endpoint=POST /orders" is doing its job
[ ] Errors distinguish faults: user-input vs internal vs third-party
    - The on-call should know whose problem it is from the log line alone
[ ] Hot-path operations have at least count + latency + failure-by-class metrics
    - Skip if the project doesn't have a metrics library wired in; flag the gap
[ ] Side-effect-producing calls (DB writes, external API calls) are safe to retry
    - OR explicitly documented as not retry-safe with a comment + reason
[ ] Error messages give the on-call a path forward — context, an error code that
    maps to a runbook, or a clear "what to do next"
```

If the change is purely internal (a refactor of a private helper, a test-only change, a doc-only change), tick "operator pass" and add a one-line "operator-irrelevant: {reason}" — don't pretend the checklist applies.

For ship-ready code (the default for stories): the items above are mandatory, not aspirational.

---

## What "trivial" means (and when items relax)

A "trivial story" is one where most of this checklist is overkill. Examples:

- Doc-only change.
- Typo fix.
- Renaming a private variable.
- Adding a single log line that was missed in a prior PR.
- Updating a dependency to a patch version.

For trivial stories:

- The PR template still loads with all items.
- The dev ticks "trivial change — N/A" for items that genuinely don't apply, with a one-line reason for *why* they don't apply.
- The CI lint accepts "N/A" with a reason as a valid tick.
- The reviewer's job is to disagree if "trivial" is overclaiming.

**The default is non-trivial.** Devs should err toward filling the checklist; reviewers should err toward asking "is this really N/A, or is it just inconvenient?"

If the reviewer disagrees that something is trivial, the dev does the work. There is no escalation path past this — the workflow trusts the reviewer's read.

---

## What's enforced by CI vs. enforced by review

| Check | Enforced by |
|---|---|
| All checkboxes ticked (or N/A with reason) | CI (PR-template lint) |
| Every `SC-{NNN}-{NN}` referenced in changed test files exists in a spec | CI (`spec-lint.yml`) |
| Every `SC-{NNN}-{NN}` in an "approved" or "implemented" spec has at least one test marker | CI (`spec-lint.yml`) |
| Tests pass | CI (`pr-checks.yml`) |
| Lint passes | CI (`pr-checks.yml`) |
| Adversary list is *credible* (not "checked" with no actual adversarial tests) | Reviewer |
| Operator list is *credible* | Reviewer |
| Out-of-scope wasn't silently expanded | Reviewer |
| Spec scenarios are actually covered, not just marker-tagged | Reviewer (verify by reading the test) |
| Documentation actually reflects the change | Reviewer |

CI catches the *mechanical* gaps; the reviewer catches the *honest* ones. Neither alone is enough.

---

## What "Done" means after merge

The story is **Done** when:

- PR is merged.
- Story issue is closed (auto-closed via `Closes #NNN`).
- Spec status (if any) is `implemented` (one-line follow-up spec PR).
- Any follow-up issues filed during the work (spec gaps, deferred tests, infrastructure asks) are linked back to the original story.

**Not done:**
- "Code is merged but the test failure is intermittent" → not done; the test is a defect.
- "It's deployed to staging but not prod" → not done if your default is "story = in production." (If your default is "story = in staging", say so explicitly in your repo's `CONTRIBUTING.md`.)
- "It works on my machine" → not done.

---

## What if the team disagrees with this checklist?

This list is a starting point; teams own their Definition of Done. To change an item:

1. Open a PR against this `DEFINITION_OF_DONE.md` file.
2. Tech lead reviews; PO is asked.
3. Merge with rationale in the commit message.
4. The team-wide announcement of the change happens at the next sprint review or daily.

Don't change the checklist mid-sprint silently. Don't allow informal "we'll skip the operator pass on small changes" — write it down or it's not the policy.

The CI lint reads from this file's structure; the PR template references it. They stay in sync because they share the source.

---

## When the checklist legitimately fails the team

There are real cases where the checklist gets in the way. Naming them honestly:

### Hotfix at 3am

If production is on fire, the hotfix path (`HOTFIX_AND_BUGS.md`) allows a fast-track PR with a reduced checklist. The follow-up is mandatory: a non-hotfix PR within 24 hours that backfills the missing checklist items (tests, operator pass, spec update).

The hotfix shortcut is *not* a get-out-of-jail-free card. It's a deferred obligation.

### Spike / exploration

A spike is research, not production code. Spikes don't go to `main` directly; they live in a branch (or a separate spike repo) and produce a write-up. The output of a spike is a *learning*, not a feature.

If a spike produces code that wants to ship, it gets re-done as a regular story with the full checklist.

### Genuinely-trivial changes

See above. The N/A escape valve exists for these. Don't abuse it; reviewers push back.

---

## Why this is non-negotiable

the demo team has no QA function. There are three lines of defense against bugs reaching production:

1. **The author's adversary pass.** First line. The dev attacks their own work.
2. **The PR template + CI checks.** Mechanical floor — can't ship if checkboxes are blank.
3. **The reviewer's adversary stance.** Second human line. Reviewer reads the diff as if it were broken.

Drop any one of those, and bugs leak. Drop two, and the team learns by production incident.

The Definition of Done is the encoding of all three. **It is the QA function, distributed across the dev team.** It only works if every PR earns the tickbox honestly.

If you find yourself rationalising a missed checkbox, *that's the moment* the QA-less workflow either holds or breaks. Tick honestly, or don't tick at all.

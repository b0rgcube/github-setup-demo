# Workflow — end to end

The single doc a new team member should read first. Walks the whole loop from "PO has an idea" to "feature is done and live."

If a step here feels heavier than it needs to be, push back. The whole point of this setup is *frictionless by default*; weight only earns its keep where it compensates for not having QA, or where a future GxP toggle needs a hook to land in.

---

## The shape of the loop

```
   1. story  ────────►  2. refine  ────────►  3. spec  ──┐
                          (PO ↔ dev)            │        │
                                                ▼        │
                                          spec-PR       │
                                                ▼        │
                                          spec merged   │
                                                │        │
                                                ▼        │
                  ┌─────────  4. sprint planning  ◄──────┘
                  │              (or pull from kanban)
                  ▼
            5. implementation  ─────────►  6. PR  ────►  7. review  ────►  8. merge  ────►  9. done
                                              (adversary stance)
```

The whole loop reads in plain English: **idea → story → refined story → approved spec → sprint slot → branch → PR → adversarial review → merge → done.** Nine steps, each is one thing the team already knows how to do.

---

## 1 · Story

A story is a unit of work small enough that one developer can finish it in a sprint (or in ≤3 days for kanban teams). Stories live as **GitHub Issues** under the `story` template.

**Who creates them:**

- **PO** for product-driven stories (most stories).
- **Tech lead** for tech-debt or platform stories (use the `tech-debt` template instead).
- **Anyone** for bugs (use the `bug` template).

**Story shape (enforced by the issue template):**

```
Title:           <user-facing capability, in plain language>
Feature ID:      F-{AREA}-{NNN}                      ← if there's a spec
Linked spec:     specs/F-{AREA}-{NNN}-*.md           ← optional at story-creation
User story:      As a <user>, I want <capability>, so that <outcome>.
Acceptance:      - Bullet list of plain-English acceptance criteria
                 - One scenario ID per criterion (filled in during refine)
Out of scope:    Explicitly what this story does NOT include.
```

The `Acceptance` list maps to scenarios in the spec once the spec is written. The "Out of scope" line saves enormous rework — fill it in even when it feels obvious.

A new story starts in the `Backlog` column of the Project board with priority `P3 (someday)` until the PO triages it.

---

## 2 · Refine — the PO ↔ dev conversation

Refinement is **not a meeting**. It's a thread on the issue, with the PO and a dev (often the tech lead, sometimes whoever will work it) talking until the story is sharp.

**What sharp means** — the story can answer all of these without further conversation:

- ✅ Who's the user? (Concrete, not a slogan.)
- ✅ What outcome are they trying to achieve?
- ✅ How do we know we did it? (The acceptance criteria.)
- ✅ What's explicitly *not* in scope?
- ✅ Any open assumptions still standing? (Tagged `[ASSUMPTION]` in the issue body.)
- ✅ Which part of the codebase will this touch? (Useful for the dev picking it up; on a 4-person team this is context, not routing.)

**Refinement output:** the story is moved to the `Ready` column. Now it's eligible for sprint planning (or pulling from kanban).

**If refinement stalls:** the story stays in `Backlog`; the dev tags the PO with the open question. Don't refine in the dark — bounce the question back.

**Tooling:** plain GitHub Issue comments. No separate refinement tool. The whole conversation lives on the issue and is searchable forever.

---

## 3 · Spec — when stories warrant one

Not every story needs a spec. The rule:

- **Trivial story (1–2 files, well-scoped, no architectural impact):** no spec required. The acceptance criteria *in the issue* are the spec.
- **Non-trivial story (≥3 files, crosses a module boundary, introduces a new concept, or has scenarios with edge cases):** spec required.

**Spec lives at:** `specs/F-{AREA}-{NNN}-{slug}.md`

**Who writes it:** architect persona (in agentic-team-enabled repos) drafts; tech lead reviews; PO approves the *behaviour* and *scenarios* sections.

**The spec template** (copied from `templates/.github/spec-template.md`):

```
---
id: F-{AREA}-{NNN}
title: <feature name>
status: draft               # draft | approved | in-progress | implemented | deprecated
owner: <PO or tech lead>
created: <YYYY-MM-DD>
last-updated: <YYYY-MM-DD>
---

# Behaviour
Plain English. Present tense. What the feature does.

# Scenarios
### SC-{NNN}-01 — Happy path: <name>
- Given <state>
- When <trigger>
- Then <outcome>
### SC-{NNN}-02 — Edge case
…
### SC-{NNN}-03 — Failure case
…

# Out of Scope
What this feature does NOT do.

# Glossary
Domain terms.

# Open Questions
Pending decisions.

# Engineering Questions
Things engineering will weigh in on. Questions only — never feasibility verdicts.

# Dependencies
Other specs, services, teams.
```

### Spec-PR — the spec gets reviewed like code

The spec is committed via a PR (separate from the implementation PR). This sounds heavy; it isn't:

- **Why a separate PR?** The spec is the contract. Reviewing it as code means the PO and tech lead explicitly agree before implementation starts. Catches misunderstandings cheaply.
- **What gets reviewed in the spec PR:** PO reviews behaviour + scenarios + out-of-scope. Tech lead reviews engineering questions, dependencies, and architectural fit. Architect persona (if available) does an inline review for boundary concerns.
- **Status:** spec status starts at `draft`; PR approval flips it to `approved`. Implementation cannot begin until the spec PR is merged.
- **Trivial stories skip this entire step.** No spec, no spec-PR.

**The CI lint runs on the spec PR:**

- Every `SC-{NNN}-{NN}` referenced in the spec must be unique within that spec.
- Every Scenario in the spec has at least Given / When / Then sections.
- The spec frontmatter is well-formed.

After merge, the spec is ready for implementation.

---

## 4 · Sprint planning (or pulling from kanban)

This setup documents **two cadences**; the team picks one at adoption time:

### Cadence A — 2-week sprints

Friday afternoons every other week, ~45 minutes:

- **PO walks through the top of the `Ready` column**, in priority order.
- **Team estimates capacity** (rough story-points, no Fibonacci theology — just "small / medium / large").
- **Stories committed to the sprint** move to the `Sprint` column.
- **Tech lead assigns** based on whose hands it makes most sense in + load balance. Anyone can volunteer.

The sprint goal is *one sentence*. The team writes it together at the end of planning. Example: *"Ship the snippet-rotation feature end-to-end so internal demo can show it on Friday."*

### Cadence B — kanban (continuous flow)

No planning meeting. Replaced by:

- **WIP limits per column** on the Project board (e.g. `In progress: 5`).
- **Daily 5-min check-in** (async via a thread or live, team's choice) — anyone with capacity pulls the highest-priority `Ready` story they can credibly handle.
- **Tech lead assigns rebalances** when WIP is uneven, not on a schedule.

Kanban suits small mature teams whose work is naturally heterogeneous; sprints suit teams that want a forcing function and predictable demos.

**Choose one and write it down in your repo's `CONTRIBUTING.md`.** Don't run both informally — that's the worst of both.

See `SPRINT_PROCESS.md` for the full ceremony details either way.

---

## 5 · Implementation

The story is assigned. The dev:

1. **Creates a branch** off `main`. Convention: `<github-username>/<feature-area>/<short-slug>`. Example: `bjwi/ccs/rotate-snippet`.
   - One branch per story. Do not rebase a story branch onto another story's WIP — keep them parallel.
2. **Reads the spec** (if any) cover to cover before writing code.
3. **Writes the implementation + happy-path tests in small commits**. Each commit message references the feature ID at minimum: `feat(ccs): add rotation endpoint — F-CCS-042`.
4. **Runs the local pre-flight** before pushing: `make test && make lint` (or whatever the repo's equivalent is).
5. **Pushes the branch**. Does not open the PR yet.
6. **Asks themselves the adversary question** before opening the PR: *"What edge cases would I attack this with if I were trying to break it?"* Adds those tests, with `SC-` markers if they correspond to spec scenarios. New failure-case scenarios discovered now get added to the spec via a follow-up commit on the spec file (in this same PR, *or* in a follow-up spec PR if it's a meaningful change).
7. **Runs `make test` again** with the adversarial tests included.

Only now does the PR open.

The order matters. Opening a PR with only happy-path tests is what shifts the adversary load to the reviewer — and the reviewer is being adversarial about *the system* (architecture, drift, operability), not a substitute for the dev's own attempt to break it.

---

## 6 · Pull request

PR title: `<concise description> — F-{AREA}-{NNN}` (e.g., `Add snippet rotation API — F-CCS-042`).

The PR template (`templates/.github/PULL_REQUEST_TEMPLATE.md`) auto-fills with required checkboxes the dev fills in *before* requesting review:

- [ ] Linked story issue: `#XXX`
- [ ] Linked spec (if non-trivial): `specs/F-...`
- [ ] All acceptance criteria covered by tests with matching `SC-{NNN}-{NN}` markers
- [ ] **Adversarial pass done by author**: edge cases, contract violations, malformed input, concurrency
- [ ] Tests run locally; output pasted in PR description
- [ ] No new lint warnings; no new TODO without owner+date
- [ ] **Operator pass**: log lines name entities; errors distinguish faults; metrics added if hot-path
- [ ] Out-of-scope items not silently expanded
- [ ] Documentation/README updated if user-facing or onboarding-relevant
- [ ] Reviewer can run this with `<exact command>` to verify

The unchecked-checkbox CI check refuses to merge if any is unticked. The reviewer's job (next step) is to verify the dev didn't lie on these — not to do them from scratch.

---

## 7 · Review — adversary stance

CODEOWNERS auto-requests both senior ICs (tech lead + senior data scientist) on every PR. Either can approve. When one of them is the author, the other reviews — GitHub doesn't request review from the PR author, so this is automatic.

**Reviewer's job:** read the diff *as if it were broken*. The reviewer is in adversary stance — not "is this code OK?" but "what would I attack this with?"

See `REVIEW_AS_ADVERSARY.md` for the full review checklist. The five-second version:

- Spec scenario IDs all covered by tests? Verify by grep, don't trust the checkbox.
- Edge cases the dev tested feel insufficient? Name what's missing.
- Operability (logs, metrics, error messages) actually gives the on-call something to work with?
- Drift: does the spec still match what got built? If the spec has changed scope mid-PR, separate-PR-it.
- Anything in the diff that *isn't* tied to the story — out-of-scope expansion?

**Comment etiquette** (lightweight, no Conventional Comments fanfare):

- `nit:` — taste; PR can merge with or without
- `q:` — question; reviewer wants an answer in-thread before approving
- `blocker:` — must be addressed before merge

A blocker should be specific and actionable. "I don't like this" is not a blocker; "this will fail when input is empty, see SC-042-12" is.

**Approval = green check + comment.** One senior approval clears the gate. The two juniors (dev, data scientist) are encouraged to also review — extra eyes, plus learning — but their approval doesn't satisfy the gate. They surface findings; one of the seniors approves.

---

## 8 · Merge

Branch protection on `main`:

- Required: 1 reviewer approval (CODEOWNERS-routed).
- Required: PR template checklist all ticked (CI check).
- Required: All CI checks green (tests, lint, scenario-ID lint).
- Required: Branch up to date with `main` before merge.
- Merge style: **Squash-and-merge** (default; keeps `main` linear).
- The squash commit subject is the PR title; body is auto-populated from the PR description.

The dev clicks merge. CI runs the post-merge release-candidate workflow. If the project has continuous deployment, the change is in staging within minutes; production after the team's release-cadence step (whatever that is).

After merge, the branch is auto-deleted (GitHub setting).

---

## 9 · Done

The story moves to `Done` on the Project board. The dev:

- Updates the story issue with a one-line summary of what shipped (auto-comment on PR merge can do this).
- Closes the issue.
- If the spec exists, updates its frontmatter status: `approved → implemented`. (One-line spec-only PR; tech lead approves quickly.)
- Files a follow-up issue if any `[ASSUMPTION]` from the spec turned out to need user-confirmation. These become validation candidates for the next refinement cycle.

For sprint teams: the story is reviewed in the next sprint-review meeting (Friday), tagged with what was learned (anything counter to the original plan?), and the team retros.

For kanban teams: the story is mentioned in the daily check-in the next morning. No formal retro — but a *cumulative* retro every 2–3 weeks looking at done stories as a batch is healthy.

---

## A typical Wednesday in a story's life

To make this concrete, here's what one day looks like in the middle of working a story:

```
09:30  - Dev opens GitHub, checks Project board.
         Story F-CCS-042 (snippet rotation) is in `In Progress`,
         assigned to her.
09:35  - Pulls latest main, rebases her branch.
09:40  - Reads spec specs/F-CCS-042-rotate-snippet.md.
         3 happy-path scenarios, 2 failure-case scenarios.
09:50  - Opens previous evening's commits, sees only happy-path
         tests passing. SC-042-04 (concurrent rotation race) and
         SC-042-05 (rotation during snapshot) not yet covered.
10:00  - Writes test_concurrent_rotation_sc_042_04.
         Hits a race in the lock acquisition. Adds repro.
10:30  - Fixes the race. Test passes. Commits.
10:35  - Writes test_rotation_during_snapshot_sc_042_05.
         Passes first try; suspicious. Manually inspects what's
         being asserted. Realizes it doesn't actually exercise
         the timing — fixes the test. Commits.
11:00  - Runs make test. All 5 scenarios pass.
11:05  - Adversary self-review: "What would I attack?"
         Tries empty snippet ID — error message is unhelpful.
         Adds a clearer error path. Commits.
11:30  - Operator self-review: "If this fails at 3am, what does
         the on-call see?" Adds two log lines with snippet ID
         and request ID; adds a counter for rotation failures.
12:00  - Pushes branch. PR template auto-populates.
         Ticks the 8 checkboxes. Pastes test output.
         Requests review (CODEOWNERS auto-requests both seniors).
12:15  - Lunch.
14:00  - Review comments come back: 1 nit (variable name),
         1 q (about whether the rotation lock is bounded;
         reviewer is right to ask), 1 blocker (the new error
         path returns a stack trace in the response — fix
         before merge).
14:45  - Addresses all three. Force-pushes (the PR is hers
         alone; squash-merge means history doesn't matter
         after merge).
15:15  - Reviewer re-approves. CI re-runs, green.
15:20  - Squash-merges. Branch auto-deletes. Spec status
         flips to `implemented` in a follow-up one-line PR
         (tech lead approves in 2 minutes).
15:30  - Updates story issue: "Shipped. Notes: SC-042-04 and
         SC-042-05 turned up a real race in the lock acquisition
         — fix in this PR. No follow-ups."
15:35  - Closes issue. Project board moves it to `Done`.
         Pulls next story.
```

That's the day. ~6 hours of dev work, ~30 min of GitHub friction. The friction is mostly review-cycle waiting; the rest is automatic. **That's the goal.**

---

## What this workflow assumes about your team

- 3–6 active people, ≥2 of whom are senior ICs (any role mix; for the demo team specifically: 1 tech lead + 1 senior data scientist).
- One PO who can be reached on a thread within a working day.
- The two seniors share review authority — every PR needs one of them to approve.
- Everyone has commit access to `main` (with branch protection).
- The team uses GitHub Projects for board management. (No Jira, no ADO. If you need those, see `gxp-github` for the heavier setup.)
- The team uses the agentic team starter pack OR has internalised the equivalent disciplines. The reviewer-as-adversary mechanism is much more reliable when the architect and adversary personas are also in the loop. See `AGENTIC_TEAM_INTEGRATION.md`.

If any of these aren't true, this workflow still works — but expect to compensate elsewhere.

# Code review — adversary stance

In the team, **the code review IS the QA pass**. There's no separate QA function reading test plans, running test cases, or filing bugs against staged builds. The reviewer is the second adversary (the first is the author of the PR), and the only one with fresh eyes.

This doc is for the reviewer. Read it before your first review on this team; come back to it whenever a review feels off.

---

## Stance — what you are doing

You are reading this code **as if it is broken**. Not as if it might be wrong. As if it is wrong, and you're hunting for where.

This is a stance, not a personality trait. The same person who wrote the code with constructive intent now reads someone else's code with adversarial intent. The stance is what makes the difference; the person is the same.

**You are not:**
- Performing QA's job. You're doing the dev-team-level adversarial pass that exists *because* there is no QA. Different scope, different depth.
- Writing the code yourself. If the diff disagrees with how *you* would have written it, that's a `nit`, not a `blocker`. The author owns implementation choices within the scope of the spec.
- Approving on vibes. Every approval is a claim that you read the diff and it earned the approval. If you're rubber-stamping, you're failing the team.

---

## Sequence — how to do a review

A good review takes 20–60 minutes for a normal PR; 5 minutes for a trivial one. If you have less time than that, ask the author to wait, or tell them to find another reviewer.

### Step 1 — Read the PR description (3 min)

- What story does this PR close? Click through. Read the acceptance criteria.
- What spec (if any)? Click through. Read the scenarios.
- Does the PR description summarise the change in a way you can verify against the diff?

If the PR description is blank or vague, send it back. **Don't review a PR you can't compare against intent.**

### Step 2 — Read the test changes first (5–15 min)

This is the load-bearing inversion. Most reviewers read implementation first, then tests. **Read tests first.**

For each test file in the diff:

- **What scenario is this asserting?** Match the test name or the `@pytest.mark.scenario("SC-...")` marker to the spec scenario. If you can't find the scenario, that's a problem.
- **Does the test actually exercise the scenario, or does it just touch the code?** A test named `test_concurrent_rotation_sc_042_04` that doesn't actually exercise concurrency is worse than no test — it claims coverage it doesn't have.
- **What does the test *not* cover?** Read the spec failure-case scenarios; check that each is covered. Read the acceptance criteria from the issue; check that each maps to at least one test.

If the tests look thin or wrong, you've already found the issue. The implementation read becomes much faster.

### Step 3 — Read the implementation (10–30 min)

Now read the implementation, with the tests in mind. You're not reading for taste; you're reading for:

- **Does the code actually do what the tests assert it does?** A test passing doesn't mean the code does the right thing — it means the code does what the test asserts. Sometimes the assertion is wrong.
- **What edge cases does the implementation silently handle, but the tests don't exercise?** These are unverified behaviours. Flag the gap.
- **What edge cases does the implementation silently *fail* on?** Off-by-one in a loop. Missing None check. Implicit type coercion. Tests probably don't catch these because the author didn't write tests for them.
- **Does the code match the spec?** Read the spec's Behaviour section; compare to the implementation. If the spec said one thing and the code does another, you've found drift.
- **Does the operator checklist actually hold?** Don't trust the tickbox. Verify: are log lines in the new code carrying the entity IDs they need? Do new error paths produce useful messages? Are metrics added for hot paths?

### Step 4 — Run the code (5–15 min)

The PR template should include a "Reviewer can verify with: `<exact command>`" line. Run it.

If the command fails, that's a blocker. If the command passes but you don't trust it, run a second one of your own. If the project has `make test` or `npm test` set up, run that.

For UI changes, pull the branch, run the dev server, click through the change manually. Five minutes of clicking finds bugs that pages of test code miss.

If you can't easily run the code locally (e.g. it depends on a service you don't have), say so in the review and ask the author what *they* did to verify. "I ran it" beats "I read it" almost every time.

### Step 5 — Write the review

Three kinds of comments. Use them precisely:

- **`nit:`** — taste. PR can merge with or without action. Only flag nits sparingly; reviewers who pile on nits train authors to skim reviews.
- **`q:`** — question. You're not sure if the code is right; you want an answer in-thread before approving. The author addresses it (with code change, with explanation, or with "you're right, missed that").
- **`blocker:`** — must be addressed before merge. Specific, actionable, and tied to a concrete failure mode (not preference).

A blocker should answer the question: *"What would happen if this merged as-is?"* If you can't answer that with a concrete failure mode, it's not a blocker — it's a `q:` or a `nit:`.

### Step 6 — Approve, request changes, or escalate

- **Approve** when blockers are resolved (or none existed) and you've genuinely read the diff. Approval is a claim about your work, not a courtesy.
- **Request changes** when there are blockers. Explicit "request changes" GitHub state — not just "I'll approve once you fix it" comments. Authors should know to address before re-requesting review.
- **Escalate** when:
  - The PR touches code you're not confident in. *(On a 4-person team this is rarer than you might think — but if it happens, ask the other senior to take it instead.)*
  - There's an architectural disagreement you can't resolve in PR comments. Pull the conversation off the PR; have it on a call or thread; come back with a decision.
  - The two seniors disagree on a blocker. The PO is the tiebreak when the disagreement is about scope; for engineering disagreements, take it to a brief sync — someone has to commit to one decision.

---

## What you check, in priority order

When time is short, do these in order. The first three are mandatory; the rest are best-effort but should be hit on a normal review.

### 1. Spec coverage (mandatory)

- Every `SC-{NNN}-{NN}` referenced in the spec has at least one test marker.
- The acceptance criteria in the issue map to tests.
- New failure modes discovered during this PR are added to the spec (or the gap is filed as a follow-up issue).

The CI catches missing markers; you catch missing *coverage* (test exists but doesn't actually exercise the scenario).

### 2. Adversarial test depth (mandatory)

- Boundary cases (empty, single, max, off-by-one) tested?
- Contract violations (wrong type, None, malformed) tested?
- Failure modes (timeout, dependency down, partial) tested or explicitly deferred?
- Concurrency considered if the code is concurrent?

The author claims this in the PR template; you verify it's not just claimed.

### 3. Operability (mandatory)

- Log lines name entities.
- Errors distinguish faults.
- Metrics on hot-path code (if metrics are wired up).
- Side-effects safe to retry, or documented as not.

For a 3am page on this code: would the on-call know what's wrong from the logs alone, or are they doing forensics?

### 4. Drift (best-effort)

- Spec ↔ code: does the implementation still match what the spec described?
- Issue ↔ PR: did the scope expand without explicit reframing?
- Out-of-scope honoured: nothing snuck in?

### 5. Architecture / boundaries (best-effort, escalate if unsure)

- Does the change cross a module boundary cleanly?
- New dependency introduced? Justified?
- Pattern matches surrounding code's idiom?

Architecture concerns should usually have been resolved in spec review, not here. If a PR introduces a meaningful architectural decision that wasn't in the spec, escalate to tech lead — even on approval — and consider asking for an ADR.

### 6. Clarity / maintainability (best-effort)

- Names carry intent.
- Functions stay under reasonable budgets (~50 lines, ≤4 nesting).
- New TODOs have owner + date.
- New abstractions earn their keep (DRY isn't a license to over-abstract).

Use `nit:` liberally; use `blocker:` rarely on this category.

---

## Patterns that should always trigger a closer look

These are smells. Not blockers automatically — but slow down and check.

- **A test passes that probably shouldn't.** A `passed` claim on a hard scenario is suspicious. Read what's being asserted.
- **A test was deleted in the PR.** Why? Could be valid (spec changed, scenario obsolete); could be that the test was failing and the author "fixed" it by removing it. Ask.
- **Comments that explain *why* code is doing something seemingly wrong.** Sometimes there's a real reason; sometimes the comment is the author trying to talk themselves out of doing it right. Ask.
- **A large refactor "while I was in there."** Adjacent rot is a constructor finishing-move; *unrelated* refactor is scope creep. Push back; suggest a follow-up PR.
- **New `# noqa` / `# type: ignore` / `eslint-disable` without explanation.** Each one should have a reason in a comment. If not, ask.
- **Public API change without explicit Out-of-Scope coverage.** New function signature, new endpoint, new event payload — these are external contracts. They should be in the spec.
- **Tests use mocks where they could use a real instance.** Mocks that test "the method was called" rather than "the system did the thing" are tests that pass on a broken implementation.

---

## Anti-patterns (you, the reviewer)

Things to *not* do as the reviewer:

### "LGTM" with no review

If you didn't read the diff, don't approve it. The team trusts your approval — your reputation as a reviewer is what makes the workflow function without QA. Spending 5 min on a non-trivial PR is malpractice; spending 30 seconds is fraud.

### Bikeshedding over architecture decisions already made

If the spec was approved last week and the implementation matches it, this isn't the time to relitigate the architecture. Disagree with the spec? Open a separate PR or ADR. The implementation PR isn't the venue.

### Asking the author to do *your* thinking

`q: not sure why this works` is fine.
`q: can you walk me through the algorithm?` is sometimes fine, sometimes a sign you should pull the branch and trace it yourself.
`q: have you considered all the edge cases?` is lazy. Name the edge case you have in mind.

### Reviewing for the third time when the same blockers come back

If the author submitted, you blocked, they pushed back without addressing, and the same blocker persists — escalate. Don't re-review the same PR five times. Tech lead breaks the tie.

### Approving while the CI is still running

Wait for green. Approving against a yellow PR is approving the *previous* state, not the current state. If the CI fails after your approval, the author can sometimes (depending on the merge button workflow) merge anyway. Wait.

---

## What the reviewer is *not* responsible for

These belong elsewhere:

- **Catching every bug.** That's an unreasonable standard. The reviewer raises the floor; some bugs get through. The team's response to bugs is post-mortem and process improvement, not blame on the reviewer who missed it.
- **Production deployment.** Once merged, deployment goes through whatever pipeline the project has. The reviewer's job ends at merge.
- **The PO's product decisions.** If the PO approved a story you think is a bad idea, that's a separate conversation; don't relitigate in code review.
- **The author's growth.** You can teach, but the review's primary job is the code, not the dev. Mentoring happens in 1:1s, not in PR threads.

---

## Two-senior review gate

The team is small enough (4 people: tech lead, dev, senior data scientist, data scientist) that everyone reads everything. There's no area-routing to a "senior backend IC" or "senior frontend IC" because there are no area teams — there's *the team*.

CODEOWNERS auto-requests both seniors (tech lead + senior data scientist) on every PR. Either approval clears the gate. When one is the author, GitHub doesn't request review from them, so the other reviews — automatic.

When you, as the senior data scientist, are reviewing a PR by the tech lead (or vice versa):

- Apply the same standards. The author's seniority doesn't pre-approve their PR.
- If you have blockers, surface them. The other senior expects this; if they don't, that's a culture problem to raise separately.
- If the architectural call in the PR conflicts with what you'd choose, separate the question of *correctness* (blocker) from *preference* (nit). Don't punish architectural choices that are within reasonable bounds.

The two juniors (dev, data scientist) are encouraged to also review. Their findings are valuable; their approval doesn't satisfy the gate. If they spot a blocker, surface it — one of the seniors will weigh it before approving.

---

## A reviewer's mindset cheat sheet

When you're stuck — not sure if something's worth blocking, not sure what to look at next — use these prompts:

- *What would I attack this with if I were trying to break it?*
- *If this fails at 3am, what does the on-call see?*
- *What is the spec actually claiming, and does the code do that?*
- *What's the smallest change that would make this fail unexpectedly?*
- *If I were onboarding a new hire and pointed at this PR, what would they not understand?*

Use one. Move on. The review is bounded; don't over-spelunk.

---

## Closing

You're the second adversary. The first was the author. The third is production. Every layer that catches a bug is a 3am page that didn't happen.

Be precise; be fair; be honest. The team's quality without QA depends on this seat being taken seriously.

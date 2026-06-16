# Onboarding — your first day, first week, first PR

You're new on the team. This doc is your map.

It assumes you've already had whatever organisational onboarding (HR, accounts, laptop) is needed. It picks up from "you have a working laptop and access to the GitHub repo."

---

## TL;DR — the first PR you'll write

Most teams have an `onboarding-task` issue waiting for new joiners — a small, real, non-trivial change that touches the workflow without being on a critical path. If yours doesn't, ask the tech lead for one. **Don't start with a fake task.** Onboarding by reading docs alone teaches you the docs; onboarding by shipping teaches you the team.

Goal for week one: ship one PR that goes through the full Definition of Done, all the way to merge. The PR can be small. What matters is that you've *touched* every step of the workflow before the team needs you to do anything that matters.

---

## Day 1 — read, clone, run

### Read first (in this order, ~90 minutes)

1. **`README.md`** in the repo root — what the project is.
2. **`CONTRIBUTING.md`** — how the team works. (If your repo follows this setup, this references the docs in `github-setup/docs/`.)
3. **`docs/WORKFLOW.md`** in this setup — the loop end-to-end.
4. **`docs/DEFINITION_OF_DONE.md`** — the most important doc; the team's quality contract.
5. **`docs/REVIEW_AS_ADVERSARY.md`** — even though you're new and won't be reviewing for a while, read it so you know what reviewers are looking for in *your* PRs.

Skim these; you'll come back. Don't try to memorise.

### Get the code running locally

Goal: by end of day, you can run the test suite. No PR yet; just confirming the local environment works.

```bash
# 1. Clone (whatever the repo's clone URL is)
git clone <repo-url>
cd <repo>

# 2. Read the README's "Getting started" section, follow it
#    (varies per repo — Python venv, node, docker, etc.)

# 3. Run the tests
make test         # or: npm test, pytest, cargo test, etc.

# 4. Run the lint
make lint         # or equivalent
```

**If anything fails:** ping the tech lead or your buddy. **Document the failure** — your fresh-eyes pain is the team's onboarding-friction signal. Open an issue: "onboarding: docs/setup says X, on macOS Apple Silicon I needed Y." This may end up being your first PR. Onboarding-pain fixes are gold.

### Set up your tooling

- **Editor / IDE.** The team isn't prescriptive. Use what you're productive in.
- **Git config.** Sign your commits if branch protection requires it (`git config commit.gpgsign true` after setting up a key). The team uses signed commits by default.
- **GitHub CLI** (`gh`) is recommended; many of the workflow shortcuts in `docs/` use it.
- **Pre-commit hooks** if the repo has them: `pre-commit install`.

---

## Week 1 — pair, ask, ship one PR

### Pair on a story

Ask the tech lead to pair you with one of the seniors (themselves or the senior data scientist, whichever is closer to your work). **Pair on a real story** they're already running — you read along, ask questions, see how they navigate the issue thread + spec + branch + PR + review cycle.

You're learning:

- What the team's commit-message conventions actually look like in practice.
- How specs are read (most teams read them less linearly than the doc implies).
- How that senior structures their adversarial pass — what they think to attack first.
- How comments on PRs flow — what's a `nit:`, what's a `q:`, what's a `blocker:`.
- The real heuristics for "trivial vs. non-trivial."

This pair session can be 60–90 minutes; a full sprint cycle's worth is overkill on day one. The point is *exposure*, not deep training.

### Attend a sprint planning (or kanban triage)

If your team runs sprints, attend the next planning meeting. Just listen. You'll learn:

- The PO's voice.
- What "small / medium / large" means to *this* team specifically.
- The kinds of stories the team is shipping right now.
- The blockers the team currently lives with.

For kanban teams: attend the daily check-in for the first week. Same goal.

### Your onboarding task

The tech lead has assigned you (or will assign you) one of:

- An open issue tagged `good-first-issue`.
- A small bug fix.
- A piece of documentation that needs updating.
- An "onboarding pain" issue you opened on day one.

**The task should be small enough to ship in 2–3 days, and real enough that the team would have done it anyway.** Avoid synthetic onboarding tasks (e.g. "add a typo") — they don't teach you the workflow honestly.

### Walk the workflow

Now you do the loop:

1. Pull the latest `main`. Read the issue. (If unclear, ask in the issue thread — *not* by DM. The team's communication norms are async-first.)
2. Branch off `main`. Convention: `<your-username>/<area>/<short-slug>`.
3. Write the code + happy-path tests. Small commits; conventional commit message format if the team uses one.
4. Run the full test suite locally. Run the lint.
5. Do the adversarial self-review. *Even if the change is small.* Practice the muscle.
6. Do the operator self-review. *Even if the change is small.* Practice the muscle.
7. Push your branch. Open the PR.
8. Fill in the PR template. **Tick honestly.** "N/A — trivial doc change" with a one-line reason is fine. "✅" with no thought is dishonest.
9. Wait for review. While waiting: read more code. The team's existing code is the textbook.
10. Address review comments. Re-request review.
11. Merge.

You've now done the full loop. **Pay attention to what felt heavy.** Was the PR template confusing? Did the CI checks make sense? Did the review feedback teach you something? File those observations — they're your fresh-eyes input to the next round of process improvement.

---

## Week 2–4 — start contributing to reviews

After your first one or two PRs are merged, the tech lead will start tagging you in PR reviews — initially as a *secondary* reviewer alongside the seniors (CODEOWNERS auto-requests both seniors; you read along).

Your job here is to learn the reviewer's stance. Read the diff *before* reading the seniors' comments. Form your own opinion. Then read theirs. Where you agreed, you've calibrated; where you didn't, ask why.

Don't apologise for missed comments; ask. *"I didn't flag SC-042-12 — were you looking at the marker presence, or did you actually run the test and see it covered the assertion?"* That's the conversation that makes you a faster reviewer.

After ~4 weeks of secondary review, the tech lead will start routing some PRs to you directly. From then on, you're part of the regular CODEOWNERS rotation for your area.

---

## Communication norms

Things that may be different from teams you've been on:

- **Async-first.** Most decisions live on issue threads or PR comments, not in chat or meetings. Decisions in Slack/Teams that affect a story should be summarised back into the issue.
- **Questions in public.** If you have a question that another new joiner might have in 6 months, ask it in the team channel (or the issue thread). Don't DM the tech lead. The team's culture explicitly rewards *visible* questions.
- **No standup theatre.** Daily check-ins are short and honest. "Yesterday: stuck on X. Today: still on X. Blocked: not yet, but if it's still stuck tomorrow, I will be." That's better than embellishment.
- **Disagreement is welcome.** PR comments push back, ICs disagree with the tech lead, the PO is challenged on priority. Done well, none of this is hostile. If it feels hostile, surface it (1:1 with tech lead) — the team intends it as direct, not aggressive.

If any of these clash with how you've worked before, talk to the tech lead about it. Adjustment is two-way; the team adapts to new joiners as much as new joiners adapt to the team.

---

## What you don't need to learn in the first month

Things that look important but can wait:

- **The full agentic team** in `.claude/agents/`. If your repo uses it (`agentic-team-starter` integration), you'll see it in code reviews. Read up when curious. It's not gating onboarding.
- **The GxP upgrade path.** Almost certainly irrelevant unless your repo just had a regulation change. Read when needed.
- **The full CI workflow internals.** You need to know that CI exists and what gates it enforces. The YAML internals are platform-engineering concerns; learn them as you contribute to them.
- **The full project history.** You'll absorb context from PRs and issues over time. Trying to read every closed issue from the last year is a waste of week one.

---

## When to ask for help

Always:

- The setup steps don't work and you've tried for ≥30 minutes.
- The acceptance criteria on your story are ambiguous after re-reading.
- The CI is failing on something that looks unrelated to your change.
- A PR comment confuses you (especially if it feels critical — better to ask "what specifically?" than to guess).

Once a day, batched, is fine. The team prefers "here are 3 questions from this morning's work" over "here's one question every 20 minutes."

If you've been blocked for ≥half a day on something not in this list, *also ask.* The "stuck for half a day in silence" pattern is what onboarding watches for. Surface it.

---

## What the team owes you

Reciprocally — what the team is responsible for during your onboarding:

- A buddy / pair-IC named explicitly. Not "ask anyone"; a specific person.
- Your first onboarding task assigned by end of day 1.
- A response to questions within a working day.
- Attendance at your first sprint planning (or kanban triage) on day 2 or 3.
- Code review on your first PR within ≤24 hours, with constructive feedback.
- A 30-day check-in with the tech lead about how onboarding has gone — what worked, what didn't, what to change for the next joiner.

If any of this isn't happening, raise it. The team's onboarding is the team's responsibility, not yours alone.

---

## A graduation milestone

You're "onboarded" when:

- You've shipped ≥3 PRs, at least one non-trivial.
- You've reviewed ≥3 PRs as primary or substantive secondary reviewer.
- You've attended ≥2 sprint reviews / retros (or the kanban equivalent).
- You can find your way around the codebase without grep-spelunking for half an hour.
- You feel comfortable disagreeing in PR comments without rehearsing the wording for 10 minutes.

For most ICs, this takes 4–8 weeks. There is no formal milestone or ceremony. The graduation is when the tech lead stops actively monitoring your onboarding and you start being asked to mentor the *next* new joiner.

Welcome to the team.

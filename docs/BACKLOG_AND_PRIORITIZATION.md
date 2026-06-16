# Backlog and prioritization — PO-facing

This doc is for the **Product Owner** (or anyone owning the backlog). It describes how the backlog is structured, how items are prioritized, and how the PO interacts with it day to day.

If you're a developer reading this: skim it. The bits you care about are *where stories come from* (top of this doc) and *how priority signals to you what to pick next* (bottom). The rest is PO mechanics.

---

## What the backlog is

A single GitHub Project board attached to the repo, with these columns:

```
┌──────────┬───────────┬──────────┬───────────────┬────────┬──────┐
│ Backlog  │  Triaged  │  Ready   │  Sprint/WIP   │ Review │ Done │
└──────────┴───────────┴──────────┴───────────────┴────────┴──────┘
```

Every item on the board is a GitHub Issue (story, bug, tech-debt, or spike). Pull requests don't live here — only issues do. PRs are linked to their issues via the `Closes #XXX` syntax.

| Column | What lives here | Who moves things in / out |
|---|---|---|
| **Backlog** | Every new issue lands here. Could be days, weeks, months old. | PO (creates), anyone (proposes) |
| **Triaged** | PO has read it, set priority, set rough size, decided it's worth doing. Not yet refined enough to start. | PO (during triage) |
| **Ready** | Story is sharp (acceptance criteria, area, scope), spec written if non-trivial, ready to be picked up. | PO + dev (after refine) |
| **Sprint/WIP** | Currently being worked on (or committed to current sprint). | Tech lead (assigns), dev (pulls) |
| **Review** | PR is open. | Auto-moved by GitHub Actions. |
| **Done** | Merged. | Auto-moved by GitHub Actions. |

The columns are minimal *on purpose*. Adding more columns ("Blocked", "Needs Spec", "QA") creates more places things can sit forgotten. The five productive states + Done is enough.

---

## Priority — P0 / P1 / P2 / P3

Every issue carries a priority label. The PO sets it; tech lead can suggest changes. Four levels:

| Label | Meaning | Triage cadence |
|---|---|---|
| `P0 — now` | Production is broken / customer-impacting / regulatory-deadline. Dropped on someone's desk now. | Within hours |
| `P1 — this sprint` | Goes into the current or next sprint. Real commitment. | Daily |
| `P2 — next sprint` | Should be done in the next sprint or two. Not yet committed. | Weekly during triage |
| `P3 — someday` | Worth tracking; not committed to any timeline. Default for new issues. | Monthly review |

**Rules:**
- An issue's priority is the PO's call. Tech lead may *suggest* a re-prioritization with rationale; the PO decides.
- A `P0` issue gets a Slack/Teams ping, not just a label change. The label is for tracking; the human signal is for action.
- `P3` is the default. New issues without explicit prioritization stay `P3` until triage.
- Only **one** axis of priority. No "P1.5", no "P1-but-also-blocked-by-X". If something can't move, it stays at its priority and gets a `blocked` label *in addition*.

---

## Value vs. effort — the second lens

Priority alone isn't enough. The PO uses a rough **value/effort** lens to decide between two `P2`s. No formal scoring; one of three buckets each:

```
       LOW     MED     HIGH
       effort  effort  effort
HIGH ┌───────┬───────┬───────┐
val. │   ⭐  │   ⭐  │   ?   │
     ├───────┼───────┼───────┤
MED  │   ⭐  │       │       │
     ├───────┼───────┼───────┤
LOW  │       │       │   ✗   │
val. └───────┴───────┴───────┘
```

- **⭐ Quick wins** (high-value, low/med-effort): pull these forward whenever capacity allows.
- **? High-value, high-effort:** worth doing, but probably needs to be split into smaller stories before sprint commitment.
- **✗ Low-value, high-effort:** don't pretend. Either deprioritize or close as `won't-do` with rationale.
- **Empty squares** (low-value, low-effort): these are usually fine to do *if a dev volunteers*; don't promote them to P1.

The PO doesn't formally label issues with these buckets — but mentally applies them when ordering the `Triaged` column.

---

## How the PO interacts with the backlog

### Triage (weekly, ~30 minutes)

PO walks the `Backlog` column top-to-bottom. For each new issue:

1. **Read it.** Does it make sense? If not, comment back to the author.
2. **Decide:** in scope or not?
   - If not in scope: close as `won't-do` with a one-line reason. Don't let the backlog grow indefinitely.
3. **Set priority** (`P0`–`P3`).
4. **Move to `Triaged`.**

If the PO has a hard week, triage is the thing to skip — *not* sprint planning. New `Backlog` issues sit; that's fine. Sprint commitments do not.

### Refinement (continuous, on the issue thread)

As stories approach being picked up, they need to be sharp. The PO answers questions in the issue thread; whoever's likely to pick the story up writes the acceptance criteria with the PO. See `WORKFLOW.md` § "Refine" for what "sharp" means.

This is *not* a meeting. It's threaded, asynchronous, and lives on the issue forever. New ICs joining the team can read past refinements as training data for the team's voice and standards.

When a story is sharp, it's moved to `Ready`. The PO does this — it's the PO's signal that "yes, this is what I want."

### Sprint planning (every 2 weeks for sprint teams) or pull cadence (continuous for kanban)

PO arrives with the `Triaged` and `Ready` columns sorted by priority. The team picks from the top. See `SPRINT_PROCESS.md`.

### Pulling priority signals (the PO's tool)

The PO has three knobs:

- **Move it up** in the column (manual reorder; the column order is the priority order at any given moment).
- **Bump priority** (`P3 → P2`, `P2 → P1`).
- **Flag for the next sprint** explicitly (apply the `next-sprint` label).

The team reads top-down. The story at the top of `Ready` is the one to pick next, unless the PO has explicitly said otherwise.

---

## Stories that don't fit on the board

Sometimes the PO has work that *isn't* a story:

- **Discovery / exploration** — when there's a fuzzy idea that needs sharpening before it becomes a story. File it as a `spike` issue (time-boxed investigation) instead of jumping to a story. The spike's output is a learning, not a feature.
- **Strategy / OKR-shaped work** — these aren't GitHub issues. Track them wherever the broader product team tracks them; reference back from any individual story that contributes to them.
- **Long-running technical investments** (e.g. "rebuild the worker tier on a different framework") — file as an **epic** issue with the `epic` label, plus a tracking checklist of child stories. The epic doesn't go to a sprint; the children do.

If you find yourself wanting to add a new column for any of these, resist. The board is for executable work; everything else lives elsewhere and references back.

---

## Common backlog antipatterns and how to avoid them

These are the patterns that break this setup. The PO is the line of defense.

### Antipattern: "everything is P1"

If most issues are `P1`, none of them are. The fix: be ruthless. `P1` means *this sprint, real commitment*. The PO should expect the active backlog to look like:

- 5–15% `P0`/`P1` (live and active)
- 20–40% `P2` (next-up)
- 50%+ `P3` (someday)

If your distribution is much different, the labels aren't doing their job.

### Antipattern: stories without `Out of Scope`

A story without an explicit "Out of Scope" line tends to grow during implementation. The dev "while they're in there" extends the change. This is exactly what wastes sprint capacity and produces unscoped reviews.

The fix: the issue template *requires* an Out of Scope field. The PO refuses to mark a story `Ready` without it. (Even "(intentionally none — this is a small, fully-scoped change)" is a valid Out of Scope.)

### Antipattern: zombie issues

Issues that have been `P3` for ≥6 months are zombies. They eat backlog hygiene cost without delivering value.

The fix: the `stale-issues.yml` workflow (see `github-config/workflows/`) automatically labels `P3` issues that have had no activity for 90 days. The PO reviews labeled-stale items quarterly and closes them as `won't-do` (preferred) or refreshes them with a reason to keep them.

### Antipattern: spec drift between issue and merge

The story changed during refinement, but the issue body wasn't updated. New devs reading it later see a mismatch with the implemented code.

The fix: the *issue* is the source of truth for what was committed to. If the spec changes during implementation, the dev edits the issue body to reflect the new scope. The story-issue at merge-time should match what shipped.

### Antipattern: PO refines in their head, not on the issue

Sometimes the PO has a clear vision, doesn't write it down, and the dev guesses. This is the single most common cause of rework.

The fix: every refinement decision happens on the issue thread. If you (PO) catch yourself thinking "I'll just tell them in standup", *write it on the issue first*, then mention it in standup.

---

## Tooling and automation

### Labels

A standard label set ships in `github-config/labels.yml`. Apply via:

```bash
gh label clone --remove-existing-labels --output -- < github-config/labels.yml
```

Categories:

- **Priority:** `P0 — now`, `P1 — this sprint`, `P2 — next sprint`, `P3 — someday`
- **Type:** `story`, `bug`, `tech-debt`, `spike`, `epic`
- **Area:** `area: backend`, `area: frontend`, `area: worker`, `area: infra`, `area: docs`
- **State:** `blocked`, `needs-spec`, `stale`, `won't-do`
- **Special:** `good-first-issue`, `external-input-needed`

Add to this set conservatively; labels accrete. Every label should have a clear question it answers.

### CI assists for the PO

- `stale-issues.yml` flags `P3` issues with no activity ≥90 days.
- The Project board has filters for "P0/P1 issues missing acceptance criteria" — these are the issues to clean up before sprint planning.
- A weekly digest comment can be set up via Actions if useful (not in the default scaffold).

---

## How the PO uses this in practice — a typical week

```
Monday morning (10 min):
  - Check P0/P1 column. Anything stuck? Anything finished over the weekend?
  - Comment on any items that progressed; thank where appropriate.

Monday – Friday (continuous, ~5 min/day):
  - Watch issue notifications for refinement questions. Answer same-day where
    possible.
  - For any new issue that comes in via stakeholder or support: read, ask
    clarifying questions in-thread, set priority + move to Triaged or
    close-as-wont-do.

Friday (30 min):
  - Walk the Backlog column. Triage everything that landed this week.
  - Walk the Ready column. Anything stuck waiting on you? Move it forward.
  - Walk the P3 column briefly, looking for things that have become P2 since.

Every 2 weeks (45 min — sprint teams):
  - Sprint planning. PO presents Ready in priority order; team commits.

Monthly (30 min):
  - Quarterly P3 review. Close zombies. Re-prioritize survivors if needed.
```

That's the PO load. Total: ~2 hours/week steady-state, with sprint planning every other Friday on top.

If it's taking *much* more than that, something's wrong — usually the backlog has accreted faster than triage. Spend one Friday catching up; reduce inflow if needed (close as `won't-do` aggressively).

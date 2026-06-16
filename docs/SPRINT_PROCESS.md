# Sprint process — both cadences

This doc covers the two cadences the team can choose between: **2-week sprints** or **continuous flow / kanban**. Pick one and write it down in your repo's `CONTRIBUTING.md`. Don't run both informally.

If you're not sure which to pick — the recommendation at the bottom of this doc has heuristics.

---

## Cadence A — 2-week sprints

Two weeks is the **default recommendation**. Long enough for non-trivial stories, short enough for quick course-correction. Anything longer (3-week, monthly) drifts; anything shorter (1-week) burns time on ceremony.

### Sprint shape

```
        Mon              Wed              Fri
W1   ┌────────────────────────────────────┐
     │                                    │
     │     working                        │
     │                                    │
     └────────────────────────────────────┘
W2   ┌────────────────────────────────────┐
     │                                    │
     │     working                        │ Sprint review (15 min, Fri)
     │                                    │ Retro (15 min, Fri)
     │                                    │ Planning for next sprint (45 min, Fri)
     └────────────────────────────────────┘
```

Total ceremony time: **~75 minutes every two weeks**. That's the hard cap; if it's drifting longer, the meetings are too unstructured.

### Ceremonies

#### Sprint planning — Friday afternoon, ~45 min

**Before the meeting:**
- PO has the `Ready` column sorted by priority.
- Tech lead has reviewed any spec PRs that should be approved before planning.
- Devs have rough capacity sense (any vacation? major existing commitments?).

**Agenda:**
1. **Sprint goal — 5 min.** PO proposes one sentence. Team refines together. Example: *"Ship snippet rotation E2E; close out the F-CCS-042 spec."*
2. **Capacity check — 5 min.** Quick "I have 7 working days, but the Tuesday is a planning offsite, so realistically 6". Devs say their numbers; total capacity is informally tracked.
3. **Story selection — 30 min.** PO walks the top of `Ready`. For each story, the team:
   - Confirms the story is still sharp.
   - Names a rough size (small / medium / large — no Fibonacci).
   - Tech lead suggests an assignee (or asks for volunteers).
   - Story moves to `Sprint/WIP` column with assignee.
4. **Stop when capacity is full.** Don't pad the sprint with optimism. If 6 stories fit, commit 6.
5. **Goal sanity check — 5 min.** Does the committed work actually advance the goal? If not, swap stories.

**Output:** `Sprint/WIP` column populated; sprint goal posted to the team chat with a link to the sprint's filtered Project board view.

#### Daily check-in — async, ~5 min/dev

**Async by default**, in a thread. Format:

```
Yesterday: <what I closed or made progress on>
Today:     <what I'm working on>
Blocked:   <if any — be specific>
```

If anyone is blocked, tech lead or PO unblocks within the day. If you find yourself doing daily check-ins synchronously and they're taking ≥15 min, simplify them — that's a smell.

#### Sprint review — Friday, ~15 min

The team gathers (in person or video) for a quick demo + discussion:

- **Demo what shipped.** ~5 min. Whoever wants to. Working software, not slides.
- **Items not finished.** ~5 min. Why? Carry to next sprint or back to `Ready`?
- **Sprint goal:** did we hit it? If not, why? (No blame; understanding.)

Stakeholders welcome. PO is required. The dev team's whole point is to ship something showable; sprint review is when it gets shown.

#### Retrospective — Friday, ~15 min

Team-only. Three buckets:

- **Keep:** what worked well; do more of it.
- **Drop:** what was friction; do less of it.
- **Try:** one experiment for the next sprint.

Tech lead facilitates if there isn't a dedicated facilitator. Limit *Try* to one item — multiple experiments in parallel is how you can't tell what worked.

Retro outcomes go in a pinned issue or wiki page so the team has continuity. Three sprints from now, you should be able to see whether last quarter's experiments stuck or rotted.

### Sprint metrics

This setup deliberately keeps metrics light. Track only:

- **Sprint goal hit rate** (did the goal get achieved? yes/no/partial). Rolling 6-sprint window.
- **Stories committed vs. stories shipped.** A persistent gap means commitment is too aggressive; close the gap rather than punish the team.

Don't track velocity points, story-points-per-day, or any individual productivity metric. Those drive bad behaviour and don't help the team ship.

---

## Cadence B — continuous flow (kanban)

For teams that find sprint ceremony overhead doesn't earn its keep — usually small mature teams whose stories are heterogeneous (mix of feature work, ad-hoc support, occasional spike).

### How it works

No sprint boundary. The Project board has WIP limits per column:

- **Sprint/WIP** column renamed to **In Progress**, with WIP limit = roughly *team size − 1*. (For a team of 4, WIP = 3. Slack matters.)
- **Review** column WIP limit = team size. (Reviews can stack temporarily; resolving them is what keeps the WIP moving.)

Devs pull from the top of `Ready` whenever they finish something. Tech lead rebalances if WIP gets uneven.

### Ceremonies (lighter than sprint version)

#### Daily check-in — async, ~5 min/dev

Same format as sprint version. Important: the daily is the *only* synchronous-ish ceremony in kanban. Don't skip it.

#### Cumulative retro — every 2–3 weeks, ~30 min

Replace the sprint retro+review with a periodic look-back at done items:

- Pull the `Done` column items closed since the last cumulative retro.
- Quick walk-through (3 min): "what shipped, what's notable."
- Discuss: any patterns? Anything stuck for too long? Any flow problems?
- Same Keep / Drop / Try outcome.

If the team is small enough that this rhythm naturally finds itself, great. If it doesn't, switch to sprint cadence — kanban without retros is technical debt for the process.

#### No formal planning meeting

Replaced by:
- PO keeps the `Ready` column sorted, top to bottom, in priority order.
- When a dev finishes a story, they pull from the top.
- For complex stories needing alignment, the dev requests a 15-min sync with the PO before pulling. Often unnecessary; available when needed.

### Kanban metrics

Track only:

- **Cycle time** (Ready → Done). Rolling 30-day median. The trend matters more than the value.
- **WIP age**. If a story has been In Progress for >2× median cycle time, it's stuck. Surface it in the daily.

That's it. Don't track throughput, don't track per-person counts.

---

## How the team chooses between sprint and kanban

The honest tradeoff:

| Sprint (2-week) | Kanban (continuous) |
|---|---|
| **Forcing function**: deadline every 2 weeks creates urgency | No external pressure; relies on team self-discipline |
| **Predictable demos** for stakeholders | Demos happen ad-hoc, when there's something to show |
| **Heavier ceremony**: ~75 min every 2 weeks | Lighter: ~30 min every 2–3 weeks (cumulative retro) |
| **Sprint goal aligns the team** | Alignment depends on PO's column ordering being honest |
| **Better for**: teams that want a forcing function; junior-heavier teams; teams shipping in 2-week external cadences | **Better for**: small mature teams; teams whose work is heterogeneous; teams already disciplined about WIP and review |

### Heuristics

- Team has dedicated QA or release-management function → sprint, almost always.
- Team is 3–4 ICs, with ≥2 seniors → kanban often works.
- Team is shipping continuously (every PR can go to production) → either; sprint adds a coordination point that may or may not be useful.
- Team has stakeholders who want predictable demos → sprint.
- Team has had `velocity-points` debates that became toxic → kanban (the sprint metric machinery is the source of that pain).

When in doubt: **start with 2-week sprints for 6 sprints (12 weeks)**, then revisit. If the ceremony feels useful, keep it. If it's pure overhead, switch. Don't switch every sprint — give each cadence enough runway to teach you what it teaches.

---

## What this section explicitly does NOT prescribe

A few things this setup leaves to the team:

- **Story sizing technique.** No story points, no Fibonacci. "Small / medium / large" is enough for capacity sense; if your team wants more rigor, add it; if not, don't.
- **Definition of "small / medium / large".** Each team calibrates. Rough heuristic: small = 1 day, medium = 2–4 days, large = ≥1 week (and probably should be split).
- **Specific tooling for daily.** Slack thread, Discord, Teams, GitHub Discussions, in-person — pick what your team will actually do.
- **Whether to involve PO in daily.** Both are fine. Some teams want the PO present; some find it tightens conversation in unhelpful ways. Decide; don't half-do.

The structure is the part this setup commits to; the team owns the texture.

---

## Common antipatterns and how to avoid them

### Antipattern: sprint goal as a list

The sprint goal is one sentence. If you can't fit it in one sentence, you don't have a goal — you have a list of stories. The list is the sprint commitment; the *goal* is the *why*.

If the goal is hard to write because the sprint is a grab-bag, that's signal: maybe this sprint shouldn't exist as a coherent unit, and the team should consider switching to kanban.

### Antipattern: "we don't have time for retro this sprint"

This is the canary. The retro is what makes the sprint a learning loop instead of a treadmill. Skip retro twice in a row and the team is just doing kanban without the discipline.

If retro consistently feels like wasted time, the format is wrong — try a different one (Liked/Learned/Lacked/Longed-for, or "one star one wish") rather than skipping.

### Antipattern: planning that becomes spec-writing

If sprint planning takes >60 minutes, it's because stories aren't sharp coming in. Refinement should happen *before* planning, on the issue thread. If a story isn't sharp at planning, defer it to the next sprint — don't refine in the meeting.

### Antipattern: kanban without WIP limits

WIP limits are the *only* thing that makes kanban work. Without them, the team has no forcing function and stories stagnate in the middle. Set the limits, enforce them.

### Antipattern: tracking velocity for cross-team comparison

Velocity, story points, throughput — these only make sense as *internal* signals to a single team. Senior management asking "why does Team A have higher velocity than Team B" is the cue to refuse to share the numbers and explain why.

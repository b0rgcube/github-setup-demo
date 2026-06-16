# Agentic team integration

How the team's existing `.claude/agents/` team plugs into the GitHub flow.

This doc is short on purpose. The agentic team starter pack itself documents the personas — see `agentic_team_starter/docs/ARCHITECTURE.md` for the full picture. This doc only covers the *integration points* with the GitHub workflow.

If your repo doesn't use the agentic team, skip this entire doc — the GitHub workflow stands on its own.

---

## How the personas map onto workflow steps

| Workflow step | Agentic persona that helps | What they do |
|---|---|---|
| Story → spec | `architect` | Drafts the spec when the lead routes the story to it |
| Spec → spec PR | `architect` + `reconciler` | Architect drafts; reconciler scans for drift against existing specs / docs |
| Implementation | `constructor` | Writes the code + happy-path tests; tests reference scenario IDs |
| Author's adversarial pass | `adversary` | Adds boundary / failure-case / contract-violation tests |
| PR open → review | `reconciler` (advisory) | Optional: scans PR for drift between spec ↔ code, posts an advisory comment |
| Pre-merge operability check | `operator` | Reads the diff for log-line entity coverage, error-class disambiguation, metrics on hot paths |
| Bug investigation | `detective` | Read-only investigation; produces a hypothesis + recommended fix |
| Decision record | `archivist` | Files the spec status flip; records consolidated patterns across discoveries |

The personas don't replace the human reviewer. They produce structured input that makes the human review faster and the author's PR sharper.

---

## When the lead invokes which persona

The lead (the developer running Claude Code) decides which personas fire on a given story. Heuristics:

- **Trivial story (1–2 files, no spec):** constructor only. Skip architect, archivist's recall, reconciler.
- **Standard story:** archivist (recall) → architect (if no spec exists) → constructor → adversary → operator (if production-bound) → reconciler (drift) → archivist (encode).
- **Multi-file change (≥5 files):** add operator and reconciler unconditionally; consider scout fan-out (archivist + reconciler in parallel) on the opening recall.
- **Bug investigation:** detective first, then constructor for the fix.

The agentic team's lead.md prompt describes the full default flow. Read it for nuance.

---

## How agent output lands in GitHub artifacts

The personas write into the same files the GitHub workflow reads:

- **architect** → `specs/F-*.md` (the same template the GitHub spec-PR uses).
- **constructor** → source files + test files. Tests carry the same `@pytest.mark.scenario("SC-...")` markers the spec-lint workflow looks for.
- **adversary** → additional test files in the same test directories.
- **operator** → small edits to log lines, error messages, metrics calls (in source files; small commits).
- **reconciler** → no file writes; produces flagged-drift output that the lead acts on.
- **archivist** → `memory/` (cross-repo, persistent across sessions) and updates to `specs/index.md` when status flips.

In short: the agentic team writes into files the GitHub workflow already cares about. There's no parallel artifact stream to maintain.

---

## What the human reviewer still does

The agentic team **augments** the human; it does not replace them. The reviewer's job (per `REVIEW_AS_ADVERSARY.md`) is unchanged:

- Verify scenario coverage by reading the tests, not trusting the marker.
- Check operability claims by reading the log lines and metrics calls.
- Sanity-check that the spec ↔ code binding actually holds.
- Catch out-of-scope expansion, architectural creep, and operability gaps.

When the agentic personas have run, the human reviewer's job is *easier* — many of the load-bearing checks were done by adversary and operator before the PR opened. But the human still owns the approval. Approval is a claim about the human's reading of the code; the agentic personas don't get a vote.

---

## When the agentic team is not present

If a contributor opens a PR without using the agentic personas — visiting from another team, contributing as an external collaborator, or simply not using Claude Code that day — the GitHub workflow still works. The PR template's required checklist is the human-facing equivalent of the agentic disciplines:

- "Adversarial pass done by author" maps to what `adversary` would have done.
- "Operator pass" maps to what `operator` would have done.
- The spec-lint CI catches the same scenario-id traceability issues that `reconciler` would catch.

The agentic team is a productivity multiplier, not a gate. **The GitHub workflow does not require it.**

---

## Cost-of-running considerations

When the agentic team is invoked on every story, model-call costs accumulate. The lead's job includes deciding when not to invoke:

- Trivial stories: constructor only is fine.
- Routine refactor with strong test coverage already: skip operator if no observability changes.
- Bug fix where the cause is obvious: skip detective.

The cost discipline is the same as for any agentic-team session — see `agentic_team_starter/docs/VALUE_PROPOSITION.md` for the broader framing.

---

## Where to read more

- `agentic_team_starter/docs/ARCHITECTURE.md` — the full agentic team rationale.
- `agentic_team_starter/.claude/agents/lead.md` — the lead's prompt; describes the routing logic.
- The the demo team agent team is at `.claude/agents/` (live, in `.gitignore`, not in tracked history).

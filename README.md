# weatherbot

> **Demo repository for the `github-setup` workflow.** This is not a real product. The code is intentionally small; the point is the *team workflow* — issues, PRs, specs, the Definition of Done, the review process. Click around the [issues](../../issues), [pull requests](../../pulls), and [project board](../../projects) to see what a small team's day-to-day looks like under this setup.

## ⚠ Solo-demo note

In real use, the [github-setup workflow](https://github.com/b0rgcube/github-setup) is designed for a 4-person team where two senior ICs (tech lead + senior data scientist) share PR review authority. **This repo is a one-person demo.** Two things are different from a real adoption:

1. **Branch protection's "require approvals" rule is disabled** — GitHub doesn't allow self-approval on a PR you authored, so with one user the rule would lock all merges. In a real adoption, this rule is **on**, and the two seniors auto-review every PR.
2. **All CODEOWNERS routes go to `@b0rgcube`** — stand-in for the whole team. In a real repo, owners are split between the two senior ICs; CODEOWNERS auto-requests both on every PR.

Everything else — the PR template, CI checks, spec ↔ test scenario-ID binding, issue templates, labels, the Definition of Done discipline — works exactly as it would in a real adoption. The demo's job is to show the *shape*; one person can't demonstrate two-person review, but they can demonstrate everything else.

## What's interesting to look at

If you have 5 minutes:

- **[The PR template](.github/PULL_REQUEST_TEMPLATE.md)** — the load-bearing artifact. Required checklist items, CI-enforced. This is what compensates for not having QA.
- **[An example merged PR](../../pulls?q=is%3Apr+is%3Amerged)** — see the template in action with real commit history and review comments.
- **[The in-flight PR](../../pulls?q=is%3Apr+is%3Aopen)** — a PR mid-conversation, with review comments awaiting response.
- **[The spec for F-CORE-001](specs/F-CORE-001-show-weather.md)** — how features are specified before code starts. Note the `SC-001-NN` scenario IDs; tests reference them via `@pytest.mark.scenario("SC-001-01")` markers.
- **[Issues](../../issues)** — labels do the work of a Project board: priority (`P0`/`P1`/`P2`/`P3`), type (`story`/`bug`/`tech-debt`/`spike`), and code touched (`code: backend`/`code: frontend`/etc.). In real adoption, the team would pair this with a GitHub Project board (Backlog → Triaged → Ready → In Progress → Review → Done); the board wasn't created here because the demo token doesn't have the `project` scope, and re-authing mid-build adds friction without changing the design.
- **[The post-mortem](docs/postmortems/)** — what happens after a P0 incident (the cache-TZ-bug).
- **[Issue #16 → PR #17](../../issues/16)** — *requirements-as-code* in action. Filing the story auto-opened a draft spec PR with a pre-filled stub; the dev (or AI teammate) checks out that PR and writes the spec there. No "remember to write the spec" step. See `.github/workflows/spec-pr-from-story.yml`.

If you have 30 minutes:

- Read `docs/WORKFLOW.md` cover-to-cover.
- Read `docs/DEFINITION_OF_DONE.md` — the team's quality contract.
- Read `docs/REVIEW_AS_ADVERSARY.md` — what reviewers do.
- Browse a few issues and the Conversation tab on a couple of merged PRs.

## What this demo *is*

A weather CLI. `weatherbot show Copenhagen` returns a deterministic mock reading for now; the v0.2 plan is to wire in a real weather API with a fallback path. The codebase is ~150 lines of Python — small enough to read in one sitting.

```bash
pip install -e ".[dev]"
weatherbot show Copenhagen
# Copenhagen: 17°C, cloudy
```

## What this demo is *not*

- A real product. Don't use this to plan your weekend.
- A complete representation of the team's workflow — see the solo-demo note above.
- An actual GxP-ready repo. See [`docs/GXP_UPGRADE_PATH.md`](docs/GXP_UPGRADE_PATH.md) for what that would actually require.

## How the demo was generated

This repo was bootstrapped from the `github-setup` starter pack and seeded with a handful of issues and PRs to feel alive. The shape of issues, PR conversations, and review comments are designed to look like what a real small team produces — not random noise. If something feels artificial, it probably is; flag it and I'll polish.

## Layout

```
github-setup-demo/
├── README.md                 ← this file
├── pyproject.toml            ← Python packaging
├── src/weatherbot/
│   ├── __init__.py
│   ├── cli.py                ← weatherbot show <city>
│   └── providers.py          ← MockProvider, WeatherProvider protocol
├── tests/
│   └── test_show_sc_001.py   ← tests bound to SC-001-NN
├── specs/
│   ├── index.md
│   ├── _template.md
│   └── F-CORE-001-show-weather.md
├── docs/
│   ├── WORKFLOW.md           ← the loop end-to-end
│   ├── BACKLOG_AND_PRIORITIZATION.md
│   ├── SPRINT_PROCESS.md
│   ├── DEFINITION_OF_DONE.md
│   ├── REVIEW_AS_ADVERSARY.md
│   ├── HOTFIX_AND_BUGS.md
│   ├── RELEASE_AND_DEPLOY.md
│   ├── GXP_UPGRADE_PATH.md
│   ├── ONBOARDING.md
│   ├── AGENTIC_TEAM_INTEGRATION.md
│   └── postmortems/
│       └── 2026-06-13-cache-tz-bug.md
└── .github/
    ├── PULL_REQUEST_TEMPLATE.md
    ├── ISSUE_TEMPLATE/
    ├── CODEOWNERS
    └── workflows/             ← pr-checks, spec-lint, stale-issues
```

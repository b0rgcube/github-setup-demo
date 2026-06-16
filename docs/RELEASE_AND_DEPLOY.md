# Release and deploy

How a merged PR gets to staging and production. This setup is opinionated: **the team owns deployment**. There is no separate release manager. The team that wrote the code is responsible for it being live.

If your team has a different operating model (a separate platform team owns prod deploys, for example), this doc is the *interface* — the team's responsibility ends at "merged to main" and the platform team picks up. The shape below is for teams that own both.

---

## Two release cadences

This setup supports two cadences, parallel to the sprint vs kanban choice:

### Cadence A — Continuous deployment

Every merge to `main` deploys to staging automatically. Promotion to production happens via tag (or via a manual approval step in the deploy workflow).

```
PR merge → CI build → staging deploy (auto)
                          │
                          ▼
                     team verifies in staging
                          │
                          ▼
                     manual: tag v*.*.*
                          │
                          ▼
                  production deploy (auto on tag)
```

**Best for:** teams that ship multiple times a day; teams whose changes are small and well-tested; teams whose product surface tolerates rapid iteration.

### Cadence B — Sprint-end release

Builds accumulate on `main` over the sprint; a release goes out at sprint end (typically Friday afternoon, before retro).

```
PR merges (sprint week 1) → all in staging
PR merges (sprint week 2) → all in staging
                                ↓
                        Sprint review verifies
                                ↓
                        Tag release v*.*.*
                                ↓
                        Production deploy
```

**Best for:** teams that need a more visible release cadence (e.g. customer comms tied to releases); teams whose changes are larger; teams that haven't yet built confidence in continuous deploy.

The sprint-end release Friday is the *latest* moment to release; teams can release more often, but they always release at least at sprint end.

---

## Tagging convention

Both cadences use semantic versioning tags: `v{major}.{minor}.{patch}`.

- **Patch** for bug fixes only.
- **Minor** for new functionality, backwards-compatible.
- **Major** for breaking changes.

Tags are signed (via the same signed-commit infrastructure as branch protection):

```bash
git tag -s v1.4.2 -m "Release 1.4.2 — snippet rotation, audit log"
git push --tags
```

The release workflow (`.github/workflows/release.yml`) fires on tag push. It builds artifacts, runs migrations (gated), deploys to production, and notifies the team channel.

---

## Hotfix tags

For hotfix releases, use a hotfix branch from the prior release tag:

```bash
git checkout v1.4.2
git checkout -b hotfix/critical-bug
# fix
git push origin hotfix/critical-bug
# PR with [hotfix] tag, merge, then:
git tag -s v1.4.3 -m "Hotfix 1.4.3 — fix snippet rotation race condition"
git push --tags
```

The hotfix tag fires the same release workflow but with `--hotfix` semantics (faster path, smaller artifact set, see deploy workflow detail).

---

## Pre-release verification

Before tagging a release, the team verifies in staging:

- [ ] All staging smoke tests pass
- [ ] Manual click-through of the changes shipped in this release
- [ ] No `P0` or `P1` bugs open against staging
- [ ] Migration plan reviewed (if migrations are present)
- [ ] Rollback plan understood (link to the doc, even if it's "git revert + redeploy")

The team owns this. There's no QA running these checks — the dev team does, with the same adversarial discipline as in code review.

For larger releases, the tech lead may delegate the click-through to multiple devs by area. Don't rely on one person to verify everything.

---

## What the release workflow does

The `.github/workflows/release.yml` (not in this starter pack — it's project-specific) typically:

1. Builds the artifacts (Docker images for backend + worker; static bundles for frontend).
2. Pushes to the artifact registry.
3. Runs migrations (gated — manual approval for production).
4. Deploys to the target environment.
5. Runs post-deploy smoke tests.
6. Notifies the team channel (success or failure).

For the demo team specifically, this includes:
- Building backend image, pushing to ECR.
- Updating Fargate service definitions.
- Running ARQ worker rollover (drain old workers, start new ones).
- MongoDB migrations (if any) via the existing migration tool.
- Frontend bundle to S3 / CloudFront.

The exact mechanics live in the project's own `.github/workflows/release.yml`. This setup doesn't ship one — every project's deploy is too specific.

---

## Rollback

The team's rollback plan is mandatory; the form depends on the release.

### Minor / patch release: revert + redeploy

Most rollbacks are a `git revert` of the merge commit, push to main, which auto-deploys to staging; verify; tag a new patch; promote to production.

### Migration-bearing release: backwards-compatible by default

Any migration that's part of a release should be backwards-compatible with the previous version of the code. This means:
- Deploy migration first (only adds; doesn't break).
- Deploy code that uses the new schema.
- (Later, in a separate release) deploy a cleanup migration that removes the old shape.

This is more work; it's worth it because rollback becomes "redeploy old code" rather than "redeploy old code + reverse migration."

If a migration is incompatible (rare; should be questioned hard during spec review), the rollback plan must be explicit, written, and rehearsed.

### Hotfix rollback

If a hotfix introduces a worse problem than the original bug, immediate revert. The hotfix path's "Risk" section in the PR is supposed to surface this; if it didn't, post-mortem.

---

## Post-deploy

### Watch metrics

The team watches the metrics dashboard for 30 minutes after a production deploy:

- Error rates by endpoint
- Latency (p50, p95, p99)
- Worker queue depth
- Critical business metrics (rotations/min for F-CCS-042 example)

If anything spikes, hotfix path triggers immediately.

### Update the release log

A short release log lives at `docs/releases/<version>.md`:

```markdown
# v1.4.2 — 2026-06-18

## Changes
- F-CCS-042: snippet rotation API
- Bug fixes: #492, #495

## Migrations
- Add `rotation_events` collection
- Add `version_history` index on snippets

## Deployed
- 2026-06-18 14:30 UTC (staging)
- 2026-06-18 16:45 UTC (production)

## Notes
- First customer-visible rotation: 2026-06-18 17:02 UTC
```

This is a tiny doc. It exists for the team's own future reference and for any auditor (under a future GxP regime) who wants to know what was released when.

---

## What this doc explicitly leaves to the project

- **Specific deploy mechanics** (which AWS service, which IaC tool, which secret manager). This setup is workflow, not platform.
- **Specific monitoring tooling** (Datadog, CloudWatch, Grafana, Honeycomb).
- **Specific approval gates** (some teams require a security review before production; some don't).
- **Customer comms about releases** (status pages, release notes for users, marketing copy).

The release-and-deploy *shape* is what this doc commits to. The rest is your project's existing infrastructure choices.

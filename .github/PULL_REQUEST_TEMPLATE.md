<!--
  PR template — required checkboxes are enforced by CI.
  See docs/DEFINITION_OF_DONE.md for what each item actually means.

  If your PR is a hotfix, prefix the title with "[hotfix]" and a different
  required block will activate. See docs/HOTFIX_AND_BUGS.md.
-->

## Summary

<!-- One paragraph: what changed, and why. Reviewers read this first. -->

## Linked issues

- Closes #
- Spec: <!-- specs/F-{AREA}-{NNN}-*.md  OR  "no spec required: <reason>" -->

## How to verify

```bash
# The exact command(s) a reviewer can run to verify this works.
# Example:
#   make test
#   curl -X POST http://localhost:8000/api/v1/snippets/42/rotate
```

## Test output

<!-- Paste the relevant output, OR link the CI run if it's already green. -->

```
$ make test
…
```

---

## Required checklist

> Each item below is mandatory. Tick honestly. Use `N/A — <reason>` for items
> that genuinely don't apply (e.g. doc-only PRs). The CI lint refuses to merge
> if any item is blank or incomplete.

- [ ] **Linked story / spec / discovery** above are filled in
- [ ] **Acceptance criteria covered** — every criterion in the linked issue has at least one matching test
- [ ] **Spec scenarios covered** — every `SC-{NNN}-{NN}` in the linked spec has at least one test referencing it (`@pytest.mark.scenario("SC-...")` for Python; equivalent grep-able marker for other stacks)

### Adversarial pass — done by author before opening this PR

- [ ] Boundary inputs tested: empty, single, max size, off-by-one
- [ ] Contract violations tested: wrong type, `None` where value expected, malformed shape
- [ ] Failure modes tested: external service down, timeout, partial result
- [ ] Concurrency considered (and tested if applicable; explicit "deferred to integration" if not unit-testable)
- [ ] Spec failure-case scenarios all have negative-path tests
- [ ] New failure modes discovered during this work added to the spec (or filed as follow-up)

### Operator pass — done by author before opening this PR

- [ ] Log lines in changed code name the relevant entities (request id, user id, resource id, etc.)
- [ ] Errors distinguish faults: user-input vs internal vs third-party
- [ ] Hot-path operations have count + latency + failure-by-class metrics (or `N/A — operator-irrelevant: <reason>`)
- [ ] Side-effect-producing calls are safe to retry (or explicitly documented as not)
- [ ] Error messages give the on-call a path forward

### Final hygiene

- [ ] No new lint warnings
- [ ] No new TODO without owner + date
- [ ] Out-of-scope items NOT silently expanded — diff stays in scope of the linked story
- [ ] Documentation updated if user-facing or onboarding-relevant

<!--
  ─────────────────── HOTFIX BLOCK ───────────────────
  Activate by prefixing the PR title with [hotfix].
  Below replaces the standard checklist for hotfixes.

  ## HOTFIX
  - [ ] Linked incident: # (or external incident reference)
  - [ ] Linked bug: #
  - [ ] Smallest viable change confirmed (no scope creep)
  - [ ] Tested locally (output pasted above)
  - [ ] Risk of this change: <one paragraph>
  - [ ] Rollback plan: <one sentence>
  - [ ] **Follow-up issue filed for full DoD compliance:** #
        (Must be filed before this PR merges. Required.)
-->

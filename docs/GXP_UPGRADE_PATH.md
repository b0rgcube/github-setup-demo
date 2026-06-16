# GxP upgrade path — what this setup does (and does not) deliver

**Read this carefully if regulatory status is changing.** Misreading this doc could create compliance liability.

---

## Honest framing — what this doc is not

This nimble setup is **not GxP-compliant**. Adopting the changes described below will not, by themselves, make a project GxP-compliant. They will get you closer; the rest is human work, audited tooling, and signed-off SOPs that aren't in this repo.

The right phrase for this setup is:

> **"GxP-compatible scaffolding"** or **"upgrade path toward compliance"** —
> *not* "GxP-compliant," "GxP-ready," "Annex 11 compliant," or "21 CFR Part 11 compliant."

Those phrases require a validated quality management system (QMS), documented Installation/Operational/Performance Qualification (IQ/OQ/PQ), a quality assurance function with documented authority, audit trails on all GxP-relevant actions, and supplier qualification of every tool in the chain — including GitHub itself. None of that is delivered here. **Do not write into a customer-facing or auditor-facing document any phrase that asserts compliance.**

If you are reading this because regulation just got confirmed, the honest first step is to engage a quality / compliance function (internal or external). This doc is what your engineering team can offer them as a starting point — not the destination.

For the heavy, audit-shaped predecessor designed around GxP from day one, see `gxp-github/`. That setup is far more comprehensive and should be the basis of any actual compliance effort. This nimble setup's GxP upgrade path is the *engineering-side scaffolding* that complements (not replaces) those processes.

---

## What the toggle actually does

If your project's GxP status changes from "unconfirmed / not GxP" to "GxP applies," and you decide to keep using this nimble setup as the engineering-side scaffolding, here is what changes:

### Layer 1 — Repo configuration (cheap to apply)

These are low-effort changes that bring the repo closer to GxP-compatibility:

| Change | What it adds | Effort |
|---|---|---|
| Enable signed commits / signed tags via branch protection | Cryptographic provenance on what got merged and who tagged the release | Low |
| Tighten branch protection: require linear history, require status checks, require *2* reviewers (currently 1) | Two-person rule on every change | Low |
| Add `requirements/` directory with frontmatter schema (`status: draft / review / approved / superseded`) | Requirements-as-code with explicit lifecycle | Medium |
| Add `.gxp/` folder with control-catalog stubs and risk-tier policy | A spine the team and any future auditor can follow | Medium |
| Add `validation/` directory for IQ/OQ/PQ artifacts | A place for the quality function to land their evidence | Low (creates the slot; filling it is the quality function's work) |

The starter pack `gxp-github/` has full templates for all of these. This nimble setup leaves the *slots* for them obvious — the upgrade path is "import from `gxp-github/`," not "redesign from scratch."

### Layer 2 — CI workflows (medium effort, real value)

| Workflow added | What it enforces |
|---|---|
| `traceability-check.yml` | Every approved requirement has a linked spec, every spec has linked tests, every test references a scenario id |
| `compliance-gate.yml` | PRs to `main` blocked unless required artifacts (test results, traceability matrix) are present and passing |
| `release-evidence.yml` | On tag, builds an evidence bundle (test results, traceability matrix, signed-commit verification, dependency manifest) and attaches to the release |
| `access-review.yml` | Periodically reports CODEOWNERS / branch protection / repo-permission state for review |

These workflows are in `gxp-github/.github/workflows/` and are designed to be copy-pasted into a GxP-toggled-on repo. **They are not in this nimble setup by default** because the audit-evidence shape is overhead for a non-regulated project.

### Layer 3 — Process and people (hardest, not in this repo)

The toggle's first two layers are mechanical. The third is not:

- **Documented SOPs** for change control, deviation handling, periodic review.
- **Quality function with documented authority** to gate releases.
- **Trained personnel** with documented role-based authorities.
- **Supplier qualification** of GitHub, of the CI runners, of every package the build depends on.
- **Computer system validation (CSV) package**: IQ, OQ, PQ on the build/release pipeline.
- **Audit trails** on user actions, code changes, deployment events — *retained per the regulatory regime's record-retention requirements*.
- **Periodic access reviews** (the CI workflow above generates the *report*; the *review* itself is human work).

This is real work. It is not optional. Ignoring it is the path that creates audit findings.

---

## What the toggle does NOT deliver

To be explicit about what's NOT included:

- **Validated tooling.** GitHub, GitHub Actions, Python, npm registries, Docker, AWS — none of these are validated for GxP use by this setup. Validation is a process the quality function runs, with vendor-supplied documentation, and culminating in IQ/OQ/PQ artifacts. None of that is automated.
- **Electronic signature** in the 21 CFR Part 11 / Annex 11 sense. PR approvals in GitHub are not legal e-signatures. They are *evidence* (and can support a Part 11 e-signature claim with the right surrounding controls), but they are not, in themselves, sufficient.
- **Audit trail retention** on the regulatory timeline. GitHub's audit log retention is finite and depends on plan. GxP audit trails commonly require 6-year+ retention (longer for some jurisdictions). The CI evidence-bundle workflow helps export, but storage is an external concern.
- **Computer system validation.** The CSV package — system-level evidence that the tooling does what it says it does, configured correctly, used correctly — is human work, often months of it, that the quality function delivers.
- **Training records.** The quality function's documented evidence that team members are trained on the SOPs.
- **Deviation and CAPA processes.** When something goes wrong, the regulated workflow has explicit deviation reports and corrective/preventive action tracking. None of that is automated here.

If a stakeholder reads this nimble setup and concludes it's "good enough for GxP," they have misread the doc. **Surface this passage explicitly when asked.**

---

## The honest sequence if regulation is confirmed

The path is roughly:

1. **Engage quality / compliance function.** They define what GxP means for *your specific* product, in your specific regulatory geography, for your specific intended use. *"GxP" is a category, not a specification* — the actual requirements depend on whether you're under Part 11, Annex 11, an ISO regime, a regional pharmacovigilance authority, etc.
2. **Risk assessment.** Categorise the system; determine which controls apply at what depth. Some systems can use lighter validation; some require the heaviest possible.
3. **Adopt the heavy GxP scaffolding** from `gxp-github/`. Layer 1 + 2 above. This is the *engineering-side* delivery.
4. **Quality function delivers Layer 3.** SOPs, training, validation package, audit trails, signed-off authorities. This is months of work; it does not happen alongside engineering work, it precedes (or, more honestly, runs in parallel and gates) engineering work.
5. **Adapt the team's process** to reflect what the SOPs say. The reviewer-as-adversary mechanism is fine for non-GxP; under GxP it needs to be augmented with documented role-based reviews and signed-off acceptance.
6. **First validated release** is a milestone, not a week's work. Plan accordingly.

If anyone in the team's organisation suggests skipping any of these steps, the honest answer is "we cannot make that compliance claim." Don't soften it.

---

## What the nimble setup gives you for free as preparation

Even without confirmed regulation, the nimble setup includes patterns that make a future GxP transition *much* cheaper:

- **Spec ↔ code traceability** via `F-{AREA}-{NNN}` / `SC-{NNN}-{NN}` IDs — already grep-able, already CI-enforced. The traceability matrix a regulator wants is *exactly this data*, just packaged differently.
- **CODEOWNERS and signed reviews** — the basic shape of role-based change control is already there.
- **Definition of Done** with explicit, mechanical, CI-enforced checklist items — exactly the shape a quality function will want, just expanded with their additional fields.
- **Post-mortems with action tracking** — the bones of a deviation/CAPA process; needs documented escalation rules and signoffs to be CAPA-grade.
- **Issue templates and PR templates** — the structured-input shape that GxP tooling demands; needs to be augmented with required regulatory fields (risk tier, spec linkage, validation status).
- **No-QA compensating controls** are explicitly named — see `DEFINITION_OF_DONE.md`. The compensating-controls pattern is what an auditor will look for in the absence of a separate QA function. Naming it explicitly preempts an audit finding.

Adopting this nimble setup is *not* a step away from GxP-compliance — it's a step *toward* GxP-readiness, with the heavy-weight machinery deferred to when (or if) it's needed.

---

## How to flip individual pieces on without going all-in

You may want some of the GxP patterns without committing to full compliance. Here's the menu:

| You want… | Adopt this from `gxp-github/` |
|---|---|
| Stricter requirements lifecycle (draft → approved → superseded) | The frontmatter schema in `requirements-as-code` |
| Two-person rule on all changes | Branch protection settings |
| Evidence bundle on every release | `release-evidence.yml` workflow |
| Access review automation | `access-review.yml` workflow |
| Periodic compliance audit reports | `compliance-gate.yml` workflow |

Each is a copy-paste plus a configuration step. None of them, alone, makes you GxP-compliant. Together with Layer 3 (process and people), they support a compliance claim.

---

## Decision checklist for the team

When considering a GxP claim — even partial — answer these before adopting any of the above:

- [ ] Has the quality / compliance function been engaged?
- [ ] Has the regulatory regime been determined (Part 11? Annex 11? Other?)
- [ ] Has the system been risk-assessed?
- [ ] Is there a validated SDLC SOP we can map this workflow to?
- [ ] Is there a CSV plan?
- [ ] Are records retention requirements understood?
- [ ] Is there budget and timeline for Layer 3 (process and people)?

If most are "no," the honest position is: *"We are aware of and prepared for a future GxP transition. We are not currently making any compliance claim."* That position is defensible. Anything stronger is not.

---

## What this doc is NOT a substitute for

This doc is technical-team-facing. It does not replace:

- Legal review of compliance posture.
- Regulatory affairs assessment of the specific product.
- Quality / compliance function's design of SOPs and validation packages.
- A formal Computer System Validation plan.

If you're being asked to make a GxP claim and don't have the above, **say no.** Saying no costs less than saying yes incorrectly.

---

## A note on language for stakeholders

If you're asked by a non-technical stakeholder ("Can we say this is GxP-compliant?"), the honest answer is some version of:

> *"This setup is structured to make a future GxP claim possible without a rewrite. By itself, it does not make us compliant. Compliance requires processes, people, and validation work that lives outside the codebase. If we need to make a compliance claim, the right next step is engaging quality and regulatory affairs."*

Don't soften this. The cost of making an incorrect GxP claim — to customers, to regulators, to the organisation's licence — is far higher than the cost of saying "not yet."

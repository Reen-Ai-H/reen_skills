---
name: product-design
description: Lead a digital product from an early idea or an existing-product redesign through a structured product interview, durable local product documentation, three distinct visual worlds, implementation, independent audit, real-user or real-model evaluation, repair loops, and GitHub release. Use when the user asks Codex to design, redesign, build, manage, or ship a product end to end; asks for a product interview or PRD; wants several agents or tasks coordinated; wants visual prototypes before coding; or wants a long-running product program with evidence-based acceptance and minimal routine approvals.
---

# Product Design Lifecycle

Run the product as a durable program, not a single prompt. Preserve product intent in local documents, delegate bounded work to stable roles, and pass evidence through explicit gates.

## Start with the interview

1. Inspect the repository, existing product, and current facts before asking questions when a project already exists.
2. Distinguish user-approved decisions from agent-authored guesses. When provenance is unclear, ask whether the current documents are an accepted baseline before inheriting them.
3. Ask one consequential question at a time. Challenge assumptions, hidden tradeoffs, and edge cases instead of collecting a shallow questionnaire.
4. Keep ordinary clarification compact. Ask at most five related low-risk questions together only when their answers do not affect one another.
5. Reflect each accepted answer as a precise decision with scope, consequences, and rejected alternatives.
6. Continue until the core decisions are coherent: user, job, pain, promise, scope, non-goals, primary flows, data/AI boundary, business/operations, risks, and success evidence.
7. Do not code or generate final visual directions before the interview gate passes unless the user explicitly asks for a throwaway exploration.

Read [interview-and-docs.md](references/interview-and-docs.md) for the interview map and document contracts.

## Establish durable project memory

After the interview reaches a stable baseline:

1. Create or reconcile `AGENTS.md`, `docs/README.md`, `docs/PRODUCT_SPEC.md`, `docs/DECISIONS.md`, `docs/UX_FLOWS.md`, `docs/DESIGN_SYSTEM.md`, `docs/ACCEPTANCE.md`, `docs/AGENT_WORKFLOW.md`, `PROGRESS.md`, and `BLOCKED.md`.
2. Use `scripts/bootstrap_project.py` only to create missing files. Never overwrite existing project facts automatically.
3. Make `docs/PRODUCT_SPEC.md` the current product answer. Treat implementation and old README files as evidence of current state, not authority over accepted decisions.
4. Record every later product change in `docs/DECISIONS.md` before changing the specification, flows, design, tests, or implementation.
5. Keep temporary execution history in `PROGRESS.md`; keep unresolved decisions in `BLOCKED.md`; keep stable facts in `docs/`.

## Run a permission and task preflight

Before starting worker tasks:

1. Inspect effective project configuration and project trust.
2. If the user explicitly authorizes unattended local development, configure the trusted project for the requested model and reasoning level and for non-interactive local execution. Use `gpt-5.6-luna` with `max` reasoning by default for this workflow when supported.
3. For the user's fully autonomous mode, use project-local `.codex/config.toml` with `approval_policy = "never"` and `sandbox_mode = "danger-full-access"`; keep it machine-local and ignored by Git unless the user explicitly wants to share it.
4. State that this removes routine Codex approval prompts, not platform safeguards, OS authentication, lock screens, provider limits, or irreversible external-action boundaries.
5. Remember that a running task keeps its launch-time permission snapshot. If it remains stuck on an obsolete approval prompt after configuration is fixed, stop or archive it and create a replacement only with the user's authorization.

Official configuration details can change. When changing Codex configuration, use the `openai-docs` skill and verify against current official documentation.

## Orchestrate stable roles

Use a manager plus stable specialist roles. Reuse the same task for each role across stages; do not create a new task for every bug or review cycle.

- **Product lead / design director:** Own the interview, decisions, priorities, task briefs, and final product/visual judgment. Do not become the primary implementer.
- **Research:** Gather current market, user, technical, or policy evidence when the decision needs it.
- **Visual design:** Produce three independent visual worlds from the same functional brief.
- **R&D:** Implement the accepted direction and provide reproducible evidence.
- **Independent audit:** Test claims adversarially without sharing the implementer's conclusions.
- **Quality evaluation:** Exercise real user, data, device, or model paths under a capped budget.
- **Release governance:** Reconcile docs, Git state, CI, artifacts, and rollback before publishing.

Parallelize only independent work. Use at most three active workers by default. Give each writable worker a separate worktree or disjoint ownership; never let two agents write the same checkout or files concurrently. Keep audit read-only while R&D writes, or audit a frozen commit.

Read [orchestration.md](references/orchestration.md) before creating or resetting tasks.

## Create three visual worlds

Default to three genuinely different visual worlds, not three color swaps.

1. Give every visual agent the same product facts, page/state matrix, content constraints, and viewport targets.
2. Keep their visual references and output directories isolated so one direction does not anchor the others.
3. Require complete image prototypes for the agreed representative pages, including key states, before implementation.
4. Define for each world: concept, emotional promise, layout grammar, typography, color, material, motion principle, signature component, and explicit anti-patterns.
5. Use image generation for visual discovery when the user requests image prototypes. Use real raster prototypes as references, then translate the accepted system into code; never ship screenshot backgrounds or transparent click maps.
6. Review all three against the same product criteria. Select one world or an explicit combination, and record the decision before coding.

Treat references as specifications after selection. For fidelity work, inspect each image, reproduce macro layout first, and compare reference and implementation at the same viewport using side-by-side and overlay evidence.

## Execute through gates

Run these gates in order unless the user explicitly narrows scope:

1. **Discovery gate:** Interview decisions and unknowns are documented.
2. **Specification gate:** Product, flows, data semantics, design constraints, and acceptance agree.
3. **Visual gate:** Three worlds exist; one direction is accepted and frozen enough to build.
4. **Prototype gate:** Critical flows are clickable with realistic states; fake capabilities are clearly labeled.
5. **Implementation gate:** Persistent data, error states, accessibility, and core tests work end to end.
6. **Independent audit gate:** P0/P1 findings are zero; lower findings are fixed or explicitly accepted.
7. **Quality gate:** Representative real-user or real-model outputs meet the rubric and cost cap.
8. **Release gate:** Documentation, repository, CI, build provenance, artifacts, rollback, and public claims agree.

Read [gates-and-evidence.md](references/gates-and-evidence.md) for pass criteria and anti-cheating rules.

## Manage the build loop

For each stage:

1. Write an outcome-focused goal with scope, protected paths, baseline numbers, permission boundary, verification matrix, and stop conditions.
2. Have R&D implement and self-correct until the stage evidence is green.
3. Require a structured callback containing what users can now do, key changes, actual commands/results, screenshots, blockers, and estimated overall completion.
4. Give the same independent auditor a focused verification goal. Do not ask R&D to declare its own audit passed.
5. Route findings back to the same R&D task, then return them to the same auditor for closure.
6. Keep implementation as the majority of effort. Timebox audits to the smallest matrix that can disprove the claims; widen only when evidence reveals risk.
7. Stop a failing action after three materially identical attempts. Record the exact blocker and continue all unaffected work.

Use [goal-contract.md](references/goal-contract.md) when drafting worker goals and callbacks.

## Apply autonomy boundaries

Proceed without routine confirmation for authorized, in-scope, reversible local work: reading, editing, dependency installation, local servers, tests, browser QA, screenshots, and non-destructive Git inspection.

Proceed with external Git writes only when the user has explicitly included commit, push, PR, or release in the requested lifecycle and the exact target is known. Reconfirm immediately before an irreversible public release when the authorization is not already explicit.

Pause for:

- real payment, purchases, or uncapped paid API use;
- credential creation, rotation, exposure, or repurposing;
- destructive deletion or irreversible data migration;
- public production deployment or publication not already authorized;
- OS authentication, lock-screen, account recovery, or platform hard-safety prompts;
- a missing product decision that materially changes users, scope, safety, or business model.

Do not pause for ordinary implementation choices. Make a reversible assumption, record it, and continue.

## Close the lifecycle

Before declaring completion:

1. Reconcile stable decisions and runtime facts with project docs.
2. Remove stale competing answers while preserving historical evidence and user data.
3. Verify the Git diff, tests, browser matrix, security/privacy boundaries, and model/provider observability.
4. If publishing, prove source commit, tag, CI checkout, build metadata, and downloadable artifacts resolve to the same source.
5. Commit intentionally; exclude secrets, `.env`, machine-local config, local accounts, generated user data, and temporary audit evidence.
6. Push the authorized branch and create the requested PR or release.
7. Report the outcome first, then evidence, residual risks, recovery path, and next decision.

## Resources

- `scripts/bootstrap_project.py`: Create missing lifecycle documents and optional autonomous Luna Max project configuration without overwriting existing files.
- `assets/templates/`: Minimal project-memory templates copied by the bootstrap script.
- `references/interview-and-docs.md`: Interview and single-source-of-truth rules.
- `references/orchestration.md`: Multi-agent topology, task reuse, permissions, and handoffs.
- `references/gates-and-evidence.md`: Lifecycle gates, visual QA, audit, evaluation, and release evidence.
- `references/goal-contract.md`: Worker goal and callback structure.

# Goal and callback contract

## Worker goal

Write goals in this order:

1. **Outcome:** What the user can do when the stage is complete.
2. **Authority:** Which local writes, tests, browsers, dependencies, Git actions, API calls, or external writes are authorized.
3. **Facts:** Repository path, current branch/commit, current test counts, authoritative documents, and known constraints.
4. **Scope:** Required features, states, and artifacts.
5. **Protected boundaries:** Paths, user data, credentials, design assets, public systems, and behaviors that must remain unchanged.
6. **Work loop:** Inspect, implement, verify, self-review, repair, and repeat.
7. **Acceptance matrix:** Exact tests, browser paths, viewports, security checks, screenshots, quality rubric, and release evidence.
8. **Anti-cheating rules:** No skips, weakened assertions, fake persistence, silent fallback, screenshot backgrounds, or self-declared audit pass.
9. **Stop conditions:** Three identical failures, a true missing product decision, system hard barrier, or explicit cost cap.
10. **Callback:** Required structured report and instruction to stop at the stage boundary.

Keep goals outcome-focused. Do not prescribe implementation details unless they protect a fragile contract.

## Callback format

Require:

```text
Stage N completion report

What users can now do
- ...

Key changes
- ...

Actual commands and results
- command -> result, failures, skipped count

Browser/device/model evidence
- paths, viewports, screenshots, provider/usage summary without secrets

Data and safety
- persistence, rollback, private fields, billing/idempotency

BLOCKED
- none, or exact blocker/evidence/options

Estimated whole-product completion
- percentage with excluded work named

Stop here. Do not enter the next stage.
```

The manager must independently inspect the evidence before writing the next goal.

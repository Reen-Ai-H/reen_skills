# Gates and evidence

## Discovery and specification

Require:

- a coherent first-release promise;
- explicit scope and non-goals;
- user, system, failure, and recovery flows;
- persistent-data and AI-authority contracts;
- measurable acceptance criteria;
- a decision ledger with unresolved items separated from facts.

## Visual worlds

Use the same page/state matrix for all three worlds. Each world must include:

- a name and one-sentence concept;
- full-page images for the agreed representative screens;
- normal, loading/working, empty, error, and critical decision states where relevant;
- desktop and one narrower breakpoint for workspaces;
- motion principles for landing/login or other expressive surfaces;
- quiet behavior for dense workspaces;
- explicit anti-patterns.

Reject a direction when it is only a recolor, hides essential product states, or relies on impossible interactions.

After selection, compare implementation at matching viewport sizes. Use reference/implementation side-by-side and, for strict fidelity work, a 50% overlay. Score macro layout before decorative detail. A functioning page is not a visual pass.

## Prototype and implementation

Require:

- real clickable paths, not disconnected mock screens;
- persistent server-side or device-appropriate data where the product promises persistence;
- refresh, resume, retry, conflict, and recovery behavior;
- honest labels for fake or unavailable integrations;
- idempotency for costly or repeated actions;
- accessibility, keyboard, reduced motion, and responsive checks;
- no secrets, user data, or paid calls in automated tests.

Protect baselines. Test totals may increase but must not fall without a documented decision. Do not manufacture green tests through skips, swallowed exceptions, weakened assertions, or mocks of the unit under test.

## Independent audit

Audit claims, not merely code. Include:

- anonymous and cross-account authorization;
- private-memory or internal-field leakage at network, state, cache, DOM, and persistence boundaries;
- persistence, refresh, multi-client conflict, and fast-navigation loss;
- background work without a foreground timer dependency;
- billing/usage idempotency and insufficient-balance behavior;
- invalid/empty inputs and rollback;
- browser paths at agreed viewport sizes;
- console, overflow, focus, scroll, notification, and reduced-motion behavior.

Classify P0-P3. Do not pass with open P0/P1. Record P2/P3 as fixed, accepted with rationale, or deferred by explicit decision.

## Real quality evaluation

Keep quality evaluation independent from implementation and security audit.

1. Verify the product path actually calls the configured provider.
2. Cap requests, tokens, time, and spend before the run.
3. Never read or print credential values.
4. Save complete outputs only when they contain no secrets or private memory.
5. Score representative multi-step samples for coherence, instruction adherence, continuity, factual consistency, style, and user usefulness.
6. Stop when the provider path is not live, repeated malformed output blocks progress, or the cap is reached.
7. Distinguish implementation success from output-quality success.

## Release

Before publishing, prove:

```text
source commit = release tag = CI checkout = build metadata = downloadable artifacts
```

Also require:

- clean intentional diff;
- docs and public claims matching actual features;
- secrets, `.env`, local config, local accounts, generated user data, and audit residue excluded;
- rollback and recovery instructions;
- downloaded-artifact hash verification;
- install/start/smoke evidence on supported platforms;
- no force-push or tag movement after publication;
- repository protections and CI status read back after configuration.

Do not use a successful CI build as a substitute for downloaded-artifact verification.

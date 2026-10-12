# Interview and durable documents

## Interview sequence

Ask one consequential question at a time. Start from evidence in an existing product; do not make the user restate known facts.

Before inheriting existing documents, identify whether each major decision was explicitly accepted by the user or merely inferred by a prior agent. If provenance is unclear and the distinction changes scope, ask one baseline-authority question before proceeding.

1. Who is the primary user and what recurring situation brings them here?
2. What do they do today, and what is painful, risky, slow, or expensive?
3. What concrete outcome should the product deliver?
4. What is the smallest coherent promise for the first release?
5. Which capabilities, users, channels, and business models are explicitly out of scope?
6. What are the primary happy path, abandonment path, failure path, and recovery path?
7. Which data must persist, synchronize, remain private, or be recoverable?
8. What may AI decide, what must the user decide, and how are uncertainty and mistakes presented?
9. What operational, pricing, account, moderation, compliance, or support constraints exist?
10. What evidence would make the user accept the product as genuinely useful?

After each answer:

- restate the decision precisely;
- name the tradeoff and rejected alternative;
- test one likely edge case;
- write the accepted result to the decision ledger;
- ask the next highest-impact unresolved question.

Do not confuse “possible later” with first-release scope. Treat “maybe” as unresolved, not accepted.

## Document system

Use this hierarchy:

1. Later explicit user decisions recorded in `docs/DECISIONS.md`.
2. Current product documents.
3. Accepted visual prototypes and research evidence.
4. Current code, schemas, tests, and runtime evidence.
5. Historical README files and abandoned prototypes.

Create these documents:

- `AGENTS.md`: shortest mandatory project rules, protected data, commands, and reading order.
- `docs/README.md`: document map, authority order, current lifecycle phase, and next task.
- `docs/PRODUCT_SPEC.md`: user, promise, scope, non-goals, capabilities, data, AI boundary, accounts, operations, and launch scope.
- `docs/DECISIONS.md`: dated decisions, rationale, consequences, rejected options, and deferred questions.
- `docs/UX_FLOWS.md`: user-visible states, transitions, persistence, background work, errors, recovery, and idempotency.
- `docs/DESIGN_SYSTEM.md`: selected world, page grammar, typography, color, components, motion, responsive behavior, and anti-patterns.
- `docs/ACCEPTANCE.md`: measurable functional, data, visual, accessibility, security, quality, and release standards.
- `docs/AGENT_WORKFLOW.md`: how tasks start, resume, report, and stop.
- `PROGRESS.md`: current goal, baseline, completed evidence, next action, and active task IDs.
- `BLOCKED.md`: unresolved decisions or true blockers with evidence and options.

Keep one detailed home for each fact. Link or summarize elsewhere; never maintain several independent copies.

## Interview gate

Pass when:

- the primary user and job are specific;
- the first-release promise is one coherent sentence;
- scope and non-goals prevent obvious expansion;
- core flows include failure and recovery;
- data and AI authority are explicit;
- acceptance evidence is measurable;
- remaining unknowns are non-blocking or recorded in `BLOCKED.md`.

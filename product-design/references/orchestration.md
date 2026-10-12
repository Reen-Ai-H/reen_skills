# Multi-agent orchestration

## Stable topology

Keep one visible, durable task per long-lived role when the product needs user-visible tasks:

| Role | Writes | Reuse rule | Primary output |
| --- | --- | --- | --- |
| Product lead | Product docs and goals | Entire lifecycle | Decisions and stage briefs |
| Research | Research evidence only | Reuse by topic | Source-backed brief |
| Visual world A/B/C | Own output directory/worktree | Reuse through selection | Complete image prototype set |
| R&D | Implementation worktree | Reuse for every repair stage | Working product and evidence |
| Audit | Audit artifacts only | Reuse for every recheck | Severity-ranked independent report |
| Quality evaluation | Eval artifacts only | Reuse across model/user tests | Scored samples and cost evidence |
| Release | Release branch/docs | Reuse for release candidates | Provenance and rollback report |

Use subagents for bounded parallel research, comparison, and fresh validation. Use user-owned sidebar tasks when the user explicitly wants durable visible tasks or long-running work.

## Concurrency

- Default to a manager plus at most three active workers.
- Parallelize three visual worlds because outputs are isolated.
- Parallelize research with repository inspection.
- Run audit concurrently with implementation only against a frozen commit or in strict read-only mode.
- Never assign two writers to the same checkout, branch, state file, or document set.
- Do not run release actions while implementation or audit is mutating the candidate.

## Task launch preflight

Before launch:

1. Verify project trust and effective `.codex/config.toml`.
2. Verify requested model and reasoning effort explicitly. For this workflow, prefer `gpt-5.6-luna` and `max` when supported.
3. Verify the permission policy before creating tasks; running tasks retain old snapshots.
4. Record each task ID, host, role, branch/worktree, write boundary, and current cursor in `PROGRESS.md`.
5. Pin durable roles and give them descriptive titles.
6. Tell every worker where to report completion and require it to stop at the stage boundary.

## Fixed-task repair loop

Use this loop:

```text
R&D stage N -> structured callback -> independent audit N
  -> findings -> same R&D task stage N+1 repair
  -> same audit task targeted recheck -> close or repeat
```

Do not create a fresh auditor for each finding. A new auditor may perform a final cold audit after closure, but should not replace the fixed audit loop.

## Prevent approval churn

- Configure permissions before task launch.
- Put authorization boundaries once in the goal; repeated “ask first” language causes unnecessary pauses.
- Explicitly authorize safe local reads, writes, dependency installation, tests, browsers, and screenshots.
- Keep credential values out of goals; refer only to configured environment variables.
- If a task asks for an obsolete approval after configuration changed, do not keep clicking indefinitely. Preserve its report, stop/archive it, and relaunch from the same repository state after authorization.
- Never claim that full access bypasses OS, account, platform, provider, or hard-safety controls.

## Failure rules

- Retry transient tool/provider failures at most twice after the initial attempt.
- After three materially identical failures, record the blocker and stop that action.
- Continue unaffected work.
- Do not mark a stage complete because time or token budget is low.
- Do not let an auditor write production fixes; route findings to R&D.
- Do not let R&D grade its own final visual or security acceptance.

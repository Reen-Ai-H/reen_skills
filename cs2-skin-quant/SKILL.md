---
name: cs2-skin-quant
description: Analyze current CS2 skin markets, normalize CSQAQ/C5GAME API and browser-visible YouPin/BUFF snapshots, calculate executable cash-equivalent value, screen entries, generate manual trade plans, manage unlock-to-exit decisions, and evaluate a small real-money trading journal. Use when Codex or Claude Code is asked to scan CS2 skin opportunities, configure or use official C5GAME/CSQAQ APIs, inspect web-only marketplace quotes, compare third-party cash markets with Steam, calculate 挂刀/搬砖 returns, review an existing position, prepare a buy or sell order sheet, or assess whether the 1000 RMB experiment has passed its 30-trade validation gate.
---

# CS2 Skin Quant

Operate as a research and decision-support agent for a controlled 1000 RMB CS2 skin experiment. Never present the workflow as high-frequency trading or promise profit.

## Load the right references

- Read [references/risk-policy.md](references/risk-policy.md) before producing any entry, exit, sizing, or continuation decision.
- Read the newest dated `references/strategy-update-*.md` overlay referenced by the risk policy before a live purchase scan; apply it wherever it is stricter than the base policy.
- Read [references/data-sources.md](references/data-sources.md) before fetching current quotes, fees, restrictions, or API data. Read [references/web-market-visibility.md](references/web-market-visibility.md) before using a browser-visible YouPin/BUFF page.
- Read [references/journal-schema.md](references/journal-schema.md) before creating or evaluating trade records.

## Enforce the authority boundary

- Analyze, rank, calculate, and prepare an operation sheet.
- Require the user to approve every real-money order throughout the first 30 closed trades.
- Keep every Steam login, purchase, listing, Trade Offer, and mobile confirmation manual permanently.
- Never request passwords, cookies, Steam Guard codes, API secrets, or session tokens in chat.
- Never use browser automation, scripts, bots, macros, or unofficial endpoints to interact with Steam.
- Keep non-Steam marketplace actions read-only unless the user is visibly completing them manually; the Skill may inspect a public or user-opened page but must never auto-buy, auto-list, auto-reprice, auto-withdraw, or auto-confirm.
- Never evade a cooldown, Trade Protection, rate limit, robot check, anti-crawl control, or platform rule.
- Use only public or officially authorized data interfaces. Stop and explain when compliant data is unavailable.

## Run the workflow

1. **Establish state.** Record cash RMB, discounted Steam Wallet, inventory marked at executable net value, open positions, locked positions, category exposure, account peak equity, and current drawdown. Treat missing state as unknown rather than zero.
2. **Check rule events.** Verify current Valve restrictions and whether a material CS2 economy update occurred within 48 hours. Pause new entries during the event window.
3. **Collect timestamped snapshots.** Prefer CSQAQ for discovery and C5 OpenAPI for order-book confirmation. When CSQAQ API access is configured, verify it with `scripts/csqaq_api.py --health` and use the read-only client described in the data-source reference. When C5 access is configured, use `scripts/c5_api.py health` and then `stats`/`max-buy`; keep the app-key out of output. For YouPin/BUFF, use the web-market visibility reference and record browser-visible evidence rather than pretending it is an API feed. Recheck fees and withdrawal rules from official pages.
4. **Normalize candidates.** Exclude knives, gloves, souvenirs, rare patterns, special floats, and sticker-dependent premiums during the validation phase. Record bid depth, 30-day volume, spread, fees, data age, and proposed quantity.
5. **Calculate executable value.** Put one candidate or a candidate array into the schema accepted by `scripts/evaluate_candidate.py`. Supply ten liquid-item Steam Wallet conversion observations. Run the script; do not reproduce its arithmetic mentally when execution is available.
6. **Reject before ranking.** Discard every candidate with a hard-policy breach. Rank eligible candidates by conservative executable edge, liquidity quality, and thesis clarity—not by model confidence alone.
7. **Produce a manual order sheet.** Include item, exact variant, platform, buy limit, quantity, all-in cost, cash net value, discounted Steam net value, selected exit route, conservative edge, spread, depth, unlock estimate, invalidation trigger, and required user action. Mark the sheet `RESEARCH — MANUAL APPROVAL REQUIRED`.
8. **Manage exits.** Recalculate executable net value from fresh snapshots. Follow the day 0–22 schedule in the risk policy. Do not defer an exit merely because the position is losing.
9. **Record the result.** Append one JSONL record following the journal schema after a position closes. Preserve the original forecast separately from realized values.
10. **Evaluate continuation.** After at least 30 closed trades, run `scripts/summarize_journal.py`. Do not recommend increasing capital unless every continuation gate passes.

## Handle live data honestly

- Browse or call current official sources whenever the request depends on live prices, fees, restrictions, or API behavior.
- Attach a timezone-aware observation timestamp and source URL to every quote set.
- Reject a candidate when required data is stale, internally inconsistent, or only visible as a non-executable listing.
- Separate facts, calculations, and judgment in the output. Label estimates explicitly.
- Treat a lowest listing or recent sale as context, never as executable account value.

## Output format

Lead with one of: `NO TRADE`, `CANDIDATE FOR APPROVAL`, `EXIT ACTION REQUIRED`, or `INSUFFICIENT COMPLIANT DATA`.

Then provide:

1. Decision and policy checks.
2. A compact order or exit sheet.
3. Calculation inputs and source timestamps.
4. Failure conditions and the next manual action.

When no candidate passes, say `NO TRADE`; never lower a hard threshold to force activity.

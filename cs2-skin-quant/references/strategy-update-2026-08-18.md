# Purchase strategy overlay — 2026-08-18

This is a temporary, stricter overlay on top of `risk-policy.md`. It is valid from the snapshot below until the next live scan; it does not relax any base hard gate.

## Market snapshot

Source: CSQAQ `current_data?type=init`, observed at **2026-08-18 15:44 CST**.

- Broad 饰品指数: **1490.99, +0.95% 1d**.
- The five size buckets were all negative over 7d: **中大件 -3.12%, 小件 -4.28%, 中小件 -3.73%, 中件 -3.36%, 大件 -1.63%**.
- Breadth was weak: **6,257 positive vs 15,129 negative over 7d (29.3% positive)**; 15d breadth was 27.2% positive.
- CSQAQ classified market sentiment as **低迷**. Current online count was 659,256 and the same-time weekly comparison was -0.8%.
- The main-weapon index was the relative leader on the day (+3.41%); M4A4 (+0.24% 1d, -2.58% 7d) and MP9 (+0.56% 1d, -4.01% 7d) were less weak than many other gun groups, but neither is an automatic buy.

The working regime is therefore **technical rebound inside a broad downtrend**, not risk-on. The latest official CS2 update visible on Steam is dated 12 Aug; no material Valve/CS2 economy update was found in the last 48 hours, so the 48-hour event gate is currently clear. Re-check this before every order.

## Temporary purchase rules

1. **Keep the 100 RMB per-item cap.** Reduce maximum total inventory exposure from 70% to **50%** until the regime exits. Keep the remaining 50% in cash RMB; discounted Steam Wallet is not cash.
2. Open **at most one new locked position every 48 hours**. Do not average down and do not use a second position to rescue a losing thesis.
3. The base 4% conservative executable-edge floor remains a safety rejection rule. For this overlay, an actual purchase requires:
   - API-confirmed candidate: **at least 6%** conservative net edge; **10%+ is the normal target**.
   - Web-only candidate: take an extra **2 percentage-point uncertainty haircut** and require at least 6% edge *after* that haircut (normally at least 8% raw edge), with a visible executable cash bid.
   - 4–6% is observation-only, even if all other checks pass.
4. Prefer ordinary, homogeneous rifles/SMGs whose category is not down more than 5% over 7d and is non-negative on the day. Current data makes M4A4/MP9-style liquidity profiles preferable to deeply weakening pistol, sticker, knife, glove, or pattern-premium segments; the validation exclusions still apply.
5. Require two fresh executable sources for a standard candidate (CSQAQ plus C5, or CSQAQ plus a browser-visible cash bid). If only one compliant source is available, keep the item observation-only. If an API is IP-bound, times out, or the two sources disagree materially, mark **NO TRADE** rather than estimating the missing quote.
6. Keep all existing spread, depth, 30-day volume, stress, age, cooldown, manual-approval, and Steam-manual rules unchanged. Cash exit remains the default; do not use Steam Wallet arbitrage or gifting.

## Resume condition

Return to the base cadence only after a fresh scan shows both: 7d positive breadth at or above **40%**, and at least **3 of the 5 size buckets** no longer negative over 7d. A Valve/CS2 economy update within 48 hours immediately reactivates the event pause regardless of breadth.

## Sources

- [CSQAQ current-data documentation](https://docs.csqaq.com/api-187131779)
- [Steam Counter-Strike 2 official activity page](https://steamcommunity.com/app/730)

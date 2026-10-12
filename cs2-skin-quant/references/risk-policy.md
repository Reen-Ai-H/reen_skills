# Risk policy

These are hard constraints agreed for the validation phase. Do not relax them because an opportunity looks attractive.

## Current regime overlay

Before the next scan, read the latest dated file matching `references/strategy-update-*.md`. The overlay is temporary and may only make these constraints stricter. The current 2026-08-18 overlay reduces total inventory exposure to 50%, limits new locked positions to one every 48 hours, and raises the operational entry target to 6% (10% preferred); its live-scan evidence and resume conditions are recorded in [strategy-update-2026-08-18.md](strategy-update-2026-08-18.md).

## Capital and authority

- Starting capital: 1000 RMB.
- Maximum single-position all-in cost: 10% of current experiment equity, initially 100 RMB.
- Maximum total inventory exposure: 70%; keep at least 30% as cash reserve.
- Maximum exposure to one weapon, collection, or shared supply thesis: 20%.
- Open at most one new locked position per natural day.
- Require user approval for every real-money order through the first 30 closed trades.
- Keep all Steam actions manual permanently.
- Do not implement gifting or any other Steam Wallet cash-out mechanism.

Value account equity as:

`cash RMB + executable inventory net value + discounted Steam Wallet`

Do not use listing prices as inventory value.

## Validation universe

Use homogeneous, liquid ordinary gun skins. Exclude:

- knives and gloves;
- souvenirs;
- rare patterns or phases;
- special-float premiums;
- sticker-dependent premiums;
- any item whose value cannot be normalized from comparable executable bids.

## Entry gates

Reject a candidate if any condition fails:

- conservative executable net edge is below 4%; treat 4–8% as observation tier and prefer at least 8%;
- spread exceeds 8%;
- 30-day average daily real volume is below 20 times planned quantity;
- top-three executable bid depth is below 3 times planned quantity;
- stress loss exceeds 8%;
- the order breaches single, total, category, or daily position limits;
- required price data is more than 20 minutes old;
- a material Valve/CS2 economy update occurred within the last 48 hours;
- the item depends on a premium excluded above.

## Steam Wallet conversion

Build a daily basket of ten liquid, homogeneous items. For each item compute:

`cash conversion observation = executable cash bid / Steam acquisition cost`

Use the median of the ten observations as the raw conversion rate. Apply a further 5% safety haircut:

`conservative conversion rate = basket median × 0.95`

Count Steam Wallet as part of equity only at this conservative rate.

## Exit route

Calculate both routes from executable prices after all fees and slippage:

- cash net value: executable cash bid minus selling, withdrawal, fixed, and expected slippage costs;
- Steam net value: seller receipt multiplied by the conservative conversion rate.

Prefer the cash route. Select Steam only when its discounted executable net value is at least 3% higher than the cash route. Steam Wallet remains non-cash, non-transferable account value.

## Exit schedule

Count days from the first day the item can be transferred or listed again:

- Days 0–7: seek the volatility-adjusted profit target.
- Days 8–10: price for execution within 72 hours.
- Days 11–12: accelerate price improvement.
- Days 13–15: price for execution within 24–48 hours.
- Day 15: default exit.
- Days 16–22: allow one manually approved extension only when all four extension tests pass.
- Day 22: mandatory exit; never grant a second extension.

Allow the one-time extension only when:

1. the original thesis remains valid for a reason other than “the position is losing”;
2. depth, spread, and volume have not materially deteriorated;
3. conservative expected holding return exceeds the opportunity cost of eligible new candidates;
4. the extension does not breach total, category, or drawdown constraints.

Set the default profit target to:

`max(5%, robust seven-day volatility)`

Estimate robust seven-day volatility from executable-bid daily returns:

`sigma7 = 1.4826 × MAD(last 60 daily returns) × sqrt(7)`

Set the item risk scale to:

`max(8%, 2 × sigma7 + spread)`

The item should have been rejected at entry if this risk scale exceeds 12%. Trigger a risk exit after two independent fresh snapshots cross the scale. Exit immediately when an official update invalidates the thesis.

## Account drawdown

- At 8% drawdown: reduce new position count or size.
- At 10% drawdown: halt all new entries and review the strategy.
- At 15% drawdown: terminate the experiment and manage exits only.

## Thirty-trade continuation gate

Do not increase capital unless all conditions pass after at least 30 closed trades:

- cumulative realized net profit is positive;
- Profit Factor is greater than 1.2;
- maximum account-equity drawdown is below 10%;
- at least 80% of positions execute within 72 hours after unlock;
- account, platform, and rule incidents equal zero.

Track average realized slippage and day-15/extension exits as diagnostics. They do not replace the five gates.

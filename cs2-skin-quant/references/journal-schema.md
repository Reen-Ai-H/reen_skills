# Journal schemas

Use JSON for candidate evaluation and JSONL for closed-trade history. Keep original forecasts immutable.

## Candidate input

`scripts/evaluate_candidate.py` accepts one object or an array of objects:

```json
{
  "candidate_id": "2026-08-05-ak47-example",
  "item_name": "Exact Steam market name",
  "item_type": "ordinary-gun-skin",
  "is_homogeneous": true,
  "has_special_premium": false,
  "capital": 1000,
  "current_total_exposure": 400,
  "current_category_exposure": 100,
  "new_positions_today": 0,
  "buy_cost_total": 90,
  "quantity": 1,
  "cash_bid_gross_total": 98,
  "cash_sell_fee_rate": 0.0,
  "cash_withdraw_fee_rate": 0.01,
  "cash_fixed_fee": 2,
  "cash_slippage_rate": 0.01,
  "steam_buyer_total": 125,
  "steam_fee_rate": 0.15,
  "wallet_conversion_observations": [0.72, 0.71, 0.73, 0.72, 0.70, 0.74, 0.71, 0.72, 0.73, 0.71],
  "spread_pct": 0.05,
  "avg_daily_volume_30d": 100,
  "top3_bid_depth_qty": 10,
  "expected_stress_loss_pct": 0.06,
  "hours_since_major_update": 120,
  "data_age_minutes": 8,
  "source_timestamp": "2026-08-05T10:00:00+08:00",
  "source_urls": ["https://example.invalid/current-snapshot"]
}
```

Provide either `steam_buyer_total` plus `steam_fee_rate`, or a direct `steam_seller_receipt_total` when the executable seller receipt is known.

All percentages are decimal fractions. All monetary values are RMB or RMB-equivalent for one proposed order, not per unit, unless the field explicitly says otherwise.

## Closed-trade JSONL

Write one JSON object per line:

```json
{"trade_id":"T001","closed_at":"2026-09-01T12:00:00+08:00","realized_net_pnl":4.2,"account_equity_after":1004.2,"hours_to_execution_after_unlock":36,"exit_stage":"days-0-7","forecast_exit_net":96.0,"realized_exit_net":94.8,"incident_count":0}
```

Required fields:

- `trade_id`: stable unique identifier.
- `realized_net_pnl`: proceeds minus all-in cost after every fee.
- `account_equity_after`: cash plus executable inventory value plus discounted Steam Wallet immediately after closing.
- `hours_to_execution_after_unlock`: elapsed hours from unlock to execution.
- `incident_count`: account, rule, platform, or unauthorized-automation incidents attributable to the trade.

Recommended fields:

- `opened_at`, `unlock_at`, `closed_at`;
- `item_name`, `quantity`, `entry_platform`, `exit_platform`;
- immutable entry snapshot and forecast identifiers;
- `forecast_exit_net`, `realized_exit_net`;
- `exit_stage`: `days-0-7`, `days-8-10`, `days-11-12`, `days-13-15`, or `extension-days-16-22`;
- decision notes and source timestamps.

Do not rewrite losing trades, omit failed orders, or replace original forecasts after observing the result.


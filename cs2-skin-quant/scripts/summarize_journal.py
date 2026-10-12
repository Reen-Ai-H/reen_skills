#!/usr/bin/env python3
"""Summarize closed CS2 skin trades and evaluate the 30-trade gate."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


def finite_number(record: dict[str, Any], key: str, line_number: int) -> float:
    value = record.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"line {line_number}: {key} must be a finite number")
    return float(value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("journal", type=Path, help="closed-trade JSONL file")
    parser.add_argument("--starting-equity", type=float, default=1000.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        records = []
        for line_number, line in enumerate(args.journal.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError(f"line {line_number}: record must be an object")
            records.append((line_number, record))
        if args.starting_equity <= 0 or not math.isfinite(args.starting_equity):
            raise ValueError("starting equity must be positive")

        profits: list[float] = []
        equity_curve = [float(args.starting_equity)]
        within_72h = 0
        incidents = 0.0
        slippages: list[float] = []
        extension_exits = 0
        trade_ids: set[str] = set()

        for line_number, record in records:
            trade_id = record.get("trade_id")
            if not isinstance(trade_id, str) or not trade_id.strip():
                raise ValueError(f"line {line_number}: trade_id must be a non-empty string")
            if trade_id in trade_ids:
                raise ValueError(f"line {line_number}: duplicate trade_id {trade_id}")
            trade_ids.add(trade_id)
            pnl = finite_number(record, "realized_net_pnl", line_number)
            equity = finite_number(record, "account_equity_after", line_number)
            hours = finite_number(record, "hours_to_execution_after_unlock", line_number)
            incident_count = finite_number(record, "incident_count", line_number)
            if equity <= 0 or hours < 0 or incident_count < 0 or not incident_count.is_integer():
                raise ValueError(f"line {line_number}: equity must be positive; hours and integer incident_count must be non-negative")
            profits.append(pnl)
            equity_curve.append(equity)
            within_72h += int(hours <= 72)
            incidents += incident_count
            extension_exits += int(record.get("exit_stage") == "extension-days-16-22")
            forecast = record.get("forecast_exit_net")
            realized = record.get("realized_exit_net")
            if isinstance(forecast, (int, float)) and isinstance(realized, (int, float)) and forecast > 0:
                slippages.append((float(forecast) - float(realized)) / float(forecast))

        gross_profit = sum(value for value in profits if value > 0)
        gross_loss = abs(sum(value for value in profits if value < 0))
        profit_factor = math.inf if gross_loss == 0 and gross_profit > 0 else gross_profit / gross_loss if gross_loss else 0.0
        peak = equity_curve[0]
        max_drawdown = 0.0
        for equity in equity_curve:
            peak = max(peak, equity)
            if peak > 0:
                max_drawdown = max(max_drawdown, (peak - equity) / peak)
        count = len(records)
        execution_rate = within_72h / count if count else 0.0
        gates = {
            "at_least_30_closed_trades": count >= 30,
            "cumulative_net_profit_positive": sum(profits) > 0,
            "profit_factor_gt_1_2": profit_factor > 1.2,
            "max_drawdown_lt_10pct": max_drawdown < 0.10,
            "unlock_to_execution_72h_rate_gte_80pct": execution_rate >= 0.80,
            "zero_incidents": incidents == 0,
        }
        result = {
            "decision": "VALIDATION PASSED" if all(gates.values()) else "DO NOT INCREASE CAPITAL",
            "closed_trades": count,
            "cumulative_realized_net_pnl": round(sum(profits), 4),
            "gross_profit": round(gross_profit, 4),
            "gross_loss": round(gross_loss, 4),
            "profit_factor": "Infinity" if math.isinf(profit_factor) else round(profit_factor, 6),
            "max_drawdown_pct": round(max_drawdown * 100, 4),
            "unlock_to_execution_72h_rate_pct": round(execution_rate * 100, 4),
            "incident_count": incidents,
            "extension_exit_rate_pct": round((extension_exits / count * 100) if count else 0.0, 4),
            "average_realized_slippage_pct": round((sum(slippages) / len(slippages) * 100) if slippages else 0.0, 4),
            "gates": gates,
        }
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2

    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

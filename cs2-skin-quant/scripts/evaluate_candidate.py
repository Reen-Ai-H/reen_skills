#!/usr/bin/env python3
"""Evaluate CS2 skin candidates against the fixed validation policy."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Any


EXCLUDED_ITEM_TYPES = {"knife", "knives", "glove", "gloves", "souvenir", "souvenirs"}


def number(candidate: dict[str, Any], key: str) -> float:
    value = candidate.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{key} must be a finite number")
    return float(value)


def wallet_rate(observations: Any) -> tuple[float, float]:
    if not isinstance(observations, list) or len(observations) < 10:
        raise ValueError("wallet_conversion_observations must contain at least 10 values")
    values: list[float] = []
    for observation in observations:
        if isinstance(observation, dict):
            cash_bid = observation.get("cash_bid")
            steam_cost = observation.get("steam_acquisition_cost")
            if not isinstance(cash_bid, (int, float)) or not isinstance(steam_cost, (int, float)) or steam_cost <= 0:
                raise ValueError("wallet basket objects require positive cash_bid and steam_acquisition_cost")
            value = float(cash_bid) / float(steam_cost)
        elif isinstance(observation, (int, float)) and not isinstance(observation, bool):
            value = float(observation)
        else:
            raise ValueError("wallet conversion observations must be numbers or ratio objects")
        if not 0 < value <= 1.5 or not math.isfinite(value):
            raise ValueError("wallet conversion observations must be finite and between 0 and 1.5")
        values.append(value)
    raw = statistics.median(values)
    return raw, raw * 0.95


def evaluate(candidate: dict[str, Any]) -> dict[str, Any]:
    capital = number(candidate, "capital")
    buy_cost = number(candidate, "buy_cost_total")
    quantity = number(candidate, "quantity")
    if capital <= 0 or buy_cost <= 0 or quantity <= 0 or not quantity.is_integer():
        raise ValueError("capital, buy_cost_total, and quantity must be positive")

    cash_gross = number(candidate, "cash_bid_gross_total")
    sell_fee = number(candidate, "cash_sell_fee_rate")
    withdrawal_fee = number(candidate, "cash_withdraw_fee_rate")
    fixed_fee = number(candidate, "cash_fixed_fee")
    slippage = number(candidate, "cash_slippage_rate")
    if cash_gross < 0 or fixed_fee < 0:
        raise ValueError("cash bid and fixed fee must be non-negative")
    for key, rate in (("cash_sell_fee_rate", sell_fee), ("cash_withdraw_fee_rate", withdrawal_fee), ("cash_slippage_rate", slippage)):
        if not 0 <= rate < 1:
            raise ValueError(f"{key} must be between 0 and 1")
    cash_net = max(0.0, cash_gross * (1 - sell_fee) * (1 - slippage) * (1 - withdrawal_fee) - fixed_fee)

    raw_wallet_rate, conservative_wallet_rate = wallet_rate(candidate.get("wallet_conversion_observations"))
    if "steam_seller_receipt_total" in candidate:
        steam_receipt = number(candidate, "steam_seller_receipt_total")
    else:
        steam_buyer_total = number(candidate, "steam_buyer_total")
        steam_fee_rate = number(candidate, "steam_fee_rate")
        if not 0 <= steam_fee_rate < 1:
            raise ValueError("steam_fee_rate must be between 0 and 1")
        steam_receipt = steam_buyer_total / (1 + steam_fee_rate)
    steam_net = max(0.0, steam_receipt * conservative_wallet_rate)

    if steam_net >= cash_net * 1.03:
        route = "steam"
        selected_net = steam_net
    else:
        route = "cash"
        selected_net = cash_net
    edge = selected_net / buy_cost - 1

    current_total = number(candidate, "current_total_exposure")
    current_category = number(candidate, "current_category_exposure")
    new_positions_today = number(candidate, "new_positions_today")
    spread = number(candidate, "spread_pct")
    volume = number(candidate, "avg_daily_volume_30d")
    depth = number(candidate, "top3_bid_depth_qty")
    stress_loss = number(candidate, "expected_stress_loss_pct")
    update_hours = number(candidate, "hours_since_major_update")
    data_age = number(candidate, "data_age_minutes")
    if min(current_total, current_category, new_positions_today, spread, volume, depth, stress_loss, update_hours, data_age) < 0:
        raise ValueError("exposure, liquidity, risk, update, and data-age values must be non-negative")
    if spread >= 1 or stress_loss >= 1 or not new_positions_today.is_integer():
        raise ValueError("spread and stress loss must be below 1; new_positions_today must be an integer")

    source_timestamp = candidate.get("source_timestamp")
    timestamp_valid = False
    if isinstance(source_timestamp, str):
        try:
            parsed_timestamp = dt.datetime.fromisoformat(source_timestamp.replace("Z", "+00:00"))
            timestamp_valid = parsed_timestamp.utcoffset() is not None
        except ValueError:
            timestamp_valid = False
    source_urls = candidate.get("source_urls")
    source_urls_valid = isinstance(source_urls, list) and bool(source_urls) and all(
        isinstance(url, str) and url.startswith(("https://", "http://")) for url in source_urls
    )

    breaches: list[str] = []
    checks = {
        "single_position_lte_10pct": buy_cost / capital <= 0.10,
        "total_exposure_lte_70pct": (current_total + buy_cost) / capital <= 0.70,
        "category_exposure_lte_20pct": (current_category + buy_cost) / capital <= 0.20,
        "one_new_position_per_day": new_positions_today < 1,
        "spread_lte_8pct": spread <= 0.08,
        "volume_gte_20x_quantity": volume >= 20 * quantity,
        "top3_depth_gte_3x_quantity": depth >= 3 * quantity,
        "edge_gte_4pct": edge >= 0.04,
        "stress_loss_lte_8pct": stress_loss <= 0.08,
        "outside_48h_update_pause": update_hours >= 48,
        "data_age_lte_20m": data_age <= 20,
        "homogeneous_item": candidate.get("is_homogeneous") is True,
        "no_special_premium": candidate.get("has_special_premium") is False,
        "allowed_item_type": str(candidate.get("item_type", "")).lower() not in EXCLUDED_ITEM_TYPES,
        "timezone_aware_source_timestamp": timestamp_valid,
        "source_urls_present": source_urls_valid,
    }
    for check, passed in checks.items():
        if not passed:
            breaches.append(check)

    tier = "preferred" if edge >= 0.08 else "observation" if edge >= 0.04 else "reject"
    return {
        "candidate_id": candidate.get("candidate_id"),
        "item_name": candidate.get("item_name"),
        "decision": "CANDIDATE FOR APPROVAL" if not breaches else "NO TRADE",
        "manual_approval_required": True,
        "selected_exit_route": route,
        "tier": tier,
        "buy_cost_total": round(buy_cost, 4),
        "cash_net_value": round(cash_net, 4),
        "steam_seller_receipt": round(steam_receipt, 4),
        "wallet_conversion_median": round(raw_wallet_rate, 6),
        "wallet_conversion_after_haircut": round(conservative_wallet_rate, 6),
        "steam_cash_equivalent_net": round(steam_net, 4),
        "selected_net_value": round(selected_net, 4),
        "conservative_edge_pct": round(edge * 100, 4),
        "checks": checks,
        "breaches": breaches,
        "source_timestamp": source_timestamp,
        "source_urls": source_urls if isinstance(source_urls, list) else [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON candidate object or array")
    parser.add_argument("--output", type=Path, help="write JSON output to this path")
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            result: Any = [evaluate(item) for item in payload]
        elif isinstance(payload, dict):
            result = evaluate(payload)
        else:
            raise ValueError("input must be a JSON object or array")
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

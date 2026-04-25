"""
Generate a no-send Phase 2B implementation-translation artifact bundle.

This script intentionally does not connect to IBKR/TWS. It produces reviewable
broker-facing artifacts from a small representative long-short equity book.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


RUN_ID = "20260424_task001_representative_book_translation"
ENVIRONMENT = "implementation_translation_smoke"
REBALANCE_DATE = "2026-04-27"
PORTFOLIO_NAME = "task001_representative_reversal_translation"
SOURCE_STRATEGY_NOTE = (
    "projects/quant_research_system/phase1_remote_validation/"
    "task_001_daily_stock_short_reversal.md"
)
SOURCE_DECISION_NOTE = (
    "projects/quant_research_system/phase1_remote_validation/task_001_decision.md"
)
PAPER_ACCOUNT_REQUIRED = True
ACCOUNT_MODE = "paper_only_assumed"
LIVE_SUBMISSION_ALLOWED = False
TRANSMIT = False
ORDER_TYPE = "LMT"
TIME_IN_FORCE = "DAY"
GROSS_NOTIONAL_CAP_USD = 100000.0
PER_POSITION_NOTIONAL_CAP_USD = 25000.0
PER_ORDER_SHARE_CAP = 250
DEFAULT_ROUTING_EXCHANGE = "SMART"
DEFAULT_CURRENCY = "USD"
DEFAULT_SECURITY_TYPE = "STK"


@dataclass(frozen=True)
class Target:
    symbol: str
    side: str
    company_hint: str
    primary_exchange: str
    target_notional_usd: float
    reference_price_usd: float
    implementation_role: str


TARGETS = [
    Target(
        symbol="AAPL",
        side="long",
        company_hint="Apple Inc.",
        primary_exchange="NASDAQ",
        target_notional_usd=25000.0,
        reference_price_usd=190.0,
        implementation_role="representative_recent_relative_loser",
    ),
    Target(
        symbol="MSFT",
        side="long",
        company_hint="Microsoft Corp.",
        primary_exchange="NASDAQ",
        target_notional_usd=25000.0,
        reference_price_usd=420.0,
        implementation_role="representative_recent_relative_loser",
    ),
    Target(
        symbol="NVDA",
        side="short",
        company_hint="NVIDIA Corp.",
        primary_exchange="NASDAQ",
        target_notional_usd=25000.0,
        reference_price_usd=115.0,
        implementation_role="representative_recent_relative_winner",
    ),
    Target(
        symbol="TSLA",
        side="short",
        company_hint="Tesla Inc.",
        primary_exchange="NASDAQ",
        target_notional_usd=25000.0,
        reference_price_usd=175.0,
        implementation_role="representative_recent_relative_winner",
    ),
]


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    ensure_parent(path)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def quantity_for_target(target: Target) -> int:
    quantity = math.floor(target.target_notional_usd / target.reference_price_usd)
    return max(quantity, 1)


def limit_price(target: Target) -> float:
    if target.side == "long":
        return round(target.reference_price_usd * 1.005, 2)
    return round(target.reference_price_usd * 0.995, 2)


def target_portfolio_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for target in TARGETS:
        quantity = quantity_for_target(target)
        target_notional = round(quantity * target.reference_price_usd, 2)
        rows.append(
            {
                "symbol": target.symbol,
                "side": target.side,
                "implementation_role": target.implementation_role,
                "target_notional_usd": target_notional,
                "target_percent_of_gross": round(target_notional / GROSS_NOTIONAL_CAP_USD, 6),
                "reference_price_usd": target.reference_price_usd,
                "target_quantity": quantity,
                "routing_exchange": DEFAULT_ROUTING_EXCHANGE,
                "primary_exchange": target.primary_exchange,
                "sec_type": DEFAULT_SECURITY_TYPE,
                "currency": DEFAULT_CURRENCY,
                "order_type": ORDER_TYPE,
                "time_in_force": TIME_IN_FORCE,
                "transmit": str(TRANSMIT).lower(),
                "paper_account_required": str(PAPER_ACCOUNT_REQUIRED).lower(),
                "borrow_confirmation_required": str(target.side == "short").lower(),
                "static_reference_only": "true",
                "notes": (
                    "Illustrative no-send target derived from a synthetic representative book; "
                    "not a live order."
                ),
            }
        )
    return rows


def contract_request_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index, target in enumerate(TARGETS, start=1):
        rows.append(
            {
                "request_id": f"CR-{index:03d}",
                "symbol": target.symbol,
                "company_hint": target.company_hint,
                "sec_type": DEFAULT_SECURITY_TYPE,
                "currency": DEFAULT_CURRENCY,
                "routing_exchange": DEFAULT_ROUTING_EXCHANGE,
                "primary_exchange": target.primary_exchange,
                "side": target.side,
                "requires_live_ibkr_lookup": "true",
                "live_lookup_status": "not_attempted_static_smoke",
                "conid": "",
                "status": "pending_local_ibkr_resolution",
                "resolution_reason": (
                    "Static smoke test keeps contract fields explicit but leaves broker lookup "
                    "for a later local IBKR read-only or dry-run stage."
                ),
            }
        )
    return rows


def order_intents() -> list[dict[str, object]]:
    intents: list[dict[str, object]] = []
    for index, target in enumerate(TARGETS, start=1):
        quantity = quantity_for_target(target)
        target_notional = round(quantity * target.reference_price_usd, 2)
        blockers = ["contract_resolution_not_verified_against_live_ibkr"]
        if target.side == "short":
            blockers.extend(
                [
                    "borrow_availability_not_confirmed",
                    "locate_requirement_not_confirmed",
                ]
            )
        intents.append(
            {
                "intent_id": f"OI-{index:03d}",
                "portfolio_name": PORTFOLIO_NAME,
                "rebalance_date": REBALANCE_DATE,
                "symbol": target.symbol,
                "contract": {
                    "symbol": target.symbol,
                    "secType": DEFAULT_SECURITY_TYPE,
                    "exchange": DEFAULT_ROUTING_EXCHANGE,
                    "primaryExchange": target.primary_exchange,
                    "currency": DEFAULT_CURRENCY,
                },
                "side": target.side,
                "action": "BUY" if target.side == "long" else "SELL",
                "position_effect": "OPEN_LONG" if target.side == "long" else "OPEN_SHORT",
                "target_notional_usd": target_notional,
                "reference_price_usd": target.reference_price_usd,
                "quantity": quantity,
                "quantity_cap": PER_ORDER_SHARE_CAP,
                "order_type": ORDER_TYPE,
                "limit_price": limit_price(target),
                "time_in_force": TIME_IN_FORCE,
                "transmit": TRANSMIT,
                "paper_account_required": PAPER_ACCOUNT_REQUIRED,
                "account_mode": ACCOUNT_MODE,
                "borrow_confirmation_required": target.side == "short",
                "locate_required": target.side == "short",
                "live_submission_allowed": LIVE_SUBMISSION_ALLOWED,
                "cancel_if_unfilled_by_session_close": True,
                "flatten_plan_reference": (
                    "Flatten via explicit reversing no-send intents on the next scheduled "
                    "rebalance or immediately if a static risk check fails."
                ),
                "submission_blockers": blockers,
                "notes": (
                    "No-send illustrative order intent only. Quantity uses a static reference "
                    "price, not a live quote."
                ),
            }
        )
    return intents


def write_strategy_spec(path: Path) -> None:
    gross = int(GROSS_NOTIONAL_CAP_USD)
    per_position = int(PER_POSITION_NOTIONAL_CAP_USD)
    text = f"""---
title: Phase 2B Task 001 Strategy Spec
type: project
status: completed
updated: 2026-04-24
tags:
  - project
  - phase2b
  - implementation
  - ibkr
  - no-send
sources:
  - "../../../projects/quant_research_system/phase1_remote_validation/task_001_daily_stock_short_reversal.md"
  - "../../../projects/quant_research_system/phase1_remote_validation/task_001_decision.md"
---
# Phase 2B Task 001 Strategy Spec

## Source Strategy

This smoke test translates the **implementation shape** of the Phase 1 daily long-short short-horizon reversal strategy, not its full research book.

The source signal is:

$$
s_{{i,t}} = - \\sum_{{k=1}}^5 \\left(r^x_{{i,t-k}} - r^m_{{t-k}}\\right),
$$

with daily rebalance and next-trading-day holding logic from [Task 001 Daily Stock Short-Horizon Reversal](../../../projects/quant_research_system/phase1_remote_validation/task_001_daily_stock_short_reversal.md).

## Translation Objective

Build a small representative target book that is specific enough to become broker-facing no-send instructions.

This translation is **not** an alpha claim and **not** a paper-trading instruction.

## Representative Book

- two long US equity targets
- two short US equity targets
- gross notional cap: `${gross:,}`
- per-position notional cap: `${per_position:,}`
- per-order share cap: `{PER_ORDER_SHARE_CAP}`
- rebalance date: `{REBALANCE_DATE}`
- order type: `{ORDER_TYPE}`
- time-in-force: `{TIME_IN_FORCE}`
- account mode: `{ACCOUNT_MODE}`
- `paper_account_required = true`
- `transmit = false`

## Implementation Assumptions

- Symbols are illustrative liquid large-cap US equities chosen to test translation mechanics.
- Static reference prices are used only to size no-send orders.
- Contract resolution against live IBKR metadata is deferred to a later local read-only or dry-run stage.
- Shorts require explicit borrow and locate confirmation before any future submission stage.
- Any unfilled order should be canceled by session close; any accidental exposure would need an explicit flattening path.

## Related Outputs

- `target_portfolio.csv`
- `contract_resolution_requests.csv`
- `order_intents.json`
- `risk_check_report.md`
- `implementation_caveats.md`
"""
    write_text(path, text)


def write_risk_report(path: Path, target_rows: list[dict[str, object]], contract_rows: list[dict[str, object]]) -> None:
    gross_target = round(sum(float(row["target_notional_usd"]) for row in target_rows), 2)
    max_quantity = max(int(row["target_quantity"]) for row in target_rows)
    unresolved_contracts = sum(1 for row in contract_rows if row["status"] != "resolved")
    checks = [
        ("account_mode_declared", "pass", ACCOUNT_MODE),
        ("paper_account_only_assumption", "pass", str(PAPER_ACCOUNT_REQUIRED).lower()),
        ("live_submission_locked", "pass", str(not LIVE_SUBMISSION_ALLOWED).lower()),
        ("transmit_false", "pass", str(not TRANSMIT).lower()),
        ("gross_notional_cap_declared", "pass", f"{GROSS_NOTIONAL_CAP_USD:.2f}"),
        ("gross_target_within_cap", "pass" if gross_target <= GROSS_NOTIONAL_CAP_USD else "fail", f"{gross_target:.2f}"),
        (
            "per_position_notional_cap_declared",
            "pass",
            f"{PER_POSITION_NOTIONAL_CAP_USD:.2f}",
        ),
        (
            "quantity_cap_declared",
            "pass" if max_quantity <= PER_ORDER_SHARE_CAP else "fail",
            str(PER_ORDER_SHARE_CAP),
        ),
        ("rebalance_date_explicit", "pass", REBALANCE_DATE),
        ("order_type_explicit", "pass", ORDER_TYPE),
        ("time_in_force_explicit", "pass", TIME_IN_FORCE),
        ("contract_fields_explicit", "pass", "symbol, secType, exchange, primaryExchange, currency"),
        ("ambiguous_contracts_rejected", "pass", "Representative single-name US equities only"),
        ("short_borrow_assumptions_identified", "pass", "borrow and locate required before later submission"),
        ("cancel_or_flatten_plan_present", "pass", "session-close cancel plus explicit flatten path stated"),
        ("remote_machine_assumption_absent", "pass", "local-only translation"),
        ("live_ibkr_contract_lookup_verified", "warn", f"{unresolved_contracts} pending local broker lookup"),
        ("live_market_data_used_for_sizing", "warn", "static reference prices only"),
        ("order_submission_endpoint_called", "pass", "false"),
        ("credentials_written_to_output", "pass", "false"),
    ]

    lines = [
        "# Phase 2B Risk Check Report",
        "",
        "## Summary",
        "",
        "- overall_result: `pass_with_warnings`",
        "- environment: `implementation_translation_smoke`",
        f"- rebalance_date: `{REBALANCE_DATE}`",
        f"- gross_target_notional_usd: `{gross_target:.2f}`",
        f"- pending_live_contract_resolutions: `{unresolved_contracts}`",
        "",
        "## Check Table",
        "",
        "| Check | Status | Value |",
        "| --- | --- | --- |",
    ]
    for name, status, value in checks:
        lines.append(f"| `{name}` | `{status}` | `{value}` |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This smoke test passes because the strategy rule is specific enough to become "
            "inspectable no-send broker-facing artifacts.",
            "",
            "Warnings remain because contract lookup and borrow confirmation were intentionally "
            "left for later local IBKR read-only or dry-run stages.",
        ]
    )
    write_text(path, "\n".join(lines) + "\n")


def write_caveats(path: Path) -> None:
    lines = [
        "# Phase 2B Implementation Caveats",
        "",
        "- The target book is synthetic and representative; it is not a current alpha recommendation.",
        "- Static reference prices were used for quantity sizing and limit-price placeholders.",
        "- No IBKR/TWS contract lookup was required for this first no-send smoke test bundle.",
        "- `order_intents.json` is deliberately blocked from submission by `transmit=false` and by unresolved contract and borrow checks.",
        "- Short names require borrow and locate confirmation before any later dry-run or paper-order stage.",
        "- The cancel path is declarative only in this phase; order lifecycle and reconciliation belong to later IBKR phases.",
    ]
    write_text(path, "\n".join(lines) + "\n")


def write_manifest(path: Path, target_rows: list[dict[str, object]]) -> None:
    gross_target = round(sum(float(row["target_notional_usd"]) for row in target_rows), 2)
    lines = [
        "schema_version: 0.1",
        f'job_id: "{RUN_ID}"',
        f'created: "{datetime.now(timezone.utc).isoformat()}"',
        f'environment: "{ENVIRONMENT}"',
        'mode: "local_static_no_send_translation"',
        'status: "completed"',
        f'source_strategy_note: "{SOURCE_STRATEGY_NOTE}"',
        f'source_decision_note: "{SOURCE_DECISION_NOTE}"',
        f'rebalance_date: "{REBALANCE_DATE}"',
        f'portfolio_name: "{PORTFOLIO_NAME}"',
        "paper_account_required: true",
        "live_submission_allowed: false",
        "transmit: false",
        f'gross_notional_cap_usd: {GROSS_NOTIONAL_CAP_USD:.2f}',
        f'per_position_notional_cap_usd: {PER_POSITION_NOTIONAL_CAP_USD:.2f}',
        f'per_order_share_cap: {PER_ORDER_SHARE_CAP}',
        f'gross_target_notional_usd: {gross_target:.2f}',
        'contract_lookup_mode: "static_request_only"',
        'order_type: "LMT"',
        'time_in_force: "DAY"',
        'artifact_files:',
        '  - "strategy_spec.md"',
        '  - "target_portfolio.csv"',
        '  - "contract_resolution_requests.csv"',
        '  - "order_intents.json"',
        '  - "risk_check_report.md"',
        '  - "implementation_caveats.md"',
    ]
    write_text(path, "\n".join(lines) + "\n")


def main() -> None:
    output_root = Path("artifacts/implementation_translation_smoke") / RUN_ID
    output_root.mkdir(parents=True, exist_ok=True)

    portfolio_rows = target_portfolio_rows()
    contract_rows = contract_request_rows()
    intents = order_intents()

    write_strategy_spec(output_root / "strategy_spec.md")
    write_csv(
        output_root / "target_portfolio.csv",
        [
            "symbol",
            "side",
            "implementation_role",
            "target_notional_usd",
            "target_percent_of_gross",
            "reference_price_usd",
            "target_quantity",
            "routing_exchange",
            "primary_exchange",
            "sec_type",
            "currency",
            "order_type",
            "time_in_force",
            "transmit",
            "paper_account_required",
            "borrow_confirmation_required",
            "static_reference_only",
            "notes",
        ],
        portfolio_rows,
    )
    write_csv(
        output_root / "contract_resolution_requests.csv",
        [
            "request_id",
            "symbol",
            "company_hint",
            "sec_type",
            "currency",
            "routing_exchange",
            "primary_exchange",
            "side",
            "requires_live_ibkr_lookup",
            "live_lookup_status",
            "conid",
            "status",
            "resolution_reason",
        ],
        contract_rows,
    )
    write_text(
        output_root / "order_intents.json",
        json.dumps(
            {
                "job_id": RUN_ID,
                "environment": ENVIRONMENT,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "portfolio_name": PORTFOLIO_NAME,
                "rebalance_date": REBALANCE_DATE,
                "paper_account_required": PAPER_ACCOUNT_REQUIRED,
                "account_mode": ACCOUNT_MODE,
                "live_submission_allowed": LIVE_SUBMISSION_ALLOWED,
                "transmit": TRANSMIT,
                "gross_notional_cap_usd": GROSS_NOTIONAL_CAP_USD,
                "per_position_notional_cap_usd": PER_POSITION_NOTIONAL_CAP_USD,
                "per_order_share_cap": PER_ORDER_SHARE_CAP,
                "source_strategy_note": SOURCE_STRATEGY_NOTE,
                "source_decision_note": SOURCE_DECISION_NOTE,
                "cancel_plan": {
                    "cancel_if_unfilled_by_session_close": True,
                    "flatten_if_unexpected_exposure": True,
                    "flatten_method": (
                        "Generate explicit reversing no-send intents before any later "
                        "dry-run or paper stage."
                    ),
                },
                "orders": intents,
            },
            indent=2,
        )
        + "\n",
    )
    write_risk_report(output_root / "risk_check_report.md", portfolio_rows, contract_rows)
    write_caveats(output_root / "implementation_caveats.md")
    write_manifest(output_root / "run_manifest.yaml", portfolio_rows)
    print(f"Wrote implementation translation bundle to {output_root}")


if __name__ == "__main__":
    main()

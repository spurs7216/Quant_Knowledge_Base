"""Verified daily_stock contract for Phase 4 AlphaEvolve-lite."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


class DailyStockContractError(ValueError):
    """Raised when daily_stock data does not satisfy the frozen contract."""


@dataclass(frozen=True)
class DailyStockContract:
    """Field mapping frozen from remote schema evidence v2."""

    contract_id: str = "daily_stock_contract_v1"
    evidence_path: str = "artifacts/schema_evidence_v2/daily_stock_schema_report.json"
    date: str = "DlyCalDt"
    security_id: str = "PERMNO"
    issuer_id: str = "PERMCO"
    total_return: str = "DlyRet"
    ex_dividend_return: str = "DlyRetx"
    price: str = "DlyPrc"
    volume: str = "DlyVol"
    dollar_volume: str = "DlyPrcVol"
    market_cap: str = "DlyCap"
    shares_outstanding: str = "ShrOut"
    exchange: str = "PrimaryExch"
    security_type: str = "SecurityType"
    share_type: str = "ShareType"
    trading_status: str = "TradingStatusFlg"
    conditional_type: str = "ConditionalType"
    us_incorporated: str = "USIncFlg"
    industry_primary: str = "SICCD"
    benchmark_return_primary: str = "vwretd"
    benchmark_return_secondary: str = "sprtrn"

    @property
    def required_columns(self) -> list[str]:
        return [
            self.security_id,
            self.issuer_id,
            self.date,
            self.total_return,
            self.ex_dividend_return,
            self.price,
            self.volume,
            self.dollar_volume,
            self.market_cap,
            self.shares_outstanding,
            self.exchange,
            self.security_type,
            self.share_type,
            self.trading_status,
            self.conditional_type,
            self.us_incorporated,
            self.industry_primary,
            self.benchmark_return_primary,
            self.benchmark_return_secondary,
        ]

    @property
    def numeric_columns(self) -> list[str]:
        return [
            self.total_return,
            self.ex_dividend_return,
            self.price,
            self.volume,
            self.dollar_volume,
            self.market_cap,
            self.shares_outstanding,
            self.industry_primary,
            self.benchmark_return_primary,
            self.benchmark_return_secondary,
        ]


CONTRACT = DailyStockContract()

MAJOR_US_EXCHANGES = frozenset({"N", "Q", "A"})
COMMON_EQUITY_SECURITY_TYPE = "EQTY"
COMMON_SHARE_TYPE = "NS"
ACTIVE_TRADING_STATUS = "A"
REGULAR_WAY_CONDITIONAL_TYPE = "RW"
US_INCORPORATED_FLAG = "Y"


def unique_preserving_order(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(values))


def validate_columns(columns: Iterable[str], contract: DailyStockContract = CONTRACT) -> None:
    """Fail closed if any contract field is absent."""

    available = set(str(col) for col in columns)
    missing = [col for col in contract.required_columns if col not in available]
    if missing:
        raise DailyStockContractError(
            f"{contract.contract_id} missing required columns: {', '.join(missing)}"
        )


def read_mapping_file(path: str | Path) -> dict[str, str | None]:
    """Read the simple generated YAML mapping without requiring PyYAML."""

    mapping: dict[str, str | None] = {}
    for raw_line in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        mapping[key.strip()] = None if value in {"", "null", "None"} else value
    return mapping


def validate_mapping_file(path: str | Path, contract: DailyStockContract = CONTRACT) -> None:
    """Check that remote schema evidence agrees with the frozen contract."""

    mapping = read_mapping_file(path)
    expected = {
        "date": contract.date,
        "security_id": contract.security_id,
        "issuer_id": contract.issuer_id,
        "total_return": contract.total_return,
        "ex_dividend_return": contract.ex_dividend_return,
        "price": contract.price,
        "volume": contract.volume,
        "dollar_volume": contract.dollar_volume,
        "market_cap": contract.market_cap,
        "shares_outstanding": contract.shares_outstanding,
        "exchange": contract.exchange,
        "security_type": contract.security_type,
        "share_type": contract.share_type,
        "trading_status": contract.trading_status,
        "conditional_type": contract.conditional_type,
        "us_incorporated": contract.us_incorporated,
        "industry_primary": contract.industry_primary,
        "benchmark_return_primary": contract.benchmark_return_primary,
    }
    mismatches = {
        key: {"expected": expected_value, "observed": mapping.get(key)}
        for key, expected_value in expected.items()
        if mapping.get(key) != expected_value
    }
    if mismatches:
        raise DailyStockContractError(
            f"{contract.contract_id} mapping mismatch: {mismatches}"
        )


def eligibility_query_description(contract: DailyStockContract = CONTRACT) -> dict[str, object]:
    """Return the fixed universe filter as serializable metadata."""

    return {
        "us_incorporated": {contract.us_incorporated: US_INCORPORATED_FLAG},
        "security_type": {contract.security_type: COMMON_EQUITY_SECURITY_TYPE},
        "share_type": {contract.share_type: COMMON_SHARE_TYPE},
        "trading_status": {contract.trading_status: ACTIVE_TRADING_STATUS},
        "conditional_type": {contract.conditional_type: REGULAR_WAY_CONDITIONAL_TYPE},
        "exchange_in": {contract.exchange: sorted(MAJOR_US_EXCHANGES)},
        "positive_price": contract.price,
        "positive_market_cap": contract.market_cap,
        "positive_volume_for_tradability": contract.volume,
        "usable_return": contract.ex_dividend_return,
    }

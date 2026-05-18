from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from research.alphaevolve_lite.daily_stock_contract import CONTRACT
from research.alphaevolve_lite.daily_stock_forward_coverage import (
    FORWARD_COVERAGE_SCHEMA_VERSION,
    profile_daily_stock_forward_coverage,
)


class DailyStockForwardCoverageTests(unittest.TestCase):
    def test_profile_writes_topn_and_forward_availability_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "synthetic_daily_stock.csv"
            _write_synthetic_daily_stock_with_gap(csv_path)

            result = profile_daily_stock_forward_coverage(
                csv_path=csv_path,
                out_dir=Path(tmp) / "forward_coverage",
                chunksize=37,
                top_n=5,
                forward_start_date="2000-02-01",
                forward_end_date="2000-02-10",
            )

            out = Path(tmp) / "forward_coverage"
            self.assertEqual(result["schema_version"], FORWARD_COVERAGE_SCHEMA_VERSION)
            self.assertTrue((out / "forward_coverage_summary.json").exists())
            self.assertTrue((out / "forward_availability_summary.json").exists())
            self.assertTrue((out / "held_availability_prompt_cards.md").exists())
            self.assertTrue((out / "top500_daily_coverage.csv").exists())
            self.assertTrue((out / "top500_monthly_coverage.csv").exists())
            self.assertTrue((out / "top500_membership_monthly.csv").exists())
            self.assertTrue((out / "top500_permno_coverage.csv").exists())
            self.assertTrue((out / "top500_membership_churn.csv").exists())
            self.assertTrue((out / "forward_availability_by_date.csv").exists())
            self.assertTrue((out / "forward_availability_by_bucket.csv").exists())
            self.assertTrue((out / "forward_availability_by_industry.csv").exists())
            self.assertTrue((out / "forward_availability_by_exchange.csv").exists())

            summary = json.loads((out / "forward_coverage_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["schema_version"], FORWARD_COVERAGE_SCHEMA_VERSION)
            self.assertEqual(summary["top_n"], 5)
            self.assertGreaterEqual(summary["topn_month_count"], 2)
            self.assertEqual(summary["topn_distinct_permnos"], 5)
            self.assertGreater(summary["eligible_trading_date_count"], 0)
            self.assertLess(summary["daily_coverage"]["min_coverage_rate"], 1.0)

            forward = summary["forward_availability"]
            self.assertTrue(forward["enabled"])
            self.assertGreater(forward["row_count"], 0)
            self.assertLess(forward["availability_rate"], 1.0)
            self.assertGreater(
                forward["cause_counts"].get("security_not_observed_next_market_date", 0),
                0,
            )

            daily = pd.read_csv(out / "top500_daily_coverage.csv")
            self.assertLess(float(daily["coverage_rate"].min()), 1.0)
            by_bucket = pd.read_csv(out / "forward_availability_by_bucket.csv")
            self.assertIn("dollar_volume_bucket", set(by_bucket["dimension"]))


def _write_synthetic_daily_stock_with_gap(path: Path) -> None:
    rows = []
    dates = pd.bdate_range("2000-01-03", "2000-03-31")
    missing_permno = 10008
    missing_date = pd.Timestamp("2000-02-02")
    for permno in range(10001, 10009):
        for idx, date in enumerate(dates):
            if permno == missing_permno and date == missing_date:
                continue
            market_cap = 10_000_000.0 + (permno - 10000) * 1_000_000.0 + idx * 1000.0
            price = 20.0 + (permno - 10000) + idx * 0.01
            volume = 50_000.0 + (idx + 1) * (permno - 10000)
            rows.append(
                {
                    CONTRACT.security_id: permno,
                    CONTRACT.issuer_id: permno + 50000,
                    CONTRACT.date: date.date().isoformat(),
                    CONTRACT.total_return: 0.001 * ((idx % 5) - 2),
                    CONTRACT.ex_dividend_return: 0.001 * ((idx % 7) - 3),
                    CONTRACT.price: price,
                    CONTRACT.volume: volume,
                    CONTRACT.dollar_volume: price * volume,
                    CONTRACT.market_cap: market_cap,
                    CONTRACT.shares_outstanding: market_cap / price,
                    CONTRACT.exchange: "N" if permno % 2 == 0 else "Q",
                    CONTRACT.security_type: "EQTY",
                    CONTRACT.share_type: "NS",
                    CONTRACT.trading_status: "A",
                    CONTRACT.conditional_type: "RW",
                    CONTRACT.us_incorporated: "Y",
                    CONTRACT.industry_primary: 2000 + (permno % 4) * 100,
                    CONTRACT.benchmark_return_primary: 0.0001,
                    CONTRACT.benchmark_return_secondary: 0.0002,
                    "Ticker": f"T{permno}",
                    "DlyRetMissFlg": "",
                    "DlyPrcFlg": "",
                    "DlyCapFlg": "",
                    "DlyVolFlg": "",
                }
            )
    pd.DataFrame(rows).to_csv(path, index=False)


if __name__ == "__main__":
    unittest.main()

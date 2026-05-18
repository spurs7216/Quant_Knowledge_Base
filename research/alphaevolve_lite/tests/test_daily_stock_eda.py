from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from research.alphaevolve_lite.daily_stock_contract import CONTRACT
from research.alphaevolve_lite.daily_stock_eda import (
    EDA_SCHEMA_VERSION,
    build_data_guidance,
    profile_daily_stock_data,
)


class DailyStockEdaTests(unittest.TestCase):
    def test_profile_writes_prompt_and_table_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "synthetic_daily_stock.csv"
            _write_synthetic_daily_stock(csv_path)

            result = profile_daily_stock_data(
                csv_path=csv_path,
                out_dir=Path(tmp) / "eda",
                chunksize=200,
                max_input_rows=800,
                sample_modulus=5,
                max_sample_rows=200,
                deep_start_date="2000-01-03",
                deep_end_date="2000-03-31",
                deep_top_n=10,
            )

            out = Path(tmp) / "eda"
            self.assertEqual(result["schema_version"], EDA_SCHEMA_VERSION)
            self.assertTrue((out / "daily_stock_eda_summary.json").exists())
            self.assertTrue((out / "daily_stock_prompt_guidance.json").exists())
            self.assertTrue((out / "prompt_data_cards.md").exists())
            self.assertTrue((out / "numeric_summary.csv").exists())
            self.assertTrue((out / "eligible_numeric_summary.csv").exists())
            self.assertTrue((out / "sample_quantiles.csv").exists())
            self.assertTrue((out / "daily_counts.csv").exists())
            self.assertTrue((out / "deep_window" / "deep_window_summary.json").exists())

            summary = json.loads((out / "daily_stock_eda_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["schema_version"], EDA_SCHEMA_VERSION)
            self.assertGreater(summary["summary"]["rows_scanned_after_date_filter"], 0)
            self.assertGreater(summary["summary"]["unique_permnos"], 0)
            self.assertIn("prompt_rules", summary["guidance"])

            numeric_summary = pd.read_csv(out / "numeric_summary.csv")
            self.assertIn("DlyRetx", set(numeric_summary["column"]))

    def test_guidance_flags_skewed_liquidity_and_outlier_returns(self) -> None:
        numeric_summary = pd.DataFrame(
            [
                {
                    "column": "DlyPrcVol",
                    "sample_q0.5": 1_000.0,
                    "sample_q0.99": 100_000.0,
                },
                {
                    "column": "DlyRetx",
                    "sample_q0.001": -0.8,
                    "sample_q0.999": 0.9,
                },
            ]
        )
        daily_counts = pd.DataFrame(
            [{"date": "2000-01-03", "eligible_static_return_count": 500}]
        )

        guidance = build_data_guidance(
            scan_summary={
                "rows_scanned_after_date_filter": 1000,
                "max_input_rows": None,
                "unique_permnos": 100,
                "unique_eligible_permnos": 90,
                "eligibility_steps": {"eligible_static_return": 900},
            },
            numeric_summary=numeric_summary,
            daily_counts=daily_counts,
            deep_summary={"enabled": False},
        )

        joined_rules = "\n".join(guidance["prompt_rules"])
        self.assertIn("DlyPrcVol", joined_rules)
        self.assertIn("winsorization", joined_rules)
        self.assertTrue(guidance["feature_primitives"])


def _write_synthetic_daily_stock(path: Path) -> None:
    rows = []
    dates = pd.bdate_range("2000-01-03", "2000-03-31")
    for permno in range(10001, 10009):
        for idx, date in enumerate(dates):
            market_cap = 1_000_000.0 + permno * 100.0 + idx * 1000.0
            price = 10.0 + (permno % 5) + idx * 0.01
            volume = 1000.0 + (idx + 1) * (permno % 7 + 1)
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

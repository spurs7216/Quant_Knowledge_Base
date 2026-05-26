import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from research.alphaevolve_lite.daily_stock_contract import CONTRACT


def _synthetic_daily_stock_csv(path: Path, names: int = 36, days: int = 135) -> None:
    dates = pd.bdate_range("2020-01-01", periods=days)
    permnos = np.arange(20000, 20000 + names)
    rows = []
    for day_idx, date in enumerate(dates):
        market = 0.0002 * np.sin(day_idx / 11.0)
        for name_idx, permno in enumerate(permnos):
            residual = 0.002 * np.sin(day_idx / 4.0 + name_idx / 5.0)
            price = 15.0 + (name_idx % 18) + day_idx * 0.015
            volume = 400_000 + 15_000 * (name_idx % 10) + 1_500 * (day_idx % 7)
            shares = 25_000_000 + name_idx * 125_000
            rows.append(
                {
                    CONTRACT.date: date,
                    CONTRACT.security_id: permno,
                    CONTRACT.issuer_id: permno + 30000,
                    CONTRACT.ex_dividend_return: market + residual,
                    CONTRACT.total_return: market + residual,
                    CONTRACT.price: price,
                    CONTRACT.volume: volume,
                    CONTRACT.dollar_volume: price * volume,
                    CONTRACT.market_cap: price * shares,
                    CONTRACT.shares_outstanding: shares,
                    CONTRACT.exchange: "N",
                    CONTRACT.security_type: "EQTY",
                    CONTRACT.share_type: "NS",
                    CONTRACT.trading_status: "A",
                    CONTRACT.conditional_type: "RW",
                    CONTRACT.us_incorporated: "Y",
                    CONTRACT.industry_primary: 1000 + name_idx % 6,
                    CONTRACT.benchmark_return_primary: market,
                    CONTRACT.benchmark_return_secondary: market,
                }
            )
    pd.DataFrame(rows).to_csv(path, index=False)


class ExpressionBridgeFollowupTest(unittest.TestCase):
    def test_bridge_followup_runner_writes_parent_child_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            csv_path = root / "daily_stock.csv"
            out_dir = root / "bridge_followup"
            _synthetic_daily_stock_csv(csv_path)

            command = [
                sys.executable,
                "research/alphaevolve_lite/scripts/run_expression_bridge_followup.py",
                "--csv-path",
                str(csv_path),
                "--out-dir",
                str(out_dir),
                "--start-date",
                "2020-01-01",
                "--end-date",
                "2020-07-31",
                "--out-sample-start",
                "2020-04-01",
                "--top-n",
                "24",
                "--cost-grid-bps",
                "0,2.5",
                "--bridge-variant-grid",
                "daily,rebalance_5,signal_decay_5",
                "--min-names-per-side",
                "2",
                "--min-portfolio-days",
                "5",
                "--min-portfolio-day-coverage",
                "0.2",
                "--run-id",
                "unit_bridge_followup",
            ]
            completed = subprocess.run(
                command,
                cwd=Path(__file__).resolve().parents[3],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            summary = json.loads(
                (out_dir / "expression_bridge_followup_summary.json").read_text(encoding="utf-8")
            )
            self.assertEqual(summary["status"], "ok")
            self.assertEqual(summary["run_id"], "unit_bridge_followup")
            self.assertEqual(summary["result_counts"]["parent_baseline_count"], 3)
            self.assertEqual(summary["result_counts"]["bridge_child_count"], 3)
            self.assertEqual(len(summary["comparison_rows"]), 3)
            self.assertFalse(summary["decision_contract"]["promotion_allowed_from_this_run"])
            self.assertTrue((out_dir / "expression_bridge_followup_rankings.csv").exists())
            self.assertTrue((out_dir / "expression_bridge_followup_comparison.csv").exists())
            self.assertTrue((out_dir / "expression_bridge_followup_cost_sensitivity.csv").exists())

            comparison = pd.read_csv(out_dir / "expression_bridge_followup_comparison.csv")
            self.assertEqual(set(comparison["bridge_variant"]), {"daily", "rebalance_5", "signal_decay_5"})
            self.assertIn("child_minus_parent_search_sample_turnover_aware_score", comparison.columns)


if __name__ == "__main__":
    unittest.main()

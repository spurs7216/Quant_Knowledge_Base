import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from research.alphaevolve_lite.daily_stock_contract import CONTRACT
from research.alphaevolve_lite.expression_episode import (
    build_expression_episode_prompt,
    expression_novelty_diagnostics,
    parse_expression_proposals,
)
from research.alphaevolve_lite.expression_evolution import DEFAULT_EXPRESSION_SEEDS


def _synthetic_daily_stock_csv(path: Path, names: int = 35, days: int = 130) -> None:
    dates = pd.bdate_range("2020-01-01", periods=days)
    permnos = np.arange(10000, 10000 + names)
    rows = []
    for day_idx, date in enumerate(dates):
        market = 0.0002 * np.sin(day_idx / 13.0)
        for name_idx, permno in enumerate(permnos):
            ret = market + 0.001 * np.sin(day_idx / 5.0 + name_idx / 3.0)
            price = 20.0 + (name_idx % 20) + day_idx * 0.02
            volume = 500_000 + 10_000 * (name_idx % 12) + 2_000 * (day_idx % 8)
            shares = 20_000_000 + name_idx * 100_000
            rows.append(
                {
                    CONTRACT.date: date,
                    CONTRACT.security_id: permno,
                    CONTRACT.issuer_id: permno + 50000,
                    CONTRACT.ex_dividend_return: ret,
                    CONTRACT.total_return: ret,
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


class ExpressionEpisodeTest(unittest.TestCase):
    def test_parse_expression_proposals_accepts_fenced_json(self) -> None:
        proposals = parse_expression_proposals(
            """```json
{"children":[{"expression_id":"a","expression":"rank(-excess_ret)","thesis":"t","mechanism":"m","expected_effect":"e"}]}
```"""
        )
        self.assertEqual(len(proposals), 1)
        self.assertEqual(proposals[0].expression, "rank(-excess_ret)")

    def test_parse_expression_proposals_rejects_malformed_json(self) -> None:
        with self.assertRaises(ValueError):
            parse_expression_proposals('{"children": [{"expression": "rank(ret)"}')

    def test_prompt_keeps_expression_contract_visible(self) -> None:
        parent = next(seed for seed in DEFAULT_EXPRESSION_SEEDS if seed.expression_id == "expr_smoothed_rev")
        _, user_prompt = build_expression_episode_prompt(
            parent=parent,
            parent_ranking={"search_turnover": 0.5},
            prior_feedback=[],
            turn=1,
            offspring_per_turn=2,
            interface_markdown="## Fields\n- `ret`: return\n## Operators\n- `rank`: rank",
        )
        self.assertIn("Do not use raw `industry`", user_prompt)
        self.assertIn('"children"', user_prompt)
        self.assertIn("expr_smoothed_rev", user_prompt)

    def test_novelty_diagnostics_flags_exact_duplicate(self) -> None:
        novelty = expression_novelty_diagnostics(
            expression=" rank(-rolling_sum(excess_ret, 5)) ",
            parent_expression="rank(-rolling_sum(excess_ret, 5))",
            prior_expressions=[],
            near_duplicate_threshold=0.98,
        )
        self.assertTrue(novelty["exact_duplicate"])

    def test_mock_episode_runner_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            csv_path = root / "daily_stock.csv"
            out_dir = root / "episode_out"
            mock_path = root / "mock_response.json"
            _synthetic_daily_stock_csv(csv_path)
            mock_path.write_text(
                json.dumps(
                    {
                        "children": [
                            {
                                "expression_id": "child_a",
                                "expression": "rank(-rolling_mean(rolling_sum(excess_ret, 5), 5))",
                                "thesis": "smooth reversal more strongly",
                                "mechanism": "causal smoothing",
                                "expected_effect": "lower turnover with broad coverage",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            command = [
                sys.executable,
                "research/alphaevolve_lite/scripts/run_expression_episode.py",
                "--csv-path",
                str(csv_path),
                "--out-dir",
                str(out_dir),
                "--start-date",
                "2020-01-01",
                "--end-date",
                "2020-06-30",
                "--out-sample-start",
                "2020-04-01",
                "--top-n",
                "20",
                "--cost-grid-bps",
                "0,2.5",
                "--min-names-per-side",
                "2",
                "--min-portfolio-days",
                "5",
                "--min-portfolio-day-coverage",
                "0.2",
                "--parent-seed-id",
                "expr_smoothed_rev",
                "--turns",
                "1",
                "--offspring-per-turn",
                "1",
                "--mock-response-json",
                str(mock_path),
            ]
            completed = subprocess.run(
                command,
                cwd=Path(__file__).resolve().parents[3],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            summary = json.loads((out_dir / "expression_episode_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["status"], "ok")
            self.assertEqual(summary["result_counts"]["child_count"], 1)
            self.assertTrue((out_dir / "expression_episode_rankings.csv").exists())


if __name__ == "__main__":
    unittest.main()

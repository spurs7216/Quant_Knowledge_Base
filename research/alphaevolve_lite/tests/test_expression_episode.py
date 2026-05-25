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
from research.alphaevolve_lite.expression_evolution import DEFAULT_EXPRESSION_SEEDS, ExpressionSpec
from research.alphaevolve_lite.expression_population import (
    branch_stop_loss_diagnostics,
    build_population_record,
    select_expression_parent,
)


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

    def test_population_parent_selection_uses_child_survivor(self) -> None:
        root = ExpressionSpec(
            expression_id="root",
            title="root",
            thesis="root",
            expression="rank(-excess_ret)",
            mechanism="reversal",
            expected_effect="baseline",
        )
        child = ExpressionSpec(
            expression_id="child",
            title="child",
            thesis="child",
            expression="rank(-rolling_sum(excess_ret, 5))",
            mechanism="smoothing",
            expected_effect="lower turnover",
        )
        choice = select_expression_parent(
            root=root,
            turn=2,
            specs_by_id={"root": root, "child": child},
            population_records=[
                {
                    "root_expression_id": "root",
                    "expression_id": "child",
                    "record_type": "child",
                    "parent_sampling_eligible": True,
                    "selection_score": 0.25,
                }
            ],
            parent_sampling_mode="population_mixed",
        )
        self.assertEqual(choice.selected_expression_id, "child")
        self.assertEqual(choice.selection_reason, "best_scored_eligible_child_survivor")

    def test_branch_stop_loss_flags_unproductive_branch(self) -> None:
        diagnostics = branch_stop_loss_diagnostics(
            root_expression_id="root",
            root_score=0.10,
            population_records=[
                {
                    "root_expression_id": "root",
                    "record_type": "child",
                    "selection_score": 0.05,
                    "parent_sampling_eligible": True,
                },
                {
                    "root_expression_id": "root",
                    "record_type": "child",
                    "selection_score": 0.08,
                    "parent_sampling_eligible": True,
                },
            ],
            min_child_count=2,
            improvement_margin=0.0,
        )
        self.assertTrue(diagnostics["pause_branch_for_population_review"])

    def test_population_record_does_not_sample_parent_baseline(self) -> None:
        record = build_population_record(
            {
                "expression_id": "root",
                "record_type": "parent_baseline",
                "status": "expression_sample_pass",
                "metrics": {"search_sample": {"turnover_aware_score": 0.12}},
                "portfolio_coverage": {"portfolio_day_coverage": 1.0},
            },
            root_expression_id="root",
            generation=0,
            split_id="test_split",
            root_score=0.12,
            branch_child_index=0,
        )
        self.assertFalse(record["parent_sampling_eligible"])

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
                "2",
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
            self.assertEqual(summary["result_counts"]["child_count"], 2)
            self.assertEqual(summary["trajectory_summaries"]["expr_smoothed_rev"]["attempt_count"], 2)
            self.assertEqual(len(summary["parent_selection_records"]), 2)
            self.assertIn("branch_diagnostics", summary)
            self.assertTrue((out_dir / "expression_episode_rankings.csv").exists())
            self.assertTrue((out_dir / "expression_population_ledger.csv").exists())
            population_summary = json.loads(
                (out_dir / "expression_population_summary.json").read_text(encoding="utf-8")
            )
            self.assertEqual(population_summary["population_record_count"], 3)

    def test_mock_episode_runner_can_sample_prior_population_parent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            csv_path = root / "daily_stock.csv"
            out_dir = root / "episode_out"
            mock_path = root / "mock_response.json"
            prior_path = root / "prior_population.jsonl"
            _synthetic_daily_stock_csv(csv_path)
            prior_path.write_text(
                json.dumps(
                    {
                        "schema_version": "expression_population_v1",
                        "run_id": "prior_run",
                        "expression_id": "hist_child",
                        "record_type": "child",
                        "root_expression_id": "expr_smoothed_rev",
                        "parent_expression_id": "expr_smoothed_rev",
                        "turn": 1,
                        "title": "Historical child",
                        "thesis": "Historical survivor",
                        "expression": "rank(-rolling_sum(excess_ret, 10))",
                        "mechanism": "historical smoothing",
                        "expected_effect": "lower turnover",
                        "tags": ["episode_child"],
                        "status": "expression_sample_pass",
                        "selection_score": 3.0,
                        "parent_sampling_eligible": True,
                        "metrics": {"search_sample": {"turnover_aware_score": 0.5}},
                        "portfolio_coverage": {"portfolio_day_coverage": 1.0},
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            mock_path.write_text(
                json.dumps(
                    {
                        "children": [
                            {
                                "expression_id": "child_a",
                                "expression": "rank(-rolling_sum(excess_ret, 3))",
                                "thesis": "try a shorter reversal horizon",
                                "mechanism": "horizon shift",
                                "expected_effect": "test cost conversion",
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
                "2",
                "--offspring-per-turn",
                "1",
                "--run-id",
                "unit_prior_run",
                "--prior-population-ledger",
                str(prior_path),
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
            self.assertEqual(summary["prior_population"]["loaded_record_count"], 1)
            self.assertEqual(summary["parent_selection_records"][1]["selected_expression_id"], "hist_child")
            population_summary = json.loads(
                (out_dir / "expression_population_summary.json").read_text(encoding="utf-8")
            )
            self.assertEqual(population_summary["historical_population_record_count"], 1)


if __name__ == "__main__":
    unittest.main()

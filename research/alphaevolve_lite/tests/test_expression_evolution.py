import unittest

import numpy as np
import pandas as pd

from research.alphaevolve_lite.daily_stock_contract import CONTRACT
from research.alphaevolve_lite.expression_evolution import (
    DEFAULT_EXPRESSION_SEEDS,
    ExpressionAttemptRecord,
    ExpressionError,
    ExpressionEvaluationConfig,
    construct_expression_portfolio,
    evaluate_expression_signal,
    evaluate_expression_to_weights,
    expression_interface_markdown,
    expression_seed_library_rows,
    expression_similarity,
    score_expression_trajectory,
)
from research.alphaevolve_lite.scripts.run_expression_seed_zoo import _status_from_metrics


def _synthetic_panel(names: int = 60, days: int = 90) -> pd.DataFrame:
    dates = pd.bdate_range("2020-01-01", periods=days)
    permnos = np.arange(10000, 10000 + names)
    rows = []
    for day_idx, date in enumerate(dates):
        market = 0.0003 * np.sin(day_idx / 7.0)
        for name_idx, permno in enumerate(permnos):
            seasonal = 0.012 * np.sin(day_idx / 5.0 + name_idx / 4.0)
            cross = 0.004 * ((name_idx % 9) - 4) / 4.0
            ret = market + 0.2 * seasonal + cross / 100.0
            price = 20.0 + (name_idx % 20) + day_idx * 0.03
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
                    CONTRACT.share_type: "COM",
                    CONTRACT.trading_status: "A",
                    CONTRACT.conditional_type: "RW",
                    CONTRACT.us_incorporated: "Y",
                    CONTRACT.industry_primary: 1000 + name_idx % 6,
                    CONTRACT.benchmark_return_primary: market,
                    CONTRACT.benchmark_return_secondary: market,
                }
            )
    return pd.DataFrame(rows)


class ExpressionEvolutionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.panel = _synthetic_panel()
        self.config = ExpressionEvaluationConfig(max_weight=0.03, min_names_per_side=4)

    def test_expression_signal_and_portfolio_are_aligned_and_constrained(self) -> None:
        signal = evaluate_expression_signal(
            "industry_neutralize(rank(-safe_divide(rolling_sum(excess_ret, 5), rolling_std(excess_ret, 20))))",
            self.panel,
            config=self.config,
        )
        self.assertEqual(len(signal), len(self.panel))
        self.assertTrue(signal.index.equals(self.panel.index))
        self.assertGreater(signal.notna().mean(), 0.5)

        weights = construct_expression_portfolio(signal, self.panel, config=self.config)
        self.assertEqual(len(weights), len(self.panel))
        self.assertLessEqual(weights.abs().max(), self.config.max_weight + 1.0e-12)

        daily_net = weights.groupby(self.panel[CONTRACT.date]).sum()
        daily_gross = weights.abs().groupby(self.panel[CONTRACT.date]).sum()
        active_days = daily_gross[daily_gross > 0].index
        self.assertGreater(len(active_days), 30)
        self.assertLessEqual(daily_net.loc[active_days].abs().max(), 1.0e-12)
        self.assertGreater(weights[weights > 0].count(), 0)
        self.assertGreater(weights[weights < 0].count(), 0)

    def test_constant_signal_skips_ambiguous_tied_days(self) -> None:
        signal = pd.Series(1.0, index=self.panel.index)
        weights = construct_expression_portfolio(signal, self.panel, config=self.config)
        self.assertEqual(float(weights.abs().sum()), 0.0)

    def test_default_seed_library_is_evaluable(self) -> None:
        failures = []
        for seed in DEFAULT_EXPRESSION_SEEDS:
            try:
                signal = evaluate_expression_signal(seed, self.panel, config=self.config)
                if signal.notna().sum() == 0:
                    failures.append(seed.expression_id)
            except ExpressionError:
                failures.append(seed.expression_id)
        self.assertEqual(failures, [])

    def test_seed_catalog_has_unique_ids_and_expressions(self) -> None:
        seed_ids = [seed.expression_id for seed in DEFAULT_EXPRESSION_SEEDS]
        expressions = [seed.expression for seed in DEFAULT_EXPRESSION_SEEDS]
        self.assertEqual(len(seed_ids), len(set(seed_ids)))
        self.assertEqual(len(expressions), len(set(expressions)))

    def test_evaluate_expression_to_weights_smoke(self) -> None:
        weights = evaluate_expression_to_weights(
            "rank(-rolling_sum(excess_ret, 5))",
            self.panel,
            config=self.config,
        )
        self.assertGreater(weights.abs().sum(), 0.0)
        self.assertLessEqual(weights.abs().max(), self.config.max_weight + 1.0e-12)

    def test_rejects_unsafe_python_and_lookahead(self) -> None:
        bad_expressions = [
            '__import__("os").system("echo unsafe")',
            "price.__class__",
            "open(1)",
            "rank(industry)",
            "delay(ret, -1)",
            "rolling_sum(ret, 0)",
        ]
        for expression in bad_expressions:
            with self.subTest(expression=expression):
                with self.assertRaises(ExpressionError):
                    evaluate_expression_signal(expression, self.panel, config=self.config)

    def test_where_and_boolean_expression(self) -> None:
        signal = evaluate_expression_signal(
            "rank(where((excess_ret < 0) & (volume > rolling_mean(volume, 20)), -excess_ret, nan))",
            self.panel,
            config=self.config,
        )
        self.assertGreater(signal.notna().sum(), 0)

    def test_oversized_and_deep_expressions_are_rejected(self) -> None:
        bad_expressions = [
            "excess_ret" + " + excess_ret" * 300,
            "rank(" * 40 + "excess_ret" + ")" * 40,
        ]
        for expression in bad_expressions:
            with self.subTest(length=len(expression)):
                with self.assertRaises(ExpressionError):
                    evaluate_expression_signal(expression, self.panel, config=self.config)

    def test_expression_seed_status_gates_missing_held_weight(self) -> None:
        metrics = {
            "search_sample": {
                "max_weight": 0.01,
                "max_abs_net_exposure": 0.0,
                "max_missing_held_weight": 0.20,
                "turnover_aware_score": 0.10,
            }
        }
        status = _status_from_metrics(
            metrics,
            {"portfolio_coverage_pass": True},
            max_weight=0.02,
            max_abs_net_exposure=1.0e-9,
            max_missing_held_weight=0.05,
        )
        self.assertEqual(status, "expression_sample_review")

    def test_similarity_and_trajectory_score(self) -> None:
        similar = expression_similarity(
            "rank(-rolling_sum(excess_ret, 5))",
            "rank(-safe_divide(rolling_sum(excess_ret, 5), rolling_std(excess_ret, 20)))",
        )
        distant = expression_similarity(
            "rank(-rolling_sum(excess_ret, 5))",
            "industry_neutralize(rolling_sum(excess_ret, 60))",
        )
        self.assertGreater(similar, distant)

        score = score_expression_trajectory(
            [
                ExpressionAttemptRecord(
                    turn=1,
                    expression_id="a",
                    expression="rank(-rolling_sum(excess_ret, 5))",
                    valid=True,
                    score=0.12,
                ),
                ExpressionAttemptRecord(
                    turn=2,
                    expression_id="b",
                    expression="rank(-safe_divide(rolling_sum(excess_ret, 5), rolling_std(excess_ret, 20)))",
                    valid=True,
                    score=0.18,
                ),
                ExpressionAttemptRecord(
                    turn=3,
                    expression_id="c",
                    expression="rank(rolling_sum(excess_ret, 20))",
                    valid=False,
                    failure_reason="semantic",
                ),
            ],
            seed_expression="rank(-rolling_sum(excess_ret, 5))",
            parent_score=0.10,
            pass_margin=0.02,
        )
        self.assertEqual(score["attempt_count"], 3)
        self.assertAlmostEqual(score["valid_ratio"], 2 / 3)
        self.assertTrue(score["pass_at_final"])
        self.assertEqual(score["best_expression_id"], "b")
        self.assertGreaterEqual(score["improvement_streak"], 1)
        self.assertGreater(score["trajectory_score"], 0.0)

    def test_interface_exports_serializable_prompt_material(self) -> None:
        rows = expression_seed_library_rows()
        self.assertEqual(len(rows), len(DEFAULT_EXPRESSION_SEEDS))
        self.assertIn("expression_id", rows[0])
        markdown = expression_interface_markdown()
        self.assertIn("Daily-Stock Expression Interface", markdown)
        self.assertIn("Starter Seeds", markdown)


if __name__ == "__main__":
    unittest.main()

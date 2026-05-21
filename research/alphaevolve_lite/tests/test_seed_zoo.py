from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from research.alphaevolve_lite.daily_stock_contract import CONTRACT
from research.alphaevolve_lite.scripts.remote_sample_eval import load_strategy_module
from research.alphaevolve_lite.seed_zoo import (
    SEED_ZOO_SCHEMA_VERSION,
    seed_zoo_rows_from_summaries,
    write_seed_zoo_programs,
)


class SeedZooProgramTests(unittest.TestCase):
    def test_rendered_seed_zoo_programs_are_importable_and_portfolio_safe(self) -> None:
        panel = _synthetic_panel()
        with tempfile.TemporaryDirectory() as tmp:
            manifest = write_seed_zoo_programs(Path(tmp) / "seed_zoo")

            self.assertEqual(manifest["schema_version"], SEED_ZOO_SCHEMA_VERSION)
            self.assertEqual(manifest["program_count"], 10)
            for row in manifest["programs"]:
                module, _ = load_strategy_module(row["program_path"])
                signal = module.compute_signal(panel, module.DEFAULT_PARAMS)
                ranked = module.rank_or_transform_signal(signal, panel, module.DEFAULT_PARAMS)
                weights = module.construct_portfolio(ranked, panel, module.DEFAULT_PARAMS)
                controlled = module.apply_risk_controls(weights, panel, module.DEFAULT_PARAMS)

                self.assertEqual(len(controlled), len(panel), row["seed_id"])
                self.assertLessEqual(float(controlled.abs().max()), float(module.DEFAULT_PARAMS["max_weight"]) + 1e-12)
                by_date = controlled.groupby(panel[CONTRACT.date])
                active_dates = [date for date, values in by_date if values.abs().sum() > 0.0]
                self.assertGreater(len(active_dates), 0, row["seed_id"])
                for date in active_dates[-5:]:
                    day = controlled.loc[panel[CONTRACT.date] == date]
                    self.assertGreater(day[day > 0].sum(), 0.0, row["seed_id"])
                    self.assertGreater(-day[day < 0].sum(), 0.0, row["seed_id"])

    def test_seed_zoo_ranking_prefers_passed_positive_os_cost_aware_candidate(self) -> None:
        summaries = [
            _summary("PROG-A", "review", is_sharpe=0.5, os_sharpe=0.8, score=-0.1),
            _summary("PROG-B", "sample_pass", is_sharpe=0.2, os_sharpe=0.4, score=0.2),
            _summary("PROG-C", "sample_pass", is_sharpe=0.7, os_sharpe=-0.2, score=0.4),
        ]

        rows = seed_zoo_rows_from_summaries(summaries)

        self.assertEqual(rows[0]["program_id"], "PROG-B")
        self.assertEqual(rows[0]["parent_candidate_tier"], "candidate")
        self.assertEqual(rows[1]["parent_candidate_tier"], "review")
        self.assertEqual(rows[2]["parent_candidate_tier"], "review")


def _summary(program_id: str, decision: str, *, is_sharpe: float, os_sharpe: float, score: float) -> dict:
    return {
        "program_id": program_id,
        "decision": decision,
        "descriptors": {
            "strategy_id": program_id.lower(),
            "strategy_family": "daily_stock_seed_zoo",
            "portfolio_day_coverage": 0.95,
        },
        "metrics": {
            "in_sample": {"sharpe": is_sharpe},
            "out_sample": {"sharpe": os_sharpe},
            "search_sample": {
                "sharpe": (is_sharpe + os_sharpe) / 2.0,
                "annualized_return": 0.01,
                "turnover": 0.5,
                "turnover_aware_score": score,
                "max_missing_held_weight": 0.01,
                "max_weight": 0.01,
            },
            "is_os_degradation": {
                "is_to_os_sharpe_degradation": is_sharpe - os_sharpe,
            },
        },
    }


def _synthetic_panel() -> pd.DataFrame:
    rows = []
    dates = pd.bdate_range("2020-01-02", periods=100)
    for permno in range(10001, 10041):
        industry = 2000 + (permno % 6) * 100
        for idx, date in enumerate(dates):
            seasonal = ((idx + permno) % 11 - 5) / 1000.0
            trend = (permno - 10020) / 1_000_000.0
            price = 20.0 + (permno - 10000) * 0.1 + idx * 0.01
            volume = 100_000.0 + (idx + 1) * (permno - 9990)
            market_cap = 1_000_000_000.0 + (permno - 10000) * 10_000_000.0 + idx * 100_000.0
            rows.append(
                {
                    CONTRACT.security_id: permno,
                    CONTRACT.issuer_id: permno + 50000,
                    CONTRACT.date: date,
                    CONTRACT.total_return: seasonal + trend,
                    CONTRACT.ex_dividend_return: seasonal + trend,
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
                    CONTRACT.industry_primary: industry,
                    CONTRACT.benchmark_return_primary: 0.0002 * ((idx % 3) - 1),
                    CONTRACT.benchmark_return_secondary: 0.0001,
                }
            )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    unittest.main()

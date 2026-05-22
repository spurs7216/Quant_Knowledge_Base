from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from research.alphaevolve_lite.daily_stock_contract import CONTRACT
from research.alphaevolve_lite.controller_batch_state import (
    parse_target_cell_schedule,
    target_cell_for_attempt,
)
from research.alphaevolve_lite.controller_execution_effect import (
    execution_effect_from_metrics,
)
from research.alphaevolve_lite.controller_sample_eval_policy import (
    compare_to_map_cell_elite,
    sample_eval_eligibility,
)
from research.alphaevolve_lite.mechanism_cards import normalize_mechanism_cards
from research.alphaevolve_lite.parent_zoo import (
    PARENT_ZOO_SCHEMA_VERSION,
    default_parent_zoo_mechanism_cards,
    write_parent_zoo_plan,
)
from research.alphaevolve_lite.sample_eval_metrics import (
    build_forward_returns_from_source,
    compare_search_sample_to_references,
    is_os_degradation_metrics,
)
from research.alphaevolve_lite.skill_library import build_controller_batch_skill_update
from research.alphaevolve_lite.splits import IS_OS_SPLIT_ID, build_is_os_splits, write_split_manifest


class SplitContractTests(unittest.TestCase):
    def test_builds_fixed_is_os_split_without_fractional_test_window(self) -> None:
        dates = pd.date_range("2022-12-19", "2023-01-10", freq="B")

        splits = build_is_os_splits(dates, out_sample_start="2023-01-01")

        self.assertEqual([split.name for split in splits], ["in_sample", "out_sample"])
        self.assertEqual(splits[0].end, pd.Timestamp("2022-12-30"))
        self.assertEqual(splits[1].start, pd.Timestamp("2023-01-02"))

    def test_split_manifest_records_active_is_os_contract(self) -> None:
        dates = pd.date_range("2022-12-19", "2023-01-10", freq="B")
        splits = build_is_os_splits(dates)
        with tempfile.TemporaryDirectory() as tmp:
            path = write_split_manifest(
                Path(tmp) / "split_manifest.yaml",
                splits=splits,
                calendar_count=len(dates),
                universe_policy="rolling_top500_market_cap",
                duplicate_policy={"duplicate_permno_date_count": 0},
            )
            text = path.read_text(encoding="utf-8")

        self.assertIn(f"split_id: {IS_OS_SPLIT_ID}", text)
        self.assertIn("split_policy: fixed_calendar_is_os", text)
        self.assertIn("name: in_sample", text)
        self.assertIn("name: out_sample", text)


class ForwardReturnSourceContractTests(unittest.TestCase):
    def test_attaches_next_day_return_after_month_end_universe_exit(self) -> None:
        signal_panel = pd.DataFrame(
            {
                CONTRACT.security_id: [10001],
                CONTRACT.date: [pd.Timestamp("2022-01-31")],
                CONTRACT.ex_dividend_return: [0.01],
                CONTRACT.benchmark_return_primary: [0.001],
            }
        )
        return_source = pd.DataFrame(
            {
                CONTRACT.security_id: [10001, 10001],
                CONTRACT.date: [pd.Timestamp("2022-01-31"), pd.Timestamp("2022-02-01")],
                CONTRACT.ex_dividend_return: [0.01, 0.05],
                CONTRACT.benchmark_return_primary: [0.001, 0.002],
            }
        )

        result = build_forward_returns_from_source(signal_panel, return_source, CONTRACT)

        self.assertEqual(result.loc[0, "fwd_date"], pd.Timestamp("2022-02-01"))
        self.assertAlmostEqual(result.loc[0, "fwd_ret"], 0.05)
        self.assertAlmostEqual(result.loc[0, "fwd_vwretd"], 0.002)
        self.assertTrue(bool(result.loc[0, "one_day_forward"]))

    def test_marks_missing_next_day_security_row_on_next_market_date(self) -> None:
        signal_panel = pd.DataFrame(
            {
                CONTRACT.security_id: [10001],
                CONTRACT.date: [pd.Timestamp("2022-01-31")],
                CONTRACT.ex_dividend_return: [0.01],
                CONTRACT.benchmark_return_primary: [0.001],
            }
        )
        return_source = pd.DataFrame(
            {
                CONTRACT.security_id: [10001, 10002],
                CONTRACT.date: [pd.Timestamp("2022-01-31"), pd.Timestamp("2022-02-01")],
                CONTRACT.ex_dividend_return: [0.01, 0.03],
                CONTRACT.benchmark_return_primary: [0.001, 0.002],
            }
        )

        result = build_forward_returns_from_source(signal_panel, return_source, CONTRACT)

        self.assertEqual(result.loc[0, "fwd_date"], pd.Timestamp("2022-02-01"))
        self.assertTrue(pd.isna(result.loc[0, "fwd_ret"]))
        self.assertFalse(bool(result.loc[0, "one_day_forward"]))


class TargetCellScheduleTests(unittest.TestCase):
    def test_forced_target_cell_schedule_cycles_exact_surface_and_intent(self) -> None:
        schedule = parse_target_cell_schedule(
            "portfolio/liquidity_weighted_sides,risk/liquidity_scaled_cap",
            available_surfaces={"signal", "ranking", "portfolio", "risk"},
        )

        first = target_cell_for_attempt(0, schedule)
        second = target_cell_for_attempt(1, schedule)
        third = target_cell_for_attempt(2, schedule)

        self.assertEqual(first.surface, "portfolio")
        self.assertEqual(first.intent, "liquidity_weighted_sides")
        self.assertEqual(first.cell_label, "portfolio:liquidity_weighted_sides")
        self.assertEqual(second.surface, "risk")
        self.assertEqual(second.intent, "liquidity_scaled_cap")
        self.assertEqual(third.surface, "portfolio")
        self.assertEqual(third.intent, "liquidity_weighted_sides")

    def test_forced_target_cell_schedule_rejects_unknown_intent_before_generation(self) -> None:
        with self.assertRaises(ValueError):
            parse_target_cell_schedule(
                "portfolio/industry_neutral_rank",
                available_surfaces={"signal", "ranking", "portfolio", "risk"},
            )

    def test_regime_aware_reversal_is_valid_for_parent_zoo_cards(self) -> None:
        schedule = parse_target_cell_schedule(
            "signal/regime_aware_reversal",
            available_surfaces={"signal", "ranking", "portfolio", "risk"},
        )

        self.assertEqual(schedule[0].surface, "signal")
        self.assertEqual(schedule[0].intent, "regime_aware_reversal")


class SampleEvalEligibilityTests(unittest.TestCase):
    def _base_attempt(self) -> dict:
        return {
            "decision": "pass",
            "child_program_path": "attempt/child_program.py",
            "target_intent_match": True,
            "target_surface": "ranking",
            "patch_intent": "industry_neutral_rank",
            "hard_gates": {"no_forward_return_replacement": True},
            "vector_smoke_metrics": {
                "active_day_count": 60,
                "min_long_count_active_day": 8,
                "min_short_count_active_day": 8,
            },
            "behavior_delta_metrics": {
                "weight_max_abs_delta": 0.02,
                "weight_changed_fraction": 0.06,
                "ranked_signal_max_abs_delta": 2.0,
            },
            "controller_search_score": 1.0,
        }

    def test_occupied_map_cell_without_elite_comparison_is_not_sample_eval_eligible(self) -> None:
        attempt = self._base_attempt()
        attempt.update(
            {
                "map_cell_already_occupied": True,
                "map_cell_elite_program_id": "PROG-OLD",
            }
        )

        result = sample_eval_eligibility(attempt)

        self.assertFalse(result["sample_eval_eligible"])
        self.assertIn(
            "occupied_map_cell_without_elite_comparison",
            result["sample_eval_eligibility_reasons"],
        )

    def test_occupied_map_cell_must_beat_and_differ_from_elite(self) -> None:
        attempt = self._base_attempt()
        elite = {
            "program_id": "PROG-OLD",
            "controller_search_score": 0.5,
            "behavior_delta_metrics": {
                "weight_max_abs_delta": 0.01,
                "weight_changed_fraction": 0.02,
                "ranked_signal_max_abs_delta": 0.5,
            },
        }
        attempt.update(compare_to_map_cell_elite(attempt, elite))
        attempt["map_cell_already_occupied"] = True

        result = sample_eval_eligibility(attempt)

        self.assertTrue(result["sample_eval_eligible"])

    def test_known_bad_attempt017_family_is_not_a_hard_sample_eval_filter(self) -> None:
        attempt = self._base_attempt()
        attempt.update(
            {
                "target_surface": "signal",
                "patch_intent": "bounded_tanh_dampening",
            }
        )

        result = sample_eval_eligibility(attempt)

        self.assertTrue(result["sample_eval_eligible"])
        self.assertNotIn(
            "known_bad_attempt017_signal_dampening_family",
            result["sample_eval_eligibility_reasons"],
        )


class ExecutionEffectTests(unittest.TestCase):
    def test_signal_only_delta_is_not_controller_execution_effective(self) -> None:
        metrics = {
            "signal_max_abs_delta": 3.0,
            "signal_changed_fraction": 0.5,
            "ranked_signal_max_abs_delta": 0.0,
            "ranked_signal_changed_fraction": 0.0,
            "weight_max_abs_delta": 0.0,
            "weight_changed_fraction": 0.0,
            "active_position_symmetric_diff_count": 0.0,
            "max_abs_gross_exposure_delta": 0.0,
            "max_abs_net_exposure_delta": 0.0,
        }

        result = execution_effect_from_metrics(metrics, target_surface="signal")

        self.assertFalse(result["controller_execution_effective"])
        self.assertIn(
            "ranked_signal_and_final_weights_unchanged",
            result["execution_effect_reasons"],
        )

    def test_portfolio_weight_delta_is_controller_execution_effective(self) -> None:
        metrics = {
            "weight_max_abs_delta": 0.01,
            "weight_changed_fraction": 0.05,
        }

        result = execution_effect_from_metrics(metrics, target_surface="portfolio")

        self.assertTrue(result["controller_execution_effective"])
        self.assertTrue(result["final_weight_delta"])


class SkillUpdateTests(unittest.TestCase):
    def test_execution_neutral_pass_is_not_success_strategy(self) -> None:
        attempt = {
            "decision": "pass",
            "program_id": "PROG-NOEFFECT",
            "target_surface": "signal",
            "patch_intent": "liquidity_adjusted_reversal",
            "map_cell_key": "surface=signal|intent=liquidity_adjusted_reversal",
            "behavior_delta_metrics": {
                "signal_max_abs_delta": 4.0,
                "signal_changed_fraction": 0.5,
                "ranked_signal_max_abs_delta": 0.0,
                "ranked_signal_changed_fraction": 0.0,
                "weight_max_abs_delta": 0.0,
                "weight_changed_fraction": 0.0,
                "active_position_symmetric_diff_count": 0.0,
            },
        }

        update = build_controller_batch_skill_update(
            source_run_id="unit_test",
            summary={"attempt_count": 1, "pass_count": 1, "failure_categories": {}},
            attempts=[attempt],
            skill_library_path=None,
            retrieved_skill_ids=[],
        )

        skill_types = [item["skill_type"] for item in update["candidate_skill_items"]]
        skill_names = [item["skill_name"] for item in update["candidate_skill_items"]]
        self.assertNotIn("success_strategy", skill_types)
        self.assertIn("Guard against execution-neutral controller passes", skill_names)


class PriorSampleEquivalenceTests(unittest.TestCase):
    def test_detects_equivalent_prior_sample_summary(self) -> None:
        metrics = {
            "search_sample": {
                "annualized_return": 0.1,
                "sharpe": 1.2,
                "turnover": 0.3,
            }
        }
        prior = {
            "program_id": "PROG-PRIOR",
            "metrics": {
                "search_sample": {
                    "annualized_return": 0.1,
                    "sharpe": 1.2,
                    "turnover": 0.3,
                }
            },
        }

        result = compare_search_sample_to_references(
            metrics,
            [prior],
            tolerance=1e-12,
            metric_names=["annualized_return", "sharpe", "turnover"],
        )

        self.assertTrue(result["metric_equivalent_to_any_reference"])
        self.assertEqual(result["equivalent_reference_program_ids"], ["PROG-PRIOR"])

    def test_is_os_degradation_reports_os_minus_is_and_sharpe_degradation(self) -> None:
        result = is_os_degradation_metrics(
            {"sharpe": 1.5, "turnover": 0.4},
            {"sharpe": 0.7, "turnover": 0.6},
        )

        self.assertAlmostEqual(result["os_minus_is_sharpe"], -0.8)
        self.assertAlmostEqual(result["os_minus_is_turnover"], 0.2)
        self.assertAlmostEqual(result["is_to_os_sharpe_degradation"], 0.8)


class MechanismCardValidationTests(unittest.TestCase):
    def test_rejects_loose_intent_and_loose_field_names(self) -> None:
        payload = {
            "cards": [
                {
                    "surface": "ranking",
                    "intent": "ranking",
                    "thesis": "loose card",
                    "required_data_fields": ["industry_code", "signal_raw"],
                }
            ]
        }

        with self.assertRaises(ValueError):
            normalize_mechanism_cards(payload)

    def test_accepts_exact_contract_fields_and_target_intent(self) -> None:
        payload = {
            "cards": [
                {
                    "surface": "ranking",
                    "intent": "industry_neutral_rank",
                    "thesis": "Rank within SIC groups using exact contract fields.",
                    "required_data_fields": ["CONTRACT.industry_primary", "signal"],
                }
            ]
        }

        result = normalize_mechanism_cards(payload)

        self.assertEqual(result["cards"][0]["intent"], "industry_neutral_rank")


class ParentZooTests(unittest.TestCase):
    def test_default_parent_zoo_mechanism_cards_include_regime_card(self) -> None:
        payload = default_parent_zoo_mechanism_cards()

        card_ids = [card["card_id"] for card in payload["cards"]]
        intents = [card["intent"] for card in payload["cards"]]
        self.assertIn("pzoo_regime_aware_reversal", card_ids)
        self.assertIn("regime_aware_reversal", intents)

    def test_parent_zoo_plan_writes_seed_roots_and_controller_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            plan = write_parent_zoo_plan(
                Path(tmp) / "parent_zoo",
                root_ids=["five_day_excess_reversal"],
                db_path="program_database.sqlite",
                controller_script="research/alphaevolve_lite/scripts/run_child_batch.py",
                program_id_prefix="PROG-TEST-PZOO",
                attempts_per_root=2,
                incumbent_summary_path="attempt017/evaluator_summary.json",
            )

            manifest = plan["manifest"]
            command = plan["commands"][0]
            self.assertEqual(manifest["schema_version"], PARENT_ZOO_SCHEMA_VERSION)
            self.assertEqual(manifest["root_count"], 1)
            self.assertTrue(Path(manifest["roots"][0]["program_path"]).exists())
            self.assertIn("--parent-root-id", command["argv"])
            self.assertIn("five_day_excess_reversal", command["argv"])
            self.assertIn("--incumbent-summary", command["argv"])


if __name__ == "__main__":
    unittest.main()

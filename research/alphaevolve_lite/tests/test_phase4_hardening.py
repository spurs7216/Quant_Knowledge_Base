from __future__ import annotations

import unittest

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
from research.alphaevolve_lite.sample_eval_metrics import compare_search_sample_to_references
from research.alphaevolve_lite.skill_library import build_controller_batch_skill_update


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


if __name__ == "__main__":
    unittest.main()
